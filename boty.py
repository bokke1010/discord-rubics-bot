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
from getRooster import getLesson

client = discord.Client()

@client.event
async def on_ready():
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

    if (not re.match(r"^!les .+", message.content)):
        return

    nextlesson = getLesson( message.content.split()[1])
    print(nextlesson)
    response = ""
    if nextlesson[0] is None and nextlesson[1] is not None:
        response = (
            "Hello {}, this person's next lesson is {} in {} from {}."
                .format(message.author.name, nextlesson[1]['subject'], nextlesson[1]['location'],
                nextlesson[1]['attendees'])
        )
    elif nextlesson[0] is None and nextlesson[1] is None:
        response = (
            "Hello {}, this person doesn't have any lessons planned."
                .format(message.author.name)
        )
    elif nextlesson[0] is not None and nextlesson[1] is None:
        response = (
            "Hello {}, this person's current lesson is {} in {} from {}."
                .format(message.author.name, nextlesson[0]['subject'], nextlesson[0]['location'],
                nextlesson[0]['attendees'])
        )
    else:
        response = (
            "Hello {}, this person's current lesson is {} in {} from {}, and your next lesson is {} in {} from {}."
                .format(message.author.name, nextlesson[0]['subject'], nextlesson[0]['location'],
                nextlesson[0]['attendees'], nextlesson[1]['subject'], nextlesson[1]['location'],
                nextlesson[1]['attendees'])
        )

    await client.send_message(message.channel, response)

client.run("NDcxOTkwOTQ1MTczMzQwMTYx.Drssew.aSz8Q82OB0ls18esjUkIrjnrgc4")
