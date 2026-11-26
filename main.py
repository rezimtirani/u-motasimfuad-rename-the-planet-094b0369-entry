"""Rename the Planet — make.fun entry.

Writes one line to $MAKEFUN_OUTPUT_DIR/entry.txt: a new name for Mars
and one funny reason for it. Only the Python standard library is used.
"""

import os
import sys

PLANET_LINE = "I hereby rename Mars 'Refund' — after 4.5 billion years of red dust and no ocean, the solar system owes us our money back."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 200 characters. The req JSON agrees here,
# but the RULES.txt figure is the authority.
MAX_CHARS = 200


def validate_line(text):
    """Return the line once it passes the sealed gate, else raise.

    The gate counts UTF-8 characters, not bytes, so the line must be a
    single line of 1 to 200 characters, not only whitespace, with no
    trailing newline and no control characters in the output file.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, gate allows 1 to {MAX_CHARS}"
        )
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    return text


def describe_line(text):
    """Summarise a line the way the sealed gate measures it.

    The gate counts UTF-8 characters, not bytes, so a line with wide
    characters reads shorter in characters than in bytes. Returns a
    one-line human-readable summary.
    """
    words = len(text.split())
    return (
        f"{len(text)} characters, {len(text.encode('utf-8'))} UTF-8 bytes, "
        f"{words} words"
    )


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not output_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    line = validate_line(PLANET_LINE)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    print(f"wrote {path} ({describe_line(line)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
