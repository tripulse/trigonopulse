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

from discord.ext.commands import (
    Cog,
    BadArgument,
    group,
    command,
)

import random
from more_itertools import grouper
from functools import reduce


class Basic(Cog):
    @command(aliases=['tst', 'ping'])
    async def test(self, ctx):
        """Verify that the bot is usable, tells the WebSocket RTT"""

        await ctx.send(round(ctx.bot.latency * 1000) + "ms")

    @command(aliases=['rnd', 'rndnum', 'rnum'])
    async def random(self, ctx, min: float, max: float):
        """Generate a uniform pseudorandom real number within (min..max]"""

        await ctx.send(random.uniform(min, max))

    @command(aliases=['choose'])
    async def pick(self, ctx, *options):
        """Pick pseudorandomly from given list of options"""

        try:
            await ctx.send(random.choice(options))
        except IndexError:
            pass

    @command(aliases=['expand'])
    async def space(self, ctx, spaces: int, *, text: str):
        """Spaces characters with a defined amount to emphasize a text"""

        if len(text) * spaces > 2000:
            raise BadArgument("Disallowing 2000 character limit of Discord")
        await ctx.send(''.join(c + ' ' * spaces for c in text))

    @command(aliases=['skwiggle', 'rndcap'])
    async def altcap(self, ctx, *, text: str):
        """Randomly capitalizes each English letter of a text"""

        await ctx.send(''.join(random.choice([c.upper, c.lower])() for c in text))

    @group(name='5igi0', aliases=['5igio', 'sigio', 'sigi0'], case_insensitive=True)
    async def sigio(self, _):
        """K3C protocol of communication whose textual representation consists of only ASCII `-` and `'` characters"""
        pass

    @sigio.command(name='encode', aliases=['enc', 'e'])
    async def sigio_encode(self, ctx, *, text: str):
        """Encode from UTF-8 characters into 5IGI0 (maximum chars: 250)"""

        text = text.encode('utf-8')[:250]  # 2000/8 = 250 bytes
        data = bytearray(len(text) * 8)

        for i,c in enumerate(text):
            for b in range(7,-1,-1):
                data[i*8 + b] = "-'"[c >> b & 1]

        await ctx.send(data.decode('ascii'))

    @sigio.command(name='decode', aliases=['dec', 'd'])
    async def sigio_decode(self, ctx, sigi0: str):
        """Decode from 5IGI0 to UTF-8 characters"""

        data = bytearray(sigi0 / 8)

        try:
            for i in range(sigi0 / 8):
                for b in range(7, -1, -1):
                    data[i] |= "-'".index(data[i*8+b]) << b
        except ValueError:
            raise BadArgument("5IGI0 sequence doesn't only contain `-` and `'` chars")

        await ctx.send(data.decode('utf-8', 'ignore')[:2000])

    @command(aliases=['interjection', 'rms', 'rmsquote', 'stallman'])
    async def interject(self, ctx, thing: str = 'Linux'):
        """I'd just like to interject for a moment"""

        await ctx.send(f"I'd just like to interject for a moment.  What you're "
                       f"referring to as {thing}, is in fact, GNU/{thing}, or as "
                       f"I've recently taken to calling it, GNU plus {thing}.")

    @command(aliases=['emtext', 'etxt'])
    async def emojitext(self, ctx, *, text: str):
        """Emojify all English letters (uppercase in output)"""

        res = ''
        for c in text.lower():  # only lowercase.
            if len(res) > 2000:
                break
            res += f':regional_indicator_{c}:' \
                if ord(c) > 96 and ord(c) < 123 \
                else c

        await ctx.send(res[:2000])
