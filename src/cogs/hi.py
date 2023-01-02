from discord.ext import commands
import os
import sys
import yaml
import asyncio
import discord
import time
import random

GREETINGS = [   "Hello! ",
                "Hi! ",
                "Howdy! ",
                "Whats popping? ",
                "Heyo! ",
                "How are you? ",
                "What's up? ",
                "How's it going? ",
                "How's everything? ",
                "Yahallo! ",
                "How's your day? ",
                "Greetings! ",
                "Salutations! ",
                "Hola! ",
                "Bonjour! ",
                "Ni hao! ",
                "Konnichiwa! ",
                "Ciao! ",
                "Olá! ",
                "Hallo! ",
                "Hej! "]



if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found!")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


async def setup(bot):
    await bot.add_cog(Hi(bot))


class Hi(commands.Cog, name="hi"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hi")
    async def hi(self, context):
        """
        Say hi to Alan.
        """
        if vc := context.author.voice:

            # join the voice channel
            voice_client = await vc.channel.connect()

            # awkward pause
            await asyncio.sleep(1)

            # play a sound
            voice_client.play(discord.FFmpegPCMAudio('./sounds/hiimalan.mp3'))

            # wait for the sound to finish playing
            await asyncio.sleep(1)

            # disconnect from the voice channel
            await voice_client.disconnect()
        else:
            if len(GREETINGS) == 0:
                await context.send("Hi " + context.author.mention + "!")
            else:
                await context.send(random.choice(GREETINGS) + context.author.mention)
