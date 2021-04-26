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
# type: ignore

"""Test manipulation with constraints."""

import os
import pytest

from thoth.python import Constraints
from thoth.python import PackageVersion
from thoth.python import Source
from thoth.python.exceptions import ConstraintsError

from .base import PythonTestCase


class TestConstraints(PythonTestCase):
    """Test manipulation with constraints."""

    def test_from_file(self) -> None:
        """Test loading a constraint file."""
        constraints_instance = Constraints.from_file(os.path.join(self.data_dir, "constraints", "constraints_0.txt"))

        assert "pandas" in constraints_instance.package_versions
        assert constraints_instance.package_versions["pandas"].to_dict() == {
            "develop": False,
            "extras": [],
            "hashes": [],
            "index": None,
            "markers": '(implementation_name == "cpython" and os_name == "posix") or ' 'python_version >= "1.0"',
            "name": "pandas",
            "version": "==1.2.4",
        }

        assert "flask" in constraints_instance.package_versions
        assert constraints_instance.package_versions["flask"].to_dict() == {
            "develop": False,
            "extras": [],
            "hashes": [],
            "index": None,
            "markers": None,
            "name": "flask",
            "version": ">=1.0",
        }

        assert "numpy" in constraints_instance.package_versions
        assert constraints_instance.package_versions["numpy"].to_dict() == {
            "develop": False,
            "extras": [],
            "hashes": [],
            "index": None,
            "markers": 'python_version > "2.0"',
            "name": "numpy",
            "version": "~=2.0",
        }

    def test_from_file_multiple_name_error(self) -> None:
        """Test loading a constraint file that holds packages multiple times."""
        with pytest.raises(ConstraintsError):
            Constraints.from_file(os.path.join(self.data_dir, "constraints", "constraints_1.txt"))

    def test_from_file_no_file_error(self) -> None:
        """Test loading non-existing constraint file results in error."""
        with pytest.raises(ConstraintsError):
            Constraints.from_file(os.path.join(self.data_dir, "constraints", "constraints_that_does_not_exist.txt"))

    def test_from_file_empty(self) -> None:
        """Test loading empty constraints file results in empty constraints."""
        constraints_instance = Constraints.from_file(
            os.path.join(self.data_dir, "constraints", "constraints_empty.txt")
        )
        assert constraints_instance.package_versions == {}

    def test_from_string(self) -> None:
        """Test loading constraints from a string."""
        assert Constraints.from_string("").package_versions == {}, "Failed to load constraints from an empty string"

        constraints_txt = """\
flask>=1.0
numpy~=2.0; python_version > '2.0'
pandas==1.2.4; (implementation_name == 'cpython' and os_name == 'posix') or python_version >= '1.0'
"""
        constraints_instance = Constraints.from_string(constraints_txt)

        assert "pandas" in constraints_instance.package_versions
        assert constraints_instance.package_versions["pandas"].to_dict() == {
            "develop": False,
            "extras": [],
            "hashes": [],
            "index": None,
            "markers": '(implementation_name == "cpython" and os_name == "posix") or ' 'python_version >= "1.0"',
            "name": "pandas",
            "version": "==1.2.4",
        }

        assert "flask" in constraints_instance.package_versions
        assert constraints_instance.package_versions["flask"].to_dict() == {
            "develop": False,
            "extras": [],
            "hashes": [],
            "index": None,
            "markers": None,
            "name": "flask",
            "version": ">=1.0",
        }

        assert "numpy" in constraints_instance.package_versions
        assert constraints_instance.package_versions["numpy"].to_dict() == {
            "develop": False,
            "extras": [],
            "hashes": [],
            "index": None,
            "markers": 'python_version > "2.0"',
            "name": "numpy",
            "version": "~=2.0",
        }

    def test_from_package_versions(self) -> None:
        """Test loading constraints from the package version abstraction."""
        assert Constraints.from_package_versions([]).package_versions == {}

        package_version_flask = PackageVersion(
            name="flask", version=">=1.0.0", index=Source("https://pypi.org/simple"), develop=False
        )

        package_version_numpy = PackageVersion(
            name="numpy", version="~=1.20.0", index=Source("https://pypi.org/simple"), develop=False
        )

        package_versions = [package_version_numpy, package_version_flask]
        constraints_instance = Constraints.from_package_versions(package_versions)
        assert constraints_instance.package_versions == {
            "flask": package_version_flask,
            "numpy": package_version_numpy,
        }

    def test_from_package_versions_error(self) -> None:
        """Test error-ing out loading constraints from the package version abstraction."""
        package_version_flask_1 = PackageVersion(
            name="flask", version=">=1.0.0", index=Source("https://pypi.org/simple"), develop=False
        )

        package_version_flask_2 = PackageVersion(
            name="flask", version="~=0.12", index=Source("https://pypi.org/simple"), develop=False
        )

        package_versions = [package_version_flask_1, package_version_flask_2]
        with pytest.raises(ConstraintsError):
            Constraints.from_package_versions(package_versions)

    def test_from_dict(self) -> None:
        """Test loading constraints from a dictionary representation."""
        serialized = [
            {"name": "flask", "version": ">=1.0.0", "markers": "python_version >= '3.6'"},
            {"name": "numpy", "version": "~=1.20.0"},
        ]
        constraints_instance = Constraints.from_dict(serialized)
        assert constraints_instance.to_dict() == [
            {"name": "flask", "version": ">=1.0.0", "markers": "python_version >= '3.6'"},
            {"name": "numpy", "version": "~=1.20.0", "markers": None},
        ]

    def test_from_dict_error(self) -> None:
        """Test error reported when loading unknown entries."""
        with pytest.raises(ConstraintsError):
            Constraints.from_dict([{"name": "pandas", "version": "==1.0.0", "hashes": "sha256:xoxo"}])
