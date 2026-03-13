# Stilwerk - Style Analysis Plugin

A Claude Code plugin for style analysis, authorship attribution, and text transformation.

## Setup

### 1. Set Projects Folder (once)

```bash
export STILWERK_PROJECTS=~/Documents/stilwerk-projects
```

Add to `~/.zshrc` or `~/.bashrc` to persist.

### 2. Create or Open a Project

```
/sw_create my-essay --profile essay
```

or

```
/sw_open my-essay
```

### 3. Work with Your Project

```
/sw_analyze input/draft.md
/sw_transform input/draft.md
/sw_info
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/sw_create <name> [--profile <n>]` | Create new project |
| `/sw_open <name>` | Open existing project |
| `/sw_info` | Show current project and commands |
| `/sw_analyze <file> [--quick\|--deep]` | Analyze text style |
| `/sw_transform <file> [--profile <n>]` | Transform to match profile |
| `/sw_learn <corpus-subdir> --name <n>` | Learn profile from corpus |
| `/sw_attribute <file> --corpus <dir>` | Authorship attribution |

All paths are relative to `$STILWERK_PROJECTS/$STILWERK_PROJECT`:
- `input/<file>` — texts to analyze/transform
- `corpus/<dir>` — exemplar texts
- `analysis/<file>` — output reports

---

## Available Profiles

- `essay` — NYT Magazine narrative style (EN)
- `technical-blog` — Conversational tech blog (EN)
- `technical-blog-de` — Technical blog (DE)
- `base-german` — Base German profile

---

## Project Structure

```
$STILWERK_PROJECTS/<project>/
├── corpus/      # Exemplar texts (for learning/attribution)
├── input/       # Texts to analyze or transform
├── analysis/    # Output reports
└── project.yaml # Project config (name, profile, settings)
```

---

## AI Detection Signals

| Metric | AI Signal | Human Signal |
|--------|-----------|--------------|
| Sentence variance | < 5 | > 10 |
| Transition density | > 0.7 | < 0.3 |
| Contraction rate | < 0.2 | > 0.5 |
| First-person rate | < 1/1000 | > 5/1000 |

---

## CLI Tools

From stilwerk repo root:

```bash
# Profiles
PYTHONPATH=. python -m stilwerk.src.cli profile list
PYTHONPATH=. python -m stilwerk.src.cli profile show <name>

# Shell metrics
cd stilwerk && ./tools/metrics.sh <file>
```

---

## References

- `./docs/instruments.md` — Style analysis instruments
- `./profiles/` — Style profile definitions
