import logging
import re
import ast
from typing import Union

import numpy as np
from discord.ext.commands import Cog, group, is_owner, Context
from discord import Embed
from sympy import Symbol
from sympy.parsing.sympy_parser import parse_expr

from xythrion.bot import Xythrion
from xythrion.utils import graph_2d, noblock, remove_whitespace

log = logging.getLogger(__name__)

# ILLEGAL_EXPRESSION_CHARACTERS = re.compile(r"[!{}\[\]]+")
# POINT_ARRAY_FORMAT = re.compile(r"(-?\d+(\.\d+)?),(-?\d(\.\d+)?)")

# TIMEOUT_FOR_GRAPHS = 10.0


AST_WHITELIST = (ast.Expression, ast.Call, ast.Name, ast.Load,
                 ast.BinOp, ast.UnaryOp, ast.operator, ast.unaryop, ast.cmpop,
                 ast.Num,
                 )


# https://stackoverflow.com/a/11952618
def sanitize_expression(expression: str) -> bool:
    tree = ast.parse(expression, mode='eval')
    return all(isinstance(node, AST_WHITELIST) for node in ast.walk(tree))

    # if valid:
    #     result = eval(
    #     compile(
    #     tree, filename='', mode='eval'), {"__builtins__": None}, safe_dict)


restriction = tuple[Union[int, float], Union[int, float]]


@noblock
async def calculate(
    expression: str,
    restrict_x: restriction,
    restrict_y: restriction,
    *,
    center: float = 0.0,
    scale: float = 1.0,
    point_amount: int = 100
) -> tuple[np.ndarray, np.ndarray]:
    s = np.random.normal(center, scale, point_amount)

    # bounds = abs(bounds)
    # x = np.arange(-bounds, bounds, bounds / 50)
    # expr = parse_expr(expression)
    # x_symbol = Symbol("x")
    #
    # y = np.array([expr.subs({x_symbol: x_point}).evalf() for x_point in x])
    #
    # return x, y


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
    async def expression(self, ctx: Context, *,
                         expression: remove_whitespace) -> None:
        if not sanitize_expression(expression):
            embed = Embed(description="Illegal expression passed.")

            await ctx.reply(embed=embed)

            return

        # *_ catches any other dimension of the array, so only 2d is captured.
        # x, y, *_ = zip(*[list(map(float, point.group(0).split(","))) for point in point_array])

        # embed = await graph_2d(x, y)

        # await ctx.send(file=embed.file, embed=embed)

    # @staticmethod
    # def calculate(expression: str, bounds: Union[int, float] = 10) -> Tuple[np.ndarray, np.ndarray]:
    #     """Calculate y-axis values from a set of x-axis values, given a math expression."""
    #     bounds = abs(bounds)
    #     x = np.arange(-bounds, bounds, bounds / 50)
    #     expr = parse_expr(expression)
    #     x_symbol = Symbol("x")
    #
    #     y = np.array([expr.subs({x_symbol: x_point}).evalf() for x_point in x])
    #
    #     return x, y
    #
    # @graph.command(aliases=("ex", "expr"))
    # @is_owner()
    # async def expression(self, ctx: Context, *, expression: remove_whitespace) -> None:
    #     expression = expression.replace("^", "**")
    #
    #     if (illegal_char := re.search(ILLEGAL_EXPRESSION_CHARACTERS, expression)) is not None:
    #         return await ctx.embed(desc=f"Illegal character in expression: {illegal_char.group(0)}")
    #
    # @graph.command(aliases=("point",))
    # @is_owner()
    # async def points(self, ctx: Context, *, points: remove_whitespace) -> None:
    #     if not (point_array := re.finditer(POINT_ARRAY_FORMAT, points)):
    #         return await ctx.embed(desc="Illegal character(s) in point array.")
    #
    #     # *_ catches any other dimension of the array, so only 2d is captured.
    #     x, y, *_ = zip(*[list(map(float, point.group(0).split(","))) for point in point_array])
    #
    #     embed = await graph_2d(x, y)
    #
    #     await ctx.send(file=embed.file, embed=embed)
