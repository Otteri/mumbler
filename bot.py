import os
from dotenv import load_dotenv
import discord
import nlp

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
            "/fin <english>         translates text to finnish. \n"
            "/kalevala <english>    translates to finnish with similar style to kalevala. \n"
            "```")
    return text

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    output = None

    if message.content.startswith("/help"):
        await message.channel.send(show_help_msg())
    elif message.content.startswith("/fin "):
        data_path = "profile1/"
        user_input = message.content.split("/fin")[1].lower().strip()
        print(">", user_input)
        output = nlp.translate(user_input, data_path=data_path)
    elif message.content.startswith("/kalevala "):
        data_path = "profile2/"
        user_input = message.content.split("/kalevala")[1].lower().strip()
        print(">", user_input)
        output = nlp.translate(user_input, data_path=data_path)
    elif message.content.startswith("/teach "):
        # TODO: must check who user! Who is trying to teach?
        #if previous_data_path is not None:
        #    nlp.teachSentence(previous_user_input, data_path=previous_data_path)
        await message.channel.send("Not yet implemented...")
    else:
        print("Invalid command")
    
    
    # Handle output
    if output is 1:
        print("Error!")
    elif output == 2:
        info_text = ("I have not heard that sentence or word before.\n"
                     "You can help me to understand it by "
                     "typing a translation within 30s using '/teach' prefix.")
        previous_data_path = data_path
        previous_user_input = user_input
        await message.channel.send(info_text)
    elif(output is not None):
        print("<", output)
        await message.channel.send(output)

client.run(os.getenv("DISCORD_TOKEN"))
