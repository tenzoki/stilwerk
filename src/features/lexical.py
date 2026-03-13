"""Lexical feature extraction (word/sentence statistics)."""

from __future__ import annotations

from typing import Any

import numpy as np

from stilwerk.src.corpus.tokenizer import Tokenizer, TokenizerConfig
from stilwerk.src.features.base import FeatureExtractor, FeatureVector


class LexicalExtractor(FeatureExtractor):
    """Extract lexical statistics from text.

    Features include:
    - Average word length
    - Average sentence length (words)
    - Vocabulary richness (type-token ratio)
    - Hapax legomena ratio
    - Long word ratio
    """

    # Feature names in order
    FEATURES = [
        "avg_word_length",
        "avg_sentence_length",
        "type_token_ratio",
        "hapax_ratio",
        "long_word_ratio",
        "short_word_ratio",
        "word_length_std",
    ]

    def __init__(
        self,
        long_word_threshold: int = 8,
        short_word_threshold: int = 3,
    ):
        """Initialize the extractor.

        Args:
            long_word_threshold: Minimum length for "long" words.
            short_word_threshold: Maximum length for "short" words.
        """
        self.long_word_threshold = long_word_threshold
        self.short_word_threshold = short_word_threshold
        self._tokenizer = Tokenizer(TokenizerConfig(lowercase=True))

    @property
    def name(self) -> str:
        """Return extractor name."""
        return "lexical"

    @property
    def feature_names(self) -> list[str]:
        """Return feature names."""
        return self.FEATURES.copy()

    def extract(self, text: str) -> FeatureVector:
        """Extract lexical features from text.

        Args:
            text: Input text.

        Returns:
            FeatureVector with lexical statistics.
        """
        # Tokenize
        tokens = self._tokenizer.tokenize_to_strings(text)

        if not tokens:
            return FeatureVector(
                values=np.zeros(len(self.FEATURES)),
                feature_names=self.FEATURES.copy(),
            )

        # Word lengths
        word_lengths = [len(t) for t in tokens]
        avg_word_length = np.mean(word_lengths)
        word_length_std = np.std(word_lengths)

        # Sentence statistics
        sentences = self._tokenizer.sentence_tokenize(text)
        if sentences:
            sentence_lengths = [len(s.split()) for s in sentences]
            avg_sentence_length = np.mean(sentence_lengths)
        else:
            avg_sentence_length = len(tokens)

        # Type-token ratio
        unique_tokens = set(tokens)
        type_token_ratio = len(unique_tokens) / len(tokens)

        # Hapax legomena (words appearing only once)
        from collections import Counter

        counts = Counter(tokens)
        hapax = sum(1 for c in counts.values() if c == 1)
        hapax_ratio = hapax / len(tokens)

        # Long/short word ratios
        long_words = sum(1 for l in word_lengths if l >= self.long_word_threshold)
        short_words = sum(1 for l in word_lengths if l <= self.short_word_threshold)
        long_word_ratio = long_words / len(tokens)
        short_word_ratio = short_words / len(tokens)

        values = np.array(
            [
                avg_word_length,
                avg_sentence_length,
                type_token_ratio,
                hapax_ratio,
                long_word_ratio,
                short_word_ratio,
                word_length_std,
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
            "long_word_threshold": self.long_word_threshold,
            "short_word_threshold": self.short_word_threshold,
            "features": self.FEATURES,
        }


class WordFrequencyDistribution(FeatureExtractor):
    """Extract word frequency distribution features.

    Features based on Zipf's law and frequency distribution patterns.
    """

    FEATURES = [
        "freq_rank_1",  # Proportion of most frequent word
        "freq_rank_2",
        "freq_rank_3",
        "freq_rank_5",
        "freq_rank_10",
        "concentration_top10",  # Sum of top 10 word proportions
        "concentration_top50",
    ]

    def __init__(self) -> None:
        """Initialize the extractor."""
        self._tokenizer = Tokenizer(TokenizerConfig(lowercase=True))

    @property
    def name(self) -> str:
        """Return extractor name."""
        return "freq_dist"

    @property
    def feature_names(self) -> list[str]:
        """Return feature names."""
        return self.FEATURES.copy()

    def extract(self, text: str) -> FeatureVector:
        """Extract frequency distribution features.

        Args:
            text: Input text.

        Returns:
            FeatureVector with distribution statistics.
        """
        from collections import Counter

        tokens = self._tokenizer.tokenize_to_strings(text)

        if not tokens:
            return FeatureVector(
                values=np.zeros(len(self.FEATURES)),
                feature_names=self.FEATURES.copy(),
            )

        counts = Counter(tokens)
        total = len(tokens)

        # Get frequencies sorted by rank
        sorted_freqs = sorted(counts.values(), reverse=True)
        proportions = [f / total for f in sorted_freqs]

        # Extract rank-based features
        def get_prop(rank: int) -> float:
            if rank <= len(proportions):
                return proportions[rank - 1]
            return 0.0

        # Concentration measures
        top10 = sum(proportions[:10]) if len(proportions) >= 10 else sum(proportions)
        top50 = sum(proportions[:50]) if len(proportions) >= 50 else sum(proportions)

        values = np.array(
            [
                get_prop(1),
                get_prop(2),
                get_prop(3),
                get_prop(5),
                get_prop(10),
                top10,
                top50,
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
