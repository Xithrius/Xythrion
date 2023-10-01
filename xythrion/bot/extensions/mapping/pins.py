from discord import Embed, Message
from discord.ext.commands import Cog, group
from httpx import Response

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import is_trusted


class Pins(Cog):
    """Linking to messages."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @group(aliases=("pinned", "pins"))
    async def pin(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @pin.command(aliases=("create",))
    @is_trusted()
    async def create_pin(
        self,
        ctx: Context,
        message: Message,
    ) -> None:
        pin = {
            "server_id": message.guild.id,
            "user_id": message.author.id,
            "message": message.jump_url,
        }

        r: Response = await self.bot.api.post("/v1/pins/", data=pin)

        data = r.json()

        embed = Embed(
            title="Created new pin",
            description=f"Pin ID: {data['id']}",
            url=message.jump_url,
        )

        await ctx.send(embed=embed)

    @pin.command(aliases=("remove", "delete", "del"))
    @is_trusted()
    async def delete_pin(self, ctx: Context, id: str) -> None:
        r: Response = await self.bot.api.delete(f"/v1/pins/{id}")

        if r.is_success:
            data = r.json()

            embed = Embed(title="Deleted pin", url=data["message"])

            await ctx.send(embed=embed)

            return

        await ctx.send(
            embed=Embed(title=f"Could not find pin with ID '{id}'"),
        )

    @pin.command(aliases=("migrate",))
    @is_trusted()
    async def migrate_pins(self, ctx: Context) -> None:
        """Puts the channel's pins in the database."""
        async with ctx.typing():
            channel_pins = await ctx.channel.pins()

            success = 0

            for pin in channel_pins:
                pin = {
                    "server_id": pin.guild.id,
                    "user_id": pin.author.id,
                    "message": pin.jump_url,
                }

                r: Response = await self.bot.api.post("/v1/pins/", data=pin)

                if r.is_success:
                    success += 1

            await ctx.send(
                embed=Embed(title=f"Migrated {success} pin(s)"),
            )

    @pin.command(aliases=("list",))
    @is_trusted()
    async def list_pins(self, ctx: Context, amount: int | None = 10) -> None:
        data = await self.bot.api.get("/v1/pins/")

        pins = "\n".join(
            [
                f"{i}. <@{pin['user_id']}>: [{pin['created_at']}]({pin['message']})"
                for (i, pin) in enumerate(data.json())
            ]
        )

        embed = Embed(
            title=f"First {amount} pin(s)",
            description=pins,
        )

        await ctx.send(embed=embed)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Pins(bot))
