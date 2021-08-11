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

import logging

from discord import Intents
from discord.ext.commands.bot import Bot, when_mentioned

from os import environ

if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)s] %(name)s: %(message)s', level=logging.INFO)
    
    bot = Bot(when_mentioned, case_insensitive=True)
    bot.intents = Intents(messages=True, guilds=True)
    bot.logger = logging.getLogger()

    bot.load_extension('cogs')

    try:
        bot.run(environ['DISCORD_TOKEN'])
    except EnvironmentError:
        print('Token for accessing Discord API was not given')
