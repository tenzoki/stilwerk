---
description: Show current project and available commands
argument-hint:
allowed-tools: Bash, Read
---

# Stilwerk Info

Show current project status and list all available commands.

## Process

1. **Show current project**
   ```bash
   echo "Projects folder: $STILWERK_PROJECTS"
   echo "Active project: $STILWERK_PROJECT"
   ```

   If `STILWERK_PROJECT` is set, also show:
   - Full path: `$STILWERK_PROJECTS/$STILWERK_PROJECT`
   - Profile (from project.yaml)
   - File counts in corpus/, input/, analysis/

2. **List all commands**

## Output Format

```
Current project: <name> in: <path>
Profile: <profile>

Commands:
  /sw_create <name> [--profile <name>]   Create new project
  /sw_open <name>                        Open existing project
  /sw_info                               Show this info
  /sw_analyze <file> [--quick|--deep]    Analyze text style
  /sw_transform <file> [--profile <name>] Transform to match profile
  /sw_learn <corpus-subdir> --name <n>   Learn profile from corpus
  /sw_attribute <file> --corpus <dir>    Authorship attribution

Paths are relative to: $STILWERK_PROJECTS/$STILWERK_PROJECT
  input/<file>     → texts to analyze/transform
  corpus/<dir>     → exemplar texts for learning
  analysis/<file>  → output reports

Available profiles: essay, technical-blog, technical-blog-de, base-german
```

## Example

```
/sw_info

Current project: my-essay in: ~/Documents/stilwerk-projects/my-essay
Profile: essay

Commands:
  /sw_create <name> [--profile <name>]   Create new project
  /sw_open <name>                        Open existing project
  /sw_info                               Show this info
  /sw_analyze <file> [--quick|--deep]    Analyze text style
  /sw_transform <file> [--profile <name>] Transform to match profile
  /sw_learn <corpus-subdir> --name <n>   Learn profile from corpus
  /sw_attribute <file> --corpus <dir>    Authorship attribution

Paths are relative to: ~/Documents/stilwerk-projects/my-essay
  input/<file>     → texts to analyze/transform
  corpus/<dir>     → exemplar texts for learning
  analysis/<file>  → output reports

Available profiles: essay, technical-blog, technical-blog-de, base-german
```
