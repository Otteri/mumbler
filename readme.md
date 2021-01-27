# Mumbler

The service consists of two individual processes
1) Discord bot
2) Chat bot

Discord bot handles communication with discord. It forwards user inputs
for the chat bot. Chat bot processes inputs, generates an output and 
passes it back for the discord bot, which shows the output for use.
Communication between these processes has been implemented using pipes.

# Usage
Mumbler can be started with following command: `$ python main.py`
Python script launches subprocesses accordingly.

Currently, it is also possible to use split terminal and launch
`talk.py` and `bot.py` or `write.py` manually. `write.py` allows
debugging without Discord.

# Dependencies
* ParlAI
* discord.py
* dotEnv

# Config
Config settings should work as is, but these can be adjusted if desired.