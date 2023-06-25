from discord.ext.commands import Cog

from xythrion.bot import Xythrion


class MinecraftStacks(Cog):
    """Stack calculations for Minecraft."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot
