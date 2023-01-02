from discord.ext import commands
import os
import sys
import yaml
import asyncio
import discord
import time
import random

# List of all facts to be randomly selected
FACTS = [   "Alan Turing was born on June 23, 1912 in Maida Vale, London, England.",
            "He is widely regarded as the father of modern computer science and artificial intelligence.",
            "During World War II, Turing played a crucial role in cracking the German Enigma code, which helped the Allies win the war.",
            "In 1950, he published a paper titled 'Computing Machinery and Intelligence,' in which he proposed the Turing Test as a way to determine a machine's ability to exhibit intelligent behavior.",
            "Turing's work on the Enigma code was depicted in the 2014 film 'The Imitation Game,' in which he was portrayed by actor Benedict Cumberbatch.",
            "Turing was a homosexual at a time when homosexuality was illegal in the UK. He was arrested and convicted in 1952 for 'gross indecency,' and was forced to undergo chemical castration as punishment.",
            "In 2009, then-British Prime Minister Gordon Brown issued a formal apology on behalf of the government for the way Turing was treated.",
            "Turing was found dead on June 8, 1954, from cyanide poisoning. His death was ruled a suicide, but some have speculated that it may have been an accidental overdose.",
            "Turing was posthumously awarded the Presidential Medal of Freedom by President Barack Obama in 2012.",
            "There are numerous statues and memorials to Turing around the world, including one in Manchester, England, where he worked during World War II.",
            "In 2017, the Bank of England released a new £50 note featuring a portrait of Turing.",
            "Turing's work has had a major impact on the development of computers and technology, and he is often referred to as one of the most important figures in the history of computing."]


if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found!")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


async def setup(bot):
    await bot.add_cog(Facts(bot))


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
            await context.send("Alan Fact: \n" + random.choice(FACTS))
