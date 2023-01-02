# Alan
import asyncio
import json
import os
import platform
import pytz
import random
import sys
import yaml
import discord
from datetime import datetime
from discord.activity import Activity
from discord.enums import ActivityType
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

ACTIVITIES = [(ActivityType.listening, 'Jim Synonym'),
              (ActivityType.listening, 'Nobody\'s Anomaly.'),
              (ActivityType.listening, 'Bury the Light'),
              (ActivityType.listening, "for 'alan '"),
              (ActivityType.playing,   'music in the back of Lowes.'),
              (ActivityType.playing,   'with the boys.'),
              (ActivityType.watching, 'Destiny 2 raid tutorials.'),
              (ActivityType.watching, 'GTA V RP.'),
              (ActivityType.watching, 'Barnyard: The Movie.'),
              ]

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found!")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

intents = discord.Intents.all()

bot = Bot(command_prefix=config["bot_prefix"], intents=intents)

# Executes when bot is ready to begin processing commands
@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()
    send_good_morning.start()
    await bot.tree.sync()


# Setup the game status task of the bot
@tasks.loop(minutes=1.0)
async def status_task():
    rand = random.choice(ACTIVITIES)
    new_activity = Activity(type=rand[0], name=rand[1])
    await bot.change_presence(activity=new_activity)

# GOOD MORNING
est = pytz.timezone('US/Eastern')

# send "Good Morning!" every weekday at 5:00 am EST
@tasks.loop()
async def send_good_morning():
    while True:
        # get current time in EST
        current_time = datetime.now(est)
        # send message on weekdays at 5:00 am EST
        if current_time.weekday() < 5 and current_time.hour == 5 and current_time.minute == 00:
            # send message to the default channel
            for gm_channel in config['gm_channels']:
                channel = bot.get_channel(gm_channel)
                await channel.send("Rise and Grind Gamers :)")
        # wait for 1 minute before checking time again
        await asyncio.sleep(60)


# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")

async def load_cogs() -> None:
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
    # Ignores if a command is being executed by a bot or by the bot itself
    if message.author == bot.user or message.author.bot:
        return
    # Ignores if a command is being executed by a blacklisted user

    if message.author.id in config["blacklist"]:
        return
    await bot.process_commands(message)


# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(
        f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")


# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="Error!",
            description="This command is on a %.2fs cool down" % error.retry_after,
            color=config["error"]
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission `" + ", ".join(
                error.missing_perms) + "` to execute this command!",
            color=config["error"]
        )
        await context.send(embed=embed)
    raise error


# Run the bot with the token
asyncio.run(load_cogs())
bot.run(config["token"])