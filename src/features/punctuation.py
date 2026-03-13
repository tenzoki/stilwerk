"""Punctuation feature extraction."""

from __future__ import annotations

from collections import Counter
from typing import Any

import numpy as np

from stilwerk.src.features.base import FeatureExtractor, FeatureVector


class PunctuationExtractor(FeatureExtractor):
    """Extract punctuation usage patterns from text.

    Punctuation style can be a strong stylistic indicator,
    including usage of:
    - Sentence-ending marks (., !, ?)
    - Structural marks (,, ;, :)
    - Quotation marks and dashes
    - Special characters
    """

    # Punctuation categories
    PUNCTUATION_GROUPS = {
        "period": {".", "\u2026"},  # period, ellipsis
        "comma": {","},
        "semicolon": {";"},
        "colon": {":"},
        "question": {"?"},
        "exclamation": {"!"},
        "dash": {"-", "\u2013", "\u2014"},  # hyphen, en-dash, em-dash
        "quote": {'"', "'", "\u201E", "\u201C", "\u201A", "\u2018", "\u2019", "\u00AB", "\u00BB"},
        "paren": {"(", ")", "[", "]", "{", "}"},
    }

    FEATURES = [
        "period_ratio",
        "comma_ratio",
        "semicolon_ratio",
        "colon_ratio",
        "question_ratio",
        "exclamation_ratio",
        "dash_ratio",
        "quote_ratio",
        "paren_ratio",
        "punct_density",  # Total punctuation per 100 words
        "sentence_end_variety",  # Ratio of ?! to total sentence ends
    ]

    def __init__(self, per_n_words: int = 100) -> None:
        """Initialize the extractor.

        Args:
            per_n_words: Normalize ratios per N words.
        """
        self.per_n_words = per_n_words
        # Build reverse lookup
        self._char_to_group: dict[str, str] = {}
        for group, chars in self.PUNCTUATION_GROUPS.items():
            for char in chars:
                self._char_to_group[char] = group

    @property
    def name(self) -> str:
        """Return extractor name."""
        return "punctuation"

    @property
    def feature_names(self) -> list[str]:
        """Return feature names."""
        return self.FEATURES.copy()

    def extract(self, text: str) -> FeatureVector:
        """Extract punctuation features from text.

        Args:
            text: Input text.

        Returns:
            FeatureVector with punctuation statistics.
        """
        # Count words (simple split)
        word_count = len(text.split())
        if word_count == 0:
            return FeatureVector(
                values=np.zeros(len(self.FEATURES)),
                feature_names=self.FEATURES.copy(),
            )

        # Count punctuation by group
        group_counts: Counter[str] = Counter()
        total_punct = 0

        for char in text:
            if char in self._char_to_group:
                group_counts[self._char_to_group[char]] += 1
                total_punct += 1

        # Normalize per N words
        factor = self.per_n_words / word_count

        # Calculate ratios
        period_ratio = group_counts["period"] * factor
        comma_ratio = group_counts["comma"] * factor
        semicolon_ratio = group_counts["semicolon"] * factor
        colon_ratio = group_counts["colon"] * factor
        question_ratio = group_counts["question"] * factor
        exclamation_ratio = group_counts["exclamation"] * factor
        dash_ratio = group_counts["dash"] * factor
        quote_ratio = group_counts["quote"] * factor
        paren_ratio = group_counts["paren"] * factor

        # Punctuation density
        punct_density = total_punct * factor

        # Sentence end variety
        sentence_ends = (
            group_counts["period"]
            + group_counts["question"]
            + group_counts["exclamation"]
        )
        if sentence_ends > 0:
            variety = (
                group_counts["question"] + group_counts["exclamation"]
            ) / sentence_ends
        else:
            variety = 0.0

        values = np.array(
            [
                period_ratio,
                comma_ratio,
                semicolon_ratio,
                colon_ratio,
                question_ratio,
                exclamation_ratio,
                dash_ratio,
                quote_ratio,
                paren_ratio,
                punct_density,
                variety,
            ],
            dtype=np.float64,
        )

        return FeatureVector(
            values=values,
            feature_names=self.FEATURES.copy(),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "per_n_words": self.per_n_words,
            "features": self.FEATURES,
        }


