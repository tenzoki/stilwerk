# Stilwerk

A Claude Code plugin for style analysis, authorship attribution, and text transformation.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Python 3.10+
- Git

## Installation

```bash
# Clone the repository
git clone git@github.com:tenzoki/stilwerk.git
cd stilwerk

# Install Python dependencies
pip install -e stilwerk/
```

## Setup

### 1. Set Projects Folder

```bash
export STILWERK_PROJECTS=~/Documents/stilwerk-projects
```

Add to your shell profile (`~/.zshrc` or `~/.bashrc`) to persist.

### 2. Create Your First Project

```bash
cd stilwerk
claude
```

Then in Claude Code:
```
/project-init my-first-analysis
```

This creates:
```
$STILWERK_PROJECTS/my-first-analysis/
├── corpus/      # Exemplar texts (for style learning)
├── input/       # Texts to analyze or transform
├── analysis/    # Output reports
└── project.yaml # Project config
```

### 3. Add Texts and Analyze

1. Copy texts to analyze into `input/`
2. Copy exemplar texts (if learning styles) into `corpus/`
3. Run commands:

```
/analyze input/my-text.md
/transform input/my-text.md --profile technical-blog
```

## Commands

| Command | Description |
|---------|-------------|
| `/project-init <name>` | Create new project |
| `/analyze <file>` | Analyze text (AI detection, rhetoric, style) |
| `/transform <file> --profile <name>` | Transform text to match profile |
| `/learn <corpus-dir> --name <name>` | Learn style profile from corpus |
| `/attribute <file> --corpus <dir>` | Authorship attribution |

### Analysis Protocols

```
/analyze input/text.md --quick      # 5 min: core metrics
/analyze input/text.md --standard   # 15 min: full analysis (default)
/analyze input/text.md --deep       # 45+ min: comprehensive
```

### Available Profiles

- `technical-blog` — Conversational tech blog (EN)
- `technical-blog-de` — Technical blog (DE)
- `base-german` — Base German profile

## Configuration

`stilwerk.conf`:
```ini
CORPUS_DIR="corpus"
ANALYSIS_DIR="analysis"
INPUT_DIR="input"
DEFAULT_LANGUAGE="de"
FIT_THRESHOLD=0.85
```

## Documentation

- `CLAUDE.md` — Agent instructions (what stilwerk can do)
- `docs/instruments.md` — Style analysis instruments reference

## License

MIT
