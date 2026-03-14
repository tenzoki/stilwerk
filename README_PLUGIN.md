# Plugin Migration Notes

This document describes the changes made to convert Stilwerk from a local `.claude/commands` project into a distributable Claude Code plugin.

## What Changed

### Directory Structure

| Before | After | Why |
|--------|-------|-----|
| `.claude/commands/sw_*.md` | `skills/<name>/SKILL.md` | Plugin skill discovery requires `skills/<name>/SKILL.md` layout; `sw_` prefix dropped since skills are namespaced under `stilwerk:` |
| `.claude/settings.json` | `settings.json` (root) | Plugin settings must be at the repository root |
| — | `.claude-plugin/plugin.json` | Required manifest for plugin identity and marketplace metadata |
| `stilwerk` (starter script) | removed | Contained a hardcoded personal path; not needed for plugin distribution |
| `stilwerk.conf` | removed | Replaced by XDG-compliant user config at `~/.config/stilwerk/config.yaml` |

### No More Central Project Directory

The old model required `$STILWERK_PROJECTS` and `/sw_create` / `/sw_open` to set up a project before doing anything. The new model works on any file directly:

```
# Old — required project setup first
export STILWERK_PROJECTS=~/Documents/stilwerk-projects
/sw_create my-essay --profile essay
/sw_analyze input/draft.md

# New — just point at a file
/stilwerk:analyze draft.md
/stilwerk:transform draft.md --profile essay
```

User data follows the XDG Base Directory Specification:
- `~/.config/stilwerk/` — user configuration
- `~/.local/share/stilwerk/profiles/` — user-created profiles
- `~/.local/share/stilwerk/corpus/` — corpora for attribution

### Command Namespacing

All slash commands are namespaced under the plugin name, with the `sw_` prefix removed:

```
/sw_analyze   →  /stilwerk:analyze
/sw_transform →  /stilwerk:transform
/sw_learn     →  /stilwerk:learn
/sw_attribute →  /stilwerk:attribute
/sw_info      →  /stilwerk:info
/sw_create    →  removed (no longer needed)
/sw_open      →  removed (no longer needed)
```

### Skill Frontmatter

Commands used `description`, `argument-hint`, and `allowed-tools`. Skills use `name` and `description`, with `$ARGUMENTS` in the body for parameter passing.

Before (`.claude/commands/sw_analyze.md`):
```yaml
---
description: Analyze text style
argument-hint: <file> [--quick|--standard|--deep]
allowed-tools: Bash, Read, Write, Glob
---
```

After (`skills/analyze/SKILL.md`):
```yaml
---
name: analyze
description: Analyze text style for AI detection, rhetoric, and provenance. Use when the user wants to analyze a text's writing style or check if text is AI-generated.
---
```

### Plugin Manifest

`.claude-plugin/plugin.json` provides the metadata needed for marketplace listing:

```json
{
  "name": "stilwerk",
  "version": "0.2.0",
  "description": "Style analysis, authorship attribution, and text transformation toolkit",
  "author": { "name": "kai" },
  "license": "MIT",
  "keywords": ["style", "analysis", "stylometry", "authorship", "attribution", "transformation", "writing"]
}
```

## Installation

### Local

```bash
claude plugin add /path/to/stilwerk
```

### From a Marketplace

```bash
/plugin install stilwerk@<marketplace-name>
```

## Verification

After installing, run `/stilwerk:info` to confirm the plugin is loaded and all commands are available.
