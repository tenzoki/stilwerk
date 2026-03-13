#!/bin/bash
# first-person.sh - Erste-Person-Rate (U05)
# Usage: ./first-person.sh <file>

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/config.sh"

INPUT="$1"

if [ -z "$INPUT" ]; then
    echo "Usage: ./first-person.sh <file>"
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

echo "=== First-Person Analysis (U05) ==="
echo ""

TEXT=$(cat "$FILE")

# Count total words
TOTAL=$(echo "$TEXT" | tr -cs '[:alpha:]' '\n' | grep -v '^$' | wc -l | tr -d ' ')

# Count first person singular
I_COUNT=$(echo "$TEXT" | grep -ow '\bI\b' | wc -l | tr -d ' ')
MY_COUNT=$(echo "$TEXT" | tr '[:upper:]' '[:lower:]' | grep -ow '\bmy\b' | wc -l | tr -d ' ')
ME_COUNT=$(echo "$TEXT" | tr '[:upper:]' '[:lower:]' | grep -ow '\bme\b' | wc -l | tr -d ' ')
MINE_COUNT=$(echo "$TEXT" | tr '[:upper:]' '[:lower:]' | grep -ow '\bmine\b' | wc -l | tr -d ' ')

# Count first person plural
WE_COUNT=$(echo "$TEXT" | tr '[:upper:]' '[:lower:]' | grep -ow '\bwe\b' | wc -l | tr -d ' ')
OUR_COUNT=$(echo "$TEXT" | tr '[:upper:]' '[:lower:]' | grep -ow '\bour\b' | wc -l | tr -d ' ')
US_COUNT=$(echo "$TEXT" | tr '[:upper:]' '[:lower:]' | grep -ow '\bus\b' | wc -l | tr -d ' ')

FIRST_SINGULAR=$((I_COUNT + MY_COUNT + ME_COUNT + MINE_COUNT))
FIRST_PLURAL=$((WE_COUNT + OUR_COUNT + US_COUNT))
FIRST_TOTAL=$((FIRST_SINGULAR + FIRST_PLURAL))

# Rate per 1000 words
if [ "$TOTAL" -gt 0 ]; then
    I_RATE=$(echo "scale=1; ($I_COUNT * 1000) / $TOTAL" | bc)
    FIRST_RATE=$(echo "scale=1; ($FIRST_TOTAL * 1000) / $TOTAL" | bc)
else
    I_RATE="0"
    FIRST_RATE="0"
fi

echo "Total words: $TOTAL"
echo ""
echo "--- First person singular ---"
echo "  I: $I_COUNT"
echo "  my: $MY_COUNT"
echo "  me: $ME_COUNT"
echo "  mine: $MINE_COUNT"
echo "  Subtotal: $FIRST_SINGULAR"
echo ""
echo "--- First person plural ---"
echo "  we: $WE_COUNT"
echo "  our: $OUR_COUNT"
echo "  us: $US_COUNT"
echo "  Subtotal: $FIRST_PLURAL"
echo ""
echo "Total first person: $FIRST_TOTAL"
echo "'I' per 1000 words: $I_RATE"
echo "All first person per 1000 words: $FIRST_RATE"
echo ""

# Interpretation
echo "--- Interpretation ---"
if (( $(echo "$I_RATE < 1" | bc -l) )); then
    echo "I-rate: LOW (< 1/1000) → AI signal (impersonal voice)"
elif (( $(echo "$I_RATE < 5" | bc -l) )); then
    echo "I-rate: MODERATE (1-5/1000) → neutral"
else
    echo "I-rate: HIGH (> 5/1000) → Human signal (personal stance visible)"
fi

if [ $FIRST_SINGULAR -gt $FIRST_PLURAL ]; then
    echo "Dominant: SINGULAR (personal/individual stance)"
else
    echo "Dominant: PLURAL (collective/inclusive stance)"
fi
