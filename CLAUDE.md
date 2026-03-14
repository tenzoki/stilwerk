# Stilwerk - Style Analysis Plugin

A Claude Code plugin for style analysis, authorship attribution, and text transformation.

## Setup

### 1. Install the Plugin

```bash
claude plugin add /path/to/stilwerk
```

### 2. (Optional) Create User Config

```bash
mkdir -p ~/.config/stilwerk
cat > ~/.config/stilwerk/config.yaml <<EOF
language: de
default_profile: essay
EOF
```

### 3. Use It on Any File

```
/stilwerk:analyze draft.md
/stilwerk:transform draft.md --profile essay
/stilwerk:info
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/stilwerk:info` | Show config, profiles, and commands |
| `/stilwerk:analyze <file> [--quick\|--deep]` | Analyze text style |
| `/stilwerk:transform <file> [--profile <n>]` | Transform to match profile |
| `/stilwerk:learn <corpus-dir> --name <n>` | Learn profile from exemplars |
| `/stilwerk:attribute <file> --corpus <dir>` | Authorship attribution |

---

## Available Profiles

- `essay` — NYT Magazine narrative style (EN)
- `technical-blog` — Conversational tech blog (EN)
- `technical-blog-de` — Technical blog (DE)
- `base-german` — Base German profile

User-created profiles are stored in `~/.local/share/stilwerk/profiles/`.

---

## File Locations (XDG)

| What | Where |
|------|-------|
| Built-in profiles | `${CLAUDE_PLUGIN_ROOT}/profiles/` |
| User profiles | `~/.local/share/stilwerk/profiles/` |
| User corpora | `~/.local/share/stilwerk/corpus/` |
| User config | `~/.config/stilwerk/config.yaml` |

---

## AI Detection Signals

| Metric | AI Signal | Human Signal |
|--------|-----------|--------------|
| Sentence variance | < 5 | > 10 |
| Transition density | > 0.7 | < 0.3 |
| Contraction rate | < 0.2 | > 0.5 |
| First-person rate | < 1/1000 | > 5/1000 |

---

## References

- `./docs/instruments.md` — Style analysis instruments
- `./profiles/` — Style profile definitions
