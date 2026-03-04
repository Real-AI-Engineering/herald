---
name: news-add
description: Add a news source (URL or topic keywords) to your herald config
allowed-tools: Bash, Read, Write, Edit
---

You are adding a news source to the user's herald config.

## Preflight

1. Check `~/.herald/config.yaml` exists. If not: "Run `/news-init` first."
2. Read config.

## Determine input type

Parse the user's input after `/news-add`:
- If it looks like a URL (starts with http/https): → URL flow
- If no argument: ask "Paste an RSS/Atom feed URL"

## URL Flow — RSS Feed

1. **Validate feed**: Fetch the URL and check it returns valid XML/RSS:
   ```bash
   curl -sL --max-time 10 "<url>" 2>/dev/null | head -5
   ```
   Look for `<?xml`, `<rss`, `<feed`, `<atom` markers.

2. **If valid feed**: Suggest a source entry:
   - id: derive from domain (e.g., `simonw` from `simonwillison.net`)
   - name: derive from domain or feed title
   - weight: 0.2 (default)
   - category: community (default)
   Ask user to confirm or customize.

3. **If not valid**: Try RSS autodiscovery:
   - Platform heuristics: github.com → `/releases.atom`, substack → `/feed`
   - Common paths: `/feed`, `/rss`, `/atom.xml`, `/feed.xml`
   If found, confirm with user. If not: "Could not find RSS feed."

4. **Add to config**: Read `~/.herald/config.yaml`, append to `sources` list via Edit tool.

5. **Confirm**: "Added <name>. Run `/news-run` to fetch articles."

## Config rules

- Only edit `~/.herald/config.yaml`
- Use Edit tool, not full rewrite
- Check for duplicate URLs or ids before adding
