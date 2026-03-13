#!/bin/bash
# transitions.sh - Übergangswörter (D01)
# Usage: ./transitions.sh <file>

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/config.sh"

INPUT="$1"

if [ -z "$INPUT" ]; then
    echo "Usage: ./transitions.sh <file>"
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

echo "=== Transition Analysis (D01) ==="
echo ""

# Extract text
TEXT=$(cat "$FILE" | tr '[:upper:]' '[:lower:]')

# Count paragraphs (non-empty lines after empty lines, approximately)
PARAGRAPHS=$(cat "$FILE" | grep -c '^[^#].*[a-zA-Z]')
if [ "$PARAGRAPHS" -lt 1 ]; then
    PARAGRAPHS=1
fi

# Transition words to check
ADDITIVE="furthermore moreover additionally also similarly likewise"
ADVERSATIVE="however but yet although nevertheless nonetheless whereas while"
CAUSAL="therefore thus consequently hence accordingly because since so"
TEMPORAL="then later meanwhile subsequently finally eventually"

# Count each category
count_words() {
    local words="$1"
    local count=0
    for word in $words; do
        c=$(echo "$TEXT" | grep -ow "\b${word}\b" | wc -l | tr -d ' ')
        count=$((count + c))
    done
    echo $count
}

ADD_COUNT=$(count_words "$ADDITIVE")
ADV_COUNT=$(count_words "$ADVERSATIVE")
CAUS_COUNT=$(count_words "$CAUSAL")
TEMP_COUNT=$(count_words "$TEMPORAL")
TOTAL_TRANS=$((ADD_COUNT + ADV_COUNT + CAUS_COUNT + TEMP_COUNT))

echo "Paragraphs (approx): $PARAGRAPHS"
echo ""
echo "--- Transition counts ---"
echo "Additive (furthermore, moreover...): $ADD_COUNT"
echo "Adversative (however, but...): $ADV_COUNT"
echo "Causal (therefore, thus...): $CAUS_COUNT"
echo "Temporal (then, later...): $TEMP_COUNT"
echo "Total transitions: $TOTAL_TRANS"
echo ""

# Density
if [ "$PARAGRAPHS" -gt 0 ]; then
    DENSITY=$(echo "scale=2; $TOTAL_TRANS / $PARAGRAPHS" | bc)
else
    DENSITY="0"
fi

echo "Transition density: $DENSITY per paragraph"
echo ""

# Interpretation
echo "--- Interpretation ---"
if (( $(echo "$DENSITY > 0.7" | bc -l) )); then
    echo "Density: HIGH (> 0.7) → AI signal (over-explicit)"
elif (( $(echo "$DENSITY > 0.3" | bc -l) )); then
    echo "Density: MODERATE (0.3-0.7) → neutral"
else
    echo "Density: LOW (< 0.3) → Human signal (implicit connections)"
fi

# Dominant type
MAX=$ADD_COUNT
TYPE="ADDITIVE"
if [ $ADV_COUNT -gt $MAX ]; then MAX=$ADV_COUNT; TYPE="ADVERSATIVE"; fi
if [ $CAUS_COUNT -gt $MAX ]; then MAX=$CAUS_COUNT; TYPE="CAUSAL"; fi
if [ $TEMP_COUNT -gt $MAX ]; then MAX=$TEMP_COUNT; TYPE="TEMPORAL"; fi

echo "Dominant type: $TYPE"
