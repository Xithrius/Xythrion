---
name: Easier type annotations for decorators with contextlib.contextmanager
source: https://youtu.be/_QXlbwRmqgI
---


```python
import contextlib
import time
from collections.abc import Generator

@contextlib.contextmanager
def timing_ctx(name: str) -> Generator[None, None, None]:
    t0 = time.monotonic()
    yield
    t1 = time.monotonic()
    print(f"{name} took {t1 - t0}s")

@timing_ctx("g.timing")
def g(x: int) -> int:
    with timing_ctx("something.else"):
        time.sleep(0.2)

    return x * 2
```

output when calling `g(10)`:

```
something.else took 0.20016720900002838s
g.timing took 0.2008831260000079s
```
