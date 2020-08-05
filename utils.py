#  Copyright (c) 2020 Tripulse.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import typing
import urllib.parse
import os


def safe_subscript(o, index):
    """Safely work with the subscript operator on an object.

    :return: value if succeeded or None.
    """

    try:
        return o[index]
    except:
        pass


class filename(typing.NamedTuple):
    """Represents a structure of a general filename, each filename has a
    optional extension to hint about the file-type without reading the file
    itself which is obviously for convenience purposes."""

    name: str
    ext: str

    def __str__(self):
        return '%(name)s.%(ext)s' % self.__dict__

    @staticmethod
    def from_str(path: str):
        """Given a path-compatible string, it builds a filename object by
        extracting out the filename and discarding the whole path.
        :param path: file path to be used to build
        :return: an instance of this class
        """

        path = str(path)  # force convert to a string.
        name, _, ext = os.path.basename(path).rpartition('.')

        return filename(name, ext)

    @staticmethod
    def from_url(url: str):
        """Same as `filename.from_str()` but constructs from a URL."""
        return filename.from_str(urllib.parse.urlparse(url)[2])