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
from discord.ext.commands import Cog, group
from discord.ext.commands.errors import CommandError

from converters.code import CodeBlockConverter
from converters.mime import RestrictedMimetypeConverter

from requests import Request
from requests.exceptions import (
    MissingSchema,
    InvalidSchema,
    InvalidURL,
    RequestException
)

import requests
import base64


def get_response_data(resp: requests.Response, amt: int) -> str:
    """Get a string out of a Response.

    :param resp: a "requests" generated Response object
    :param amt: amount of bytes to read in-memory
    :return: a decoded string if succeeded or ASCII Base64 representation of
    read bytes
    """

    try:
        data = next(resp.iter_content(amt, True))
    except StopIteration:
        return ''

    if isinstance(data, bytes):
        try:
            return data.decode('utf-8')
        except ValueError:
            return base64.encodebytes(data).decode('ascii')
    return data


class Web(Cog):
    def __init__(self, _):
        self._req = requests.Session()
        self._req.stream = True  # always stream by default.

    @group(case_insensitive=True)
    async def http(self, ctx):
        """Do HTTP related operations, such as - GET, POST."""
        pass

    @http.command(name='get')
    async def http_get(self, ctx, url: str):
        """Perform a HTTP GET request on the given URL."""

        await self.perform_request(ctx, Request('GET', url).prepare())

    @http.command(name='head')
    async def http_head(self, ctx, url: str):
        """Perform a HTTP HEAD request on the given URL."""

        await self.perform_request(ctx, Request('HEAD', url).prepare())

    @http.command(name='post')
    async def http_post(self, ctx, url: str,
                        mimetype: RestrictedMimetypeConverter = 'text/plain',
                        *, body: CodeBlockConverter = ''):
        """Perform a HTTP POST request on the given URL, by sending out a
        request body with a given mimetype (default: text/plain)."""

        await self.perform_request(ctx, Request('POST', url, data=body,
            headers={'Content-Type': mimetype}).prepare())

    # will perform a PreparedRequest and send data to a given Context aswell.
    async def perform_request(self, ctx, request: requests.PreparedRequest):
        try:
            request = self._req.send(request)
        except (InvalidURL, InvalidSchema,
                MissingSchema, RequestException) as exc:
            raise CommandError(exc)

        if not request.ok:
            raise CommandError("A non-ok HTTP status code got: "
                               f"{request.status_code}")

        message = Embed()
        message.add_field(name='Headers', value=
            '\n'.join(f'**{k}**: {v}' for k,v in request.headers.items()))

        data = get_response_data(request, 2042)
        if data:
            message.description = f'```{data}```'

        await ctx.send(embed=message)

    def cog_unload(self):
        self._req.close()
