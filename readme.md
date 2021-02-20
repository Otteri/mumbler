# Mumbler
An interactive discord chat bot. User can add the bot to a Discord server and then it is possible to chit-chat with the bot using discord's chat feature. Bot uses neural network and it has been trained to resemble human.

### Table of contents:
* [Dependencies](#Dependencies)
* [Installation](#Installation)
* [Usage](#Usage)
* [Config](#Config)
* [Docker](#Docker)
* [References](#References)

### Brief implementation introduction
The service consists of two individual processes
1) Discord bot
2) Chat bot

Discord bot reads user input from a Discord chat service. It forwards the input
for the Chat bot, which then processes the user input, generates an output and 
passes it back for the discord bot. Discord bot writes the result to chat. Division between these processes is very evident. Communication between processes is implemented using pipes.

# Dependencies
* [ParlAI](https://github.com/facebookresearch/ParlAI)
* [discord.py](https://github.com/Rapptz/discord.py)
* [dotEnv](https://github.com/theskumar/python-dotenv)

# Installation
**Note:** It is recommended to use [Docker](#Docker), which basically allows to ignore this section.

First, one should install all dependencies. Then, link your discord bot account with chat read/write permissions at least. Create `.env` file inside `mumbler/` and place following line inside the file:  
`DISCORD_TOKEN = <your-token>`

Mumbler is heavily tied to ParlAI. ParlAI recommends custom code to be placed inside `ParlAI/parlai_internal/`, but in order to recude coupling, this project source code is kept separated. In docker containers, the source code is automatically moved into correct location. If one does not want to use Docker, then source code should be manually placed into aforementioned directory (symlinking is alternative method). This step allows ParlAI to find custom models, agents and tasks.

Now it should be possible to start ParlAI agent and Discord bot either separately or simultaneously.

# Usage
Mumbler can be started with following command: `$ python main.py`
Script starts ParlAI agent and Discord bot instances.

It is also possible to run and debug only ParlAI agent. Run the agent in one terminal:
`$ python talk.py -t internal:blended_skill_talk -mf zoo:blender/blender_90M/model` and in another terminal, use `write.py` script to pass text for the agent. Hence, Discord setup is not necessarily required for only toying with the agent.

# Config
All config settings should work as is. However, for optimized performance, these can be adjusted if desired.

# Docker
Mumbler can be run using Docker. Production version can be built and launched with:
```
$ docker build -f Dockerfile.prod -t mumbler .
$ docker run --gpus all -it mumbler
```
For more rapid development cycles, there is also an debug version of the image.
In debug version, the developer is expected to mount his local source files,
which allows changes to be tested without need of always rebuilding the image. 
Because task of mounting several directories is somewhat unpleasant to do, 
there is a `start-debug.bash` script which can be used for starting the debug environment automatically.

# References
[Recipes for building an open-domain chatbot](https://arxiv.org/abs/2004.13637)