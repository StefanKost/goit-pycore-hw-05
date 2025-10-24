import sys
from pathlib import Path
import re
from colorama import Fore, Style
from typing import Dict, List

LOG_LEVEL_ORDER = ["INFO", "ERROR", "DEBUG", "WARNING"]
COLOR_FILE = Fore.GREEN
COLOR_ERROR = Fore.RED
COLOR_WARNING = Fore.YELLOW
COLOR_INFO = Fore.BLUE
COLOR_DEBUG = Fore.MAGENTA
COLOR_HEADER = Fore.LIGHTBLUE_EX + Style.BRIGHT


def parse_log_line(line: str) -> dict:
    line = line.rstrip("\n")
    m = re.match(
        r"^\s*(\d{4}-\d{2}-\d{2})\s+"
        r"(\d{2}:\d{2}:\d{2})\s+"
        r"([A-Za-z]+)\s*"
        r"(.*)\s*$",
        line,
    )
    if not m:
        raise ValueError("Malformed log line")

    date, tm, level, msg = m.groups()
    return {
        "date": date,
        "time": tm,
        "level": level.upper(),
        "message": msg or "",
    }


def load_logs(file_path: str) -> List[dict]:
    logs: List[dict] = []
    skipped = 0
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if not line.strip():
                    continue
                try:
                    logs.append(parse_log_line(line))
                except ValueError:
                    skipped += 1
                    print(f"Warning: skip invalid line {i}", file=sys.stderr)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"No permission to read: {file_path}")
    except OSError as e:
        raise OSError(f"Cannot read '{file_path}': {e}")

    if skipped:
        print(f"Note: skipped {skipped} invalid line(s).", file=sys.stderr)
    return logs


def filter_logs_by_level(logs: List[dict], level: str) -> List[dict]:
    level_up = level.upper()
    if level_up not in LOG_LEVEL_ORDER:
        raise ValueError(f"Unknown level '{level}'. Use one of possible: {', '.join(LOG_LEVEL_ORDER)}")
    return [rec for rec in logs if rec.get("level") == level_up]


def count_logs_by_level(logs: List[dict]) -> Dict[str, int]:
    counts: Dict[str, int] = {level: 0 for level in LOG_LEVEL_ORDER}
    for rec in logs:
        level = rec.get("level", "").upper()
        if level in counts:
            counts[level] += 1
    return counts


def get_level_color(level: str) -> str:
    colors = {
        "INFO": COLOR_INFO,
        "ERROR": COLOR_ERROR,
        "DEBUG": COLOR_DEBUG,
        "WARNING": COLOR_WARNING
    }
    return colors.get(level, "")


def display_log_counts(counts: Dict[str, int]) -> None:
    rows = [(lvl, counts.get(lvl, 0)) for lvl in LOG_LEVEL_ORDER]
    level_width = max(len("LEVEL"), *(len(lvl) for lvl, _ in rows))
    count_width = max(len("COUNT"), *(len(str(cnt)) for _, cnt in rows))

    sep = f"-{'-' * level_width}-|-{'-' * count_width}-"
    header = f" {COLOR_HEADER}{'LEVEL'.ljust(level_width)}{Style.RESET_ALL} | {COLOR_HEADER}{'COUNT'.ljust(count_width)}{Style.RESET_ALL} "

    print(sep)
    print(header)
    print(sep)
    for lvl, cnt in rows:
        color = get_level_color(lvl)
        print(f" {color}{lvl.ljust(level_width)}{Style.RESET_ALL} | {str(cnt).ljust(count_width)} ")
    print(sep)


def validate_path(path_str: str) -> Path:
    path = Path(path_str)

    if not path.exists():
        raise FileNotFoundError(f"File '{path_str}' does not exist")

    if not path.is_file():
        raise FileNotFoundError(f"'{path_str}' is not a file")

    return path


def main():
    if len(sys.argv) < 2:
        print("Usage: python loglib/main.py <directory_path>")
        sys.exit(1)

    log_path_str = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) >= 3 else None

    try:
        path = validate_path(log_path_str)

        try:
            print(f"{COLOR_FILE}{path}{Style.RESET_ALL}")
        except NameError:
            print(path)

        logs = load_logs(str(path))
        counts = count_logs_by_level(logs)
        display_log_counts(counts)

        if level:
            try:
                selected = filter_logs_by_level(logs, level)
            except ValueError as e:
                print(f"{COLOR_ERROR}Error: {e}{Style.RESET_ALL}")
                sys.exit(2)

            level_color = get_level_color(level.upper())
            print(f"\n{'-' * 80}")
            print(f"Logs for level: {level_color}{level.upper()}{Style.RESET_ALL} (total {len(selected)})")
            print("-" * 80)
            for rec in selected:
                rec_color = get_level_color(rec['level'])
                print(f"{rec['date']} {rec['time']} {rec_color}{rec['level']}{Style.RESET_ALL} {rec['message']}")

    except (FileNotFoundError, PermissionError) as e:
        print(f"{COLOR_ERROR}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{COLOR_ERROR}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
