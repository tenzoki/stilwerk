---
name: info
description: Show stilwerk configuration, available profiles, and commands. Use when the user wants help with available stilwerk commands or wants to see their setup.
---

# Stilwerk Info

Show configuration and available commands.

## Process

1. **Show configuration**
   - Check for user config at `~/.config/stilwerk/config.yaml`
   - List built-in profiles from `${CLAUDE_PLUGIN_ROOT}/profiles/`
   - List user profiles from `~/.local/share/stilwerk/profiles/`
   - List corpora from `~/.local/share/stilwerk/corpus/`

2. **List all commands**

## Output Format

```
Stilwerk — Style Analysis Plugin

Configuration:
  User config: ~/.config/stilwerk/config.yaml (found / not found)
  User data:   ~/.local/share/stilwerk/

Built-in profiles: essay, technical-blog, technical-blog-de, base-german
User profiles:     <list or "none">
Corpora:           <list or "none">

Commands:
  /stilwerk:info                                Show this info
  /stilwerk:analyze <file> [--quick|--deep]     Analyze text style
  /stilwerk:transform <file> [--profile <name>] Transform to match profile
  /stilwerk:learn <corpus-dir> --name <n>       Learn profile from exemplars
  /stilwerk:attribute <file> --corpus <dir>     Authorship attribution
```
