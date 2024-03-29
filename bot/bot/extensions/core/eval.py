import contextlib
import inspect
import pprint
import re
import textwrap
import traceback
from io import StringIO
from typing import Any

import discord
from discord.ext.commands import Cog, group

from bot.bot import Xythrion
from bot.context import Context
from bot.utils import is_trusted


def find_nth_occurrence(string: str, substring: str, n: int) -> int | None:
    """Return index of `n`th occurrence of `substring` in `string`, or None if not found."""
    index = 0
    for _ in range(n):
        index = string.find(substring, index + 1)
        if index == -1:
            return None
    return index


class Eval(Cog):
    """
    Administrator and Core Developer commands.

    https://github.com/python-discord/bot/blob/main/bot/exts/utils/internal.py#L222-L227
    """

    def __init__(self, bot: Xythrion):
        self.bot = bot
        self.env = {}  # type: ignore [var-annotated]
        self.ln = 0
        self.stdout = StringIO()

        self.socket_events: int = 0
        self.socket_event_total: int = 0

    @Cog.listener()
    async def on_socket_event_type(self, event_type: str) -> None:
        """When a websocket event is received, increase our counters."""
        self.socket_event_total += 1
        self.socket_events[event_type] += 1  # type: ignore [var-annotated,index]

    def _format(self, inp: str, out: Any) -> str | tuple[str, discord.Embed | None]:
        """Format the eval output into a string & attempt to format it into an Embed."""
        self._ = out

        res = ""

        # Erase temp input we made
        if inp.startswith("_ = "):
            inp = inp[4:]

        # Get all non-empty lines
        lines = [line for line in inp.split("\n") if line.strip()]
        if len(lines) != 1:
            lines += [""]

        # Create the input dialog
        for i, line in enumerate(lines):
            if i == 0:
                # Start dialog
                start = f"In [{self.ln}]: "

            else:
                # Indent the 3 dots correctly;
                # Normally, it's something like
                # In [X]:
                #    ...:
                #
                # But if it's
                # In [XX]:
                #    ...:
                #
                # You can see it doesn't look right.
                # This code simply indents the dots
                # far enough to align them.
                # we first `str()` the line number
                # then we get the length
                # and use `str.rjust()`
                # to indent it.
                start = "...: ".rjust(len(str(self.ln)) + 7)

            if i == len(lines) - 2:
                if line.startswith("return"):
                    line = line[6:].strip()

            # Combine everything
            res += start + line + "\n"

        self.stdout.seek(0)
        text = self.stdout.read()
        self.stdout.close()
        self.stdout = StringIO()

        if text:
            res += text + "\n"

        if out is None:
            # No output, return the input statement
            return res, None

        res += f"Out[{self.ln}]: "

        if isinstance(out, discord.Embed):
            # We made an embed? Send that as embed
            res += "<Embed>"
            res = (res, out)  # type: ignore [assignment]

        else:
            if isinstance(out, str) and out.startswith(
                "Traceback (most recent call last):\n",
            ):
                # Leave out the traceback message
                out = "\n" + "\n".join(out.split("\n")[1:])

            if isinstance(out, str):
                pretty = out
            else:
                pretty = pprint.pformat(out, compact=True, width=60)

            if pretty != str(out):
                # We're using the pretty version, start on the next line
                res += "\n"

            if pretty.count("\n") > 20:
                # Text too long, shorten
                li = pretty.split("\n")

                pretty = (
                    "\n".join(li[:3])  # First 3 lines
                    + "\n ...\n"  # Ellipsis to indicate removed lines
                    + "\n".join(li[-3:])
                )  # last 3 lines

            # Add the output
            res += pretty
            res = (res, None)  # type: ignore [assignment]

        return res

    async def _eval(self, ctx: Context, code: str) -> discord.Message | None:
        """Eval the input code string & send an embed to the invoking context."""
        self.ln += 1

        if code.startswith("exit"):
            self.ln = 0
            self.env = {}
            return await ctx.send("```Reset history!```")

        env = {
            "message": ctx.message,
            "author": ctx.message.author,
            "channel": ctx.channel,
            "guild": ctx.guild,
            "ctx": ctx,
            "self": self,
            "bot": self.bot,
            "inspect": inspect,
            "discord": discord,
            "contextlib": contextlib,
        }

        self.env.update(env)

        # Ignore this code, it works
        code_ = """
async def func():  # (None,) -> Any
    try:
        with contextlib.redirect_stdout(self.stdout):
{}
        if '_' in locals():
            if inspect.isawaitable(_):
                _ = await _
            return _
    finally:
        self.env.update(locals())
""".format(
            textwrap.indent(code, "            "),
        )

        try:
            exec(code_, self.env)  # noqa: S102
            func = self.env["func"]
            res = await func()

        except Exception:
            res = traceback.format_exc()

        out, embed = self._format(code, res)  # type: ignore [misc]
        out = out.rstrip("\n")  # Strip empty lines from output

        # Truncate output to max 15 lines or 1500 characters
        newline_truncate_index = find_nth_occurrence(out, "\n", 15)

        if newline_truncate_index is None or newline_truncate_index > 1500:
            truncate_index = 1500
        else:
            truncate_index = newline_truncate_index

        if len(out) > truncate_index:
            await ctx.send(
                f"```py\n{out[:truncate_index]}\n```... response truncated",
                embed=embed,
            )
            return None

        await ctx.send(f"```py\n{out}```", embed=embed)
        return None

    @group(name="internal", aliases=("int",))
    @is_trusted()
    async def internal_group(self, ctx: Context) -> None:
        await ctx.check_subcommands()

    @internal_group.command(name="eval", aliases=("e",))
    @is_trusted()
    async def eval(self, ctx: Context, *, code: str) -> None:
        """Run eval in a REPL-like format."""
        code = code.strip("`")
        if re.match("py(thon)?\n", code):
            code = "\n".join(code.split("\n")[1:])

        if (
            not re.search(  # Check if it's an expression
                r"^(return|import|for|while|def|class|from|exit|[a-zA-Z0-9]+\s*=)",
                code,
                re.M,
            )
            and len(code.split("\n")) == 1
        ):
            code = "_ = " + code

        await self._eval(ctx, code)


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(Eval(bot))
