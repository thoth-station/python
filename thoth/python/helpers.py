#!/usr/bin/env python3
# thoth-python
# Copyright(C) 2018-2021 Fridolin Pokorny
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


"""Helper functions and utilities."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import TYPE_CHECKING
from itertools import chain
import logging
from packaging.requirements import Requirement
from packaging.markers import Variable
from packaging.markers import Op
from packaging.markers import Value
from packaging.utils import canonicalize_name

from .source import Source
from .package_version import PackageVersion
from .exceptions import FileLoadError

if TYPE_CHECKING:
    from .project import Project

_LOGGER = logging.getLogger(__name__)


def fill_package_digests(generated_project: "Project") -> "Project":
    """Temporary fill package digests stated in Pipfile.lock."""
    if generated_project.pipfile_lock is None:
        raise ValueError("Generated project PipfileLock is not set.")
    for package_version in chain(generated_project.pipfile_lock.packages, generated_project.pipfile_lock.dev_packages):
        if package_version.hashes:
            # Already filled from the last run.
            continue

        if package_version.index:
            scanned_hashes = package_version.index.get_package_hashes(
                package_version.name, package_version.locked_version
            )
        else:
            for source in generated_project.pipfile.meta.sources.values():
                try:
                    scanned_hashes = source.get_package_hashes(package_version.name, package_version.locked_version)
                    break
                except Exception:
                    continue
            else:
                raise ValueError("Unable to find package hashes")

        for entry in scanned_hashes:
            package_version.hashes.append("sha256:" + entry["sha256"])

    return generated_project


def _marker_reduction(marker, extra):  # type: ignore
    """Convert internal packaging marker representation to interpretation which can be evaluated.

    As markers also depend on `extra' which will cause issues when evaluating marker in the solver
    environment, let's substitute `extra' marker with a condition which evaluates always to true.
    """
    if isinstance(marker, str):
        return marker

    if isinstance(marker, list):
        result_markers = []
        for nested_marker in marker:
            reduced_marker = _marker_reduction(nested_marker, extra)  # type: ignore
            result_markers.append(reduced_marker)

        return result_markers

    if marker[0].value != "extra":
        return marker

    extra.add(str(marker[2]))
    # A special case to handle extras in markers - substitute extra with a marker which always evaluates to true:
    return Variable("python_version"), Op(">="), Value("0.0")


def parse_requirement_str(requirement_str: str) -> Dict[str, Any]:
    """Parse a string representation of marker."""
    # Some notes on this implementation can be found at: https://github.com/pypa/packaging/issues/211
    requirement = Requirement(requirement_str)

    evaluation_result = None
    evaluation_error = None
    extra = set()  # type: Set[str]
    marker_evaluated_str = None
    marker_str = str(requirement.marker) if requirement.marker else None
    if requirement.marker:
        # We perform a copy of marker specification during the traversal so that we
        # do not evaluate "extra" marker - according to PEP-508, this behavior
        # raises an error if the interpreting environment does not explicitly
        # define them. As we are aggregating "generic" data and extra is
        # user-defined on the actual resolution, we exclude this extra marker
        # here.
        markers_copy = []
        for marker in requirement.marker._markers:
            marker_copy = _marker_reduction(marker, extra)  # type: ignore
            markers_copy.append(marker_copy)

        try:
            requirement.marker._markers = markers_copy
            evaluation_result = requirement.marker.evaluate()
            marker_evaluated_str = str(requirement.marker)
        except Exception as exc:
            _LOGGER.exception("Failed to evaluate marker {}".format(requirement.marker))
            evaluation_error = str(exc)
    else:
        evaluation_result = True

    return {
        "package_name": requirement.name,
        "normalized_package_name": canonicalize_name(requirement.name),
        "specifier": str(requirement.specifier) if requirement.specifier else None,
        "resolved_versions": [],
        "extras": list(requirement.extras),
        "extra": list(extra),
        "marker": marker_str,
        "marker_evaluated": marker_evaluated_str,
        "marker_evaluation_result": evaluation_result,
        "marker_evaluation_error": evaluation_error,
    }


def parse_requirements(file_path: str) -> Tuple[List[Source], List[PackageVersion]]:
    """Parse requirements.{txt,in} file."""
    try:
        with open(file_path, "r") as input_file:
            content = input_file.read()
    except Exception as exc:
        raise FileLoadError(f"Failed to load requirements file at {file_path!r}: {str(exc)}") from exc

    return parse_requirements_str(content)


def parse_requirements_str(
    requirements: str, _file_path: Optional[str] = None
) -> Tuple[List[Source], List[PackageVersion]]:
    """Parse content of requirements.{txt,in} file."""
    sources = []
    package_versions = []

    # Remove escaped new lines.
    content = requirements.replace("\\\n", "")
    for line in content.splitlines():
        line = line.lstrip()
        if line.startswith("#"):
            continue

        if not line:
            continue

        if line.startswith(("-i", "--index-url", "--extra-index-url")):
            index_url = line.split(" ", maxsplit=1)[1]
            sources.append(Source(index_url))
            continue

        if line.startswith("-"):
            if _file_path:
                _LOGGER.warning("Ignoring line in %r: %s", _file_path, line)
            else:
                _LOGGER.warning("Ignoring line: %s", line)

            continue

        parts = line.split("--hash=")
        hashes = parts[1:]

        req = parse_requirement_str(parts[0])
        package_versions.append(
            PackageVersion(
                name=req["normalized_package_name"],
                version=req["specifier"] or "*",
                extras=req["extras"],
                markers=req["marker"] or None,
                hashes=hashes,
                develop=False,  # XXX: we could add Thoth's specific comment for develop packages.
            )
        )

    return sources, package_versions
