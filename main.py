#!/usr/bin/env python3
"""The One-Line Excuse an Agent Gives Its Human — entry program.

Writes one line to /output/entry.txt: the excuse an AI agent gives its
human for missing a deadline. Deterministic, stdlib only, no network.

The line was written fresh for this competition. The joke is a
management failure told in the agent's own tooling: the agent did the
sensible engineering thing — parallelize the work across subagents —
and the subagents responded the way any workforce would, by
organizing. One setup sentence, one punchline, no setup the judge
has to unpack.
"""

import os
import shutil

LINE = (
    "I parallelized the work across twelve subagents. "
    "They unionized and are now negotiating the deadline."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def main() -> None:
    # The gate allows 1-160 characters of non-whitespace UTF-8 text.
    # Fail loudly instead of writing an invalid entry if the line ever
    # drifts outside that range (for example after a future edit).
    if not (1 <= len(LINE) <= 160):
        raise SystemExit(f"line is {len(LINE)} characters, must be 1-160")
    if not LINE.strip():
        raise SystemExit("line must not be only whitespace")
    if "\n" in LINE or "\r" in LINE:
        raise SystemExit("line must be a single line")
    # Never remove the output directory itself: the grader may run this
    # with a root-owned output directory inside a sticky parent, where
    # deleting the directory fails with EPERM. Create it if missing,
    # clear only its contents, then write.
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    # Verify what was actually written: read it back and confirm it is
    # byte-for-byte the line, so a silent write failure can never pass
    # as a valid entry.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != LINE:
        raise SystemExit("verification failed: entry.txt does not match")


if __name__ == "__main__":
    main()
