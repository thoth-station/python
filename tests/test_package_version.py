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

"""Tests for package-version parsing and handling."""

import pytest

from thoth.python.package_version import PackageVersion
from thoth.python.pipfile import PipfileMeta
from thoth.python.exceptions import UnsupportedConfiguration
from thoth.python.exceptions import PipfileParseError
from thoth.python.exceptions import InternalError

from .base import PythonTestCase

# Share meta for all the sources.
_META = PipfileMeta.from_dict({
    "hash": {
        "sha256": "ffd9f5a6a04f9aa6c56cbf43ceda5c41644b1d2304a6b798a654b6e421c7d23a"
    },
    "pipfile-spec": 6,
    "requires": {},
    "sources": [
        {
            "name": "pypi",
            "url": "https://pypi.python.org/simple",
            "verify_ssl": True
        },
        {
            "name": "redhat-aicoe-experiments",
            "url": "https://index-aicoe.a3c1.starter-us-west-1.openshiftapps.com",
            "verify_ssl": True
        }

    ]
})


class TestPackageVersion(PythonTestCase):

    @pytest.mark.parametrize(
        "package_name,package_info,expected_values,is_locked",
        [
            (
                'tensorflow',
                {'version': '==1.9.0rc0', 'index': 'redhat-aicoe-experiments'},
                {'index': 'redhat-aicoe-experiments', 'version': '==1.9.0rc0'},
                True
            ),
            (
                'tensorflow',
                {'version': '*'},
                {'index': None, 'version': '*'},
                False
            ),
            (
                'tensorflow',
                {'version': '<1.9'},
                {'index': None, 'version': '<1.9'},
                False
            )
        ]
    )
    def test_from_pipfile_entry(self, package_name, package_info, expected_values, is_locked):
        package_version = PackageVersion.from_pipfile_entry(
            package_name,
            package_info,
            develop=False,
            meta=_META
        )

        for name, value in expected_values.items():
            if name == 'index':
                if value is None:
                    assert package_version.index is None
                    continue

                assert package_version.index is not None
                package_version.index.name == value
                continue

            assert getattr(package_version, name) == value,\
                f"Expected value for {name} for instance does not match: {value}"

        assert package_version.is_locked() is is_locked

    @pytest.mark.parametrize(
        "package_name,package_info",
        [
            (
                'igitt',
                {'git': 'https://gitlab.com/gitmate/open-source/IGitt.git'}
            )
        ]
    )
    def test_from_pipfile_entry_error(self, package_name, package_info):
        with pytest.raises(UnsupportedConfiguration):
            PackageVersion.from_pipfile_entry(package_name, package_info, develop=False, meta=_META)

    @pytest.mark.parametrize(
        "package_name,package_info,expected_values",
        [
            (
                'tensorflow',
                {'version': '==1.9.0rc0', 'index': 'redhat-aicoe-experiments', 'hashes':
                    [
                        "sha256:9c2dc36b84f3729361990b4488b7fde1cbe5afb9e3b59456aafc6928684fcd4b"
                    ]
                 },
                {'index': 'redhat-aicoe-experiments', 'version': '==1.9.0rc0', 'hashes':
                    [
                        "sha256:9c2dc36b84f3729361990b4488b7fde1cbe5afb9e3b59456aafc6928684fcd4b"
                    ]
                 }
            )
        ]
    )
    def test_from_pipfile_lock_entry(self, package_name, package_info, expected_values):
        package_version = PackageVersion.from_pipfile_lock_entry(
            package_name,
            package_info,
            develop=False,
            meta=_META
        )

        for name, value in expected_values.items():
            if name == 'index':
                assert package_version.index.name == value
                continue

            assert getattr(package_version, name) == value, \
                f"Expected value {name} for locked package {package_name} does not match: {value}"

        assert package_version.is_locked() is True

    @pytest.mark.parametrize(
        "package_name,package_info",
        [
            (
                # Package index not used.
                'igitt',
                {'git': 'https://gitlab.com/gitmate/open-source/IGitt.git'}
            ),
            (
                # No hashes present.
                'tensorflow',
                {'version': '==1.9.0rc0', 'index': 'redhat-aicoe-experiments', 'hashes': []}
            ),
            (
                # Missing version information.
                'tensorflow',
                {'index': 'redhat-aicoe-experiments', 'hashes':
                    [
                        "sha256:9c2dc36b84f3729361990b4488b7fde1cbe5afb9e3b59456aafc6928684fcd4b"
                    ]
                 }
            )
        ]
    )
    def test_from_pipfile_lock_entry_error(self, package_name, package_info):
        with pytest.raises(PipfileParseError):
            PackageVersion.from_pipfile_lock_entry(
                package_name,
                package_info,
                develop=False,
                meta=_META
            )

    def test_parse_semver(self):
        package_version = PackageVersion(
            name="tensorflow",
            version="==1.9.0",
            index="https://pypi.org/simple",
            develop=False
        )
        assert package_version.semantic_version.major == 1
        assert package_version.semantic_version.minor == 9
        assert package_version.semantic_version.patch == 0

    def test_parse_semver_leading_zeros(self):
        package_version = PackageVersion(
            name="pyyaml",
            version="==3.01.2",
            index="https://pypi.org/simple",
            develop=False
        )
        assert package_version.semantic_version.major == 3
        assert package_version.semantic_version.minor == 1
        assert package_version.semantic_version.patch == 2

    def test_sorted(self):
        array = []
        for version in ('==1.0.0', '==0.1.0', '==3.0.0'):
            array.append(PackageVersion(name='tensorflow', version=version, develop=False))

        assert sorted(pv.locked_version for pv in array) == ['0.1.0', '1.0.0', '3.0.0']

    def test_semver_error(self):
        with pytest.raises(InternalError):
            return PackageVersion(name='tensorflow', version='>1.0.0', develop=False).semantic_version

    def test_version_specification(self):
        pv = PackageVersion(name='tensorflow', version='==0.1.0', develop=False).semantic_version
        vs = PackageVersion(name='tensorflow', version='<1.0.0', develop=False).version_specification
        assert pv in vs

        pv = PackageVersion(name='tensorflow', version='==2.1.0', develop=False).semantic_version
        assert pv not in vs

        vs = PackageVersion(name='tensorflow', version='==2.1.0', develop=False).version_specification
        assert pv in vs

    def test_normalize_python_package_name(self):
        package_version = PackageVersion(name='Cython', version='0.29.13', develop=False)
        assert package_version.name == "cython"

        package_version = PackageVersion(name='semantic_version', version='2.6.0', develop=False)
        assert package_version.name == "semantic-version"

        package_version = PackageVersion(name='delegator.py', version='0.1.1', develop=False)
        assert package_version.name == "delegator-py"

    def test_normalize_python_package_version(self):
        package_version = PackageVersion(name='oauth2client', version='1.0beta2', develop=False)
        assert package_version.version == "1.0b2"

        package_version = PackageVersion(name="regex", version="2019.02.06", develop=False)
        assert package_version.version == "2019.2.6"

        package_version = PackageVersion(name="xgboost", version="0.7.post2", develop=False)
        assert package_version.version == "0.7.post2"

        package_version = PackageVersion(name="xgboost", version="0.71", develop=False)
        assert package_version.version == "0.71"

        package_version = PackageVersion(name="ipywidgets", version="6.0.0.rc3", develop=False)
        assert package_version.version == "6.0.0rc3"

        package_version = PackageVersion(name="pytz", version="2011b", develop=False)
        assert package_version.version == "2011b0"

        package_version = PackageVersion(name="gitpython", version="0.3.2.RC1", develop=False)
        assert package_version.version == "0.3.2rc1"

        package_version = PackageVersion(name="ipywidgets", version="5.0.0.b5", develop=False)
        assert package_version.version == "5.0.0b5"
