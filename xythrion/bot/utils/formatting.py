def markdown_link(desc: str, link: str, t: str = "") -> str:
    """Gets rid of the thinking while creating a link for markdown."""
    if not (desc or link):
        raise ValueError("Description and link must exist")
    return f"[{t}{desc}{t}]({link})"


def and_join(items: list[str], sep: str = ", ") -> str:
    """Joins a list by a separator with an 'and' at the very end."""
    items_length = len(items)

    if items_length <= 1:
        return "" if items_length == 0 else items[0]
    return f"{sep.join(str(x) for x in items[:-1])}{sep}and {items[-1]}"


def codeblock(code: str | list[str], language: str = "python") -> str:
    """Returns a string in the format of a Discord codeblock."""
    block = "\n".join(code) if isinstance(code, list) else code

    return f"```{language}\n{block}\n```"