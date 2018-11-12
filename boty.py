import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
# import time
# from PIL import Image, ImageDraw, ImageFont
# import math
import re
import os
import atexit
import json

from dotenv import load_dotenv
load_dotenv()

from getRooster import getLesson

try:
    with open("data.json") as f:
        data = json.load(f)
        try:
            data["lln-s"] = data["lln-s"]
        except KeyError:
            data["lln-s"] = {}
except FileNotFoundError:
    data = {"lln-s":{}}

client = discord.Client()
prefix = "!"

@client.event
async def on_ready():
    print(client.user.name+"#"+client.user.discriminator+" is now online")

    message = (
        "Hello, I'm now listing for commands in this channel!\nType `!les <number>` to try me out :slight_smile:"
    )

    for channel in client.get_all_channels():
        if channel.type == discord.ChannelType.text:
            if channel.name == "bot-test":
                await client.send_message(channel, message)

@client.event
async def on_message(message: discord.Message):
    if (message.author.id == client.user.id):
        return

    if (isCommand("leerlingnummer", message.content) or isCommand("lln", message.content) or isCommand("studentnumber", message.content) or isCommand("studnr", message.content)):
        data["lln-s"][message.author.id] = message.content.split()[1]
        with open("data.json", "w+") as write_file:
            json.dump(data, write_file)
        print(message.channel.id)
        await client.send_message(message.channel, "Data saved")
        return

    elif (isCommand("delete", message.content) or isCommand("del", message.content)):
        try:
            del data["lln-s"][message.author.id]
            with open("data.json", "w+") as write_file:
                json.dump(data, write_file)
            await client.send_message(message.channel, "The data has been deleted")
        except KeyError:
            await client.send_message(message.channel, "There was no data to be deleted")
            return
        return

    elif (isCommand("les", message.content)) or isCommand("lesson", message.content):
        try:
            if len(message.content.split()) > 1:
                lln = message.content.split()[1]
                personPosesive = "this person's"
                personPosesive2 = "their"
                personSubject = "this person"
                verb = "does"
            else:
                lln = data["lln-s"][message.author.id]
                personPosesive = "your"
                personPosesive2 = "your"
                personSubject = "you"
                verb = "do"
        except:
            await client.send_message(message.channel, "Could not find student ''")
            return

        nextlesson = getLesson(lln)
        response = ""
        if nextlesson[0] is "error":
            await client.send_message(message.channel, "Could not find student '" + str(lln) + "'")
            return
        elif nextlesson[0] is None and nextlesson[1] is not None:
            response = (
                "Hello {}, {} next lesson is **{}** in **{}** from **{}**."
                    .format(message.author.name, personPosesive, nextlesson[1]['subject'], nextlesson[1]['location'],
                    nextlesson[1]['attendees'])
            )
        elif nextlesson[0] is None and nextlesson[1] is None:
            response = (
                "Hello {}, {} {}n't have any lessons planned."
                    .format(message.author.name, personSubject, verb)
            )
        elif nextlesson[0] is not None and nextlesson[1] is None:
            response = (
                "Hello {}, {} current lesson is **{}** in **{}** from **{}**."
                    .format(message.author.name, personPosesive, nextlesson[0]['subject'], nextlesson[0]['location'],
                    nextlesson[0]['attendees'])
            )
        else:
            response = (
                "Hello {}, {} current lesson is **{}** in **{}** from **{}**, and {} next lesson is **{}** in **{}** from **{}**."
                    .format(message.author.name, personPosesive, nextlesson[0]['subject'], nextlesson[0]['location'],
                    nextlesson[0]['attendees'], personPosesive2, nextlesson[1]['subject'], nextlesson[1]['location'],
                    nextlesson[1]['attendees'])
            )

        await client.send_message(message.channel, response)
        return

def isCommand(command, string):
    return re.match(r"^"+prefix+command+"(| .+)", string)

client.run(os.getenv("TOKEN"))
