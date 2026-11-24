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


def _gate_ok(text: str) -> bool:
    """The gate's own conditions, checked against the actual text."""
    return (
        1 <= len(text) <= 160
        and text.strip() != ""
        and "\n" not in text
        and "\r" not in text
    )


def main() -> None:
    # Fail loudly instead of writing an invalid entry if the line ever
    # drifts outside the gate (for example after a future edit).
    if not _gate_ok(LINE):
        raise SystemExit(
            f"line is {len(LINE)} characters, must be 1-160, "
            "single line, not only whitespace"
        )
    # Never remove the output directory itself: the grader may run this
    # with a root-owned output directory inside a sticky parent, where
    # deleting the directory fails with EPERM. Create it if missing,
    # clear only its contents, then write. An entry that vanishes
    # between listing and removal (a concurrent grader cleanup) is
    # already gone, so treat that as done, not as an error.
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, name)
        try:
            if os.path.isdir(path) and not os.path.islink(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except FileNotFoundError:
            continue
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    # Verify what was actually written: read it back and confirm it is
    # byte-for-byte the line and still passes the gate, so a silent
    # write failure can never pass as a valid entry.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != LINE or not _gate_ok(written):
        raise SystemExit("verification failed: entry.txt does not match")


if __name__ == "__main__":
    main()
