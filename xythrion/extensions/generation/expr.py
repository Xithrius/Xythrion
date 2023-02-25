import ast
from typing import Union

import numpy as np
from discord.ext.commands import Cog, group, is_owner, Context
from discord import Embed, File
from sympy import Symbol
from sympy.parsing.sympy_parser import parse_expr

from xythrion.bot import Xythrion
from xythrion.utils import graph_2d, noblock, remove_whitespace

AST_WHITELIST = (
    ast.Expression, ast.Call, ast.Name, ast.Load, ast.BinOp, ast.UnaryOp,
    ast.operator, ast.unaryop, ast.cmpop, ast.Num,
)


# https://stackoverflow.com/a/11952618
def sanitize_expression(expression: str) -> bool:
    tree = ast.parse(expression, mode='eval')
    return all(isinstance(node, AST_WHITELIST) for node in ast.walk(tree))


restriction = tuple[Union[int, float], Union[int, float]]


@noblock
def calculate(
    expression: str,
    restrict_x: restriction,
    *,
    point_amount: int = 25
) -> tuple[np.ndarray, np.ndarray]:
    x = np.linspace(restrict_x[0], restrict_x[1], point_amount)

    expr = parse_expr(expression)
    x_symbol = Symbol("x")

    y = np.array([expr.subs({x_symbol: x_point}).evalf() for x_point in x])

    return x, y


class GraphExpression(Cog):
    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    @is_owner()
    async def graph(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.reply("Missing subcommand")

    @graph.command(aliases=("ex", "expr"))
    @is_owner()
    async def expression(
        self,
        ctx: Context,
        *,
        expression: remove_whitespace
    ) -> None:
        if not sanitize_expression(expression):
            embed = Embed(description="Illegal expression passed.")

            await ctx.reply(embed=embed)

            return

        x, y = await calculate(expression, (-10, 10))

        buffer = await graph_2d(x, y)

        embed = Embed()

        embed.set_image(url="attachment://tmp_graph.png")

        file = File(fp=buffer, filename="tmp_graph.png")

        await ctx.send(embed=embed, file=file)
