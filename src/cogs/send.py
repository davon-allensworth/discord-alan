from discord.ext import commands
import os
import sys
import yaml
import asyncio
import discord
import time
import random

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found!")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


async def setup(bot):
    await bot.add_cog(Send(bot))


class Send(commands.Cog, name="send"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="send")
    async def Send(self, context, arg):
        """
        Assume control.
        """

        if context.channel.type is discord.ChannelType.private and context.message.author.id in config["admins"]:
            for adm_channel in config['admin_channels']:
                channel = self.bot.get_channel(adm_channel)
                await channel.send(arg)
        
