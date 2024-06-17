import math
import re

from discord.ext.commands import Cog, command

from bot.bot import Xythrion
from bot.context import Context
from bot.utils.checks import is_trusted

SYNDICATION_URL = "https://cdn.syndication.twimg.com"

TWEET_ID = re.compile(r"https:\/\/x.com\/\w+\/status\/([0-9]+)$")


class Twitter(Cog):
    """
    Using the Twitter CDN for images/videos.

    Original source (in javascript):
    https://github.com/vercel/react-tweet/blob/main/packages/react-tweet/src/api/fetch-tweet.ts
    """

    def __init__(self, bot: Xythrion):
        self.bot = bot

    async def fetch_tweet(self, tweet_id: str) -> dict:
        def __get_tweet_token(internal_tweet_id: str) -> str:
            result = (float(internal_tweet_id) / 1e15) * math.pi
            encoded = int(result * 36**2)
            return str(encoded).lstrip("0")

        url = f"{SYNDICATION_URL}/tweet-result"
        params = {
            "id": tweet_id,
            "lang": "en",
            "features": ";".join(
                [
                    "tfw_timeline_list:",
                    "tfw_follower_count_sunset:true",
                    "tfw_tweet_edit_backend:on",
                    "tfw_refsrc_session:on",
                    "tfw_fosnr_soft_interventions_enabled:on",
                    "tfw_show_birdwatch_pivots_enabled:on",
                    "tfw_show_business_verified_badge:on",
                    "tfw_duplicate_scribes_to_settings:on",
                    "tfw_use_profile_image_shape_enabled:on",
                    "tfw_show_blue_verified_badge:on",
                    "tfw_legacy_timeline_sunset:true",
                    "tfw_show_gov_verified_badge:on",
                    "tfw_show_business_affiliate_badge:on",
                    "tfw_tweet_edit_frontend:on",
                ],
            ),
            "token": __get_tweet_token(tweet_id),
        }

        response = await self.bot.http_client.get(url, params=params)

        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()

        raise ValueError("Twitter response is not application/json")

    @staticmethod
    def extract_twitter_data_urls(data: dict) -> list[str]:
        media_urls = []

        items = data["mediaDetails"]
        for item in items:
            if item["type"] == "photo":
                photo_url = item["media_url_https"]
                media_urls.append(photo_url)
            elif item["type"] == "video":
                video_url = item["video_info"]["variants"][-1]["url"]
                media_urls.append(video_url)

        return media_urls

    @command()
    @is_trusted()
    async def convert_twitter_link(self, ctx: Context, url: str) -> None:
        if (tweet_match := re.match(TWEET_ID, url)) is None:
            await ctx.reply("Could not find twitter ID in this link")
            return

        tweet_id = tweet_match.groups()[0]

        data = await self.fetch_tweet(tweet_id)

        links = self.extract_twitter_data_urls(data)

        for link in links:
            await ctx.send(link)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Twitter(bot))
