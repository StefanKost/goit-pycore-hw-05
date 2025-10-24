from typing import Dict, Callable
from utils import record_time


def caching_fibonacci() -> Callable[[int], int]:
    cache: Dict[int, int] = {}

    @record_time
    def fibonacci(n: int) -> int:
        if n in cache:
            return cache[n]
        if n <= 1:
            return n
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci
