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

from functools import lru_cache

import attr
import asyncio
import aiohttp
from urllib.parse import urljoin
from urllib.parse import unquote

from bs4 import BeautifulSoup

from .exceptions import NotFoundError
from .artifact import Artifact
from .source import Source

from typing import Optional, Set, Tuple, List, Dict

_LOGGER = logging.getLogger(__name__)


class AsyncIterablePackages:
    """Async Iterator for Packages."""

    def __init__(self, _packages: Set[str]):  # Ignore PyDocStyleBear
        """Initialize Async Iterable instance for Packages."""
        self.packages = _packages

    def __aiter__(self):  # Ignore PyDocStyleBear
        """Return asynchronous iterator."""
        return self

    async def __anext__(self) -> str:  # Ignore PyDocStyleBear
        """Return awaitable object."""
        data = await self.fetch_data()

        if data:
            return data
        else:
            raise StopAsyncIteration

    async def fetch_data(self) -> Optional[str]:  # Ignore PyDocStyleBear
        """Fetch data."""
        await asyncio.sleep(0)  # Other coros get to run

        if len(self.packages) == 0:
            return None

        return self.packages.pop()


class AsyncIterableVersions:
    """Async Iterator for Versions."""

    def __init__(self, _versions: Set[str]):  # Ignore PyDocStyleBear
        """Initialize Async Iterable Versions instance for Versions."""
        self.versions = _versions

    def __aiter__(self):  # Ignore PyDocStyleBear
        """Return asynchronous iterator."""
        return self

    async def __anext__(self) -> str:  # Ignore PyDocStyleBear
        """Return awaitable object."""
        data = await self.fetch_data()

        if data:
            return data
        else:
            raise StopAsyncIteration

    async def fetch_data(self) -> Optional[str]:  # Ignore PyDocStyleBear
        """Fetch data."""
        await asyncio.sleep(0)  # Other coros get to run

        if len(self.versions) == 0:
            return None

        return self.versions.pop()


class AsyncIterableArtifacts:
    """Async Iterator for Artifacts."""

    def __init__(self, artifacts: List[Tuple[str, str]]):  # Ignore PyDocStyleBear
        """Initialize Async Iterable instance for Artifacts."""
        self.artifacts = artifacts

    def __aiter__(self):  # Ignore PyDocStyleBear
        """Return asynchronous iterator."""
        return self

    async def __anext__(self) -> Tuple:  # Ignore PyDocStyleBear
        """Return awaitable object."""
        data = await self.fetch_data()

        if data:
            return data
        else:
            raise StopAsyncIteration

    async def fetch_data(self) -> Optional[Tuple]:  # Ignore PyDocStyleBear
        """Fetch data."""
        await asyncio.sleep(0)  # Other coros get to run

        if len(self.artifacts) == 0:
            return None

        return self.artifacts.pop()


