from discord import Embed, Message, User
from discord.ext.commands import (
    Cog,
    Context,
    group,
    is_owner,
)

from xythrion.bot import Xythrion


class WebMapper(Cog):
    def __init__(self, bot: Xythrion):
        self.bot = bot
