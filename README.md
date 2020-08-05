Discord users sometimes decide to make personal bots. Sometimes working with libraries, like discord.py, gives little 
resources which is why this miminimal build-base for a discord.py bot was assembled.

---

To start things:
  - Get a Python interpreter, either [CPython](https://python.org) or [PyPy](https://www.pypy.org/) (I prefer PyPy).
  - Get a good editor (eg. PyCharm, VSCode). I use PyCharm Community Edition.
  - Clone this repository, through `git clone https://github.com/tripulse/discord.py-bot`, then switch you current
  directory to the cloned folder.
  - [Get a Bot access token from Discord][0] and put it in `DISCORD_TOKEN` environment variable.
  - Run `pip3 install -r requirements.txt` (use `pip` if needed).
---
When you've everything settled, just run `python3 __main__.py` or `pypy3 __main__.py`.

Now for example, head onto a DM with the bot and say `hi`, it'd respond `Hello!`, that's resulting because of this code.
```python
@command()
    async def hi(self, ctx):
        await ctx.send("Hello!")
```
As you can see the ease of creating commands. Though this is not the entire code, some code has still to be glued to make it work.


### Adding a Module
In the `cogs` folder create a new file `demo.py`, this'll be automatically loaded upon bot-start with certain conditions we'll later talk about on. For now putin this code:

```
from discord.ext.commands import Cog, command

class Demo(Cog):
  @command()
  def succ(self, ctx):
    await ctx.send("acquire the power of S  u  C  c")

__cogexport__ = [Demo]
```

- A [`Cog`][1] is a collection of commands aka. category, well not just commands also event listeners! These make the codebase not a mess through a very modular format, free-floating commands are generally avoided because they're a potential cause of mess.
- `__cogexport__` tells the loader which classes exactly to pick (this maybe changed in future). This can be any kind of iterator, while mostly you'd just use either a `list` or a `tuple`.

When you turn the bot on and type in `succ` in the DMs, it'll respond with `acquire the power of S  u  C  c`.

---

A bot can't just be limited to DMs because that's not the very nature of bots. To invoke the bot in a server, in the message add a user mention aka. ping at first, then the command to invoke (eg. `@demo-bot help`).


[0]: https://discordpy.readthedocs.io/en/latest/discord.html
[1]: https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html