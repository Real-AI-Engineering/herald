---
name: news-stop
description: Show cleanup options for herald data
allowed-tools: Bash, Read
---

You are helping the user clean up herald data.

## Steps

1. **Check status**:
```bash
cd "${CLAUDE_PLUGIN_ROOT}" && PYTHONPATH=. python3 -m herald.cli status 2>/dev/null
```

2. **Show cleanup options**:
   - "To delete all data and config: `rm -rf ~/.herald/`"
   - "To re-initialize: run `/news-init`"

3. **Do NOT delete data automatically.** The user decides.