class SpecialCharacterExtractor(FeatureExtractor):
    """Extract special character usage patterns.

    Tracks usage of:
    - Gender-inclusive markers (:, *, _)
    - Emojis and unicode symbols
    - Foreign characters
    """

    FEATURES = [
        "gender_colon",  # Bürger:innen style
        "gender_star",  # Bürger*innen style
        "gender_underscore",  # Bürger_innen style
        "gender_capital",  # BürgerInnen style
        "emoji_count",
        "special_unicode",
    ]

    def __init__(self) -> None:
        """Initialize the extractor."""
        import re

        # Gender-inclusive patterns
        self._gender_colon = re.compile(r"\w+:innen\b", re.IGNORECASE)
        self._gender_star = re.compile(r"\w+\*innen\b", re.IGNORECASE)
        self._gender_underscore = re.compile(r"\w+_innen\b", re.IGNORECASE)
        self._gender_capital = re.compile(r"\w+In(?:nen)?\b")

        # Simple emoji detection (common emoji ranges)
        self._emoji_pattern = re.compile(
            r"[\U0001F600-\U0001F64F"  # Emoticons
            r"\U0001F300-\U0001F5FF"  # Misc symbols
            r"\U0001F680-\U0001F6FF"  # Transport
            r"\U0001F700-\U0001F77F"  # Alchemical
            r"\U0001F780-\U0001F7FF"  # Geometric
            r"\U0001F800-\U0001F8FF"  # Supplemental arrows
            r"\U0001F900-\U0001F9FF"  # Supplemental symbols
            r"\U0001FA00-\U0001FA6F"  # Chess
            r"\U0001FA70-\U0001FAFF"  # Symbols/pictographs
            r"\U00002702-\U000027B0"  # Dingbats
            r"]+",
            re.UNICODE,
        )

    @property
    def name(self) -> str:
        """Return extractor name."""
        return "special_chars"

    @property
    def feature_names(self) -> list[str]:
        """Return feature names."""
        return self.FEATURES.copy()

    def extract(self, text: str) -> FeatureVector:
        """Extract special character features.

        Args:
            text: Input text.

        Returns:
            FeatureVector with character statistics.
        """
        word_count = len(text.split())
        if word_count == 0:
            factor = 0.0
        else:
            factor = 100 / word_count

        # Count gender-inclusive markers
        gender_colon = len(self._gender_colon.findall(text)) * factor
        gender_star = len(self._gender_star.findall(text)) * factor
        gender_underscore = len(self._gender_underscore.findall(text)) * factor
        gender_capital = len(self._gender_capital.findall(text)) * factor

        # Count emojis
        emojis = self._emoji_pattern.findall(text)
        emoji_count = len(emojis) * factor

        # Count other special unicode (non-ASCII, non-German)
        # German chars we allow: umlauts, special quotes, dashes, ellipsis
        allowed_german = set("äöüÄÖÜß") | {
            "\u201E", "\u201C", "\u201A", "\u2018", "\u2019",  # German quotes
            "\u2013", "\u2014", "\u2026",  # dashes and ellipsis
            "\u00AB", "\u00BB",  # guillemets
        }
        special = 0
        for char in text:
            if ord(char) > 127 and char not in allowed_german:
                special += 1
        special_unicode = special * factor

        values = np.array(
            [
                gender_colon,
                gender_star,
                gender_underscore,
                gender_capital,
                emoji_count,
                special_unicode,
            ],
            dtype=np.float64,
        )

        return FeatureVector(
            values=values,
            feature_names=self.FEATURES.copy(),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "features": self.FEATURES,
        }
