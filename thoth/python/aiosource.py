#!/usr/bin/env python3
# thoth-python
# Copyright(C) 2018, 2019 Fridolin Pokorny
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
import typing
from functools import lru_cache
from urllib.parse import urlparse

import attr
import aiohttp

from bs4 import BeautifulSoup

import semantic_version as semver

from .exceptions import NotFound
from .exceptions import InternalError
from .exceptions import VersionIdentifierError
from .configuration import config
from .artifact import Artifact

_LOGGER = logging.getLogger(__name__)


@attr.s(frozen=True, slots=True)
class AIOSource:
    """Representation of source (Python index) for Python packages."""

    url = attr.ib(type=str)
    name = attr.ib(type=str)
    verify_ssl = attr.ib(type=bool, default=True)
    warehouse = attr.ib(type=bool)
    warehouse_api_url = attr.ib(default=None, type=str)

    http_session = aiohttp.ClientSession()

    _NORMALIZED_PACKAGE_NAME_RE = re.compile("[a-z-]+")

    async def __del__(self):
        """Descructor! Let's clean up the AIHTTP session object."""
        await self.http_session.close()

    @name.default
    def default_name(self):
        """Create a name for source based on url if not explicitly provided."""
        parsed_url = urlparse(self.url)
        return parsed_url.netloc.replace(".", "-")

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

    async def _warehouse_get_api_package_version_info(self, package_name: str, package_version: str) -> dict:
        """Use API of the deployed Warehouse to gather package version information."""
        url = self.get_api_url() + f"/{package_name}/{package_version}/json"
        json = None

        _LOGGER.debug("Gathering package version information from Warehouse API: %r", url)

        async with self.http_session.get(self.url) as response:
            if response.status == 404:
                raise NotFound(
                    f"Package {package_name} in version {package_version}"
                    f" not found on warehouse {self.url} ({self.name})"
                )

            json = await response.json()

        return json

    async def _warehouse_get_api_package_info(self, package_name: str) -> dict:
        """Use API of the deployed Warehouse to gather package information."""
        url = self.get_api_url() + f"/{package_name}/json"
        json = None

        _LOGGER.debug("Gathering package information from Warehouse API: %r", url)

        async with self.http_session.get(self.url) as response:
            if response.status == 404:
                raise NotFound(f"Package {package_name} not found on warehouse {self.url} ({self.name})")

            json = await response.json()

        return json

    def _warehouse_get_package_hashes(
        self, package_name: str, package_version: str, with_included_files: bool = False
    ) -> typing.List[dict]:
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
    async def get_packages(self) -> set:
        """List packages available on the source package index."""
        soup = None
        links = []

        _LOGGER.debug(f"Discovering packages available on {self.url} (simple index name: {self.name})")

        async with self.http_session.get(self.url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, "lxml")

        links = soup.find_all("a")
        _LOGGER.debug(f"Links discovered on {self.url}: {links}")

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

            if self.is_normalized_python_package_name(package_name) and package_name == link_text:
                packages.add(package_name)

        return packages

    @staticmethod
    def _parse_artifact_version(package_name: str, artifact_name: str) -> str:
        """Parse package version based on artifact name available on the package source index."""
        if artifact_name.endswith(".tar.gz"):
            # +1 for dash delimiting package name and package version.
            version = artifact_name[len(package_name) + 1:-len(".tar.gz")]

        elif artifact_name.endswith(".whl"):
            # TODO: we will need to improve this based on PEP-0503.
            parsed_package_name, version, _ = artifact_name.split("-", maxsplit=2)
            if parsed_package_name.lower() != package_name:
                _LOGGER.warning(
                    f"It looks like package name does not match the one parsed from artifact when "
                    f"parsing version from wheel - package name is {package_name}, "
                    f"pared version is {version}, artifact is {artifact_name}"
                )
        else:
            raise InternalError(
                f"Unable to parse artifact name from artifact {artifact_name} for package {package_name}"
            )

        _LOGGER.debug(f"Parsed package version for package {package_name} from artifact {artifact_name}: {version}")
        return version

    async def _simple_repository_list_versions(self, package_name: str) -> list:
        """List versions of package available on a simple repository."""
        result = set()

        artifacts = await self._simple_repository_list_artifacts(package_name)
        _LOGGER.debug("Artifacts for %r (index with name %r): %r", package_name, self.name, artifacts)

        for artifact_name, _ in artifacts:
            result.add(self._parse_artifact_version(package_name, artifact_name))

        result = list(result)
        _LOGGER.debug("Versions available on %r (index with name %r): %r", self.url, self.name, result)

        return result

    @lru_cache(maxsize=10)
    async def get_package_versions(self, package_name: str) -> list:
        """Get listing of versions available for the given package."""
        if not self.warehouse:
            _versions = await self._simple_repository_list_versions(package_name)
            return _versions

        package_info = await self._warehouse_get_api_package_info(package_name)
        return list(package_info["releases"].keys())

    async def get_latest_package_version(
        self, package_name: str, graceful: bool = False
    ) -> typing.Optional[semver.base.Version]:
        """Get the latest version for the given package."""
        try:
            all_versions = self.get_package_versions(package_name)
        except NotFound:
            if graceful:
                _LOGGER.warning(f"Package {package_name!r} was not found on index {self.name} ({self.url!r})")
                return None
            raise

        # Transform versions to semver for sorting:
        semver_versions = []
        for version in all_versions:
            try:
                version = semver.Version.coerce(version)
            except Exception as exc:
                error_msg = f"Cannot parse semver version {version} for package {package_name}: {str(exc)}"
                if graceful:
                    _LOGGER.warning(error_msg)
                    return None
                raise VersionIdentifierError(error_msg) from exc

            semver_versions.append(version)

        return sorted(semver_versions)[-1]

    async def _simple_repository_list_artifacts(self, package_name: str) -> list:
        """Parse simple repository package listing (HTML) and return artifacts present there."""
        url = self.url + "/" + package_name
        soup = None

        _LOGGER.debug(f"Discovering package %r artifacts from %r", package_name, url)

        async with self.http_session.get(url) as response:
            _LOGGER.debug(f"Response %r", response)

            if response.status == 404:
                raise NotFound(f"Package {package_name} is not present on index {self.url} (index {self.name})")

            text = await response.text()
            soup = BeautifulSoup(text, "lxml")

        links = soup.find_all("a")
        artifacts = []
        for link in links:
            artifact_name = str(link["href"]).rsplit("/", maxsplit=1)
            if len(artifact_name) == 2:
                # If full URL provided by index.
                artifact_name = artifact_name[1]
            else:
                artifact_name = artifact_name[0]

            artifact_parts = artifact_name.rsplit("#", maxsplit=1)
            if len(artifact_parts) == 2:
                artifact_name = artifact_parts[0]

            if not artifact_name.endswith((".tar.gz", ".whl")):
                _LOGGER.debug("Link does not look like a package for %r: %r", package_name, link["href"])
                continue

            artifact_url = link["href"]
            if not artifact_url.startswith(("http://", "https://")):
                artifact_url = url + f"/{artifact_name}"

            artifacts.append((artifact_name, artifact_url))

        return artifacts

    async def get_package_artifacts(self, package_name: str, package_version: str):
        """Return list of artifacts corresponding to package name and package version."""
        to_return = []
        for artifact_name, artifact_url in self._simple_repository_list_artifacts(package_name):
            # Convert all artifact names to lowercase - as a shortcut we simply convert everything to lowercase.
            artifact_name.lower()
            if not artifact_name.startswith(f"{package_name}-{package_version}"):
                # TODO: this logic has to be improved as package version can be a suffix of another package version:
                #   mypackage-1.0.whl, mypackage-1.0.0.whl, ...
                # This will require parsing based on PEP or some better logic.
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
    ) -> typing.Generator[tuple, None, None]:
        """Download the given artifact from Warehouse and compute desired info."""
        for artifact_name, artifact_url in self._simple_repository_list_artifacts(package_name):
            # Convert all artifact names to lowercase - as a shortcut we simply convert everything to lowercase.
            artifact_name.lower()
            if not artifact_name.startswith(f"{package_name}-{package_version}"):
                # TODO: this logic has to be improved as package version can be a suffix of another package version:
                #   mypackage-1.0.whl, mypackage-1.0.0.whl, ...
                # This will require parsing based on PEP or some better logic.
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

            yield (artifact_name, artifact.sha, hashes, symbols)

    def provides_package_version(self, package_name: str, package_version: str) -> bool:
        """Check if the given source provides package in the given version."""
        try:
            return package_version in self.get_package_versions(package_name)
        except NotFound:
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
