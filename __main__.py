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

import discord
from discord.ext.commands import Bot
import discord.utils

from utils.misc import at
import os
import re


def retrieve_prefix(bot, message):
    """Get the current prefix to look for to do a valid command invocation,
    in DMs a prefix isn't required but a guild context a mention is though.

    :return: prefix string if found or None if not.
    :raises SyntaxError: if nothing matched the prefix.
    """

    return '' if isinstance(message.channel, discord.DMChannel) else \
        [f'<@!{bot.user.id}>' + (at(
            re.match(rf'@{bot.user.name}(\s*)',
                     message.clean_content), 1) or '')]


if __name__ == '__main__':
    # make instance of Bot that'd handle all the events or commands fired by
    # discord, the prefix is through mentioning the bot user or in DMs just
    # without prefix because it's redundant in a two-user channel.
    handler = Bot(retrieve_prefix, case_insensitive=True)

    handler.load_extension('cogs')
    try:
        handler.run(os.environ['DISCORD_TOKEN'])
    except EnvironmentError:
        print('Token for accessing Discord API was not given')
