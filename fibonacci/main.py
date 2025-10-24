from fibonacci import caching_fibonacci


def main():
    fib = caching_fibonacci()
    print(fib(10))  # Will output 55
    print(fib(15))  # Will output 610. Will take from cache when fib <= 10
    print(caching_fibonacci()(11))  # Will calculate without caching
    print(fib(11))  # Will output 89. Get from cache and should be fast


if __name__ == "__main__":
    main()
