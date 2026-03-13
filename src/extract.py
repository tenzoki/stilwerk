"""Extract style metrics from text."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class MetricResult:
    """Result of a single metric extraction."""

    id: str
    name: str
    value: float
    raw: str = ""  # Raw output from tool


@dataclass
class ExtractionResult:
    """Complete extraction result for a text."""

    metrics: dict[str, float] = field(default_factory=dict)
    raw_outputs: dict[str, str] = field(default_factory=dict)

    def get(self, metric_id: str, default: float = 0.0) -> float:
        """Get metric value by ID."""
        return self.metrics.get(metric_id, default)


# Metric IDs and their corresponding shell tools
METRIC_TOOLS = {
    "U01": ("sentence-stats.sh", "variance"),  # Sentence variance
    "TTR": ("word-stats.sh", "ttr"),  # Type-Token Ratio
    "D01": ("transitions.sh", "density"),  # Transition density
    "L06": ("contractions.sh", "rate"),  # Contraction rate
    "U05": ("first-person.sh", "rate"),  # First-person rate
}


def extract_metrics(
    text: str,
    tools_dir: Path | None = None,
) -> ExtractionResult:
    """Extract all style metrics from text.

    Args:
        text: Text content to analyze.
        tools_dir: Path to stilwerk/tools directory.

    Returns:
        ExtractionResult with all metrics.
    """
    result = ExtractionResult()

    # Extract metrics using Python implementations
    result.metrics["U01"] = _extract_sentence_variance(text)
    result.metrics["TTR"] = _extract_ttr(text)
    result.metrics["D01"] = _extract_transition_density(text)
    result.metrics["L06"] = _extract_contraction_rate(text)
    result.metrics["U05"] = _extract_first_person_rate(text)

    return result


def extract_from_file(
    path: Path,
    tools_dir: Path | None = None,
) -> ExtractionResult:
    """Extract metrics from a file.

    Args:
        path: Path to text file.
        tools_dir: Path to stilwerk/tools directory.

    Returns:
        ExtractionResult with all metrics.
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    return extract_metrics(text, tools_dir)


def extract_excerpt(text: str, max_length: int = 500) -> str:
    """Extract a representative excerpt from text.

    Tries to find a complete paragraph near the beginning.

    Args:
        text: Full text content.
        max_length: Maximum excerpt length.

    Returns:
        Excerpt string.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    if not paragraphs:
        return text[:max_length]

    # Find a good paragraph (not too short, not too long)
    for para in paragraphs[1:5]:  # Skip first (often intro), look at next few
        if 100 < len(para) < max_length:
            return para

    # Fallback: use first substantial paragraph
    for para in paragraphs:
        if len(para) > 50:
            return para[:max_length]

    return text[:max_length]


# --- Python implementations of metrics ---


def _extract_sentence_variance(text: str) -> float:
    """Calculate sentence length variance (U01).

    Returns standard deviation of sentence lengths.
    """
    sentences = _split_sentences(text)
    if len(sentences) < 2:
        return 0.0

    lengths = [len(s.split()) for s in sentences]
    mean = sum(lengths) / len(lengths)
    variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
    return variance ** 0.5  # Standard deviation


def _extract_ttr(text: str) -> float:
    """Calculate Type-Token Ratio.

    Returns ratio of unique words to total words.
    """
    words = _tokenize(text)
    if not words:
        return 0.0

    unique = set(words)
    return len(unique) / len(words)


def _extract_transition_density(text: str) -> float:
    """Calculate transition word density (D01).

    Returns transitions per sentence.
    """
    # German and English transition words
    transitions = {
        # German
        "außerdem", "darüber hinaus", "ferner", "weiterhin", "zusätzlich",
        "jedoch", "allerdings", "dennoch", "trotzdem", "andererseits",
        "deshalb", "daher", "folglich", "somit", "dementsprechend",
        "erstens", "zweitens", "drittens", "schließlich", "abschließend",
        "zum beispiel", "beispielsweise", "insbesondere", "nämlich",
        "zusammenfassend", "insgesamt", "im grunde", "letztendlich",
        # English
        "furthermore", "moreover", "additionally", "however", "nevertheless",
        "therefore", "consequently", "thus", "hence", "accordingly",
        "firstly", "secondly", "thirdly", "finally", "in conclusion",
        "for example", "for instance", "specifically", "namely",
        "in summary", "overall", "ultimately", "essentially",
        "it's important to note", "it is worth noting",
    }

    text_lower = text.lower()
    sentences = _split_sentences(text)
    if not sentences:
        return 0.0

    count = sum(1 for t in transitions if t in text_lower)
    return count / len(sentences)


def _extract_contraction_rate(text: str) -> float:
    """Calculate contraction rate (L06).

    Returns contractions per 100 words.
    """
    # Common contractions
    contractions_en = [
        "n't", "'re", "'ve", "'ll", "'d", "'m", "'s",
        "don't", "doesn't", "didn't", "won't", "wouldn't",
        "can't", "couldn't", "shouldn't", "wouldn't",
        "i'm", "you're", "we're", "they're", "he's", "she's", "it's",
        "i've", "you've", "we've", "they've",
        "i'll", "you'll", "we'll", "they'll",
        "i'd", "you'd", "we'd", "they'd",
        "let's", "that's", "there's", "here's", "what's",
    ]

    # German contractions
    contractions_de = [
        "im", "am", "zum", "zur", "vom", "beim",
        "ans", "aufs", "ins", "ums", "fürs", "durchs",
    ]

    text_lower = text.lower()
    words = _tokenize(text)
    if not words:
        return 0.0

    count = 0
    for c in contractions_en:
        count += text_lower.count(c)

    # For German, only count if they replace expanded forms
    # (these are always contractions in German)
    for c in contractions_de:
        # Count word occurrences (not substrings)
        count += len(re.findall(rf"\b{c}\b", text_lower))

    return (count / len(words)) * 100


def _extract_first_person_rate(text: str) -> float:
    """Calculate first-person pronoun rate (U05).

    Returns first-person pronouns per 1000 words.
    """
    first_person = {
        # English
        "i", "me", "my", "mine", "myself",
        "we", "us", "our", "ours", "ourselves",
        # German
        "ich", "mir", "mich", "mein", "meine", "meiner", "meinem", "meinen",
        "wir", "uns", "unser", "unsere", "unserer", "unserem", "unseren",
    }

    words = _tokenize(text)
    if not words:
        return 0.0

    count = sum(1 for w in words if w in first_person)
    return (count / len(words)) * 1000


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    # Simple sentence splitting on . ! ?
    # Handles abbreviations roughly
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ])', text)
    return [s.strip() for s in sentences if s.strip()]


def _tokenize(text: str) -> list[str]:
    """Tokenize text into lowercase words."""
    # Remove punctuation except apostrophes
    text = re.sub(r"[^\w\s']", " ", text.lower())
    words = text.split()
    return [w for w in words if len(w) > 0]
