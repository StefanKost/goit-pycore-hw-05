from typing import Generator
from decimal import Decimal
import re


def generator_numbers(text: str) -> Generator[Decimal]:
    for match in re.finditer(r'[+-]?\d+(?:[.,]\d+)?', text):
        number = match.group().replace(',', '')
        yield Decimal(number)
