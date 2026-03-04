# Herald

<div align="center">

**Curate your daily news digest with zero API keys**

![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-5b21b6?style=flat-square)
![Version](https://img.shields.io/badge/version-1.0.0-5b21b6?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-5b21b6?style=flat-square)

```bash
claude plugin marketplace add heurema/emporium
claude plugin install herald@emporium
```

</div>

## What it does

Most developer news tools require API keys, cloud accounts, or paid tiers to be useful. Herald fetches RSS feeds and the public HN Algolia API, runs a local scoring pipeline, and writes a ranked top-10 Markdown digest to your machine — no credentials, no network calls to third-party LLMs, no data leaving your box. You configure topics and sources via slash commands; the daily scheduler handles the rest.

## Install

<!-- INSTALL:START — auto-synced from emporium/INSTALL_REFERENCE.md -->
```bash
claude plugin marketplace add heurema/emporium
claude plugin install herald@emporium
```
<!-- INSTALL:END -->

<details>
<summary>Manual install from source</summary>

```bash
git clone https://github.com/heurema/herald
cd herald
pip install -e .
# Copy the plugin manifest into Claude Code's plugin directory
cp -r plugin/ ~/.claude/plugins/herald/
```

Then restart Claude Code and run `/news-init`.

</details>

## Quick start

```
/news-init
/news-digest
```

`/news-init` runs preflight checks, creates a Python venv, installs dependencies, copies the default config, and sets up a daily scheduler. `/news-digest` reads today's digest once the first run completes.

## Commands

| Command | What it does |
|---------|-------------|
| `/news-init` | Interactive setup wizard — pick preset, schedule time, verify |
| `/news-init <topic>` | Add a topic pack (e.g., `rust`, `devops`) to existing setup |
| `/news-add <url>` | Add any URL — auto-discovers RSS feed, suggests name and priority |
| `/news-add <topic>` | Add a built-in topic pack with feeds + keywords |
| `/news-sources` | View all active sources grouped by tier |
| `/news-sources remove <name>` | Remove a source (preset or custom) |
| `/news-sources restore <name>` | Restore a removed preset source |
| `/news-sources export` | Export full config as standalone YAML |
| `/news-sources import <path>` | Import sources from a shared config file |
| `/news-digest` | Read today's digest, grouped by topic |
| `/news-run` | Manually trigger collection + analysis |
| `/news-stop` | Disable scheduler, show cleanup options |

## Features

Herald runs a five-stage local pipeline on every collection cycle:

```
Daily: scheduler → run.sh → collect.py → analyze.py → digest.md
                                ↓
                  20 RSS feeds + HN Algolia API
                                ↓
                  dedup → keyword filter → signal scoring → top 10
```

1. **Collect** — fetches RSS feeds and HN front-page stories via public APIs
2. **Dedup** — 3-layer deduplication (URL hash, normalization, title similarity)
3. **Filter** — keyword matching against your configured topics
4. **Score** — signal scoring based on source weight, points, keyword density, recency
5. **Digest** — top 10 items as a Markdown file, grouped by topic

### Adding sources

The fastest way to add sources — no YAML editing required:

```
/news-add https://simonwillison.net       # auto-discovers RSS feed
/news-add rust                            # adds Rust topic pack (3 feeds + keywords)
/news-init devops                         # adds DevOps topic pack to existing setup
```

Built-in topic packs: `rust`, `devops`, `golang`, `typescript`, `security`, `python`, `data`.

To manage existing sources:

```
/news-sources                             # see all active sources
/news-sources remove "r/MachineLearning"  # remove a source
/news-sources restore "r/MachineLearning" # restore a removed preset source
```

## Configuration

Config lives at `~/.config/herald/config.yaml`. It layers your overrides on top of a preset:

```yaml
version: 1
preset: "ai-engineering"    # base preset
schedule_time: "06:00"
timezone: "local"
max_items: 10

# Add your own feeds
add_feeds:
  - name: "My Blog"
    url: "https://myblog.com/feed"
    tier: 1
    weight: 0.25

# Remove preset feeds you don't want
remove_feeds:
  - "r/MachineLearning"

# Add keyword topics
add_keywords:
  devops:
    - "kubernetes"
    - "terraform"

# Remove keyword topics
remove_keywords:
  - ai_finance
```

The default preset is `ai-engineering` — 20 curated feeds across 5 tiers (HN, newsletters, release feeds, finance, community) and 5 keyword categories. To start from scratch:

```
/news-init --preset blank --time 08:00
```

Then add your own feeds and keywords directly in the config file or via `/news-add`.

### Data paths

```
~/.config/herald/          # config
~/.local/share/herald/     # data + venv
├── .venv/
└── data/
    ├── raw/YYYY-MM-DD.jsonl    # raw items (90-day retention)
    ├── digests/YYYY-MM-DD.md   # daily digests (365-day retention)
    └── state/
        ├── seen_urls.txt       # dedup index (90-day retention)
        ├── last_run.json       # run metadata
        └── collect.log         # run log
```

## Requirements

- Python 3.10+
- macOS or Linux (Windows via WSL)
- Claude Code

## Privacy

Herald makes no calls to paid or authenticated APIs. It fetches only public RSS feeds and the HN Algolia API. All collected data and digests stay on your machine under `~/.local/share/herald/`. No telemetry, no cloud sync.

Optional: a free-tier Tavily search key unlocks richer article previews, but it is not required for core functionality.

## See also

- [skill7.dev](https://skill7.dev) — plugin registry and documentation
- [emporium](https://github.com/heurema/emporium) — heurema plugin marketplace
- [signum](https://github.com/heurema/signum) — risk-adaptive development pipeline with adversarial code review
- [proofpack](https://github.com/heurema/proofpack) — proof-carrying CI gate for AI agent changes

## License

[MIT](LICENSE)
