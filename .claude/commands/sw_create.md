---
description: Create a new stilwerk project
argument-hint: <project-name> [--profile <name>]
allowed-tools: Bash, Read, Write
---

# Create Project

Create a new stilwerk project and set it as the active project.

## Prerequisites

`STILWERK_PROJECTS` must be set:
```bash
export STILWERK_PROJECTS=~/Documents/stilwerk-projects
```

## Process

1. **Check STILWERK_PROJECTS**
   ```bash
   echo $STILWERK_PROJECTS
   ```
   If not set, error and stop.

2. **Create project structure**
   ```bash
   mkdir -p $STILWERK_PROJECTS/<project-name>/corpus
   mkdir -p $STILWERK_PROJECTS/<project-name>/input
   mkdir -p $STILWERK_PROJECTS/<project-name>/analysis
   touch $STILWERK_PROJECTS/<project-name>/corpus/.gitkeep
   touch $STILWERK_PROJECTS/<project-name>/input/.gitkeep
   touch $STILWERK_PROJECTS/<project-name>/analysis/.gitkeep
   ```

3. **Create project.yaml**
   ```yaml
   name: "<project-name>"
   created: "<ISO-date>"
   language: "de"
   profile: "<profile-name>"  # only if --profile provided

   features:
     method: "mfw"
     mfw_count: 100

   distance:
     measure: "burrows_delta"
     normalize: true

   clustering:
     method: "ward"
   ```

4. **Set active project**
   ```bash
   export STILWERK_PROJECT=<project-name>
   ```

5. **Confirm**
   ```
   Created project: <project-name>
   Location: $STILWERK_PROJECTS/<project-name>

   Active project set. Run /sw_info to see available commands.
   ```

## Example

```
/sw_create my-essay --profile essay

Created project: my-essay
Location: ~/Documents/stilwerk-projects/my-essay
Active project set. Run /sw_info to see available commands.
```
