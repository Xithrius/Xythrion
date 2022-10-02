import os

from disnake.ext import commands
from disnake import AllowedMentions
from dotenv import load_dotenv
from loguru import logger as log

from xythrion.bot import Xythrion
from xythrion.extensions import EXTENSIONS

load_dotenv()

bot = Xythrion(
    command_prefix=commands.when_mentioned,
    case_insensitive=True,
    help_command=None,
    allowed_mentions=AllowedMentions(everyone=False),
)

for extension in EXTENSIONS:
    bot.load_extension(extension)
    log.info(f'Loaded extension "{extension}"')

bot.run(os.getenv("BOT_TOKEN"))
