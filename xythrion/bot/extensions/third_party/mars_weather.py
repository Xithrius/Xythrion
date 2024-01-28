from os import getenv

from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import is_trusted

# https://api.nasa.gov/assets/insight/InSight%20Weather%20API%20Documentation.pdf
BASE_API_URL = "https://api.nasa.gov/insight_weather/?api_key={}&feedtype=json&ver=1.0"
DATA_SECTIONS = ["AT", "HWS", "PRE", "WD"]


class MarsWeather(Cog):
    """Weather on Mars."""

    def __init__(self, bot: Xythrion):
        self.bot = bot
        self.mars_api_key = getenv("NASA_API_KEY", None)

    async def get_mars_weather(self) -> dict:
        j = await self.bot.http_client.get(BASE_API_URL.format(self.mars_api_key))

        return j.json()

    @group()
    @is_trusted()
    async def mars(self, ctx: Context) -> None:
        await ctx.check_subcommands()


    # TODO: Make this command look way better
    @mars.command(enabled=False)
    @is_trusted()
    async def weather(self, ctx: Context) -> None:
        j = await self.get_mars_weather()

        try:
            first_sol_checked = j["validity_checks"]["sols_checked"][0]
            valid = any(j["validity_checks"][first_sol_checked][x]["valid"] for x in DATA_SECTIONS)

            if not valid:
                err = True

        except IndexError:
            err = True

        if err:
            await ctx.send("Mars weather could not be retrieved at this time.")

            return

        # TODO: ONCE IN A VALID STATE, PARSE THE WEATHER
        await ctx.send(valid)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(MarsWeather(bot))
