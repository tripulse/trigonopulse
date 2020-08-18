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
    """Collect all exported Cog inherited objects exported by Python modules
    in the current directory, methods starting with an underscore are
    considered private and not loaded.

    :return: an iterator of retrieved Cogs.
    """

    def load_module(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)
        return module

    return itertools.chain.from_iterable(
        map(lambda mod: map(lambda x: x[1],  # extract actual object.
            filter(
                # check if one of their superclasses was Cog, but
                # not Cog itself as its an abstract class.
                lambda e: safe_funccall(issubclass, e[1], Cog) and
                          e[1] != Cog,
                load_module(Filename.from_str(mod).name, mod)
                    .__dict__.items())),  # get global objects.
            pathlib.Path(os.path.dirname(__file__)).glob('*.py')))


def setup(bot):
    @bot.event
    async def on_command_error(ctx, exception):
        # a custom error handler for defining where should the "generalized"
        # exceptions go.
        if isinstance(exception,
            (BadArgument, CommandNotFound, CommandOnCooldown,
             CheckAnyFailure, NoPrivateMessage, MissingPermissions,
             UnexpectedQuoteError, BotMissingPermissions,
             MaxConcurrencyReached, MissingRequiredArgument,
             ExpectedClosingQuoteError, InvalidEndOfQuotedStringError)):
            await ctx.send(f"```{exception}```")
        else:
            traceback.print_exception(exception.__class__, exception,
                                      exception.__traceback__)

    for cog in collect_cogs():
        bot.add_cog(cog(bot))
