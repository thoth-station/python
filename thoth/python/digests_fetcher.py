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

"""Fetching package artifact digests."""

import typing
import logging

from .source import Source
from .exceptions import NotFoundError

_LOGGER = logging.getLogger(__name__)


class DigestsFetcherBase:
    """A base class implementing digests fetching."""

    def fetch_digests(self, package_name: str, package_version: str) -> dict:
        """Fetch digests for the given package in specified version from the given package index."""
        raise NotImplementedError


class PythonDigestsFetcher(DigestsFetcherBase):
    """Fetch digests from the given PEP-503 compatible package source index."""

    def __init__(self, sources: typing.List[Source]):
        """Set a list of package sources that should be considered when obtaining package digests."""
        self._sources = sources

    def fetch_digests(self, package_name: str, package_version: str) -> dict:
        """Fetch digests for the given package in specified version from the given package index."""
        report = {}

        for source in self._sources:
            try:
                report[source.url] = source.get_package_hashes(package_name, package_version)
            except NotFoundError as exc:
                _LOGGER.debug(
                    f"Package {package_name} in version {package_version} not "
                    f"found on index {source.name}: {str(exc)}"
                )

        return report
