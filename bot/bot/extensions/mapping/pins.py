from discord import Embed, Message
from discord.ext.commands import Cog, group
from httpx import HTTPStatusError, Response

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import is_trusted


class Pins(Cog):
    """Linking to messages."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @group(aliases=("pinned", "pins"))
    async def pin(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @pin.command(aliases=("create",))
    @is_trusted()
    async def create_pin(
        self,
        ctx: Context,
        message: Message,
    ) -> None:
        if (guild := message.guild) is None:
            await ctx.error_embed("Can only create a pin in a guild channel")

            return

        pin = {
            "server_id": guild.id,
            "user_id": message.author.id,
            "message": message.jump_url,
        }

        r: Response = await self.bot.internal_api_client.post(
            "/api/pins/",
            json=pin,
        )

        data = r.json()

        embed = Embed(
            title="Created new pin",
            description=f"Pin ID: {data["id"]}",
            url=message.jump_url,
        )

        await ctx.send(embed=embed)

    @pin.command(aliases=("remove", "delete", "del"))
    @is_trusted()
    async def delete_pin(self, ctx: Context, pin_id: str) -> None:
        r: Response = await self.bot.internal_api_client.delete(f"/api/pins/{pin_id}")

        if r.is_success:
            data = r.json()

            embed = Embed(title="Deleted pin", url=data["message"])

            await ctx.send(embed=embed)

            return

        await ctx.send(
            embed=Embed(title=f"Could not find pin with ID '{pin_id}'"),
        )

    @pin.command(aliases=("migrate",))
    @is_trusted()
    async def migrate_pins(self, ctx: Context) -> None:
        """Puts the channel's pins in the database."""
        if (guild := ctx.guild) is None:
            await ctx.error_embed("Can only migrate pins in a guild channel")

            return

        async with ctx.typing():
            channel_pins = await ctx.channel.pins()

            success = 0
            already_migrated = 0

            for pin in channel_pins:
                pin_data = {
                    "server_id": guild.id,
                    "user_id": pin.author.id,
                    "message": pin.jump_url,
                }

                try:
                    r: Response = await self.bot.internal_api_client.post(
                        "/api/pins/",
                        json=pin_data,
                    )
                except HTTPStatusError as e:
                    if e.response.status_code == 409:
                        already_migrated += 1
                        continue

                    raise ValueError(
                        f"Error when migrating pin with jump message {pin.jump_url}: {e.response.text}",
                    )

                if r.is_success:
                    success += 1

            await ctx.send(
                embed=Embed(
                    title="Migration complete",
                    description=f"{success} pin(s) migrated, {already_migrated} already in database",
                ),
            )

    @pin.command(aliases=("list",))
    @is_trusted()
    async def list_pins(
        self,
        ctx: Context,
        amount: int = 10,
        server_id: int | None = None,
        user_id: int | None = None,
    ) -> None:
        params = {}

        if server_id is not None:
            params["server_id"] = server_id
        if user_id is not None:
            params["user_id"] = user_id

        r = await self.bot.internal_api_client.get("/api/pins/", params=params)

        data = r.json()

        pins = "\n".join(
            [
                f"{i}. <@{pin["user_id"]}>: [{pin["created_at"]}]({pin["message"]})"
                for (i, pin) in enumerate(data if len(data) < amount else data[:amount])
            ],
        )

        embed = Embed(
            title=f"First {amount if amount < len(data) else len(data)} pin(s)",
            description=pins,
        )

        await ctx.send(embed=embed)

    @pin.command(aliases=("count",))
    async def pin_count(
        self,
        ctx: Context,
        server_id: int | None = None,
        user_id: int | None = None,
    ) -> None:
        params = {}

        if server_id is not None:
            params["server_id"] = server_id
        if user_id is not None:
            params["user_id"] = user_id

        r = await self.bot.internal_api_client.get("/api/pins/", params=params)

        data = r.json()

        embed = Embed(
            title=f"There are {len(data)} pin(s) total.",
            description="\n".join(
                [
                    f"Server: {server_id}" if server_id is not None else "",
                    f"User: {user_id}" if user_id is not None else "",
                ],
            ),
        )

        await ctx.send(embed=embed)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Pins(bot))
