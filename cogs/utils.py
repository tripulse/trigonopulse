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

from discord import Embed
from discord.ext.commands import (
    Cog,
    BucketType,
    group,
    command,
    max_concurrency,
    has_permissions,
    bot_has_permissions,
    has_guild_permissions,
    bot_has_guild_permissions,
)
from discord.ext.commands.converter import (
    TextChannelConverter,
    MessageConverter,
    UserConverter
)

from aioitertools import chain, takewhile, filterfalse
from aioitertools import iter as aiter
from aioitertools.more_itertools import chunked

class Utils(Cog):
    @command()
    @has_permissions(manage_messages=True, read_message_history=True)
    @bot_has_permissions(manage_messages=True, read_message_history=True)
    @max_concurrency(number=1, per=BucketType.channel)
    async def purge(self, ctx, end: MessageConverter, *targets: UserConverter):
        """Delete messages upto a sentinel message (exclusive) posted by certain members or anyone"""

        total    = 0  # deleted total
        ref_time = ctx.message.created_at
        messages = ctx.history(after=end, oldest_first=False)
        targets  = tuple(map(lambda u: u.id, targets))

        await messages.__anext__()  # skip invoking message

        # message matching is defined mathematically as
        #
        #   TargetMatch(m) = (Author(m) ∈ Targets) ∨ (Targets ≡ ∅)
        #   Selection      = {m ∈ Messages | Age(m) ≤ 14, TargetMatch(m)}
        #
        # for bulk-deletion specifically, (2 ≤ |Selection| ≤ 100)
        bulk_msgs = takewhile(lambda m: (ref_time - m.created_at).days < 15, messages)

        if targets:
            bulk_msgs = filterfalse(lambda m: m.author.id not in targets, bulk_msgs)

        async for bulk in chunked(bulk_msgs, 100):
            if len(bulk) == 1:
                messages = chain(bulk, messages)
                break
            
            await ctx.channel.delete_messages(bulk)  # 100 snowflakes/request
            total += len(bulk)

        # if can't bulk delete anymore, do manual.
        if targets:
            async for m in messages:
                if m.author.id in targets:
                    await m.delete()
                    total += 1
        else:
            async for m in messages:
                await m.delete()
                total += 1
        
        await ctx.send(f"Purged {total} messages in {ctx.channel.mention}")
    
    async def _cpmsg(self, _, dest, msgs):
        async for m in aiter(msgs):
            dest_msg = Embed.from_dict({
                'description': m.content,
                'author': {
                    'name': m.author.name,
                    'icon_url': str(m.author.avatar_url)
                }
            })

            # TODO: video isn't supported for some reason.
            first_url       = m.attachments[0].url if len(m.attachments) > 0 else None
            first_embedable = first_url.rpartition('.')[2] in ['jpg','jpeg','png','gif','webp'] \
                                if first_url else False

            if first_embedable:
                dest_msg.set_image(url=first_url)

            if (attach_repr := '\n'.join(a.url for a in m.attachments)):
                dest_msg.add_field(name='Attachments', value=attach_repr)

            await dest.send(embed=dest_msg)
    
    @group(aliases=['cpmessage', 'copymsg', 'cpmsg'], invoke_without_command=True, case_insensitive=True)
    @has_guild_permissions(read_message_history=True, send_messages=True, manage_messages=True)
    @bot_has_guild_permissions(read_message_history=True, send_messages=True, manage_messages=True)
    async def copymessage(self, _, dest: TextChannelConverter, *msgs: MessageConverter):
        """Copy given messages in the current channel to an another channel"""

        await self._cpmsg(dest, msgs)

    @copymessage.command(name='bulk')
    async def bulk_copymessage(self, ctx, dest: TextChannelConverter, end: MessageConverter, begin: MessageConverter = None):
        """Bulk copy a range of messages defined by two sentinel messages (exclusive)"""

        await self._cpmsg(ctx, dest, ctx.history(limit=None, after=end, before=begin or ctx.message))