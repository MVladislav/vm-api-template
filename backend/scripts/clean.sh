#!/usr/bin/env bash

set -e
set -x

rm -r logs/.mypy_cache logs/html_dir
rm logs/format-imports.log logs/lint.log logs/test-cov-html.log logs/test.log

exit 0
