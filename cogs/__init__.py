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

import os.path
import pathlib
import importlib.util
import utils
import itertools

from discord.ext.commands import Cog
from typing import (
    Iterator
)


def collect_cogs() -> Iterator[Cog]:
    """Collect all exported Cog objects exported through the `__cogexport__`
    variable in the command modules in the current directory.

    :return: an iterator of retrieve Cogs, entries which don't inherit from
    the Cog superclass are discarded.
    """

    def load_module(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)
        return module

    return itertools.chain.from_iterable(
        map(lambda mod: filter(
                lambda e: issubclass(e, Cog),  # only allow subclass of Cog.
                getattr(load_module(utils.filename.from_str(mod).name, mod),
                        '__cogexport__', None) or []),  # get exported cogs.
            pathlib.Path(os.path.dirname(__file__)).glob('*.py')))


def setup(bot):
    for cog in collect_cogs():
        bot.add_cog(cog(bot))
