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

from discord import Colour
from random import choice
from utils.misc import at


def get_color() -> Colour:
    """Get a random :code:`Colour` object."""

    return getattr(Colour, choice([
        'teal', 'dark_teal', 'green', 'dark_green', 'blue', 'dark_blue',
        'purple', 'dark_purple', 'magenta', 'dark_magenta', 'gold',
        'dark_gold', 'orange', 'dark_orange', 'red', 'dark_red', 'lighter_grey',
        'darker_grey', 'blurple', 'greyple']))()


def get_member_color(member) -> Colour:
    """Get the final rendered color of a guild member as of its highest role."""

    return getattr(at(member.roles, -1), 'colour', None) or \
        Colour.default()
