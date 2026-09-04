#!/usr/bin/env bash
# One-off build of the site into _site/
cd "$(dirname "$0")" || exit 1
export PATH="/c/Ruby34-x64/bin:$PATH"
exec ruby C:/Ruby34-x64/bin/jekyll build "$@"
