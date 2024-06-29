from discord.ext.commands import Cog, command

from bot.bot import Xythrion
from bot.context import Context
from bot.utils.formatting import codeblock, final_join

SCRIPTS = {
    "dogma": [
        "In the first age, in the first battle, when the shadows first lengthened, one stood",
        "He chose the path of perpetual torment",
        "In his ravenous hatred he found no peace",
        "And with boiling blood he scoured the Umbral Plains seeking vengeance against the dark lords who had wronged him",  # noqa: E501
        "And those that tasted the bite of his sword named him",
        "The Doom Slayer",
    ],
    "demigod": [
        "Tempered by the fires of hell",
        "His iron will remain steadfast through the passage",
        "That preys upon the weak",
        "He set forth without pity",
        "And hunted the slaves of doom with barbarous cruelty",
        "Unbreakable, incorruptible, unyielding",
        "None could stand before the horde, but the doom-slayer",
        "For he alone was the hell-walker",
    ],
    "dakhma": [
        "They knew he would come, as he always had, as he always will, to feast on the blood of the wicked",
        "The Doomslayer sought to end the dominion of the dark realm",
        "Dispair spread before him, like a plague, striking fear into the shadowdwellers, driving them to deeper and darker pits",  # noqa: E501
        "His power grew, swift and unrelenting",
    ],
    "doom": [
        "Blinded by his fervor, the lure drew him in",
        "The priests entombed him in the cursed sarcophagus",
        "The mark of the doom slayer was burned upon his crypt",
        "A warning to all of hell that the terror within must never be freed",
        "And there he lies still",
        "Ever more",
        "In silent suffering",
    ],
}
DOOT_YOUTUBE_URL = "https://youtu.be/hzPpWInAiOg"


class Doom(Cog):
    """Doom Cog."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command()
    async def doot(self, ctx: Context) -> None:
        await ctx.send(DOOT_YOUTUBE_URL)

    @command(aliases=("d",))
    async def doom(self, ctx: Context, entry: str) -> None:
        if (script := SCRIPTS.get(entry)) is None:
            raise ValueError(
                f"'{entry}' is not of {final_join(list(SCRIPTS.keys()), final="or")}",
            )

        await ctx.send(codeblock(script))


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Doom(bot))
