To get things working.

- Get a copy of [PyPy](https://pypy.org/), good for this job.
- Clone this repository.
- Run `pip3 install -r requirements.txt`, to satisfy all deps.
- Collect a Discord *bot token* then put it in `DISCORD_TOKEN` environ.
- Finally to run the bot, run `pypy3 __main__.py`.

Now to invoke the bot mention it like `@botname [command]` in servers and just `[command]` in its DMs (eg. `@botname help` will show all the commands available). NOTE that, you've to replace `botname` with what its actual name on Discord is else it will not work. Also, not all commands work on DMs though but you're not most likely to use in a DM context.
