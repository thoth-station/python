#!/usr/bin/env python3
# thoth-python
# Copyright(C) 2018, 2019, 2020 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Representation of source (index) for Python packages."""

import logging
import re
from functools import lru_cache
from urllib.parse import unquote
from urllib.parse import urljoin
from urllib.parse import urlparse
from datetime import datetime

from typing import Optional, List, Union, Generator

import attr
import requests
from bs4 import BeautifulSoup
from packaging.version import Version
from packaging.version import LegacyVersion
from packaging.version import parse as parse_version

from .exceptions import NotFoundError
from .exceptions import InternalError
from .exceptions import VersionIdentifierError
from .configuration import config
from .artifact import Artifact

from thoth.common.helpers import parse_datetime

_LOGGER = logging.getLogger(__name__)
LEGACY_URLS = {"https://pypi.python.org/simple": "https://pypi.org/simple"}


def normalize_url(url: str) -> str:
    """We normalize url to remove legacy urls."""
    url = url.rstrip("/")
    if url in LEGACY_URLS:
        return LEGACY_URLS[url]
    return url


@attr.s(frozen=True, slots=True)
class Source:
    """Representation of source (Python index) for Python packages."""

    url = attr.ib(type=str, converter=normalize_url)
    name = attr.ib(type=str)
    verify_ssl = attr.ib(type=bool, default=True)
    warehouse = attr.ib(type=bool)
    warehouse_api_url = attr.ib(default=None, type=Optional[str])

    _NORMALIZED_PACKAGE_NAME_RE = re.compile("[a-z-]+")

    @name.default
    def default_name(self):
        """Create a name for source based on url if not explicitly provided."""
        parsed_url = urlparse(self.url)
        name = parsed_url.netloc + parsed_url.path
        return re.sub(r"[^A-Za-z0-9]", "-", name)

    @warehouse.default
    def warehouse_default(self):
        """Check if the given url is registered in default warehouses."""
        return self.url in config.warehouses

    def get_api_url(self):
        """Construct URL to Warehouse instance."""
        if not self.warehouse:
            raise NotImplementedError("Cannot retrieve API url for non-warehouse repository")

        if self.warehouse_api_url:
            return self.warehouse_api_url

        return self.url[: -len("/simple")] + "/pypi"

    @classmethod
    def from_dict(cls, dict_: dict):
        """Parse source from its dictionary representation."""
        _LOGGER.debug("Parsing package source to dict representation")
        dict_ = dict(dict_)
        warehouse_url = dict_.pop("url")
        instance = cls(
            name=dict_.pop("name"),
            url=warehouse_url,
            verify_ssl=dict_.pop("verify_ssl"),
            warehouse=dict_.pop("warehouse", warehouse_url in config.warehouses),
        )

        if dict_:
            _LOGGER.warning("Ignored source configuration entries: %s", dict_)

        return instance

    def to_dict(self, include_warehouse: bool = False) -> dict:
        """Convert source definition to its dict representation."""
        _LOGGER.debug("Converting package source to dict representation")
        result = {"url": self.url, "verify_ssl": self.verify_ssl, "name": self.name}

        if include_warehouse:
            result["warehouse"] = self.warehouse

        return result

    @staticmethod
    def normalize_package_name(package_name: str) -> str:
        """Normalize package name on index according to PEP-0503."""
        return re.sub(r"[-_.]+", "-", package_name).lower()

    def _warehouse_get_api_package_version_info(self, package_name: str, package_version: str) -> dict:
        """Use API of the deployed Warehouse to gather package version information."""
        url = self.get_api_url() + f"/{package_name}/{package_version}/json"
        _LOGGER.debug("Gathering package version information from Warehouse API: %r", url)
        response = requests.get(url, verify=self.verify_ssl)
        if response.status_code == 404:
            raise NotFoundError(
                f"Package {package_name} in version {package_version} not found on warehouse {self.url} ({self.name})"
            )
        response.raise_for_status()
        return response.json()

    def _warehouse_get_api_package_info(self, package_name: str) -> dict:
        """Use API of the deployed Warehouse to gather package information."""
        url = self.get_api_url() + f"/{package_name}/json"
        _LOGGER.debug("Gathering package information from Warehouse API: %r", url)
        response = requests.get(url, verify=self.verify_ssl)
        if response.status_code == 404:
            raise NotFoundError(f"Package {package_name} not found on warehouse {self.url} ({self.name})")
        response.raise_for_status()
        return response.json()

    def _warehouse_get_package_hashes(
        self, package_name: str, package_version: str, with_included_files: bool = False
    ) -> List[dict]:
        """Gather information about SHA hashes available for the given package-version release."""
        package_info = self._warehouse_get_api_package_version_info(package_name, package_version)

        result = []
        for item in package_info["urls"]:
            result.append({"name": item["filename"], "sha256": item["digests"]["sha256"]})
            # this checks whether to gather digests for all files in the given artifact
            if with_included_files:
                artifact = Artifact(item["filename"], item["url"], verify_ssl=self.verify_ssl)
                result[-1]["digests"] = artifact.gather_hashes()
                result[-1]["symbols"] = artifact.get_versioned_symbols()

        return result

    @classmethod
    def is_normalized_python_package_name(cls, package_name: str) -> bool:
        """Check if the given Python package name is normalized."""
        # https://www.python.org/dev/peps/pep-0503/#normalized-names
        return cls._NORMALIZED_PACKAGE_NAME_RE.match(package_name) is not None

    @lru_cache(maxsize=10)
    def get_packages(self) -> set:
        """List packages available on the source package index."""
        _LOGGER.debug(f"Discovering packages available on {self.url} (simple index name: {self.name})")
        response = requests.get(self.url, verify=self.verify_ssl)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.find_all("a")

        packages = set()
        for link in links:
            package_parts = link["href"].rsplit("/", maxsplit=2)
            # According to PEP-503, package names must have trailing '/', but check this explicitly
            if not package_parts[-1]:
                package_parts = package_parts[:-1]
            package_name = package_parts[-1]

            # Discard links to parent dirs (package name of URL does not match the text.
            link_text = link.text
            if link_text.endswith("/"):
                # Link names should end with trailing / according to PEEP:
                #   https://www.python.org/dev/peps/pep-0503/
                link_text = link_text[:-1]

            # Normalize link_text for comparison below
            link_text = self.normalize_package_name(link_text)

            if self.is_normalized_python_package_name(package_name) and package_name == link_text:
                packages.add(package_name)

        return packages

    def provides_package(self, package_name: str) -> bool:
        """Check if the given package is provided by this package source index."""
        _LOGGER.debug("Checking availability of package %r on index %r", package_name, self.url)
        package_name = self.normalize_package_name(package_name)
        url = self.url + "/" + package_name
        response = requests.get(url, verify=self.verify_ssl)

        if response.status_code == 404:
            return False

        # Raise on other inappropriate error codes.
        response.raise_for_status()
        return True

    @staticmethod
    def _parse_artifact_version(package_name: str, artifact_name: str) -> str:
        """Parse package version based on artifact name available on the package source index."""
        if artifact_name.endswith(".tar.gz"):
            # +1 for dash delimiting package name and package version.
            version = artifact_name[len(package_name) + 1 : -len(".tar.gz")]

        elif artifact_name.endswith(".whl"):
            # TODO: we will need to improve this based on PEP-0503.
            parsed_package_name, version, _ = artifact_name.split("-", maxsplit=2)
            if parsed_package_name.lower() != package_name:
                _LOGGER.warning(
                    f"It looks like package name does not match the one parsed from artifact when "
                    f"parsing version from wheel - package name is {package_name}, "
                    f"parsed version is {version}, artifact is {artifact_name}"
                )
        else:
            raise InternalError(
                f"Unable to parse artifact name from artifact {artifact_name} for package {package_name}"
            )

        _LOGGER.debug(f"Parsed package version for package {package_name} from artifact {artifact_name}: {version}")

        return version

    def _simple_repository_list_versions(self, package_name: str) -> list:
        """List versions of package available on a simple repository."""
        simple_repos = set()
        for artifact_name, _ in self._simple_repository_list_artifacts(package_name):
            simple_repos.add(self._parse_artifact_version(package_name, artifact_name))

        result = list(simple_repos)
        _LOGGER.debug("Versions available on %r (index with name %r): %r", self.url, self.name, result)
        return result

    @lru_cache(maxsize=10)
    def get_package_versions(self, package_name: str) -> list:
        """Get listing of versions available for the given package."""
        if not self.warehouse:
            return self._simple_repository_list_versions(package_name)

        package_info = self._warehouse_get_api_package_info(package_name)
        return list(package_info["releases"].keys())

    def get_sorted_package_versions(
        self,
        package_name: str,
        graceful: bool = False,
        reverse: bool = True,  # default to newest first
    ) -> Optional[List[Union[Version, LegacyVersion]]]:
        """Get sorted versions for the given package."""
        try:
            all_versions = self.get_package_versions(package_name)
        except NotFoundError:
            if graceful:
                _LOGGER.warning(f"Package {package_name!r} was not found on index {self.name} ({self.url!r})")
                return None
            raise

        # Transform versions to semver for sorting:
        semver_versions = []
        for version in all_versions:
            try:
                version = parse_version(version)
            except Exception as exc:
                error_msg = f"Cannot parse semver version {version} for package {package_name}: {str(exc)}"
                if graceful:
                    _LOGGER.warning(error_msg)
                    return None
                raise VersionIdentifierError(error_msg) from exc

            semver_versions.append(version)
        return sorted(semver_versions, reverse=reverse)

    def get_latest_package_version(
        self, package_name: str, graceful: bool = False
    ) -> Optional[Union[Version, LegacyVersion]]:
        """Get the latest version for the given package."""
        semver_versions = self.get_sorted_package_versions(package_name=package_name, graceful=graceful)
        if semver_versions is None:  # only None if graceful so don't check
            return None
        return semver_versions[0]

    def _simple_repository_list_artifacts(self, package_name: str) -> list:
        """Parse simple repository package listing (HTML) and return artifacts present there."""
        url = self.url + "/" + package_name

        _LOGGER.debug(f"Discovering package {package_name} artifacts from {url}")
        response = requests.get(url, verify=self.verify_ssl)
        if response.status_code == 404:
            raise NotFoundError(f"Package {package_name} is not present on index {self.url} (index {self.name})")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        links = soup.find_all("a")
        artifacts = []
        for link in links:
            artifact_names = str(link["href"]).rsplit("/", maxsplit=1)
            if len(artifact_names) == 2:
                # If full URL provided by index.
                artifact_name = artifact_names[1]
            else:
                artifact_name = artifact_names[0]

            artifact_parts = artifact_name.rsplit("#", maxsplit=1)
            if len(artifact_parts) == 2:
                artifact_name = artifact_parts[0]

            if not artifact_name.endswith((".tar.gz", ".whl")):
                _LOGGER.debug("Link does not look like a package for %r: %r", package_name, link["href"])
                continue

            artifact_url = link["href"]
            if not artifact_url.startswith(("http://", "https://")):
                artifact_url = urljoin(url, artifact_url)

            # Decode characters in link retrieved
            artifact_name = unquote(artifact_name)

            artifacts.append((artifact_name, artifact_url))

        return artifacts

    def get_package_artifacts(self, package_name: str, package_version: str):
        """Return list of artifacts corresponding to package name and package version."""
        to_return = []
        possible_continuations = [".win32", ".tar.gz", ".whl", ".zip", ".exe", ".egg", "-"]
        for artifact_name, artifact_url in self._simple_repository_list_artifacts(package_name):
            # Convert all artifact names to lowercase - as a shortcut we simply convert everything to lowercase.
            artifact_name = artifact_name.lower()

            for i in possible_continuations:
                if (
                    artifact_name.startswith(f"{package_name}-{package_version}")
                    or artifact_name.startswith(f"{package_name.replace('-', '_')}-{package_version}")
                ) and artifact_name.endswith(i):
                    break
            else:
                _LOGGER.debug(
                    "Skipping artifact %r as it does not match required version %r for package %r",
                    artifact_name,
                    package_version,
                    package_name,
                )
                continue
            to_return.append(Artifact(artifact_name, artifact_url, verify_ssl=self.verify_ssl))

        return to_return

    def _download_artifacts_data(
        self, package_name: str, package_version: str, with_included_files: bool = False
    ) -> Generator[tuple, None, None]:
        """Download the given artifact from Warehouse and compute desired info."""
        possible_continuations = [".win32", ".tar.gz", ".whl", ".zip", ".exe", ".egg", "-"]
        for artifact_name, artifact_url in self._simple_repository_list_artifacts(package_name):
            # Convert all artifact names to lowercase - as a shortcut we simply convert everything to lowercase.
            artifact_name.lower()

            for i in possible_continuations:
                if artifact_name.startswith(f"{package_name}-{package_version}{i}"):
                    break
            else:
                _LOGGER.debug(
                    "Skipping artifact %r as it does not match required version %r for package %r",
                    artifact_name,
                    package_version,
                    package_name,
                )
                continue
            artifact = Artifact(artifact_name, artifact_url, verify_ssl=self.verify_ssl)

            symbols = None
            hashes = None
            if with_included_files:
                symbols = artifact.get_versioned_symbols()
                hashes = artifact.gather_hashes()

            yield (
                artifact_name,
                artifact.sha,
                hashes,
                symbols,
            )

    def provides_package_version(self, package_name: str, package_version: str) -> bool:
        """Check if the given source provides package in the given version."""
        try:
            return package_version in self.get_package_versions(package_name)
        except NotFoundError:
            # Package was not found on the index.
            return False

    @lru_cache(maxsize=10)
    def get_package_data(self, package_name: str, package_version: str, with_included_files: bool = False) -> list:
        """Get information about release hashes and symbols available in this source index."""
        if self.warehouse:
            return self._warehouse_get_package_hashes(package_name, package_version, with_included_files)

        artifacts = self.get_package_artifacts(package_name, package_version)
        result = []
        for artifact in artifacts:
            doc = {}
            doc["name"] = artifact.artifact_name
            doc["sha256"] = artifact.sha
            if with_included_files:
                doc["digests"] = artifact.gather_hashes()
                doc["symbols"] = artifact.get_versioned_symbols()
            result.append(doc)

        return result

    @lru_cache(maxsize=10)
    def get_package_hashes(self, package_name: str, package_version: str, with_included_files: bool = False) -> list:
        """Get information about release hashes available in this source index."""
        if self.warehouse:
            return self._warehouse_get_package_hashes(package_name, package_version, with_included_files)

        artifacts = self.get_package_artifacts(package_name, package_version)
        result = []
        for artifact in artifacts:
            doc = {}
            doc["name"] = artifact.artifact_name
            doc["sha256"] = artifact.sha
            if with_included_files:
                doc["digests"] = artifact.gather_hashes()
            result.append(doc)

        return result

    def get_package_release_date(
        self,
        package_name: str,
        package_version: str,
    ) -> datetime:
        """Get time at which package was uploaded to package index."""
        package_json = self._warehouse_get_api_package_info(package_name)
        release = package_json["releases"].get(package_version)
        if release is None:
            raise NotFoundError(f"Version {package_version} not found for {package_name} on {self.warehouse_api_url}.")
        artifact = next(x for x in release if x["python_version"] == "source")
        if artifact is None:
            raise NotFoundError(
                f"No source distribution for {package_name}==={package_version} found on {self.warehouse_api_url}."
            )

        return parse_datetime(artifact["upload_time_iso_8601"][:-1])
