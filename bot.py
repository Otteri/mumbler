import os
from dotenv import load_dotenv
from parlai_internal.mumbler import config as cfg
import discord

read_pipe =  cfg.PIPE_AGENT2DISCORD
write_pipe = cfg.PIPE_DISCORD2AGENT
TOKEN = cfg.TOKEN

# Make sure that env is clean
if os.path.exists(read_pipe):
    os.remove(read_pipe)
if os.path.exists(write_pipe):
    os.remove(write_pipe)

# Create pipes
wf = os.mkfifo(write_pipe)
rf = os.mkfifo(read_pipe)

# Open the pipes
wf = os.open(write_pipe, os.O_SYNC | os.O_CREAT | os.O_RDWR)
rf = os.open(read_pipe, os.O_RDONLY) # os.O_NONBLOCK

print("Pipes have been created")

load_dotenv()
client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as '{0.user}'".format(client))

def sanitize(string):
    return string.lower().strip()

def show_help_msg():
    text = ("```\n"
            "Command:               info:\n"
            ">> <english>           Talk with the bot \n"
            "```")
    return text

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = None

    if message.content.startswith("$help"):
        await message.channel.send(show_help_msg())

    elif message.content.startswith(TOKEN):
        # Pass message for the agent
        user_input = message.content.split(TOKEN)[1].lower().strip()
        content = f"{user_input}!".encode("utf8")
        os.write(wf, content)
        
        # Recieve data (blocking: waits until gets response)
        response = os.read(rf, cfg.MSG_LENGTH).decode('utf-8')

        if response:
            await message.channel.send(response)

client.run(os.getenv("DISCORD_TOKEN"))
