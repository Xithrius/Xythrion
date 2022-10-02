from disnake.ext import commands

from dotenv import load_dotenv

import os

load_dotenv()

bot = commands.Bot(command_prefix=commands.when_mentioned)


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


bot.run(os.getenv("BOT_TOKEN"))
