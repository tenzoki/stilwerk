#!/bin/bash
# metrics.sh - Alle automatisierten Metriken
# Usage: ./metrics.sh <file> [-o|--output] [-q|--quiet]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# Parse arguments
OUTPUT_TO_FILE=false
QUIET_MODE=false
INPUT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_TO_FILE=true
            shift
            ;;
        -q|--quiet)
            QUIET_MODE=true
            shift
            ;;
        -h|--help)
            echo "Usage: ./metrics.sh <file> [options]"
            echo ""
            echo "Options:"
            echo "  -o, --output   Write results to ANALYSIS_DIR/<filename>/metrics.txt"
            echo "  -q, --quiet    Suppress console output (use with -o)"
            echo "  -h, --help     Show this help"
            echo ""
            echo "Examples:"
            echo "  ./metrics.sh the-makers-paradox.md           # output to console"
            echo "  ./metrics.sh the-makers-paradox.md -o        # output to file"
            echo "  ./metrics.sh the-makers-paradox.md -o -q     # file only, no console"
            echo ""
            echo "Configuration:"
            echo "  CORPUS_DIR:   $CORPUS_DIR"
            echo "  ANALYSIS_DIR: $ANALYSIS_DIR"
            exit 0
            ;;
        *)
            INPUT="$1"
            shift
            ;;
    esac
done

if [ -z "$INPUT" ]; then
    echo "Usage: ./metrics.sh <file> [options]"
    echo ""
    echo "Examples:"
    echo "  ./metrics.sh the-makers-paradox.md        # looks in CORPUS_DIR"
    echo "  ./metrics.sh /absolute/path/to/file.md   # absolute path"
    echo "  ./metrics.sh file.md -o                  # write to ANALYSIS_DIR"
    echo ""
    echo "Current CORPUS_DIR: $CORPUS_DIR"
    echo "Current ANALYSIS_DIR: $ANALYSIS_DIR"
    echo ""
    echo "Use -h for more options."
    exit 1
fi

# Resolve the file path
FILE=$(resolve_corpus_file "$INPUT")

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    echo "Error: File not found: $INPUT"
    echo "Searched in:"
    echo "  - Current directory"
    echo "  - $CORPUS_DIR"
    exit 1
fi

# Prepare output destination
OUTPUT_FILE=""
if [ "$OUTPUT_TO_FILE" = true ]; then
    ensure_analysis_dir
    OUTPUT_FILE=$(resolve_output_path "$FILE" "metrics")
fi

# Function to output (handles both console and file)
run_analysis() {
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║           STILWERK - Automated Metrics Report                 ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║  File: $(basename "$FILE")"
    echo "║  Path: $FILE"
    echo "║  Date: $(date '+%Y-%m-%d %H:%M')"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    "$SCRIPT_DIR/sentence-stats.sh" "$FILE"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    "$SCRIPT_DIR/word-stats.sh" "$FILE"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    "$SCRIPT_DIR/transitions.sh" "$FILE"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    "$SCRIPT_DIR/contractions.sh" "$FILE"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    "$SCRIPT_DIR/first-person.sh" "$FILE"
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    METRICS COMPLETE                           ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
}

# Execute analysis with appropriate output handling
if [ "$OUTPUT_TO_FILE" = true ] && [ "$QUIET_MODE" = true ]; then
    # File only
    run_analysis > "$OUTPUT_FILE"
    echo "Results written to: $OUTPUT_FILE"
elif [ "$OUTPUT_TO_FILE" = true ]; then
    # Both console and file
    run_analysis | tee "$OUTPUT_FILE"
    echo ""
    echo "Results also written to: $OUTPUT_FILE"
else
    # Console only
    run_analysis
fi