@attr.s(frozen=True, slots=True)
class AIOSource(Source):
    """Representation of source (Python index) for Python packages."""

    async def _warehouse_get_api_package_version_info(  # type: ignore
        self, package_name: str, package_version: str
    ) -> Dict:
        """Use API of the deployed Warehouse to gather package version information."""
        url = self.get_api_url() + f"/{package_name}/{package_version}/json"

        _LOGGER.debug("Gathering package version information from Warehouse API: %r", url)

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            try:
                async with session.get(url) as response:
                    return await response.json()
            except aiohttp.ClientResponseError as exc:
                if exc.status == 404:
                    raise NotFoundError(
                        f"Package {package_name} in version {package_version} not "
                        f"found on warehouse {self.url} ({self.name})"
                    )

                raise

    async def _warehouse_get_package_hashes(  # type: ignore
        self, package_name: str, package_version: str, with_included_files: bool = False
    ) -> List[Dict]:
        """Gather information about SHA hashes available for the given package-version release."""
        package_info = await self._warehouse_get_api_package_version_info(package_name, package_version)

        result = []
        for item in package_info["urls"]:
            result.append({"name": item["filename"], "sha256": item["digests"]["sha256"]})
            # this checks whether to gather digests for all files in the given artifact
            if with_included_files:
                artifact = Artifact(item["filename"], item["url"], verify_ssl=self.verify_ssl)
                result[-1]["digests"] = artifact.gather_hashes()
                result[-1]["symbols"] = artifact.get_versioned_symbols()

        return result

    async def _warehouse_get_api_package_info(self, package_name: str) -> Dict:  # type: ignore
        """Use API of the deployed Warehouse to gather package information."""
        url = self.get_api_url() + f"/{package_name}/json"

        _LOGGER.debug("Gathering package information from Warehouse API: %r", url)

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            try:
                async with session.get(url) as response:
                    return await response.json()
            except aiohttp.ClientResponseError as exc:
                if exc.status == 404:
                    raise NotFoundError(f"Package {package_name} not found on warehouse {self.url} ({self.name})")

                raise

    async def _simple_repository_list_versions(self, package_name: str) -> List:  # type: ignore
        """List versions of package available on a simple repository."""
        result = set()
        a = await self._simple_repository_list_artifacts(package_name)

        async for artifact_name, _ in a:
            result.add(self._parse_artifact_version(package_name, artifact_name))

        to_ret = list(result)

        _LOGGER.debug("Versions available on %r (index with name %r): %r", self.url, self.name, result)
        return to_ret

    async def _simple_repository_list_artifacts(self, package_name: str) -> AsyncIterableArtifacts:  # type: ignore
        """Parse simple repository package listing (HTML) and return artifacts present there."""
        url = self.url + "/" + package_name
        links = []

        _LOGGER.debug("Discovering package %r artifacts from %r", package_name, url)

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            try:
                async with session.get(url) as response:
                    text = await response.text()
                    soup = BeautifulSoup(text, "lxml")
                    links = soup.find_all("a")
            except aiohttp.ClientResponseError as exc:
                if exc.status == 404:
                    raise NotFoundError(
                        f"Package {package_name} is not present on index {self.url} (index {self.name})"
                    )

                raise

        artifacts = []  # List[Tuple[str,str]]
        for link in links:
            artifact_name_full = str(link["href"]).rsplit("/", maxsplit=1)
            if len(artifact_name_full) == 2:
                # If full URL provided by index.
                artifact_name = artifact_name_full[1]
            else:
                artifact_name = artifact_name_full[0]

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

        return AsyncIterableArtifacts(artifacts)

    async def get_packages(self) -> Optional[AsyncIterablePackages]:  # type: ignore
        """List packages available on the source package index."""
        _LOGGER.debug(f"Discovering packages available on {self.url} (simple index name: {self.name})")

        links = []

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(self.url) as resp:
                text = await resp.text()

                soup = BeautifulSoup(text, "lxml")
                links = soup.find_all("a")

        if len(links) == 0:
            return None

        packages = set()
        for link in links:
            package_parts = link["href"].rsplit("/", maxsplit=2)
            # According to PEP-503, package names must have trailing '/', but check this explicitly
            if not package_parts[-1]:
                package_parts = package_parts[:-1]
            package_name = self.normalize_package_name(package_parts[-1])

            # Discard links to parent dirs (package name of URL does not match the text.
            link_text = self.normalize_package_name(link.text)
            if link_text.endswith("/"):
                # Link names should end with trailing / according to PEEP:
                #   https://www.python.org/dev/peps/pep-0503/
                link_text = link_text[:-1]

            if package_name == link_text:
                packages.add(package_name)

        return AsyncIterablePackages(packages)

    @lru_cache(maxsize=64)
    async def get_package_versions(self, package_name: str) -> AsyncIterableVersions:  # type: ignore
        """Get listing of versions available for the given package."""
        if not self.warehouse:
            return AsyncIterableVersions(set(await self._simple_repository_list_versions(package_name)))

        package_info = await self._warehouse_get_api_package_info(package_name)
        return AsyncIterableVersions(set(package_info["releases"].keys()))

    async def get_package_artifacts(self, package_name: str, package_version: str):
        """Return list of artifacts corresponding to package name and package version."""
        to_return = []
        possible_continuations = [".win32", ".tar.gz", ".whl", ".zip", ".exe", ".egg", "-"]
        async for artifact_name, artifact_url in await self._simple_repository_list_artifacts(package_name):
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

    @lru_cache(maxsize=10)
    async def get_package_hashes(  # type: ignore
        self, package_name: str, package_version: str, with_included_files: bool = False
    ) -> List:
        """Get information about release hashes available in this source index."""
        if self.warehouse:
            return await self._warehouse_get_package_hashes(package_name, package_version, with_included_files)

        artifacts = await self.get_package_artifacts(package_name, package_version)
        result = []
        for artifact in artifacts:
            doc = {}
            doc["name"] = artifact.artifact_name
            doc["sha256"] = artifact.sha
            if with_included_files:
                doc["digests"] = artifact.gather_hashes()
            result.append(doc)

        return result
