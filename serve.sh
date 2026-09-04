#!/usr/bin/env bash
# Preview the blog locally at http://127.0.0.1:4000
# Rebuilds automatically when you save a file.
cd "$(dirname "$0")" || exit 1
export PATH="/c/Ruby34-x64/bin:$PATH"
exec ruby C:/Ruby34-x64/bin/jekyll serve --port 4000 --host 127.0.0.1 --livereload
