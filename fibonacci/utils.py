import time


def record_time(func):
    """Decorator that prints the execution time of the wrapped function."""

    depth = 0

    def wrapper(*args, **kwargs):
        nonlocal depth
        is_outermost = depth == 0
        depth += 1

        if is_outermost:
            start = time.time()
        result = func(*args, **kwargs)
        depth -= 1

        if is_outermost and start:
            elapsed = time.time() - start
            print(f"{func.__name__} executed in {elapsed:.10f} seconds")

        return result

    return wrapper
