#!/bin/sh
reset-repo
clear
exec python3 "$(dirname "$0")/serve.py" "$@"
