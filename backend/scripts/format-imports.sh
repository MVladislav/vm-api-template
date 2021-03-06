#!/bin/sh -e
set -x

# Sort imports one per line, so autoflake can remove unused imports
python3 -m isort --recursive --force-single-line-imports --apply app
sh ./scripts/format.sh
