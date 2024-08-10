"""Process bang markup
"""

from functools import reduce
import subprocess


def variables(markup: str) -> dict[str, str]:
    """Process markup to retrive variable key value pairs."""

    def _read(filepath: str) -> str:
        """Read file contents."""
        with open(filepath, "r") as f:
            return f.read()

    def _command(command: str) -> str:
        """Run command, return stdout + strerr"""
        output = subprocess.run(
            command,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return output.stdout + output.stderr

    get_value = {
        "!": lambda value: value,
        "!!": lambda value: _read(value),
        "!!!": lambda value: _command(value),
    }
    return {
        line.split(" ", 1)[0].replace("!", ""): get_value[(len(line) - len(line.lstrip('!'))) * "!"](line.split(" ", 1)[-1])
        for line in markup.split("\n")
        if line.startswith("!")
    }


def process(text: str, **variables) -> str:
    """Process markup.

    Args:
         input (str): input text

    Returns:
        str: processed text
    """
    for i in range(100):
        text = reduce(
            lambda text, variable: text.replace(
               f"!!{variable}!!", variables[variable]
            ),
            variables,
            text
        )
    return text
