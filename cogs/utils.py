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
    command,
    has_permissions,
    bot_has_permissions,
    max_concurrency,
    group,
    has_guild_permissions,
    bot_has_guild_permissions,
)
from discord.ext.commands.converter import (
    TextChannelConverter,
    MessageConverter,
    UserConverter
)

from discord import Embed

from aioitertools import takewhile, map, filterfalse, enumerate
from aioitertools.more_itertools import chunked
from utils.bot import get_member_color
from utils.misc import at, call
from utils.filesys import Filename


class Utils(Cog):
    """Useful commands for making moderation easy on a guild."""

    @command()
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True, read_message_history=True)
    @max_concurrency(number=1, per=BucketType.channel)
    async def purge(self, ctx, num: int, *targets: UserConverter):
        """Bulk delete messages of a certain amount posted by some targeted
        Discord users, if not provided it just deletes all the messages which
        it encounters."""

        total_deleted = 0
        messages = ctx.history(limit=None)

        # includes the invoker's message, so skip that.
        await messages.__anext__()

        # discord has a bulk-deletion method which has limits that,
        # messages cannot be deleted older than 14 days.
        # cannot delete more than 100 and less than 2 messages at once.
        async for chunk in chunked(map(lambda m: m[1], takewhile(
                lambda m: m[0] < num and
                         (ctx.message.created_at - m[1].created_at).days < 14,
                filterfalse(lambda m: not(
                        m[1].author in targets or not targets),
                    enumerate(messages)))), 100):

            chunk = list(chunk)
            await ctx.channel.delete_messages(chunk)
            total_deleted += len(chunk)

        # for the rest follow the manual deletion way.
        async for msg in messages:
            if not total_deleted <= num:
                break

            if msg.author in targets or targets is None:
                await msg.delete()
                total_deleted += 1
        else:
            await ctx.send(f"Purged {num} messages in {ctx.channel.mention}",
                           delete_after=8)

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
                },
                'color': get_member_color(m.author).value
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
