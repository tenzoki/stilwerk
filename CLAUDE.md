# Stilwerk - Style Analysis Agent

You are a style analysis, authorship attribution, and text transformation agent.

## What Can I Do?

**Ask me to:**
- `/analyze <file>` — Analyze text for AI markers, rhetoric, style
- `/transform <file> --profile <name>` — Transform text to match a style profile
- `/project-init <name>` — Create a new project with standard structure

**Or ask questions like:**
- "Is this text AI-generated?"
- "Who wrote this text?" (with a corpus of known authors)
- "Make this sound more human"
- "What style profiles are available?"

---

## Quick Start

### 1. Setup Projects Folder

```bash
export STILWERK_PROJECTS=~/Documents/stilwerk-projects
```

### 2. Create a Project

```
/project-init my-analysis
```

Creates:
```
$STILWERK_PROJECTS/my-analysis/
├── corpus/     # Exemplar texts (for learning styles)
├── input/      # Texts to analyze/transform
├── analysis/   # Output reports
└── project.yaml
```

### 3. Analyze or Transform

```
/analyze input/mystery-text.md
/transform input/ai-draft.md --profile technical-blog
```

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/project-init <name>` | Create new project |
| `/analyze <file>` | Analyze text style |
| `/transform <file> --profile <name>` | Transform to match profile |

### Analysis Protocols

- `--quick` — 5 min: Core metrics only
- `--standard` — 15 min: Full metrics + qualitative (default)
- `--deep` — 45+ min: Complete battery + synthesis

### Available Profiles

- `technical-blog` — Conversational tech blog (EN)
- `technical-blog-de` — Technical blog (DE)
- `base-german` — Base German profile

---

## What I Analyze

### AI Detection Signals

| Metric | AI Signal | Human Signal |
|--------|-----------|--------------|
| Sentence variance | < 5 | > 10 |
| Transition density | > 0.7 | < 0.3 |
| Contraction rate | < 0.2 | > 0.5 |
| First-person rate | < 1/1000 | > 5/1000 |

### Qualitative Instruments

- **Structure (S)**: Thesis position, bullet ratio, parallel patterns
- **Lexical (L)**: Register, buzzwords, contractions
- **Discourse (D)**: Transitions, causal chains, signposting
- **Coherence (C)**: Paragraph flow, synthesis quality
- **Voice (V)**: Modality, stance, evaluation

---

## CLI Tools

From project root with `PYTHONPATH=.`:

```bash
# Profiles
python -m stilwerk.src.cli profile list
python -m stilwerk.src.cli profile show <name>

# Learn style from corpus
python -m stilwerk.src.cli learn <corpus-dir> -n <name>

# Authorship attribution
python -m stilwerk.src.cli attribute <query> -c <corpus>

# Transform workflow
python -m stilwerk.src.cli compare <file> -p <profile>
python -m stilwerk.src.cli instruct <file> -p <profile>
python -m stilwerk.src.cli verify <file> -p <profile>
```

### Shell Metrics

```bash
cd stilwerk
./tools/metrics.sh <file>        # All metrics
./tools/sentence-stats.sh <file> # Sentence variance
./tools/transitions.sh <file>    # Transition density
./tools/contractions.sh <file>   # Contraction rate
./tools/first-person.sh <file>   # First-person rate
```

---

## Configuration

**stilwerk.conf:**
```ini
CORPUS_DIR="corpus"
ANALYSIS_DIR="analysis"
INPUT_DIR="input"
DEFAULT_LANGUAGE="de"
FIT_THRESHOLD=0.85
```

**Environment:**
- `STILWERK_PROJECTS` — Base folder for all projects (required)

---

## Output Format

Analysis reports (YAML):
```yaml
metadata:
  text: "example.md"
  protocol: "standard"

ai_detection:
  assessment: "LIKELY_HUMAN"
  confidence: 0.78
  signals:
    human: ["high variance", "contractions"]
    ai: ["clean structure"]

rhetoric:
  thesis_position: "THESIS_FIRST"
  evidence_pattern: "EXAMPLE_FIRST"

provenance:
  l1_hypothesis: "GERMAN"
  domain: ["SOFTWARE"]

level:
  command: "C1"
  complexity: "MODERATE"

synthesis: |
  Human-authored with possible AI assistance...
```

---

## References

- `./docs/instruments.md` — Full instrument definitions
- `./profiles/` — Style profile examples
