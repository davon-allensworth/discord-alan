from discord.ext import commands
import os
import sys
import yaml
import asyncio
import discord
import time
import random

# List of all facts to be randomly selected
FACTS = ["Alan Turing was born on June 23rd, 1912 in London.",
         "Alan Turing is considered to be the father of modern computer science.",
         "Alan Turing cracked the Enigma, a device used to encode German messages in World War II. "
         "This played a key role in helping US troops to avoid German submarine attacks.",
         "Alan Turing rode his bike 62 miles to get to school on the first day due to transportation issues.",
         "Alan Turing was almost an Olympic athlete. He ended up placing fifth in a qualifying marathon with a time "
         "of 2 hours and 46 minutes.",
         ]

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found!")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


def setup(bot):
    bot.add_cog(Facts(bot))


class Facts(commands.Cog, name="facts"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fact")
    async def fact(self, context):
        """
        Get a random fact about Alan Turing.
        """
        if len(FACTS) == 0:
            await context.send("Someone tell Dev to add more facts about Alan.")
        else:
            await context.send("Hello everyone! \nDid you know that " + random.choice(FACTS))
