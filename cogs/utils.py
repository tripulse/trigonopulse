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
from discord import Embed

from aioitertools import islice, chain, takewhile, filterfalse
from aioitertools import iter as aiter
from aioitertools.more_itertools import chunked

from utils.bot import get_member_color


class Utils(Cog):
    @command()
    @has_permissions(manage_messages=True, read_message_history=True)
    @bot_has_permissions(manage_messages=True, read_message_history=True)
    @max_concurrency(number=1, per=BucketType.channel)
    async def purge(self, ctx, n: int, *targets: UserConverter):
        """Delete messages of certain amount posted by certain members or by anyone"""

        total = 0  # deleted total
        ref_time = ctx.message.created_at
        messages = ctx.history(limit=None)

        await messages.__anext__()  # skip invoking message

        # message matching is defined mathematically as
        #
        #   TargetMatch(m) = (Author(m) ∈ Targets) ∨ (Targets ≡ ∅)
        #   Selection      = {m ∈ Messages | Age(m) ≤ 14, TargetMatch(m)}
        #
        # for bulk-deletion specifically, (2 ≤ |Selection| ≤ 100)
        bulk_msgs = takewhile(lambda m: (ref_time - m.created_at).days < 15, messages)
        bulk_msgs = filterfalse(lambda m: m.author not in targets or targets)

        for bulk in chunked(islice(bulk_msgs, n), 100): 
            if len(bulk) == 1:
                messages = chain(bulk, messages)
                break
            
            ctx.channel.delete_messages(bulk)  # 100 snowflakes/request
            total += len(bulk)

        # if can't bulk delete anymore, do manual.
        async for m in messages:
            if not total <= n:
                break

            if m.author in targets or targets is None:
                await m.delete()
                total += 1
        
        await ctx.send(f"Purged {total} messages in {ctx.channel.mention}")

    @group(aliases=['cpmessage', 'copymsg', 'cpmsg'], invoke_without_command=True, case_insensitive=True)
    @has_guild_permissions(read_message_history=True, send_messages=True, manage_messages=True)
    @bot_has_guild_permissions(read_message_history=True, send_messages=True, manage_messages=True)
    async def copymessage(self, _, dest: TextChannelConverter, *msgs: MessageConverter):
        """Copy messages in the current channel of certain amount to an another"""

        async for m in aiter(msgs):
            dest_msg = Embed.from_dict({
                'description': m.content,
                'author': {
                    'name': m.author.nick or m.author.name,
                    'icon_url': str(m.author.avatar_url)
                }
            })

            # TODO: video isn't supported for some reason.
            first_url = getattr(m.attachments.get(0), 'url', None)
            first_embedable = first_url.rpartition('.')[2] in ['jpg','jpeg','png','gif','webp']

            if first_embedable:
                dest_msg.set_image(first_url)

            if not first_embedable or len(m.attachments) > 1:
                # if first one is embeddable don't include it, else do.
                if (attach_repr := '\n'.join(a.url for a in m.attachments[int(not first_embedable):])):
                    dest_msg.add_field(name='Attachments', value=attach_repr)

            await dest.send(embed=dest_msg)

    @copymessage.command(name='bulk')
    async def bulk_copymessage(self, ctx, dest: TextChannelConverter, num: int):
        """Bulk move a certain amount of messages to a channel, in order they appear in"""

        await self.copymessage(ctx, dest, ctx.history(limit=num+1, oldest_first=True))
