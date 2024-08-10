#!/usr/bin/env bash
# Batch processing script
# Process text files from ``in`` and process with ``bang`` to ``out``.
# Also copy image files

find "in" \
  -type f \
  \( \
     -iname '*.txt' \
  -o -iname '*.html' \
  -o -iname '*.md' \
  -o -iname '*.css' \
  \) \
  -exec basename {} \; \
  | grep -vE 'jpg|gif|png|jpeg' \
  | xargs -I% bash -c './bang.sh markup.bang in/% > out/%'

cp "in/"*.{png,jpg,gif,jpeg} out/ 2>/dev/null

cp out/index.html .
sed -i index.html 's/style.css/out\/style.css/'

URL="file://`pwd`/out/index.html"; xdg-open $URL || sensible-browser $URL || x-www-browser $URL || gnome-open $URL

