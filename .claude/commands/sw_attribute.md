---
description: Attribute authorship of a text
argument-hint: <file> --corpus <corpus-subdir>
allowed-tools: Bash, Read
---

# Authorship Attribution

Determine the likely author of a text by comparing against a corpus of known authors.

**Requires active project.** Paths are relative to `$STILWERK_PROJECTS/$STILWERK_PROJECT`.

## Corpus Structure

The corpus subdirectory should have one folder per author:
```
corpus/<subdir>/
├── author1/
│   ├── text1.txt
│   └── text2.txt
├── author2/
│   └── text1.txt
└── author3/
    └── text1.txt
```

## Process

1. **Check active project**
   ```bash
   echo $STILWERK_PROJECT
   ```
   If not set, error: "No active project. Run /sw_open or /sw_create first."

2. **Validate inputs**
   - Query file must exist: `$STILWERK_PROJECTS/$STILWERK_PROJECT/<file>`
   - Corpus must exist: `$STILWERK_PROJECTS/$STILWERK_PROJECT/corpus/<subdir>`

3. **Run attribution**
   ```bash
   stilwerk attribute \
     $STILWERK_PROJECTS/$STILWERK_PROJECT/<file> \
     --corpus $STILWERK_PROJECTS/$STILWERK_PROJECT/corpus/<subdir> \
     --n-features 100 --json
   ```

4. **Display results**
   - Most likely author
   - Distance score (lower = more similar)
   - Nearest neighbors ranked

## Example

```
/sw_attribute input/mystery.txt --corpus authors

Analyzing: input/mystery.txt
Comparing against: corpus/authors/ (3 authors, 25 texts)

Attribution result:
  Most likely author: hamilton
  Distance: 0.423

Nearest neighbors:
  1. hamilton/fed51.txt: 0.423
  2. hamilton/fed72.txt: 0.445
  3. madison/fed10.txt: 0.512

Confidence: HIGH
```
