#!/bin/bash

trap 'rm -f "$TMPFILE"' EXIT

set -e

TMPFILE=$(mktemp -t noggin-requirements-XXXXXX.txt)

poetry export --dev -f requirements.txt --without-hashes -o $TMPFILE
# poetry run pip freeze --exclude-editable --isolated > $TMPFILE

poetry run liccheck -r $TMPFILE
