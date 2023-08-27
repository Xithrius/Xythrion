import ast

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
    if not expression:
        raise ValueError("Expression must exist")
    tree = ast.parse(expression, mode="eval")
    return all(isinstance(node, AST_WHITELIST) for node in ast.walk(tree))
