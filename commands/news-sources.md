---
name: news-sources
description: View and manage your herald news sources
allowed-tools: Bash, Read, Write, Edit
---

You are showing and managing the user's herald sources.

## Preflight

1. Check `~/.herald/config.yaml` exists. If not: "Run `/news-init` first."
2. Read config. If YAML parse fails: "Config file has invalid YAML."

## Default: show all sources

1. Read `~/.herald/config.yaml`
2. Display sources grouped by category:

```
Sources:
  community:
    - hn: Hacker News (weight: 0.3)
  official:
    - openai: OpenAI Blog (weight: 0.25)

Topics: ai_agents, ai_models
Total: N sources
```

3. Show available commands:
   - `/news-add <url>` — add a source
   - `/news-sources remove <name>` — remove a source

## Subcommand: remove <name>

1. Read config
2. Find source by id or name (case-insensitive match)
3. If found: remove from sources list, write config via Edit tool
4. Confirm: "Removed <name>. Run `/news-run` to update."
5. If not found: "Source '<name>' not found. Run `/news-sources` to see all."

## Config rules

- Only edit `~/.herald/config.yaml`
- Use Edit tool for targeted changes
- Preserve YAML comments
- Always confirm before writing
