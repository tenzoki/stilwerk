---
name: learn
description: Learn a style profile from exemplar texts. Use when the user wants to create a custom style profile from sample writings.
---

# Learn Style Profile

Learn a style profile from a collection of exemplar texts.

## Arguments

$ARGUMENTS should be: `<corpus-dir> --name <profile-name>`

`<corpus-dir>` is any directory containing exemplar texts — absolute or relative path.

## Process

1. **Validate inputs**
   - `<corpus-dir>` must exist and contain text files
   - `--name` is required

2. **Ensure user profile directory exists**
   ```bash
   mkdir -p ~/.local/share/stilwerk/profiles
   ```

3. **Run style learning**
   ```bash
   stilwerk learn <corpus-dir> \
     --name <profile-name> \
     --output ~/.local/share/stilwerk/profiles/<profile-name>.yaml
   ```

4. **Show learned metrics**
   - Sentence variance range
   - Type-token ratio range
   - First-person rate range
   - Number of texts analyzed

5. **Confirm**
   ```
   Profile saved: ~/.local/share/stilwerk/profiles/<profile-name>.yaml
   Use with: /stilwerk:transform <file> --profile <profile-name>
   ```

## Example

```
/stilwerk:learn ~/writing/essays --name my-style

Learning from: ~/writing/essays/
Analyzed 12 texts.

Learned metrics:
- Sentence variance: (9.5, 16.2)
- Type-token ratio: (0.58, 0.71)
- First-person rate: (3.1, 7.8)

Profile saved: ~/.local/share/stilwerk/profiles/my-style.yaml
Use with: /stilwerk:transform <file> --profile my-style
```
