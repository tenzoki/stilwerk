---
name: analyze
description: Analyze text style for AI detection, rhetoric, and provenance. Use when the user wants to analyze a text's writing style or check if text is AI-generated.
---

# Analyze Text

Analyze a text for style characteristics: AI detection, rhetoric, provenance.

## Arguments

$ARGUMENTS should be: `<file> [--quick|--standard|--deep]`

`<file>` is any path — absolute or relative to the current working directory.

## Process

1. **Read the text**
   ```bash
   cat <file>
   ```

2. **Run metrics**
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/tools/metrics.sh <file>
   ```

3. **Apply instruments** (based on protocol)

   `--quick`: U01, S01, S02, A01
   `--standard` (default): All metrics + A01-A03, V01-V05, C01-C03
   `--deep`: Full battery + synthesis

4. **Interpret signals**

   | Metric | AI Signal | Human Signal |
   |--------|-----------|--------------|
   | Sentence variance | < 5 | > 10 |
   | Transition density | > 0.7 | < 0.3 |
   | Contraction rate | < 0.2 | > 0.5 |
   | First-person rate | < 1/1000 | > 5/1000 |

5. **Output report**
   Display the analysis inline. Optionally save to `<file>.analysis.yaml` next to the input file.

## Example

```
/stilwerk:analyze draft.md

Analyzing: draft.md

Metrics:
- Sentence variance: 12.3 (human signal)
- Transition density: 0.45 (neutral)
- Contraction rate: 0.38 (human signal)
- First-person rate: 4.2/1000 (human signal)

Assessment: LIKELY_HUMAN
Confidence: 0.78
```
