---
name: transform
description: Transform text to match a style profile. Use when the user wants to rewrite or adapt text to match a specific writing style.
---

# Transform Text

Transform a text to match a target style profile.

## Arguments

$ARGUMENTS should be: `<file> [--profile <name>]`

`<file>` is any path — absolute or relative to the current working directory.

## Profile Resolution

1. If `--profile` is provided, use that
2. If a `.stilwerk.yaml` exists in the file's directory, use its `profile` field
3. If `~/.config/stilwerk/config.yaml` has a default profile, use that
4. Otherwise error: "No profile specified. Use --profile <name>"

Profiles are loaded from (in order):
- `${CLAUDE_PLUGIN_ROOT}/profiles/` (built-in)
- `~/.local/share/stilwerk/profiles/` (user-created)

## Workflow

```
COMPARE → INSTRUCT → TRANSFORM → VERIFY → (iterate until fit > threshold)
```

## Process

1. **Read the text**
   ```bash
   cat <file>
   ```

2. **Load profile** from resolved location

3. **Compare against profile**
   ```bash
   stilwerk compare <file> --profile <name>
   ```

4. **Generate and apply transformations**
   - Remove blacklisted phrases
   - Adjust sentence variance
   - Add contractions where natural
   - Adjust voice/perspective as needed

5. **Verify result**
   ```bash
   stilwerk verify <file> --profile <name>
   ```

6. **Iterate** until `overall_fit >= threshold` (max 5 iterations)

7. **Save result** to `<file-stem>-transformed.md` next to the input file

## Available Built-in Profiles

- `essay` — NYT Magazine narrative style (EN)
- `technical-blog` — Conversational tech blog (EN)
- `technical-blog-de` — Technical blog (DE)
- `base-german` — Base German profile

## Example

```
/stilwerk:transform draft.md --profile essay

Using profile: essay
Transforming: draft.md

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

Saved: draft-transformed.md
```
