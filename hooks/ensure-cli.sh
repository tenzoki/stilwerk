#!/bin/bash
# Ensures the stilwerk Python CLI is installed

# Check if stilwerk command exists
if command -v stilwerk &> /dev/null; then
    exit 0
fi

# Get plugin root from environment or derive from script location
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(realpath "$0")")")}"

# Try to install
if [ -f "$PLUGIN_ROOT/pyproject.toml" ]; then
    pip install -q "$PLUGIN_ROOT" 2>/dev/null || pip install --user -q "$PLUGIN_ROOT" 2>/dev/null
fi

exit 0
