import argparse
import sys
from pathlib import Path
from typing import NoReturn

VERSION_PATH = Path("VERSION")


def main(args: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["check", "update"])
    parsed_args = parser.parse_args(args)

    status_code = 1
    try:
        if parsed_args.command == "check":
            status_code = check_version()
        else:
            status_code = update_version()
    except Exception as exc:
        print(str(exc))

    return status_code


def check_version() -> int | NoReturn:
    version = read_version()
    lines = version.splitlines()
    if len(lines) != 1:
        raise ValueError(f"Number of lines in {VERSION_PATH} should be exactly 1")

    if not version.isdigit():
        raise ValueError(f"Invalid version number '{version}'")

    return 0


def read_version() -> str:
    return VERSION_PATH.read_text(encoding="utf-8").strip()


def update_version() -> int:
    old_version = int(read_version())
    new_version = old_version + 1
    VERSION_PATH.write_text(str(new_version), encoding="utf-8")
    print(f"Version number has been updated from {old_version} to {new_version}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
