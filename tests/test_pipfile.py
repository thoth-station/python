#!/usr/bin/env python3
# thoth-python
# Copyright(C) 2018 Fridolin Pokorny
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

"""Tests for Pipfile and Pipfile.lock handling."""

import os

import pytest
import contoml as toml

from thoth.python import Pipfile
from thoth.python import PipfileLock
from thoth.python import PackageVersion
from thoth.python import Source

from .base import PythonTestCase


class TestPipfile(PythonTestCase):

    @pytest.mark.parametrize("pipfile", [
        'Pipfile_test1',
    ])
    def test_from_string(self, pipfile: str):
        with open(os.path.join(self.data_dir, 'pipfiles', pipfile), 'r') as pipfile_file:
            content = pipfile_file.read()

        instance = Pipfile.from_string(content)
        # Sometimes toml does not preserve inline tables causing to_string() fail. However, we produce valid toml.
        assert instance.to_dict() == toml.loads(content).primitive


class TestPipfileLock(PythonTestCase):

    @pytest.mark.parametrize("pipfile_lock", [
        'Pipfile_test1.lock',
    ])
    def test_from_string(self, pipfile_lock: str):
        with open(os.path.join(self.data_dir, 'pipfiles', pipfile_lock), 'r') as pipfile_lock_file:
            content = pipfile_lock_file.read()

        with open(os.path.join(self.data_dir, 'pipfiles', pipfile_lock[:-len('.lock')]), 'r') as pipfile_file:
            pipfile_content = pipfile_file.read()

        pipfile_instance = Pipfile.from_string(pipfile_content)
        instance = PipfileLock.from_string(content, pipfile=pipfile_instance)
        assert instance.to_string() == content

    def test_indexes_in_meta(self):
        pipfile = Pipfile.from_file(os.path.join(self.data_dir, 'pipfiles', 'Pipfile_test2'))
        package_version = PackageVersion(
            name='tensorflow',
            version='==1.9.0',
            develop=False,
            index=Source('http://tensorflow.pypi.thoth-station.ninja/index/fedora28/jemalloc/simple/tensorflow/')
        )
        pipfile.add_package_version(package_version)
        pipfile_dict = pipfile.to_dict()

        assert len(pipfile_dict['source']) == 2
        assert pipfile_dict['source'] == [
            {
                'url': 'https://pypi.org/simple',
                'verify_ssl': True,
                'name': 'pypi'
            },
            {
                'url': 'http://tensorflow.pypi.thoth-station.ninja/index/fedora28/jemalloc/simple/tensorflow/',
                'verify_ssl': True,
                'name': 'tensorflow-pypi-thoth-station-ninja'
            }
        ]
