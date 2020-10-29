#!/usr/bin/env python3
# thoth-python
# Copyright(C) 2020 Fridolin Pokorny
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
# type: ignore

"""Tests for module helpers."""

import os
from thoth.python.helpers import parse_requirements
from thoth.python.helpers import parse_requirement_str
from thoth.python import PackageVersion
from thoth.python import Source

from .base import PythonTestCase


class TestHelpers(PythonTestCase):
    """Test helpers module."""

    def test_parse_requirement_str(self) -> None:
        """Test parsing requirements string."""
        assert parse_requirement_str("Flask<1.1.0>0.12") == {
            "extra": [],
            "extras": [],
            "marker": None,
            "marker_evaluated": None,
            "marker_evaluation_error": None,
            "marker_evaluation_result": True,
            "normalized_package_name": "flask",
            "package_name": "Flask",
            "resolved_versions": [],
            "specifier": "<1.1.0>0.12",
        }
        assert parse_requirement_str("enum34; python_version <= '3.3'") == {
            "extra": [],
            "extras": [],
            "marker": 'python_version <= "3.3"',
            "marker_evaluated": 'python_version <= "3.3"',
            "marker_evaluation_error": None,
            "marker_evaluation_result": False,
            "normalized_package_name": "enum34",
            "package_name": "enum34",
            "resolved_versions": [],
            "specifier": None,
        }
        assert parse_requirement_str("selinon") == {
            "extra": [],
            "extras": [],
            "marker": None,
            "marker_evaluated": None,
            "marker_evaluation_error": None,
            "marker_evaluation_result": True,
            "normalized_package_name": "selinon",
            "package_name": "selinon",
            "resolved_versions": [],
            "specifier": None,
        }
        assert parse_requirement_str("click[cool]==7.0; python_version >= '2.7'") == {
            "extra": [],
            "extras": ["cool"],
            "marker": 'python_version >= "2.7"',
            "marker_evaluated": 'python_version >= "2.7"',
            "marker_evaluation_error": None,
            "marker_evaluation_result": True,
            "normalized_package_name": "click",
            "package_name": "click",
            "resolved_versions": [],
            "specifier": "==7.0",
        }

    def test_parse_requirements_empty(self) -> None:
        """Test parsing requirements file."""
        requirements_path = os.path.join(self.data_dir, "requirements", "parse_requirements_empty.txt")
        assert parse_requirements(requirements_path) == ([], [])

    def test_parse_requirements(self) -> None:
        """Test parsing requirements file."""
        requirements_path = os.path.join(self.data_dir, "requirements", "parse_requirements.txt")
        parsed = parse_requirements(requirements_path)
        assert isinstance(parsed, tuple)
        assert len(parsed) == 2
        assert parsed[0] == [
            Source(
                url="https://pypi.org/simple", name="pypi-org", verify_ssl=True, warehouse=True, warehouse_api_url=None
            ),
            Source(
                url="https://tensorflow.pypi.thoth-station.ninja/simple",
                name="tensorflow-pypi-thoth-station-ninja",
                verify_ssl=True,
                warehouse=False,
                warehouse_api_url=None,
            ),
        ]
        assert parsed[1] == [
            PackageVersion(
                name="click",
                version="==7.0",
                develop=False,
                index=None,
                hashes=["sha256:2335065e6395b9e67ca716de5f7526736bfa6ceead690adf616d925bdc622b13"],
                markers=None,
                extras=["cool"],
            ),
            PackageVersion(
                name="flask",
                version="<=1.1.1>0.12",
                develop=False,
                index=None,
                hashes=["sha256:45eb5a6fd193d6cf7e0cf5d8a5b31f83d5faae0293695626f539a823e93b13f6"],
                markers='python_version >= "2.7"',
            ),
            PackageVersion(
                name="werkzeug",
                version="==0.16.0",
                develop=False,
                index=None,
                hashes=["sha256:7280924747b5733b246fe23972186c6b348f9ae29724135a6dfc1e53cea433e7"],
                markers=None,
            ),
        ]
