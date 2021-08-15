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

import traceback

from discord.embeds import Embed
from discord.ext.commands import Cog
from discord.ext.commands.errors import (
    BadArgument,
    CommandError,
    CheckAnyFailure,
    CommandNotFound,
    CommandOnCooldown,
    NoPrivateMessage,
    MissingPermissions,
    UnexpectedQuoteError,
    BotMissingPermissions,
    MaxConcurrencyReached,
    MissingRequiredArgument,
    ExpectedClosingQuoteError,
    InvalidEndOfQuotedStringError,
)

from pathlib import Path
from os.path import dirname

from importlib.util import spec_from_file_location, module_from_spec


def setup(bot):
    @bot.event
    async def on_command_error(ctx, exception):
        # if the exception is of any of selected classes redirect to discord
        if isinstance(exception,
            (BadArgument, CommandError, CommandNotFound, CommandOnCooldown, CheckAnyFailure, NoPrivateMessage,
             MissingPermissions, UnexpectedQuoteError, BotMissingPermissions, MaxConcurrencyReached,
             MissingRequiredArgument, ExpectedClosingQuoteError, InvalidEndOfQuotedStringError)):
            await ctx.send(embed=Embed(description=str(exception)))

        # as well as in stdout with rest of the exception classes too
        traceback.print_exception(exception.__class__, exception, exception.__traceback__)

    
    # underscored files will be ignored as private
    for path in Path(dirname(__file__)).glob('[!_]*.py'):
        spec = spec_from_file_location(path.stem, path)
        mod = module_from_spec(spec)

        # do we need to do this?
        spec.loader.exec_module(mod)

        for o in mod.__dict__.values():
            if isinstance(o, type) and o != Cog and issubclass(o, Cog):
                bot.add_cog(o())
