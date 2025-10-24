from typing import Dict, List, Tuple
from commands import commands


def main() -> None:
    contacts: Dict[str, str] = {}
    print("Welcome to the assistant bot!\n"
          "Available commands:\n"
          "  hello                     - Show greeting\n"
          "  add <username> <phone>    - Add new contact\n"
          "  change <username> <phone> - Update existing contact\n"
          "  phone <username>          - Show contact's phone number\n"
          "  all                       - Show all contacts\n"
          "  close, exit               - Exit the bot\n")

    while True:
        try:
            user_input = input("Enter a command: ").strip()
            if not user_input:
                continue

            command, args = parse_input(user_input)
            result = handle_command(command, args, contacts)

            if result == "exit":
                print("Good bye!")
                break
            print(result)

        except KeyboardInterrupt:
            print("\nGood bye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            break


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    args = user_input.split()
    if not args:
        return "", []

    command = args[0].lower()
    args = args[1:] if len(args) > 1 else []
    return command, args


def handle_command(command: str, args: List[str], contacts: Dict[str, str]) -> str:
    match command:
        case "close" | "exit":
            return "exit"
        case cmd if cmd in commands:
            return commands[cmd](args, contacts)
        case _:
            available = ', '.join(sorted(commands.keys()) + ['close', 'exit'])
            return f"Invalid command. Available commands: {available}"


if __name__ == "__main__":
    main()
