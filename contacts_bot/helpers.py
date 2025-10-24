import re
from typing import List, Tuple, Union


def validate_phone(phone: str) -> bool:
    if not re.match(r'^[+\-()\d\s]+$', phone):
        raise ValueError("Phone number can only contain digits, spaces, parentheses (), hyphens -, and plus sign +")

    return True


def normalize_phone(phone_number: str) -> str:
    """
    Normalizes a phone number to the standard format.

    :param phone_number: raw phone number string in any format
    :return: normalized phone number string
    """

    ua_code = '38'
    ua_phone_len = 13
    prefix = '+'
    normalized_number = re.sub(r"[^\d+]", "", phone_number)

    if normalized_number.startswith(ua_code):
        normalized_number = f"{prefix}{normalized_number}"
    elif not normalized_number.startswith(prefix):
        normalized_number = f"{prefix}{ua_code}{normalized_number}"

    if normalized_number.startswith(f"{prefix}{ua_code}") and len(normalized_number) != ua_phone_len:
        raise ValueError('Invalid phone number.')
    return normalized_number


def parse_contact_args(args: List[str], required_count: int, operation: str) -> Union[str, Tuple[str, ...]]:
    if len(args) < required_count:
        missing = required_count - len(args)
        arg_names = ["username", "phone"] if required_count == 2 else ["username"]
        raise ValueError(
            f"{operation} requires {required_count} arguments: {', '.join(arg_names[:required_count])}. Missing {missing} argument(s).")

    if required_count == 1:
        return args[0].strip()
    elif required_count == 2:
        username, phone = args[0].strip(), args[1].strip()
        validate_phone(phone)
        return username, normalize_phone(phone)

    return tuple(arg.strip() for arg in args[:required_count])
