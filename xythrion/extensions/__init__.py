from pkgutil import iter_modules

EXTENSIONS = frozenset(
    extension.name for extension in iter_modules(("xythrion/extensions",), "xythrion.extensions.")
)
