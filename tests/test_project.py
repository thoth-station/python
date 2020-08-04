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
# type: ignore

"""Tests for module project."""

import os

import attr
import pytest
from packaging.version import Version

from thoth.common import cwd
from thoth.python import Project
from thoth.python import Source
from thoth.python import Pipfile
from thoth.python import PipfileLock
from thoth.python import PackageVersion
from thoth.python.exceptions import InternalError
from thoth.python.exceptions import FileLoadError

from .base import PythonTestCase


class TestProject(PythonTestCase):
    """Test TestProject module."""

    def test_add_package(self):
        """Test add package."""
        pipfile = Pipfile.from_file(os.path.join(self.data_dir, "pipfiles", "Pipfile_test1"))
        pipfile_lock = PipfileLock.from_file(os.path.join(self.data_dir, "pipfiles", "Pipfile_test1.lock"))
        project = Project(pipfile=pipfile, pipfile_lock=pipfile_lock)

        assert "selinon" not in project.pipfile.packages.packages
        project.add_package("selinon", "==1.0.0")

        assert "selinon" in project.pipfile.packages.packages
        assert project.pipfile.packages["selinon"].version == "==1.0.0"
        assert project.pipfile.packages["selinon"].index is None
        assert project.pipfile.packages["selinon"].develop is False

        # Do not add the package to the lock - lock has to be explicitly done.
        assert "selinon" not in project.pipfile_lock.packages.packages

    def test_add_package_develop(self):
        """Test add package develop."""
        pipfile = Pipfile.from_file(os.path.join(self.data_dir, "pipfiles", "Pipfile_test1"))
        pipfile_lock = PipfileLock.from_file(os.path.join(self.data_dir, "pipfiles", "Pipfile_test1.lock"))
        project = Project(pipfile=pipfile, pipfile_lock=pipfile_lock)

        source = Source(name="foo", url="https://foo.bar", verify_ssl=True, warehouse=False)

        assert "selinon" not in project.pipfile.dev_packages.packages

        with pytest.raises(InternalError):
            # Trying to add package with source but source is not present in the meta.
            project.add_package("selinon", "==1.0.0", develop=True, source=source)

        source = project.add_source(url="https://foo.bar")
        project.add_package("selinon", "==1.0.0", develop=True, source=source)

        assert "selinon" in project.pipfile.dev_packages.packages
        assert project.pipfile.dev_packages["selinon"].version == "==1.0.0"
        assert project.pipfile.dev_packages["selinon"].index == "foo-bar"
        assert project.pipfile.dev_packages["selinon"].develop is True
        # Do not add the package to the lock - lock has to be explicitly done.
        assert "selinon" not in project.pipfile_lock.dev_packages.packages

    def test_add_source(self):
        """Test add source."""
        pipfile = Pipfile.from_file(os.path.join(self.data_dir, "pipfiles", "Pipfile_test1"))
        pipfile_lock = PipfileLock.from_file(os.path.join(self.data_dir, "pipfiles", "Pipfile_test1.lock"))
        project = Project(pipfile=pipfile, pipfile_lock=pipfile_lock)

        source = project.add_source(url="https://foo.bar")

        assert source.name is not None

        assert source.name in project.pipfile.meta.sources
        assert source is project.pipfile.meta.sources[source.name]

        assert source.name in project.pipfile_lock.meta.sources
        assert source is project.pipfile_lock.meta.sources[source.name]

    def test_get_outdated_package_versions_indirect(self):
        """Test get outdated package versions indirect."""
        # The difference between direct and indirect - Pipenv states "index" in
        # the Pipfile.lock file if the given package is a direct dependency.
        # The "index" key for indirect dependencies is omitted though. This way
        # we check both - logic for indirect/direct is slightly different.
        # We cannot use flexmock as Source has slots.
        @attr.s
        class MySource:
            url = attr.ib(type=str)
            verify_ssl = attr.ib(type=bool)
            name = attr.ib(type=str)
            warehouse = attr.ib(type=bool, default=False)
            warehouse_api_url = attr.ib(default=None, type=str)

            def get_latest_package_version(_, package_name):  # noqa: N805
                return {
                    "certifi": PackageVersion.parse_semantic_version("2018.10.15"),
                    "chardet": PackageVersion.parse_semantic_version("3.0.4"),
                    "idna": PackageVersion.parse_semantic_version("2.10"),  # Bumped from 2.7
                    "requests": PackageVersion.parse_semantic_version("2.19.1"),
                    "termcolor": PackageVersion.parse_semantic_version("1.1.0"),
                    "urllib3": PackageVersion.parse_semantic_version("1.23"),
                }[package_name]

        project = Project.from_files(
            os.path.join(self.data_dir, "pipfiles", "Pipfile_test2"),
            os.path.join(self.data_dir, "pipfiles", "Pipfile_test2.lock"),
        )

        new_sources = {}
        for source in project.pipfile_lock.meta.sources.values():
            new_sources[source.name] = MySource(**source.to_dict())
        project.pipfile_lock.meta.sources = new_sources

        for package_version in project.iter_dependencies_locked(with_devel=True):
            if package_version.index:
                package_version.index = new_sources[package_version.index.name]

        result = project.get_outdated_package_versions()
        assert len(result) == 1
        assert "idna" in result
        assert len(result["idna"]) == 2
        assert result["idna"][0] is project.pipfile_lock.packages["idna"]
        assert isinstance(result["idna"][1], Version)
        assert str(result["idna"][1]) == "2.10"

    def test_get_outdated_package_versions_direct(self):
        """Test get outdated package versions direct."""
        # See previous test comments for more info.
        # We cannot use flexmock as Source has slots.
        @attr.s
        class MySource:
            url = attr.ib(type=str)
            verify_ssl = attr.ib(type=bool)
            name = attr.ib(type=str)
            warehouse = attr.ib(type=bool, default=False)
            warehouse_api_url = attr.ib(default=None, type=str)

            def get_latest_package_version(_, package_name):  # noqa: N805
                return {
                    "certifi": PackageVersion.parse_semantic_version("2018.10.15"),
                    "chardet": PackageVersion.parse_semantic_version("3.0.4"),
                    "idna": PackageVersion.parse_semantic_version("2.7"),
                    "requests": PackageVersion.parse_semantic_version("3.0.0"),
                    "termcolor": PackageVersion.parse_semantic_version("1.1.0"),
                    "urllib3": PackageVersion.parse_semantic_version("1.23"),
                }[package_name]

        project = Project.from_files(
            os.path.join(self.data_dir, "pipfiles", "Pipfile_test2"),
            os.path.join(self.data_dir, "pipfiles", "Pipfile_test2.lock"),
        )

        new_sources = {}
        for source in project.pipfile_lock.meta.sources.values():
            new_sources[source.name] = MySource(**source.to_dict())
        project.pipfile_lock.meta.sources = new_sources

        for package_version in project.iter_dependencies_locked(with_devel=True):
            if package_version.index:
                package_version.index = new_sources[package_version.index.name]

        result = project.get_outdated_package_versions()
        assert len(result) == 1
        assert "requests" in result
        assert len(result["requests"]) == 2
        assert result["requests"][0] is project.pipfile_lock.packages["requests"]
        assert isinstance(result["requests"][1], Version)
        assert str(result["requests"][1]) == "3.0.0"

    def test_indexes_in_meta(self):
        """Check indexes being adjusted when inserting a new package."""
        package_version = PackageVersion(
            name="tensorflow",
            version="==1.9.0",
            develop=False,
            index=Source("http://tensorflow.pypi.thoth-station.ninja/index/fedora28/jemalloc/simple/tensorflow/"),
        )

        project = Project.from_package_versions([package_version])

        project_dict = project.to_dict()
        pipfile_dict = project_dict["requirements"]
        pipfile_lock_dict = project_dict["requirements_locked"]

        assert pipfile_lock_dict is None

        assert len(pipfile_dict["source"]) == 1
        assert pipfile_dict["source"] == [
            {
                "url": "http://tensorflow.pypi.thoth-station.ninja/index/fedora28/jemalloc/simple/tensorflow/",
                "verify_ssl": True,
                "name": "tensorflow-pypi-thoth-station-ninja",
            }
        ]

    def test_from_pip_compile_files_example_dir2(self) -> None:
        """Test loading project from pip-compile files."""
        with cwd(os.path.join(self.data_dir, "requirements", "example_dir2")):
            assert Project.from_pip_compile_files(allow_without_lock=False) == Project.from_pip_compile_files(
                allow_without_lock=True
            )
            project = Project.from_pip_compile_files(allow_without_lock=False)

        assert list(project.iter_dependencies()) == [
            PackageVersion(name="flask", version="*", develop=False, index=Source(url="https://pypi.org/simple"))
        ]
        assert list(project.iter_dependencies_locked()) == [
            PackageVersion(
                name="click",
                version="==7.0",
                develop=False,
                index=Source(url="https://pypi.org/simple"),
                hashes=["sha256:2335065e6395b9e67ca716de5f7526736bfa6ceead690adf616d925bdc622b13"],
            ),
            PackageVersion(
                name="flask",
                version="==1.1.1",
                develop=False,
                index=Source(url="https://pypi.org/simple"),
                hashes=["sha256:45eb5a6fd193d6cf7e0cf5d8a5b31f83d5faae0293695626f539a823e93b13f6"],
            ),
            PackageVersion(
                name="itsdangerous",
                version="==1.1.0",
                develop=False,
                index=Source(url="https://pypi.org/simple"),
                hashes=["sha256:b12271b2047cb23eeb98c8b5622e2e5c5e9abd9784a153e9d8ef9cb4dd09d749"],
            ),
            PackageVersion(
                name="jinja2",
                version="==2.10.3",
                develop=False,
                index=Source(url="https://pypi.org/simple"),
                hashes=["sha256:74320bb91f31270f9551d46522e33af46a80c3d619f4a4bf42b3164d30b5911f"],
            ),
            PackageVersion(
                name="markupsafe",
                version="==1.1.1",
                develop=False,
                index=Source(url="https://pypi.org/simple"),
                hashes=["sha256:09027a7803a62ca78792ad89403b1b7a73a01c8cb65909cd876f7fcebd79b161"],
            ),
            PackageVersion(
                name="werkzeug",
                version="==0.16.0",
                develop=False,
                index=Source(url="https://pypi.org/simple"),
                hashes=["sha256:e5f4a1f98b52b18a93da705a7458e55afb26f32bff83ff5d19189f92462d65c4"],
            ),
        ]

    def test_from_pip_compile_files_example_dir1(self) -> None:
        """Test loading only if requirements.txt is present."""
        with cwd(os.path.join(self.data_dir, "requirements", "example_dir1")):
            with pytest.raises(FileLoadError):
                Project.from_pip_compile_files()

            project = Project.from_pip_compile_files(allow_without_lock=True)

            assert project.pipfile_lock is None
            assert list(project.iter_dependencies()) == [
                PackageVersion(
                    name="click", version="*", develop=False, hashes=[], index=Source("https://pypi.org/simple")
                )
            ]

    def test_from_pip_compile_files_example_dir3(self) -> None:
        """Test loading only if only requirements.in is present."""
        with cwd(os.path.join(self.data_dir, "requirements", "example_dir3")):
            project = Project.from_pip_compile_files(allow_without_lock=True)

            assert project.pipfile_lock is None
            assert list(project.iter_dependencies()) == [
                PackageVersion(name="flask", version="*", develop=False, hashes=[], index=None)
            ]
