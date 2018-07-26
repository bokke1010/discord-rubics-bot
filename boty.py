import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from PIL import Image, ImageDraw, ImageFont
import math
import re
import os
import atexit

client = discord.Client()

@client.event
async def on_ready():
    message = (
        "Hello, I'm now listing for commands in this channel!\n"
        "Type `!cube help` to try me out :slight_smile:"
    )

    for channel in client.get_all_channels():
        if channel.type == discord.ChannelType.text:
            await client.send_message(channel, message)

@client.event
async def on_message(message: discord.Message):
    if (message.author.id == client.user.id):
        return
    
    if (not re.match(r"^!cube .+", message.content)):
        return

    response = (
        "Hello {}, your user id is {}."
            .format(message.author.name, message.author.id)
    )

    await client.send_message(message.channel, response)

client.run(os.environ["DISCORD_KEY"])
