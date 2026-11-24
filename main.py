"""One Word for the Boss.

Writes exactly one word describing the boss to entry.txt.

The word: Ghost. The boss who is never there -- no meeting, no reply,
no sign of life, yet somehow still in charge. Every office has one:
the chair is warm, the calendar is full, the boss is nowhere.
It beats the first word anyone reaches for ("micromanager") on freshness
while staying instantly true, and it travels -- a ghost boss haunts a
kitchen, a warehouse or an office alike.
"""

import os
import stat
import sys

WORD = "Ghost"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    data = WORD.encode("utf-8")

    # Gate self-check: exactly one word, 1-30 chars, no whitespace at all.
    text = WORD
    if not (1 <= len(text) <= 30):
        print(f"word length {len(text)} outside 1-30", file=sys.stderr)
        return 1
    if text != text.strip() or any(ch.isspace() for ch in text):
        print("word contains whitespace", file=sys.stderr)
        return 1
    if len(text.split()) != 1:
        print("not exactly one word", file=sys.stderr)
        return 1

    tmp = target + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, target)
    os.chmod(target, 0o644)

    # Read back and verify: bytes match exactly, decode as UTF-8,
    # no trailing newline, world-readable mode 0644.
    with open(target, "rb") as fh:
        actual = fh.read()
    if actual != data:
        print(f"verify failed: {actual!r} != {data!r}", file=sys.stderr)
        return 1
    if actual.decode("utf-8") != WORD:
        print("verify failed: not valid UTF-8 word", file=sys.stderr)
        return 1
    mode = stat.S_IMODE(os.stat(target).st_mode)
    if mode != 0o644:
        print(f"verify failed: mode {oct(mode)} != 0o644", file=sys.stderr)
        return 1
    if actual.endswith(b"\n"):
        print("verify failed: trailing newline", file=sys.stderr)
        return 1

    print(f"wrote {target}: {WORD!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
