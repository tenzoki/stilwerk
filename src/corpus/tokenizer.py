"""Language-aware tokenization for stylometric analysis."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TokenizerConfig:
    """Configuration for the tokenizer."""

    lowercase: bool = True
    min_length: int = 1
    keep_punctuation: bool = False
    keep_numbers: bool = False
    language: str = "de"
    custom_patterns: list[str] = field(default_factory=list)


@dataclass
class Token:
    """A single token with metadata."""

    text: str
    original: str
    position: int
    is_punctuation: bool = False
    is_number: bool = False

    def __str__(self) -> str:
        return self.text


class Tokenizer:
    """Language-aware tokenizer for text analysis.

    Handles German-specific characters and patterns, including:
    - Umlauts (ä, ö, ü) and eszett (ß)
    - Compound words
    - Gender-inclusive forms (Bürger:innen, Freund*innen)
    """

    # German-specific patterns
    GENDER_PATTERNS = [
        r"(\w+)[:*_]innen",  # Bürger:innen, Freund*innen
        r"(\w+)In(?:nen)?",  # BürgerInnen, BürgerIn
    ]

    # Punctuation characters (including German quotes and dashes)
    PUNCTUATION = set(".,;:!?()[]{}\"'-") | {
        "\u2013",  # en-dash
        "\u2014",  # em-dash
        "\u2026",  # ellipsis
        "\u201E",  # German opening quote „
        "\u201C",  # left double quote "
        "\u201A",  # single low quote ‚
        "\u2018",  # left single quote '
        "\u2019",  # right single quote '
        "\u00AB",  # left guillemet «
        "\u00BB",  # right guillemet »
    }

    # Number pattern
    NUMBER_PATTERN = re.compile(r"^\d+([.,]\d+)?$")

    def __init__(self, config: TokenizerConfig | None = None):
        """Initialize the tokenizer.

        Args:
            config: Tokenizer configuration.
        """
        self.config = config or TokenizerConfig()
        # Word pattern: German letters + punctuation
        punct_chars = r".,;:!?()\[\]{}\"\'\-\u2013\u2014\u2026\u201E\u201C\u201A\u2018\u2019\u00AB\u00BB"
        self._word_pattern = re.compile(
            r"[\w\u00E4\u00F6\u00FC\u00C4\u00D6\u00DC\u00DF]+|[" + punct_chars + "]",
            re.UNICODE,
        )

    def tokenize(self, text: str) -> list[Token]:
        """Tokenize text into a list of tokens.

        Args:
            text: Input text.

        Returns:
            List of Token instances.
        """
        tokens = []
        position = 0

        for match in self._word_pattern.finditer(text):
            original = match.group()
            is_punct = original in self.PUNCTUATION
            is_number = bool(self.NUMBER_PATTERN.match(original))

            # Skip based on config
            if is_punct and not self.config.keep_punctuation:
                continue
            if is_number and not self.config.keep_numbers:
                continue
            if len(original) < self.config.min_length and not is_punct:
                continue

            # Apply lowercase if configured
            processed = original.lower() if self.config.lowercase else original

            token = Token(
                text=processed,
                original=original,
                position=position,
                is_punctuation=is_punct,
                is_number=is_number,
            )
            tokens.append(token)
            position += 1

        return tokens

    def tokenize_to_strings(self, text: str) -> list[str]:
        """Tokenize text and return just the token strings.

        Args:
            text: Input text.

        Returns:
            List of token strings.
        """
        return [t.text for t in self.tokenize(text)]

    def word_frequencies(self, text: str) -> dict[str, int]:
        """Count word frequencies in text.

        Args:
            text: Input text.

        Returns:
            Dictionary mapping words to counts.
        """
        tokens = self.tokenize_to_strings(text)
        freq: dict[str, int] = {}
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1
        return freq

    def sentence_tokenize(self, text: str) -> list[str]:
        """Split text into sentences.

        Handles German-specific abbreviations and patterns.

        Args:
            text: Input text.

        Returns:
            List of sentences.
        """
        # Simple sentence boundary detection
        # End markers followed by space and capital letter or end of string
        pattern = re.compile(
            r"(?<=[.!?])\s+(?=[A-ZÄÖÜ])|(?<=[.!?])$",
            re.UNICODE,
        )

        sentences = pattern.split(text)
        return [s.strip() for s in sentences if s.strip()]

    def ngrams(self, text: str, n: int = 2) -> list[tuple[str, ...]]:
        """Extract n-grams from text.

        Args:
            text: Input text.
            n: N-gram size.

        Returns:
            List of n-gram tuples.
        """
        tokens = self.tokenize_to_strings(text)
        if len(tokens) < n:
            return []
        return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]

    def character_ngrams(self, text: str, n: int = 3) -> list[str]:
        """Extract character n-grams from text.

        Args:
            text: Input text.
            n: N-gram size.

        Returns:
            List of character n-gram strings.
        """
        text = text.lower() if self.config.lowercase else text
        # Remove extra whitespace
        text = " ".join(text.split())
        if len(text) < n:
            return []
        return [text[i : i + n] for i in range(len(text) - n + 1)]

    def to_dict(self) -> dict[str, Any]:
        """Convert tokenizer config to dictionary."""
        return {
            "lowercase": self.config.lowercase,
            "min_length": self.config.min_length,
            "keep_punctuation": self.config.keep_punctuation,
            "keep_numbers": self.config.keep_numbers,
            "language": self.config.language,
        }


def tokenize(text: str, **kwargs: Any) -> list[str]:
    """Convenience function for simple tokenization.

    Args:
        text: Input text.
        **kwargs: Tokenizer configuration options.

    Returns:
        List of token strings.
    """
    config = TokenizerConfig(**kwargs)
    tokenizer = Tokenizer(config)
    return tokenizer.tokenize_to_strings(text)


def word_count(text: str, **kwargs: Any) -> int:
    """Count words in text.

    Args:
        text: Input text.
        **kwargs: Tokenizer configuration options.

    Returns:
        Word count.
    """
    return len(tokenize(text, **kwargs))
