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

"""Exceptions used in the thoth-python package."""


class ThothPythonException(Exception):
    """A base class for thoth-python exceptions."""


class DirectDependencyRemoval(ThothPythonException):
    """Raised if trying to remove direct dependency from application stack.

    Or there is no option to remove the given dependency from application stack.
    """


class UnableLock(ThothPythonException):
    """Raised if trying to lock invalid application stack or resolution cannot be done."""


class PipfileParseError(ThothPythonException):
    """An exception raised on invalid Pipfile or Pipfile.lock."""


class InternalError(ThothPythonException):
    """An exception raised on bugs in the code base."""


class VersionIdentifierError(ThothPythonException):
    """An exception raised if the given version identifier is not a semver identifier."""


class UnsupportedConfiguration(ThothPythonException):
    """Raised on unsupported configuration options."""


class NotFound(ThothPythonException):
    """Raised if the given artifact cannot be found."""
