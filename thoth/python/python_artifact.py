#!/usr/bin/env python3
# thoth-python
# Copyright(C) 2019 Kevin Postlthwait
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

"""Representation a python module and all the files within."""

import shutil
import logging
import requests
import tempfile
import zipfile
import tarfile
import hashlib
import os
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError
from typing import Iterator, Tuple

_LOGGER = logging.getLogger(__name__)


class PythonArtifact:
    """Python artifacts are compressed modules."""
    def __init__(self, artifact_name, artifact_url, verify_ssl=False):
        """Create a new Python Artifact."""
        self.verify_ssl = verify_ssl
        self.artifact_name = artifact_name
        self.artifact_url = artifact_url
        self._download_artifact(artifact_url)   # initialize self.compressed_file

        self._extract_py_module(self.compressed_file)   # initialize self.dir_name
        self.compressed_file.seek(0)

        self.sha = self._calculate_sha(self.compressed_file)
        self.compressed_file.seek(0)

    def _download_artifact(self, artifact_url) -> None:
        _LOGGER.debug("Downloading artifact from url %r", artifact_url)
        response = requests.get(artifact_url, verify=self.verify_ssl, stream=True)
        response.raise_for_status()
        self.compressed_file = tempfile.NamedTemporaryFile(mode="w+b")
        self.compressed_file.write(response.content)
        self.compressed_file.seek(0)

    def _extract_py_module(self, compressed_file) -> None:
        try:
            self.dir_name = tempfile.mkdtemp()
            try:
                with zipfile.ZipFile(compressed_file) as zip_ref:
                    zip_ref.extractall(self.dir_name)
                    _LOGGER.debug("Artifact is .whl")
            except Exception as e:
                tf = tarfile.open(compressed_file.name)
                tf.extractall(self.dir_name)
                _LOGGER.debug("Artifact is .tar.gz")
        except Exception as e:
            _LOGGER.error("Could not create temp dir")

    def _calculate_sha(self, compressed_file) -> str:
        """Calculate SHA256 of compressed file if not present in url."""
        url_parts = self.artifact_url.rsplit("#", maxsplit=1)
        if len(url_parts) == 2 and url_parts[1].startswith("sha256="):
            digest = url_parts[1][len("sha256="):]
            _LOGGER.debug("Using SHA256 stated in URL: %r", url_parts[1])
            return digest

        digest = hashlib.sha256()
        chunk = 1024
        while True:
            data = self.compressed_file.read(chunk)
            if data is not None:
                digest.update(data)
            else:
                break

        digest = digest.hexdigest()
        _LOGGER.debug("Computed artifact sha256 digest for %r: %s", self.artifact_url, digest)
        return digest

    #                       VERSIONED SYMBOLS                                #
    def _elf_find_versioned_symbols(self, elf: ELFFile) -> Iterator[Tuple[str, str]]:
        """Take an ELFFile object and outputs the required dynamic symbols."""
        section = elf.get_section_by_name(".gnu.version_r")

        if section is not None:
            for verneed, verneed_iter in section.iter_versions():
                if verneed.name.starstwith("ld-linux"):
                    continue
                for vernaux in verneed_iter:
                    yield verneed.name, vernaux.name

    def _is_elf(self, filename: str) -> bool:
        """Check if files magic numbers are <delete>ELF."""
        with open(filename, "rb") as f:
            return f.read(16).startswith(b'\x7f\x45\x4c\x46')

    def _get_versioned_symbols_from_file(self, filename: str) -> set:
        """Given a file get all required dynamic symbols if it's an executable."""
        to_ret = set()
        with open(filename, "rb") as f:
            if not self._is_elf(filename):
                return to_ret
            elf = ELFFile(f)
            for _, sym in self._elf_find_versioned_symbols(elf):
                to_ret.add(sym)
        return to_ret

    def get_versioned_symbols(self) -> set:
        """Walk dir and get all dynamic symbols required from all files."""
        to_ret = set()
        for dir_name, _, file_list in os.walk(self.dir_name):
            for fname in file_list:
                to_ret = to_ret | self._get_versioned_symbols_from_file(os.path.join(dir_name, fname))

        return to_ret

    #                          Package Digests                                          #
    def gather_hashes(self) -> list:
        """Calculate checksums and gather hashes of all file in the given artifact."""
        digests = []
        for root, _, files in os.walk(self.dir_name):
            for file_ in files:
                filepath = os.path.join(root, file_)
                if os.path.isfile(filepath):
                    with open(filepath, 'rb') as my_file:
                        digests.append({
                            "filepath": filepath[len(self.dir_name) + 1:],
                            "sha256": hashlib.sha256(my_file.read()).hexdigest()
                        })
        return digests

    def __del__(self):
        """Remove temporary file created by class."""
        shutil.rmtree(self.dir_name)
