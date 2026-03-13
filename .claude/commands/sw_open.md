---
description: Open an existing stilwerk project
argument-hint: <project-name>
allowed-tools: Bash, Read
---

# Open Project

Set an existing project as the active project for this session.

## Process

1. **Check STILWERK_PROJECTS**
   ```bash
   echo $STILWERK_PROJECTS
   ```
   If not set, error and stop.

2. **Verify project exists**
   ```bash
   ls $STILWERK_PROJECTS/<project-name>/project.yaml
   ```
   If not found, error: "Project not found"

3. **Set active project**
   ```bash
   export STILWERK_PROJECT=<project-name>
   ```

4. **Read and show project info**
   Read `$STILWERK_PROJECTS/<project-name>/project.yaml` and display:
   ```
   Opened project: <project-name>
   Profile: <profile or "not set">
   Language: <language>

   Contents:
   - corpus/: <n> files
   - input/: <n> files
   - analysis/: <n> files
   ```

## Example

```
/sw_open my-essay

Opened project: my-essay
Profile: essay
Language: de

Contents:
- corpus/: 3 files
- input/: 1 file
- analysis/: 0 files
```
