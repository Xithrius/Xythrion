from discord import Embed, Permissions
from discord.ext.commands import Cog, Context, command
from discord.utils import oauth_url

from xythrion.bot import Xythrion
from xythrion.utils import markdown_link

GITHUB_URL = "https://github.com/Xithrius/Xythrion"

# Read/send messages in channels/threads, view channels, embed links,
# attach files, read message history, add reactions, use slash commands.
PERMISSIONS_INTEGER = 277025508416

BOT_ID_INTEGER = 591885341812850699


class Links(Cog):
    """Links to many things around the internet, including bot statistics."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(aliases=("repository", "repo"))
    async def info(self, ctx: Context) -> None:
        """Information about bot origin."""
        embed = Embed(description=markdown_link("Xythrion Github Repository", GITHUB_URL))

        await ctx.reply(embed=embed)

    @command()
    async def invite(self, ctx: Context) -> None:
        """Provides an invitation link that refers to this bot."""
        url = oauth_url(BOT_ID_INTEGER, permissions=Permissions(PERMISSIONS_INTEGER))

        embed = Embed(description=markdown_link("Invite link", url))

        await ctx.reply(embed=embed)
