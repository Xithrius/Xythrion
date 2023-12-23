def format_nanosecond_time(
    ns: int,
    *,
    microsecond_threshold: int | None = 1_000,
    millisecond_threshold: int | None = 1_000_000,
    second_threshold: int | None = 1_000_000_000,
) -> str:
    if ns < microsecond_threshold:
        return f"{ns}ns"

    if ns < millisecond_threshold:
        return f"{ns / microsecond_threshold:.2f}µs"

    if ns < second_threshold:
        return f"{ns / millisecond_threshold:.2f}ms"

    return f"{ns / second_threshold:.2f}s"
