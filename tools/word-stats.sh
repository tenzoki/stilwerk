#!/bin/bash
# word-stats.sh - Wortstatistiken (CMD01, CX05)
# Usage: ./word-stats.sh <file>

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/config.sh"

INPUT="$1"

if [ -z "$INPUT" ]; then
    echo "Usage: ./word-stats.sh <file>"
    exit 1
fi

# Resolve file path
if [ -f "$INPUT" ]; then
    FILE="$INPUT"
else
    FILE=$(resolve_corpus_file "$INPUT")
fi

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    echo "Error: File not found: $INPUT"
    exit 1
fi

echo "=== Word Statistics (CMD01, CX05) ==="
echo ""

# Extract words, lowercase, remove punctuation
WORDS=$(cat "$FILE" | sed 's/^#.*//g' | tr '[:upper:]' '[:lower:]' | tr -cs '[:alpha:]' '\n' | grep -v '^$')

# Total words
TOTAL=$(echo "$WORDS" | wc -l | tr -d ' ')

# Unique words (types)
TYPES=$(echo "$WORDS" | sort -u | wc -l | tr -d ' ')

# Type-Token Ratio
if [ "$TOTAL" -gt 0 ]; then
    TTR=$(echo "scale=3; $TYPES / $TOTAL" | bc)
else
    TTR="0"
fi

echo "Total words (tokens): $TOTAL"
echo "Unique words (types): $TYPES"
echo "Type-Token Ratio: $TTR"
echo ""

# Most frequent words
echo "--- Top 20 words ---"
echo "$WORDS" | sort | uniq -c | sort -rn | head -20
echo ""

# Academic vocabulary check (simplified AWL sample)
AWL_WORDS="analysis approach area assessment assume authority available benefit concept consistent constitute context contract create data define derive design distribute economy environment establish estimate evident factor feature final focus formula function identify impact implement indicate individual interpret involve issue labour legal legislate major method occur percent period policy principle proceed process range region regulate relevant research resource respond role section sector significant similar source specific strategy structure survey text theory tradition transfer"

AWL_COUNT=0
for word in $AWL_WORDS; do
    COUNT=$(echo "$WORDS" | grep -c "^${word}$" 2>/dev/null)
    if [ -n "$COUNT" ] && [ "$COUNT" -gt 0 ] 2>/dev/null; then
        AWL_COUNT=$((AWL_COUNT + COUNT))
    fi
done

if [ "$TOTAL" -gt 0 ]; then
    AWL_PERCENT=$(echo "scale=2; ($AWL_COUNT * 100) / $TOTAL" | bc)
else
    AWL_PERCENT="0"
fi

echo "--- Academic Vocabulary ---"
echo "AWL words found: $AWL_COUNT"
echo "AWL percentage: ${AWL_PERCENT}%"
echo ""

# Interpretation
echo "--- Interpretation ---"
if (( $(echo "$TTR > 0.6" | bc -l) )); then
    echo "TTR: HIGH (> 0.6) → varied vocabulary"
elif (( $(echo "$TTR > 0.4" | bc -l) )); then
    echo "TTR: MODERATE (0.4-0.6)"
else
    echo "TTR: LOW (< 0.4) → repetitive vocabulary"
fi

if (( $(echo "$AWL_PERCENT > 5" | bc -l) )); then
    echo "AWL: HIGH (> 5%) → academic register"
elif (( $(echo "$AWL_PERCENT > 2" | bc -l) )); then
    echo "AWL: MODERATE (2-5%) → educated register"
else
    echo "AWL: LOW (< 2%) → general register"
fi
