"""bang - Static website generator.
"""

import argparse

from .markup import process, variables


def get_parser() -> argparse.ArgumentParser:
    """Returns: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    parser.add_argument(
        "markup",
        help="markup file",
        type=str,
    )
    parser.add_argument(
        "input",
        help="input file",
        type=str,
    )
    return parser

def main() -> None:
    """Main entry point
    """
    args = get_parser().parse_args()
    with open(args.markup, "r") as f:
        markup = f.read()
    with open(args.input, "r") as f:
        input = f.read()
    print(process(input, **variables(markup)))


if __name__ == "__main__":
    main()
