import os
from dotenv import load_dotenv
from parlai_internal.mumbler import config as cfg
import discord
from discord.ext import commands

# This file implements the discord bot
#
# References: 
# https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html

def create_pipes():
    read_pipe =  cfg.PIPE_AGENT2DISCORD
    write_pipe = cfg.PIPE_DISCORD2AGENT

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
    print("=== Pipes have been created ===")
    return rf, wf

class Chat(commands.Cog):
    def __init__(self, bot, rf, rw):
        self.bot = bot
        self.rf = rf
        self.wf = wf

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as '{0.user}'".format(self.bot))

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        response = None
        # Ignore own messages
        if message.author == self.bot.user:
            return

        if message.content.startswith(cfg.TALK_PREFIX):
            # Pass message for the chat-agent
            user_input = message.content.split(cfg.TALK_PREFIX)[1].lower().strip()
            content = f"{user_input}!".encode("utf8")
            os.write(self.wf, content)
            
            # Recieve data (blocking: waits until gets response)
            response = os.read(self.rf, cfg.MSG_LENGTH).decode('utf-8')

            if response:
                await ctx.send(response)

    @commands.command()
    async def version(self, ctx):
        version = "Mumbler - v0.0"
        await ctx.send(version)

    @commands.command()
    async def help(self, ctx):
        text = (
                "```\n"
                "Command:               info:\n"
                "{prefix} <english>           Talk with the bot \n"
                "```".format(prefix=cfg.TALK_PREFIX)
                )
        await ctx.send(text)


if __name__ == "__main__":

    # 1) Load environment variables
    load_dotenv()

    # 2) Establish IPC
    rf, wf = create_pipes()

    # 3) Initialize discord bot
    intents = discord.Intents(messages=True)
    bot = commands.Bot(command_prefix=cfg.COMMAND_PREFIX, intents=intents, help_command=None)
    bot.add_cog(Chat(bot, rf, wf))
    bot.run(os.getenv("DISCORD_TOKEN"))
