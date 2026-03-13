---
description: Analyze text style
argument-hint: <file> [--quick|--standard|--deep]
allowed-tools: Bash, Read, Write, Glob
---

# Analyze Text

Analyze a text for style characteristics: AI detection, rhetoric, provenance.

**Requires active project.** File path is relative to `$STILWERK_PROJECTS/$STILWERK_PROJECT`.

## Process

1. **Check active project**
   ```bash
   echo $STILWERK_PROJECT
   ```
   If not set, error: "No active project. Run /sw_open or /sw_create first."

2. **Locate text**
   ```bash
   cat $STILWERK_PROJECTS/$STILWERK_PROJECT/<file>
   ```
   Typically: `input/<filename>`

3. **Run metrics**
   ```bash
   cd stilwerk && ./tools/metrics.sh $STILWERK_PROJECTS/$STILWERK_PROJECT/<file>
   ```

4. **Apply instruments** (based on protocol)

   `--quick`: U01, S01, S02, A01
   `--standard` (default): All metrics + A01-A03, V01-V05, C01-C03
   `--deep`: Full battery + synthesis

5. **Interpret signals**

   | Metric | AI Signal | Human Signal |
   |--------|-----------|--------------|
   | Sentence variance | < 5 | > 10 |
   | Transition density | > 0.7 | < 0.3 |
   | Contraction rate | < 0.2 | > 0.5 |
   | First-person rate | < 1/1000 | > 5/1000 |

6. **Write report**
   Save to `$STILWERK_PROJECTS/$STILWERK_PROJECT/analysis/<filename>.yaml`

## Example

```
/sw_analyze input/draft.md

Analyzing: ~/Documents/stilwerk-projects/my-essay/input/draft.md

Metrics:
- Sentence variance: 12.3 (human signal)
- Transition density: 0.45 (neutral)
- Contraction rate: 0.38 (human signal)
- First-person rate: 4.2/1000 (human signal)

Assessment: LIKELY_HUMAN
Confidence: 0.78

Report saved: analysis/draft.yaml
```
