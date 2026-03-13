---
description: Learn style profile from corpus
argument-hint: <corpus-subdir> --name <profile-name>
allowed-tools: Bash, Read, Write
---

# Learn Style Profile

Learn a style profile from exemplar texts in the corpus.

**Requires active project.** Corpus path is relative to `$STILWERK_PROJECTS/$STILWERK_PROJECT/corpus/`.

## Process

1. **Check active project**
   ```bash
   echo $STILWERK_PROJECT
   ```
   If not set, error: "No active project. Run /sw_open or /sw_create first."

2. **Validate inputs**
   - Corpus subdirectory must exist
   - Profile name required (`--name`)

3. **Run style learning**
   ```bash
   stilwerk learn \
     $STILWERK_PROJECTS/$STILWERK_PROJECT/corpus/<subdir> \
     --name <profile-name> \
     --output stilwerk/profiles/<profile-name>.yaml
   ```

4. **Show learned metrics**
   - Sentence variance range
   - Type-token ratio range
   - First-person rate range
   - Number of texts analyzed

5. **Confirm**
   ```
   Profile saved: stilwerk/profiles/<profile-name>.yaml
   Use with: /sw_transform <file> --profile <profile-name>
   ```

## Example

```
/sw_learn essays --name my-style

Learning from: ~/Documents/stilwerk-projects/my-essay/corpus/essays/
Analyzed 12 texts.

Learned metrics:
- Sentence variance: (9.5, 16.2)
- Type-token ratio: (0.58, 0.71)
- First-person rate: (3.1, 7.8)

Profile saved: stilwerk/profiles/my-style.yaml
Use with: /sw_transform <file> --profile my-style
```
