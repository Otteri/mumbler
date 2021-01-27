import os
from dotenv import load_dotenv
import discord

# Create pipes
IPC_FIFO_NAME =  "/tmp/discord2agent"
IPC_FIFO_NAME2 = "/tmp/agent2discord"

# Make sure that env is clean
if os.path.exists(IPC_FIFO_NAME):
    os.remove(IPC_FIFO_NAME)
if os.path.exists(IPC_FIFO_NAME2):
    os.remove(IPC_FIFO_NAME2)

# Create pipes
fifo = os.mkfifo(IPC_FIFO_NAME)
fifo2 = os.mkfifo(IPC_FIFO_NAME2)

# Open the pipes
fifo2 = os.open(IPC_FIFO_NAME2, os.O_RDONLY)
fifo = os.open(IPC_FIFO_NAME, os.O_SYNC | os.O_CREAT | os.O_RDWR)

load_dotenv()
client = discord.Client()
TOKEN = ">>"

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
        os.write(fifo, content)
        
        # Recieve data (blocking: waits until gets response)
        response = os.read(fifo2, 512).decode('utf-8')

        if response:
            await message.channel.send(response)

client.run(os.getenv("DISCORD_TOKEN"))
