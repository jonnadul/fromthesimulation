#!/usr/bin/env python3
"""Create a new Jekyll post with correct front matter.

Usage:
    python tools/new_post.py "My Post Title" [--subtitle "Optional subtitle"]

Creates _posts/YYYY-MM-DD-my-post-title.md and opens it in the default editor.
"""
import argparse
import datetime
import os
import re
import subprocess
import sys

SITE = r"C:\Users\jonna\blog"
POSTS = os.path.join(SITE, "_posts")


def slugify(text):
    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")[:70] or "post"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("title")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()

    today = datetime.date.today().strftime("%Y-%m-%d")
    slug = slugify(args.title)
    path = os.path.join(POSTS, "%s-%s.md" % (today, slug))

    if os.path.exists(path):
        print("ERROR: already exists: %s" % path)
        sys.exit(1)

    fm = [
        "---",
        "layout: post",
        'title: "%s"' % args.title.replace('"', '\\"'),
    ]
    if args.subtitle:
        fm.append('subtitle: "%s"' % args.subtitle.replace('"', '\\"'))
    fm.append("date: %s 12:00:00" % today)
    fm.append("categories: []")
    fm.append("tags: []")
    fm.append("---")
    fm.append("")
    fm.append("Write your post here.")
    fm.append("")

    os.makedirs(POSTS, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(fm))

    print("Created: %s" % path)
    if not args.no_open:
        try:
            os.startfile(path)  # noqa: S606 - intended native Windows open
        except Exception as e:
            print("(could not auto-open: %s)" % e)


if __name__ == "__main__":
    main()
