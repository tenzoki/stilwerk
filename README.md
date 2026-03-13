# Stilwerk

A Claude Code plugin for style analysis, authorship attribution, and text transformation.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Python 3.10+
- Git

## Installation

```bash
git clone git@github.com:tenzoki/stilwerk.git
cd stilwerk
pip install -e .
```

## Setup

### 1. Set Projects Folder

```bash
export STILWERK_PROJECTS=~/Documents/stilwerk-projects
```

Add to `~/.zshrc` or `~/.bashrc` to persist.

### 2. Start Claude Code

```bash
cd stilwerk
claude
```

### 3. Create Your First Project

```
/sw_create my-analysis --profile essay
```

This creates:
```
$STILWERK_PROJECTS/my-analysis/
├── corpus/      # Exemplar texts (for style learning)
├── input/       # Texts to analyze or transform
├── analysis/    # Output reports
└── project.yaml
```

### 4. Add Texts and Work

1. Copy texts to `$STILWERK_PROJECTS/my-analysis/input/`
2. Run commands:

```
/sw_analyze input/my-text.md
/sw_transform input/my-text.md
```

## Commands

| Command | Description |
|---------|-------------|
| `/sw_create <name> [--profile <n>]` | Create new project |
| `/sw_open <name>` | Open existing project |
| `/sw_info` | Show current project and commands |
| `/sw_analyze <file>` | Analyze text (AI detection, style) |
| `/sw_transform <file>` | Transform text to match profile |
| `/sw_learn <corpus-dir> --name <n>` | Learn style profile from corpus |
| `/sw_attribute <file> --corpus <dir>` | Authorship attribution |

### Analysis Protocols

```
/sw_analyze input/text.md --quick      # Core metrics
/sw_analyze input/text.md --standard   # Full analysis (default)
/sw_analyze input/text.md --deep       # Comprehensive
```

### Available Profiles

- `essay` — NYT Magazine narrative style (EN)
- `technical-blog` — Conversational tech blog (EN)
- `technical-blog-de` — Technical blog (DE)
- `base-german` — Base German profile

## Documentation

- `CLAUDE.md` — Agent instructions
- `docs/instruments.md` — Style analysis instruments reference

## License

MIT
