"""Command-line entry point."""

import argparse
import sys
from pathlib import Path
from .analyzer import analyze_safe


def interactive() -> None:
    print("Arithmetic Expression Analyzer")
    while True:
        print("\n1. Analyze expression\n2. Exit")
        choice = input("Choice: ").strip()
        if choice == "2":
            return
        if choice == "1":
            print(analyze_safe(input("Expression: ")))
        else:
            print("Please choose 1 or 2.")


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Analyze arithmetic expressions.")
    parser.add_argument("expression", nargs="?", help="single expression to analyze")
    parser.add_argument("-f", "--file", type=Path, help="read one expression from a file")
    args = parser.parse_args(argv)
    if args.expression is not None and args.file is not None:
        parser.error("use an expression or --file, not both")
    if args.file is not None:
        try:
            text = args.file.read_text(encoding="utf-8")
        except OSError as error:
            print(f"Error: cannot read file: {error}")
            return 1
        print(analyze_safe(text))
        return 0
    if args.expression is not None:
        print(analyze_safe(args.expression))
        return 0
    try:
        interactive()
    except (EOFError, KeyboardInterrupt):
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
