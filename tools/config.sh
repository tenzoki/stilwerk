#!/bin/bash
# config.sh - Load Stilwerk configuration
# Source this file in other scripts: source "$(dirname "$0")/config.sh"

# Find config file (look in script dir, then parent)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STILWERK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Config file location (can be overridden by env var)
CONFIG_FILE="${STILWERK_CONFIG:-$STILWERK_DIR/stilwerk.conf}"

# Default values
CORPUS_DIR="../corpus"
ANALYSIS_DIR="./analysis"

# Load config file if exists
if [ -f "$CONFIG_FILE" ]; then
    # Source only variable assignments (safe parsing)
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ "$key" =~ ^[[:space:]]*# ]] && continue
        [[ -z "$key" ]] && continue

        # Remove leading/trailing whitespace and quotes
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs | sed 's/^["'\'']//;s/["'\'']$//')

        # Export the variable
        case "$key" in
            CORPUS_DIR|ANALYSIS_DIR)
                export "$key=$value"
                ;;
        esac
    done < "$CONFIG_FILE"
fi

# Environment variables override config file
CORPUS_DIR="${STILWERK_CORPUS:-$CORPUS_DIR}"
ANALYSIS_DIR="${STILWERK_ANALYSIS:-$ANALYSIS_DIR}"

# Resolve relative paths (relative to stilwerk.conf location)
resolve_path() {
    local path="$1"
    if [[ "$path" != /* ]]; then
        # Relative path - resolve from STILWERK_DIR
        path="$STILWERK_DIR/$path"
    fi
    # Normalize path
    echo "$(cd "$(dirname "$path")" 2>/dev/null && pwd)/$(basename "$path")"
}

CORPUS_DIR="$(resolve_path "$CORPUS_DIR")"
ANALYSIS_DIR="$(resolve_path "$ANALYSIS_DIR")"

# Export for use in scripts
export CORPUS_DIR ANALYSIS_DIR STILWERK_DIR

# Helper function to resolve corpus file
resolve_corpus_file() {
    local file="$1"

    # If already absolute path and exists, use it
    if [[ "$file" == /* ]] && [ -f "$file" ]; then
        echo "$file"
        return 0
    fi

    # If relative, try relative to current dir first
    if [ -f "$file" ]; then
        echo "$(pwd)/$file"
        return 0
    fi

    # Try in corpus dir
    if [ -f "$CORPUS_DIR/$file" ]; then
        echo "$CORPUS_DIR/$file"
        return 0
    fi

    # Try stripping "corpus/" prefix if present
    local basename="${file#corpus/}"
    if [ -f "$CORPUS_DIR/$basename" ]; then
        echo "$CORPUS_DIR/$basename"
        return 0
    fi

    # Not found
    echo ""
    return 1
}

export -f resolve_corpus_file

# Helper function to get output path for a file
# Creates necessary directories if they don't exist
resolve_output_path() {
    local input_file="$1"
    local suffix="${2:-metrics}"

    # Extract base filename without extension
    local basename=$(basename "$input_file")
    local name="${basename%.*}"

    # Create output directory if needed
    local output_dir="$ANALYSIS_DIR/$name"
    mkdir -p "$output_dir" 2>/dev/null

    echo "$output_dir/${suffix}.txt"
}

export -f resolve_output_path

# Ensure analysis directory exists
ensure_analysis_dir() {
    if [ ! -d "$ANALYSIS_DIR" ]; then
        mkdir -p "$ANALYSIS_DIR"
        echo "Created analysis directory: $ANALYSIS_DIR"
    fi
}

export -f ensure_analysis_dir
