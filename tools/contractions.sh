#!/bin/bash
# contractions.sh - Kontraktionsrate (L06)
# Usage: ./contractions.sh <file>

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/config.sh"

INPUT="$1"

if [ -z "$INPUT" ]; then
    echo "Usage: ./contractions.sh <file>"
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

echo "=== Contraction Analysis (L06) ==="
echo ""

TEXT=$(cat "$FILE")

# Common contractions
CONTRACTIONS="'s 's 't 't 're 're 've 've 'll 'll 'd 'd n't n't"

# Count contractions
CONTR_COUNT=0
for c in $CONTRACTIONS; do
    count=$(echo "$TEXT" | grep -o "$c" | wc -l | tr -d ' ')
    CONTR_COUNT=$((CONTR_COUNT + count))
done

# Count opportunities (approximate: count full forms)
OPP_WORDS="is are have has will would not does did"
OPP_COUNT=0
for word in $OPP_WORDS; do
    count=$(echo "$TEXT" | tr '[:upper:]' '[:lower:]' | grep -ow "\b${word}\b" | wc -l | tr -d ' ')
    OPP_COUNT=$((OPP_COUNT + count))
done

# Total opportunities = contractions found + full forms found
TOTAL_OPP=$((CONTR_COUNT + OPP_COUNT))

if [ "$TOTAL_OPP" -gt 0 ]; then
    RATE=$(echo "scale=2; $CONTR_COUNT / $TOTAL_OPP" | bc)
else
    RATE="0"
fi

echo "Contractions found: $CONTR_COUNT"
echo "Full forms found: $OPP_COUNT"
echo "Total opportunities: $TOTAL_OPP"
echo "Contraction rate: $RATE"
echo ""

# List found contractions
echo "--- Contractions found ---"
echo "$TEXT" | grep -oE "[a-zA-Z]+'[a-zA-Z]+" | sort | uniq -c | sort -rn | head -10
echo ""

# Interpretation
echo "--- Interpretation ---"
if (( $(echo "$RATE < 0.2" | bc -l) )); then
    echo "Rate: LOW (< 0.2) → AI signal (formal even in casual context)"
elif (( $(echo "$RATE < 0.5" | bc -l) )); then
    echo "Rate: MODERATE (0.2-0.5) → neutral"
else
    echo "Rate: HIGH (> 0.5) → Human signal (natural informality)"
fi
