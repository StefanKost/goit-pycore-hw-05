from typing import Callable, Generator
from decimal import Decimal
from helpers import generator_numbers


def sum_profit(text: str, func: Callable[[str], Generator[Decimal]]) -> Decimal:
    return sum(func(text), Decimal('0'))


def main():
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений " \
           "додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Total income: {total_income}")


if __name__ == "__main__":
    main()
