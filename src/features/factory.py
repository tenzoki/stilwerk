"""Feature extractor factory for creating extractors from configuration."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from stilwerk.src.features.base import FeatureExtractor, CompositeExtractor
from stilwerk.src.features.function_words import (
    FunctionWordExtractor,
    MostFrequentWordsExtractor,
    DEFAULT_GERMAN_FUNCTION_WORDS,
)
from stilwerk.src.features.lexical import LexicalExtractor
from stilwerk.src.features.punctuation import PunctuationExtractor

if TYPE_CHECKING:
    from stilwerk.src.config.schema import FeaturesConfig
    from stilwerk.src.corpus.loader import Corpus


# Default English function words
DEFAULT_ENGLISH_FUNCTION_WORDS = [
    "the", "of", "and", "to", "a", "in", "that", "is", "was", "he",
    "for", "it", "with", "as", "his", "on", "be", "at", "by", "i",
    "this", "had", "not", "are", "but", "from", "or", "have", "an", "they",
    "which", "one", "you", "were", "her", "all", "she", "there", "would", "their",
    "we", "him", "been", "has", "when", "who", "will", "more", "no", "if",
    "out", "so", "said", "what", "up", "its", "about", "into", "than", "them",
    "can", "only", "other", "new", "some", "could", "time", "these", "two", "may",
    "then", "do", "first", "any", "my", "now", "such", "like", "our", "over",
    "man", "me", "even", "most", "made", "after", "also", "did", "many", "before",
    "must", "through", "back", "years", "where", "much", "your", "way", "well", "down",
]

# Language to function words mapping
FUNCTION_WORDS_BY_LANGUAGE = {
    "de": DEFAULT_GERMAN_FUNCTION_WORDS,
    "en": DEFAULT_ENGLISH_FUNCTION_WORDS,
}


def get_function_words(language: str) -> list[str]:
    """Get default function words for a language.

    Args:
        language: Language code (de, en).

    Returns:
        List of function words.

    Raises:
        ValueError: If language is not supported.
    """
    if language not in FUNCTION_WORDS_BY_LANGUAGE:
        raise ValueError(
            f"No function words for language '{language}'. "
            f"Supported: {list(FUNCTION_WORDS_BY_LANGUAGE.keys())}"
        )
    return FUNCTION_WORDS_BY_LANGUAGE[language].copy()


def create_extractor(
    config: "FeaturesConfig",
    corpus: "Corpus | None" = None,
    language: str = "de",
) -> FeatureExtractor:
    """Create a feature extractor from configuration.

    Args:
        config: Features configuration.
        corpus: Corpus for fitting MFW extractor (required if method is 'mfw').
        language: Language code for function word defaults.

    Returns:
        Configured FeatureExtractor.

    Raises:
        ValueError: If method is 'mfw' and corpus is None.
    """
    method = config.method

    if method == "mfw":
        if corpus is None:
            raise ValueError("Corpus required for MFW extractor")

        extractor = MostFrequentWordsExtractor(n_words=config.mfw_count)
        texts = {doc.label: doc.text for doc in corpus}
        extractor.fit(texts)
        return extractor

    elif method == "function_words":
        if config.function_words_file:
            return FunctionWordExtractor.from_file(Path(config.function_words_file))
        else:
            words = get_function_words(language)
            return FunctionWordExtractor(function_words=words)

    elif method == "lexical":
        return LexicalExtractor()

    elif method == "punctuation":
        return PunctuationExtractor()

    elif method == "all":
        if corpus is None:
            raise ValueError("Corpus required for 'all' method (MFW needs fitting)")

        mfw = MostFrequentWordsExtractor(n_words=config.mfw_count)
        texts = {doc.label: doc.text for doc in corpus}
        mfw.fit(texts)

        return CompositeExtractor([
            mfw,
            LexicalExtractor(),
            PunctuationExtractor(),
        ])

    else:
        raise ValueError(f"Unknown feature method: {method}")


def create_extractor_for_corpus(
    corpus: "Corpus",
    method: str = "mfw",
    mfw_count: int = 100,
    language: str = "de",
) -> FeatureExtractor:
    """Convenience function to create an extractor for a corpus.

    Args:
        corpus: Corpus to analyze.
        method: Feature extraction method.
        mfw_count: Number of MFW (if using mfw method).
        language: Language code for function word defaults.

    Returns:
        Fitted FeatureExtractor.
    """
    from stilwerk.src.config.schema import FeaturesConfig

    config = FeaturesConfig(method=method, mfw_count=mfw_count)
    return create_extractor(config, corpus=corpus, language=language)
