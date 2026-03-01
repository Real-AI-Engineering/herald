---
name: news digest
description: Read today's curated news digest
allowed-tools: Bash, Read
---

You are presenting the user's daily news digest from herald.

## Steps

0. **Check for --demo flag**: If the user's message includes `--demo`:
   - Determine venv path and python binary:
     ```bash
     HERALD_VENV="${XDG_DATA_HOME:-$HOME/.local/share}/herald/.venv"
     HERALD_PYTHON="$HERALD_VENV/bin/python"
     ```
   - If venv exists (`test -f "$HERALD_PYTHON"`): use it for full demo (RSS + HN).
   - If venv does NOT exist: attempt best-effort quick setup:
     ```bash
     python3 -m venv "$HERALD_VENV" 2>/dev/null && \
       "$HERALD_PYTHON" -m pip install -q --timeout 15 -r "${CLAUDE_PLUGIN_ROOT}/pipeline/requirements.txt" 2>/dev/null
     ```
     - If quick setup succeeds: use `$HERALD_PYTHON` for full demo.
     - If quick setup fails or times out: fall back to system `python3` (HN-only mode). After output, add note: "This is an HN-only preview. Run `/news init` for full RSS feeds (20+ sources)."
   - Run demo:
     ```bash
     cd "${CLAUDE_PLUGIN_ROOT}" && PYTHONPATH=. "$HERALD_PYTHON" -m pipeline.demo 2>&1
     ```
     (Replace `$HERALD_PYTHON` with `python3` in fallback mode.)
   - Display the stdout output.
   - STOP here — do not continue to remaining steps

1. **Find latest digest**: Check these paths in order:
   - `~/.local/share/herald/data/digests/$(date +%Y-%m-%d).md` (today)
   - Yesterday's date as fallback

2. **Read last_run.json**: Read `~/.local/share/herald/data/state/last_run.json` for run metadata.

3. **Show header**: "Last run: YYYY-MM-DD HH:MM (STATUS). Items: X kept from Y collected."

4. **Handle edge cases**:
   - No digest file exists: "No digest available. Run /news run or check /news init."
   - Digest exists but zero items: "No relevant items found today. Your filters may be too narrow. Edit ~/.config/herald/config.yaml to adjust."
   - last_run.json shows error: "Last run had errors. Check ~/.local/share/herald/data/state/collect.log"

5. **Present digest**: Read the digest markdown file and present the items grouped by topic. Highlight items most relevant to the user's current work context.

6. **Ask**: "Anything actionable here? I can help you dive deeper into any of these items."
