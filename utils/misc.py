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

def safe_subscript(o, index):
    """Safely work with the subscript operator on an object.

    :return: value if succeeded or None.
    """

    try:
        return o[index]
    except:
        pass


def safe_funccall(func, *args, **kwargs):
    """Safely call a function without fear of exceptions.

    :param func: actual function to wrap
    :return: function's actual value if succeeded or None
    """

    try:
        return func(*args, **kwargs)
    except:
        return None
