Trigonopulse is a K3C (Kook Kak Koq Consortium) compliant fast, well-written and optimized Discord bot.
It has K3C compliant features like GRS Upvote generator, K3CV format encoding/decoding, Sinusoidal spacing
and some features not provided by any Discord bot.

To get things working.

- Install [Python](https://python.org/) and ensure it's on PATH.
- Clone this repository.
- Run `pip -3 install -r requirements.txt` install dependencies.
- Put the *bot token* in `DISCORD_TOKEN` environment variable.
- Finally to run the bot, execute `python3 __main__.py`.

The bot does not work in (Group) DMs. It is invoked like `@trigonopulse command` which removes the need for prefixes.
Slash commands might be used in future.
