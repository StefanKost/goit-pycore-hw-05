from typing import Dict, List, Callable
import helpers


def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    try:
        username, phone = helpers.parse_contact_args(args, 2, "Add command")
    except ValueError as e:
        return str(e)

    if username in contacts:
        return f"Contact '{username}' already exists. Use 'change' command to update."

    contacts[username] = phone
    return "Contact added."


def change_contact(args: List[str], contacts: Dict[str, str]) -> str:
    try:
        username, phone = helpers.parse_contact_args(args, 2, "Change command")
    except ValueError as e:
        return str(e)

    if username not in contacts:
        return f"Contact '{username}' not found."

    contacts[username] = phone
    return "Contact updated."


def show_phone(args: List[str], contacts: Dict[str, str]) -> str:
    try:
        username = helpers.parse_contact_args(args, 1, "Phone command")
    except ValueError as e:
        return str(e)

    if username not in contacts:
        return f"Contact '{username}' not found."

    return f"Phone: {contacts[username]}"


def show_all(contacts: Dict[str, str]) -> str:
    if not contacts:
        return "No contacts found."

    result = "All contacts:\n"
    for username, phone in sorted(contacts.items()):
        result += f"{username}: {phone}\n"

    return result.rstrip()


commands: Dict[str, Callable[[List[str], Dict[str, str]], str]] = {
    "hello": lambda args, contacts: "How can I help you?",
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": lambda args, contacts: show_all(contacts)
}
