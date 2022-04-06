#!/usr/bin/env python3
# thoth-python
# Copyright(C) 2018, 2019, 2020 Red Hat, Inc.
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

"""Python ecosystem specific routines."""

from .aiosource import AIOSource
from .aiosource import AsyncIterableArtifacts
from .aiosource import AsyncIterablePackages
from .aiosource import AsyncIterableVersions
from .constraints import Constraints
from .digests_fetcher import DigestsFetcherBase
from .digests_fetcher import PythonDigestsFetcher
from .packages import Packages
from .package_version import PackageVersion
from .pipfile import Pipfile
from .pipfile import PipfileLock
from .pipfile import PipfileMeta
from .project import Project
from .source import Source


__version__ = "0.16.10"
__author__ = "Fridolin Pokorny <fridolin@redhat.com>, Christoph Görn <goern@redhat.com>"
__copyright__ = "Copyright 2018, 2019 Red Hat, Inc."
__license__ = "GPLv3+"


__all__ = [
    "AIOSource",
    "AsyncIterableArtifacts",
    "AsyncIterablePackages",
    "AsyncIterableVersions",
    "Constraints",
    "DigestsFetcherBase",
    "Packages",
    "PackageVersion",
    "Pipfile",
    "PipfileLock",
    "PipfileMeta",
    "Project",
    "PythonDigestsFetcher",
    "Source",
]
