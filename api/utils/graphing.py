import ast
from io import BytesIO
from typing import Union

import numpy as np
from loguru import logger as log
from sympy.simplify import Symbol, parse_expr

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.style.use("dark_background")

except (ImportError, ImportWarning) as e:
    log.error(
        "Error when importing Matplotlib.",
        exc_info=(type(e), e, e.__traceback__),
    )

from utils.decorators import noblock

AST_WHITELIST = (
    ast.Expression,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.BinOp,
    ast.UnaryOp,
    ast.operator,
    ast.unaryop,
    ast.cmpop,
    ast.Num,
)


# https://stackoverflow.com/a/11952618
def sanitize_expression(expression: str) -> bool:
    tree = ast.parse(expression, mode="eval")
    return all(isinstance(node, AST_WHITELIST) for node in ast.walk(tree))


restriction = tuple[Union[int, float], Union[int, float]]


@noblock
def calculate(
    expression: str, restrict_x: restriction, *, point_amount: int = 25
) -> tuple[np.ndarray, np.ndarray]:
    x = np.linspace(restrict_x[0], restrict_x[1], point_amount)

    expr = parse_expr(expression)
    x_symbol = Symbol("x")

    y = np.array([expr.subs({x_symbol: x_point}).evalf() for x_point in x])

    return x, y


@noblock
def graph(
    x: np.ndarray,
    y: np.ndarray,
) -> BytesIO:
    buffer = BytesIO()

    fig, axis = plt.subplots()
    axis.grid(True, linestyle="-.", linewidth=0.5)

    axis.plot(x, y)

    fig.savefig(buffer, format="png")

    buffer.seek(0)

    return buffer
