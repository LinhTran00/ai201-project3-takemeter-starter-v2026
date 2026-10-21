#!/usr/bin/env python3
"""
Turn saved r/VisitingNYC threads into a CSV of comments ready for labelling.

Reddit blocks logged-out scripts, so you save each thread from your browser:

  1. Open a thread while logged in to Reddit.
  2. Add `.json` to the end of the URL and press Enter, e.g.
       https://www.reddit.com/r/VisitingNYC/comments/abc123/some_title/.json
  3. Save the page (Ctrl+S) into a `threads/` folder. Any name ending .json.

Then:

    python collect_comments.py
    python collect_comments.py --dir threads --limit 300

Adds comments to labels.csv as `text,label,note`, with `label` left blank for
you to fill in. Safe to re-run after saving more threads: rows already in
labels.csv (and any labels you've filled in) are kept, and only new comments
are added. The two example rows from labels_template.csv are dropped.
"""

import argparse
import csv
import json
from pathlib import Path

SKIP_BODIES = {"[deleted]", "[removed]", ""}
SKIP_AUTHORS = {"AutoModerator"}
TEMPLATE_LABEL = "your_label_here"


def walk_comments(children):
    """Yields every comment in a thread, replies included."""
    for child in children:
        if child.get("kind") != "t1":
            continue  # "more" stubs are comments Reddit didn't load; skip them
        data = child["data"]
        yield data
        replies = data.get("replies")
        if isinstance(replies, dict):
            yield from walk_comments(replies["data"]["children"])


def thread_comments(path, min_chars):
    with open(path, encoding="utf-8") as f:
        post, comments = json.load(f)
    op = post["data"]["children"][0]["data"].get("author")
    for c in walk_comments(comments["data"]["children"]):
        body = (c.get("body") or "").strip()
        if body in SKIP_BODIES or c.get("author") in SKIP_AUTHORS:
            continue
        # The person who made the post mostly replies "thanks!", so skip them.
        if c.get("is_submitter") or (op not in (None, "[deleted]") and c.get("author") == op):
            continue
        if len(body) < min_chars:
            continue
        yield body


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dir", default="threads",
                        help="folder of saved thread .json files")
    parser.add_argument("--limit", type=int, default=300,
                        help="stop once labels.csv holds this many rows")
    parser.add_argument("--min-chars", type=int, default=15,
                        help="skip comments shorter than this (e.g. 'lol', 'this')")
    parser.add_argument("--out", default="labels.csv")
    args = parser.parse_args()

    files = sorted(Path(args.dir).glob("*.json"))
    if not files:
        raise SystemExit(f"No .json files in {args.dir}/ — see the steps at the top of this file.")
    print(f"{len(files)} threads to read")

    rows = []
    if Path(args.out).exists():
        with open(args.out, encoding="utf-8", newline="") as f:
            rows = [r for r in csv.DictReader(f) if r.get("label") != TEMPLATE_LABEL]
    kept = len(rows)
    seen = {r["text"] for r in rows}

    for path in files:
        if len(rows) >= args.limit:
            break
        try:
            new = 0
            for body in thread_comments(path, args.min_chars):
                if body in seen:
                    continue
                seen.add(body)
                rows.append({"text": body, "label": "", "note": ""})
                new += 1
                if len(rows) >= args.limit:
                    break
            print(f"  +{new:3d}  {path.name}")
        except (ValueError, KeyError) as e:  # not a saved thread, or saved as HTML
            print(f"  skipped ({e})  {path.name}")

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label", "note"],
                                extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nKept {kept} existing rows, added {len(rows) - kept} new comments.")
    print(f"{args.out} now has {len(rows)} rows.")


if __name__ == "__main__":
    main()
