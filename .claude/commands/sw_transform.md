---
description: Transform text to match a style profile
argument-hint: <file> [--profile <name>]
allowed-tools: Bash, Read, Write, Edit, Glob
---

# Transform Text

Transform a text to match a target style profile.

**Requires active project.** File path is relative to `$STILWERK_PROJECTS/$STILWERK_PROJECT`.

## Workflow

```
COMPARE → INSTRUCT → TRANSFORM → VERIFY → (iterate until fit > threshold)
```

## Process

1. **Check active project**
   ```bash
   echo $STILWERK_PROJECT
   ```
   If not set, error: "No active project. Run /sw_open or /sw_create first."

2. **Resolve profile**
   - If `--profile` provided, use that
   - Else read `$STILWERK_PROJECTS/$STILWERK_PROJECT/project.yaml` for default profile
   - If no profile found, error: "No profile specified"

3. **Load text**
   ```bash
   cat $STILWERK_PROJECTS/$STILWERK_PROJECT/<file>
   ```

4. **Compare against profile**
   ```bash
   stilwerk compare \
     $STILWERK_PROJECTS/$STILWERK_PROJECT/<file> --profile <name>
   ```

5. **Generate and apply transformations**
   - Remove blacklisted phrases
   - Adjust sentence variance
   - Add contractions where natural
   - Adjust voice/perspective as needed

6. **Verify result**
   ```bash
   stilwerk verify \
     $STILWERK_PROJECTS/$STILWERK_PROJECT/<file> --profile <name>
   ```

7. **Iterate** until `overall_fit >= threshold` (max 5 iterations)

8. **Save result**
   Save to `$STILWERK_PROJECTS/$STILWERK_PROJECT/analysis/<filename>-transformed.md`

## Available Profiles

- `essay` — NYT Magazine narrative style (EN)
- `technical-blog` — Conversational tech blog (EN)
- `technical-blog-de` — Technical blog (DE)
- `base-german` — Base German profile

## Example

```
/sw_transform input/draft.md

Using profile: essay (from project.yaml)
Transforming: ~/Documents/stilwerk-projects/my-essay/input/draft.md

Iteration 1:
- Fit: 0.42
- Removing: "Furthermore", "It's important to note"
- Adding scene-driven opening
- Varying sentence lengths

Iteration 2:
- Fit: 0.81
- Adding specific details
- Reducing passive voice

Iteration 3:
- Fit: 0.86 ✓ (threshold: 0.80)

Saved: analysis/draft-transformed.md
```
