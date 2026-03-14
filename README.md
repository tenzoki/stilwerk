# Stilwerk

A Claude Code plugin for style analysis, authorship attribution, and text transformation.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Python 3.10+ (for CLI tools)

## Installation

### From a marketplace

```bash
/plugin install stilwerk@<marketplace-name>
```

### Local development

```bash
claude plugin add /path/to/stilwerk
```

### Python dependencies (for CLI tools)

```bash
pip install -e /path/to/stilwerk
```

## Quick Start

```
/stilwerk:analyze draft.md
/stilwerk:transform draft.md --profile essay
```

No project setup required — just point it at any file.

## Commands

| Command | Description |
|---------|-------------|
| `/stilwerk:info` | Show config, profiles, and commands |
| `/stilwerk:analyze <file>` | Analyze text (AI detection, style) |
| `/stilwerk:transform <file>` | Transform text to match profile |
| `/stilwerk:learn <corpus-dir> --name <n>` | Learn style profile from exemplars |
| `/stilwerk:attribute <file> --corpus <dir>` | Authorship attribution |

### Analysis Protocols

```
/stilwerk:analyze text.md --quick      # Core metrics
/stilwerk:analyze text.md --standard   # Full analysis (default)
/stilwerk:analyze text.md --deep       # Comprehensive
```

### Available Profiles

- `essay` — NYT Magazine narrative style (EN)
- `technical-blog` — Conversational tech blog (EN)
- `technical-blog-de` — Technical blog (DE)
- `base-german` — Base German profile

## Configuration (Optional)

Stilwerk follows the XDG Base Directory Specification:

| What | Where |
|------|-------|
| User config | `~/.config/stilwerk/config.yaml` |
| User profiles | `~/.local/share/stilwerk/profiles/` |
| User corpora | `~/.local/share/stilwerk/corpus/` |

Example config:
```yaml
language: de
default_profile: essay
```

## Plugin Structure

```
stilwerk/
├── .claude-plugin/
│   └── plugin.json        # Plugin manifest
├── skills/                # Plugin skills (slash commands)
│   ├── analyze/
│   ├── attribute/
│   ├── info/
│   ├── learn/
│   └── transform/
├── profiles/              # Built-in style profiles
├── docs/                  # Documentation
├── src/                   # Python CLI tools
├── tools/                 # Shell metric scripts
└── settings.json          # Default permissions
```

## Documentation

- `CLAUDE.md` — Agent instructions
- `docs/instruments.md` — Style analysis instruments reference

## License

MIT
