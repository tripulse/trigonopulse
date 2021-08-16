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

from math import tau, cos
from functools import reduce
from random import choice, uniform, choices

class Basic(Cog):
    @command(aliases=['tst', 'ping'])
    async def test(self, ctx):
        """Verify that the bot is usable, tells the WebSocket RTT"""

        await ctx.send(round(ctx.bot.latency * 1000) + "ms")

    @command(aliases=['rnd', 'rndnum', 'rnum'])
    async def random(self, ctx, min: float, max: float):
        """Generate a uniform pseudorandom real number within (min..max]"""

        await ctx.send(uniform(min, max))

    @command(aliases=['choose'])
    async def pick(self, ctx, *options):
        """Pick pseudorandomly from given list of options"""

        if not options:
            pass
        await ctx.send(choice(options))

    @command(aliases=['expand'])
    async def space(self, ctx, spaces: int, *, text: str):
        """Spaces characters with a certain amount"""

        await ctx.send(''.join(c + ' ' * spaces for c in text[:int(2000/spaces)]))

    @command(aliases=['skwiggle', 'rndcap'])
    async def altcap(self, ctx, *, text: str):
        """Randomly capitalizes each English letter of a text"""

        await ctx.send(''.join(choice([c.upper, c.lower])() for c in text))

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

    @command(aliases=['wavespc', 'wavyspc', 'wavify'])
    async def sinspc(self, ctx, A: float, w: float, *, text: str):
        """Space text sinusodially with a certain amplitude (A) and wavelength (w)

        s[i] = M * -cos(τ * (1/w) * (i/N)) + M   [M := M/2]
            where i = char index
                  M = maximum spacing
                  w = strech factor
                  N = number of chars
                  s = list of num spaces after each char

            for w < 0, w = N
        """

        w  = len(text)-1 if w < 0 else w
        A /= 2
        f  = 1/w

        shaping = lambda x: int(A * -cos(tau * f * x) + A)
        shaping = map(shaping, range(len(text) - 1))

        out  = reduce(lambda acc,t_s: acc + t_s[0] + ' ' * t_s[1], zip(text, shaping), '')
        out += text[-1]

        await ctx.send(out)

    @command(aliases=['upgen', 'upvote', 'genupvote'])
    async def grsupvote(self, ctx, k: int):
        """Generate a GRS upvote of a certain length"""

        out = choices('^0123456789', cum_weights=[70,71,72,73,74,75,76,92,93,94,95], k=k)
        await ctx.send(''.join(out))
