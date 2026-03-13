#!/bin/bash
# sentence-stats.sh - Satzstatistiken (U01, CX01)
# Usage: ./sentence-stats.sh <file>

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/config.sh"

INPUT="$1"

if [ -z "$INPUT" ]; then
    echo "Usage: ./sentence-stats.sh <file>"
    exit 1
fi

# Resolve file path (support both direct path and corpus lookup)
if [ -f "$INPUT" ]; then
    FILE="$INPUT"
else
    FILE=$(resolve_corpus_file "$INPUT")
fi

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    echo "Error: File not found: $INPUT"
    exit 1
fi

# Extract text, remove markdown formatting
TEXT=$(cat "$FILE" | sed 's/^#.*//g' | sed 's/\*\*//g' | sed 's/\*//g' | sed 's/`//g' | tr '\n' ' ')

# Split into sentences (approximate: split on . ! ?)
# Count words per sentence
echo "=== Sentence Statistics (U01, CX01) ==="
echo ""

# Use awk to split and count
echo "$TEXT" | awk '
BEGIN {
    RS = "[.!?]+"
    sum = 0
    sumsq = 0
    count = 0
    min = 999999
    max = 0
}
{
    # Count words in this sentence
    gsub(/^[[:space:]]+|[[:space:]]+$/, "")  # trim
    if (length($0) > 0) {
        n = split($0, words)
        if (n > 2) {  # ignore very short fragments
            sum += n
            sumsq += n*n
            count++
            if (n < min) min = n
            if (n > max) max = n
            lengths[count] = n
        }
    }
}
END {
    if (count > 0) {
        mean = sum / count
        variance = (sumsq / count) - (mean * mean)
        if (variance < 0) variance = 0
        stddev = sqrt(variance)

        print "Sentence count: " count
        print "Mean length: " sprintf("%.1f", mean) " words"
        print "Std deviation: " sprintf("%.1f", stddev)
        print "Min length: " min " words"
        print "Max length: " max " words"
        print ""

        # Interpretation
        print "--- Interpretation ---"
        if (stddev < 5) {
            print "Variance: LOW (< 5) → AI signal (monotonous rhythm)"
        } else if (stddev < 10) {
            print "Variance: MODERATE (5-10) → neutral"
        } else {
            print "Variance: HIGH (> 10) → Human signal (natural variation)"
        }

        if (mean < 15) {
            print "Complexity: SIMPLE (mean < 15)"
        } else if (mean < 25) {
            print "Complexity: MODERATE (mean 15-25)"
        } else if (mean < 35) {
            print "Complexity: COMPLEX (mean 25-35)"
        } else {
            print "Complexity: VERY COMPLEX (mean > 35)"
        }
    } else {
        print "No sentences found"
    }
}
'
