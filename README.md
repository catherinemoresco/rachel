# Rachel - a Telegram bot
Rachel is a general-use bot for use in the Telegram app meant to fulfill personal communication needs. Need a gif quick? She can help you out. Need to make a spur-of-the-moment decision? She's got your back.


## Setup
- First, set up your bot with the Telegram API. You'll receive a bot token. Disable private mode for full functionality.
- Put the bot token into `config-template.py`, and rename `config-template.py` to `config.py`. 
- Create an empty directory in which you will store intermediate files between when they are downloaded from the Internet (e.g. via the Giphy API) and when the bot sends them out. Put the path to this file into `config.py` as `FILE_PATH`.
- Run Rachel from the command line with `python rachel.py`.

And that's it! It's really that simple.

## Functions
Rachel is constantly growing, but here's a list of her current talents:
- `**[hello|hey|hi]**`: send a greeting
- `**gif [search terms]**`: fetch and send a gif from Giphy
- `**[this] OR [that]**`: choose between `this` or `that`
- `**i love you**`: get some love
- `**right, rachel?**`: get some affirmation