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

from discord import Intents
from discord.ext.commands import Bot, when_mentioned

import os

if __name__ == '__main__':
    bot = Bot(command_prefix=when_mentioned, case_insensitive=True)
    bot.intents = Intents(guild=True, members=True, guild_messages=True)

    bot.load_extension('cogs')
    
    try:
        bot.run(os.environ['DISCORD_TOKEN'])
    except EnvironmentError:
        print('Token for accessing Discord API was not given')
