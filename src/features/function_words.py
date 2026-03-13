"""Function word frequency extraction."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

from stilwerk.src.corpus.tokenizer import Tokenizer, TokenizerConfig
from stilwerk.src.features.base import FeatureExtractor, FeatureVector


# Default German function words
DEFAULT_GERMAN_FUNCTION_WORDS = [
    "und", "die", "der", "in", "den", "von", "zu", "das", "mit", "sich",
    "des", "auf", "für", "ist", "im", "dem", "nicht", "ein", "eine", "als",
    "auch", "es", "an", "werden", "aus", "er", "hat", "dass", "sie", "nach",
    "wird", "bei", "einer", "um", "am", "sind", "noch", "wie", "einem", "über",
    "so", "zum", "war", "haben", "nur", "oder", "aber", "vor", "zur", "bis",
    "mehr", "durch", "man", "dann", "soll", "hier", "alle", "schon", "wenn",
    "was", "vom", "dieser", "kann", "uns", "wir", "ihre", "sein", "eines",
    "diese", "einem", "ob", "mir", "ohne", "da", "ihren", "seiner", "unter",
    "zwischen", "dort", "selbst", "gegen", "jetzt", "kein", "keine", "bereits",
    "sehr", "muss", "dieses", "denn", "weil", "welche", "damit", "also",
    "sondern", "ihrer", "unserem", "unsere", "unser", "unserer", "unseren",
    "diesem", "ich", "du", "wer", "wo", "wann", "warum", "doch", "etwa",
    "ja", "nein", "nie", "immer", "oft", "viel", "wenig", "ganz", "gar",
]


class FunctionWordExtractor(FeatureExtractor):
    """Extract function word frequencies from text.

    Function words (articles, prepositions, pronouns, etc.) are commonly
    used in stylometric analysis as they are largely unconscious choices
    by authors and thus serve as stylistic fingerprints.
    """

    def __init__(
        self,
        function_words: list[str] | None = None,
        normalize: bool = True,
        mfw: int | None = None,
    ):
        """Initialize the extractor.

        Args:
            function_words: List of function words to track.
                          Defaults to German function words.
            normalize: Whether to normalize frequencies (divide by total).
            mfw: Most frequent words limit. If set, only use top N words
                 from the function word list by corpus frequency.
        """
        self.function_words = function_words or DEFAULT_GERMAN_FUNCTION_WORDS.copy()
        self.normalize = normalize
        self.mfw = mfw
        self._tokenizer = Tokenizer(TokenizerConfig(lowercase=True))

    @property
    def name(self) -> str:
        """Return extractor name."""
        return "function_words"

    @property
    def feature_names(self) -> list[str]:
        """Return function word list as feature names."""
        if self.mfw and self.mfw < len(self.function_words):
            return self.function_words[: self.mfw]
        return self.function_words

    def extract(self, text: str) -> FeatureVector:
        """Extract function word frequencies from text.

        Args:
            text: Input text.

        Returns:
            FeatureVector with frequencies for each function word.
        """
        tokens = self._tokenizer.tokenize_to_strings(text)
        counts = Counter(tokens)
        total = len(tokens) if self.normalize else 1

        values = []
        for word in self.feature_names:
            freq = counts.get(word, 0)
            if self.normalize and total > 0:
                freq = freq / total
            values.append(freq)

        return FeatureVector(
            values=np.array(values, dtype=np.float64),
            feature_names=self.feature_names,
        )

    def fit(self, texts: dict[str, str]) -> "FunctionWordExtractor":
        """Fit extractor to corpus (compute most frequent words).

        Args:
            texts: Dictionary of label -> text.

        Returns:
            Self for chaining.
        """
        if self.mfw is None:
            return self

        # Count function words across corpus
        total_counts: Counter[str] = Counter()
        for text in texts.values():
            tokens = self._tokenizer.tokenize_to_strings(text)
            for token in tokens:
                if token in self.function_words:
                    total_counts[token] += 1

        # Sort by frequency and keep top N
        sorted_words = [
            word for word, _ in total_counts.most_common(self.mfw)
        ]

        # Update function words list
        self.function_words = sorted_words

        return self

    @classmethod
    def from_file(cls, path: Path, **kwargs: Any) -> "FunctionWordExtractor":
        """Load function words from a file.

        Args:
            path: Path to file (one word per line or YAML).
            **kwargs: Additional arguments for __init__.

        Returns:
            FunctionWordExtractor instance.
        """
        path = Path(path)
        words: list[str] = []

        if path.suffix in (".yaml", ".yml"):
            import yaml

            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            words = data.get("words", [])
        else:
            with open(path, "r", encoding="utf-8") as f:
                words = [line.strip() for line in f if line.strip()]

        return cls(function_words=words, **kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "function_word_count": len(self.function_words),
            "normalize": self.normalize,
            "mfw": self.mfw,
        }


class MostFrequentWordsExtractor(FeatureExtractor):
    """Extract most frequent word frequencies from text.

    Unlike FunctionWordExtractor which uses a predefined list,
    this extractor learns the most frequent words from the corpus.
    """

    def __init__(
        self,
        n_words: int = 100,
        min_length: int = 2,
        normalize: bool = True,
    ):
        """Initialize the extractor.

        Args:
            n_words: Number of most frequent words to use.
            min_length: Minimum word length.
            normalize: Whether to normalize frequencies.
        """
        self.n_words = n_words
        self.min_length = min_length
        self.normalize = normalize
        self._mfw: list[str] = []
        self._tokenizer = Tokenizer(
            TokenizerConfig(lowercase=True, min_length=min_length)
        )

    @property
    def name(self) -> str:
        """Return extractor name."""
        return "mfw"

    @property
    def feature_names(self) -> list[str]:
        """Return learned most frequent words."""
        return self._mfw

    def fit(self, texts: dict[str, str]) -> "MostFrequentWordsExtractor":
        """Learn most frequent words from corpus.

        Args:
            texts: Dictionary of label -> text.

        Returns:
            Self for chaining.
        """
        total_counts: Counter[str] = Counter()

        for text in texts.values():
            tokens = self._tokenizer.tokenize_to_strings(text)
            total_counts.update(tokens)

        # Get top N words
        self._mfw = [
            word for word, _ in total_counts.most_common(self.n_words)
        ]

        return self

    def extract(self, text: str) -> FeatureVector:
        """Extract MFW frequencies from text.

        Args:
            text: Input text.

        Returns:
            FeatureVector with frequencies.

        Raises:
            ValueError: If extractor hasn't been fit.
        """
        if not self._mfw:
            raise ValueError("Extractor must be fit before extraction")

        tokens = self._tokenizer.tokenize_to_strings(text)
        counts = Counter(tokens)
        total = len(tokens) if self.normalize else 1

        values = []
        for word in self._mfw:
            freq = counts.get(word, 0)
            if self.normalize and total > 0:
                freq = freq / total
            values.append(freq)

        return FeatureVector(
            values=np.array(values, dtype=np.float64),
            feature_names=self._mfw,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "n_words": self.n_words,
            "min_length": self.min_length,
            "normalize": self.normalize,
            "fitted": len(self._mfw) > 0,
        }
