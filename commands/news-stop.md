---
name: news stop
description: Disable the daily news scheduler and show cleanup options
allowed-tools: Bash, Read
---

You are disabling the herald daily scheduler.

## Steps

1. **Uninstall scheduler**:

```bash
VENV_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/herald/.venv"
if [ -f "$VENV_DIR/bin/python" ]; then
    PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" "$VENV_DIR/bin/python" -c "
from pipeline.scheduler import uninstall_scheduler, get_scheduler_status
status = get_scheduler_status()
if not status['installed']:
    print('No scheduler found.')
else:
    ok = uninstall_scheduler()
    print('Scheduler removed.' if ok else 'Failed to remove scheduler.')
"
else
    echo "ERROR: venv not found at $VENV_DIR. Run /news init first."
fi
```

2. **Confirm to user**: "Scheduler removed. Data preserved at ~/.local/share/herald/"

3. **Show cleanup options**:
   - "To delete all data: `rm -rf ~/.local/share/herald/`"
   - "To delete config: `rm -rf ~/.config/herald/`"
   - "To re-enable: run `/news init`"

4. **Do NOT delete data or config automatically.** The user decides.
