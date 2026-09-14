#!/usr/bin/env bash
# Detached launcher for scripts/main.py using keys from .claude/settings.json
export $(python -c "import json,shlex;print(' '.join(f\"{k}={shlex.quote(v)}\" for k,v in json.load(open('.claude/settings.json'))['env'].items()))")
python scripts/main.py