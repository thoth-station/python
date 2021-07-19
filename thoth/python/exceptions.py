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

"""Exceptions used in the thoth-python package."""


class ThothPythonExceptionError(Exception):
    """A base class for thoth-python exceptions."""


class DirectDependencyRemovalError(ThothPythonExceptionError):
    """Raised if trying to remove direct dependency from application stack.

    Or there is no option to remove the given dependency from application stack.
    """


class UnableLockError(ThothPythonExceptionError):
    """Raised if trying to lock invalid application stack or resolution cannot be done."""


class PipfileParseError(ThothPythonExceptionError):
    """An exception raised on invalid Pipfile or Pipfile.lock."""


class InternalError(ThothPythonExceptionError):
    """An exception raised on bugs in the code base."""


class PackageVersionAlreadyPresentError(ThothPythonExceptionError):
    """An exception raised when adding a package in specific version that is already present."""


class SourceNotFoundError(ThothPythonExceptionError):
    """An exception raise when the given package source is not found."""


class ConstraintsError(ThothPythonExceptionError):
    """An exception raised when an issue with constraints found."""


class VersionIdentifierError(ThothPythonExceptionError):
    """An exception raised if the given version identifier is not a semver identifier."""


class UnsupportedConfigurationError(ThothPythonExceptionError):
    """Raised on unsupported configuration options."""


class NotFoundError(ThothPythonExceptionError):
    """Raised if the given artifact cannot be found."""


class FileLoadError(ThothPythonExceptionError):
    """Raised when failed to open or parse a file."""
