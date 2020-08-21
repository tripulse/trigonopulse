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

from discord.ext.commands.converter import Converter
from discord.ext.commands.errors import BadArgument

import re


class RestrictedMimetypeConverter(Converter):
    """A restricted subset of mimetype allowance decided on interactional
    capabilities through this bot."""

    _VALIDATION = re.compile(r'(?:application/json)|(?:text/([a-z]+))')

    async def convert(self, _, mime) -> str:
        if not self._VALIDATION.match(mime):
            raise BadArgument("Disallowed or malformed mimetype given,"
                              " must be application/json or text/* but"
                              f" got {mime}")
        return mime
