# Mumbler
An interactive Discord chat bot. User can chit-chat with the bot using Discord chat feature after adding the bot to a server. Chat bot uses large neural network and it has been trained to resemble human.

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

If developing, you may want to download and build datasets outside the container and then copy these inside, so one does not need to spend time on building the same dictionaries over and over again. In other words, download datasets right after cloning and installing ParlAI.

# Usage
Mumbler can be started with following command: `$ python main.py`
Script starts ParlAI agent and Discord bot instances.

It is also possible to run and debug only ParlAI agent. Instead of Discord bot, run `write.py` script, which is used for communicating with the agent via terminal. Then, launch the agent in another terminal with:  
`$ python talk.py -t internal:blended_skill_talk -mf zoo:blender/blender_90M/model`
(/app/ParlAI/parlai_internal/models/vainamoinen_90M.checkpoint)

# Config
All config settings should work as is. However, for optimized performance, these can be adjusted if desired.

# Docker
Mumbler can be run using Docker. Production version can be built and launched with:
```
$ docker build -f Dockerfile.prod -t mumbler .
$ docker run --gpus all -it mumbler
```
For more rapid development cycles, there is also a debug version of the image.
In debug version, the developer is expected to mount his local source files,
which allows changes to be tested without need of always rebuilding the image. 
Because task of mounting several directories is somewhat unpleasant to do, 
there is a `start-debug.bash` script which can be used for launching the debug environment automatically.
Debug environment with mounted `models` directory can be also used for training a model.

# References
* [Recipes for building an open-domain chatbot](https://arxiv.org/abs/2004.13637)
* [🧙 of Wikipedia : Knowledge-powered conversational agents](https://arxiv.org/pdf/1811.01241.pdf)
* [Personalizing Dialogue Agents: I have a dog, do you have pets too?](https://arxiv.org/abs/1801.07243)
