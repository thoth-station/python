#!/usr/bin/env python3
# thoth-python
# Copyright(C) 2021 Fridolin Pokorny
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

"""Implementation of an abstraction keeping constraints."""

import logging

from typing import Any
from typing import Dict
from typing import List

import attr
from .package_version import PackageVersion
from .helpers import parse_requirements
from .helpers import parse_requirements_str

from .exceptions import ConstraintsError

_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class Constraints:
    """Constraints manipulation."""

    package_versions = attr.ib(type=Dict[str, PackageVersion], kw_only=True, default=attr.Factory(dict))

    @classmethod
    def from_file(cls, constraints_file: str) -> "Constraints":
        """Load constraints from a file."""
        try:
            _, package_versions = parse_requirements(constraints_file)
        except Exception as exc:
            raise ConstraintsError(f"Failed to parse constraints: {str(exc)}") from exc

        return cls.from_package_versions(package_versions)

    @classmethod
    def from_string(cls, content: str) -> "Constraints":
        """Load constraints from a string."""
        try:
            _, package_versrsions = parse_requirements_str(content)
        except Exception as exc:
            raise ConstraintsError(f"Failed to parse constraints: {str(exc)}") from exc

        return cls.from_package_versions(package_versrsions)

    @classmethod
    def from_dict(cls, dict_: List[Dict[str, Any]]) -> "Constraints":
        """Instantiate constraints from a dictionary representation."""
        package_versions = []
        for item in dict_:
            name = item.get("name")
            if not name:
                raise ConstraintsError(f"Name of a package not provided in constraints entry: {str(item)}")

            unknown = set(item.keys()) - {"name", "version", "markers"}
            if unknown:
                raise ConstraintsError(
                    f"Unknown entries in the constraint serialized representation: {', '.join(unknown)}"
                )

            package_version = PackageVersion(
                name=name,
                version=item.get("version"),
                markers=item.get("markers"),
                develop=False,
                index=None,
                hashes=[],
                extras=[],
            )
            package_versions.append(package_version)

        return cls.from_package_versions(package_versions)

    @classmethod
    def from_package_versions(cls, package_versions: List[PackageVersion]) -> "Constraints":
        """Instantiate constraints from package versions, perform checks to verify correct instance."""
        package_versions_dict = {}
        for pv in package_versions:
            if pv.name in package_versions_dict:
                raise ConstraintsError(f"Multiple constraints found for package {pv.name!r}")

            if pv.extras:
                raise ConstraintsError(
                    f"Specifying extras in constraints is not supported for {pv.name!r}: {pv.extras!r}"
                )

            if pv.hashes:
                raise ConstraintsError(f"Specifying hashes in constraints is not supported for {pv.name}")

            package_versions_dict[pv.name] = pv

        return cls(package_versions=package_versions_dict)

    def to_dict(self) -> List[Dict[str, Any]]:
        """Serialize constraint instance to a dictionary representation."""
        result = []
        for package_version in self.package_versions.values():
            # Use only constraint relevant fields for package version abstraction.
            result.append(
                {
                    "name": package_version.name,
                    "version": package_version.version,
                    "markers": package_version.markers,
                }
            )

        return result
