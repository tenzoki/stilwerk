"""Feature extraction for stylometric analysis."""

from stilwerk.src.features.base import FeatureExtractor, CompositeExtractor, FeatureMatrix, FeatureVector
from stilwerk.src.features.function_words import FunctionWordExtractor, MostFrequentWordsExtractor, DEFAULT_GERMAN_FUNCTION_WORDS
from stilwerk.src.features.lexical import LexicalExtractor
from stilwerk.src.features.punctuation import PunctuationExtractor, SpecialCharacterExtractor
from stilwerk.src.features.factory import create_extractor, create_extractor_for_corpus, get_function_words

__all__ = [
    # Base classes
    "FeatureExtractor",
    "CompositeExtractor",
    "FeatureMatrix",
    "FeatureVector",
    # Extractors
    "FunctionWordExtractor",
    "MostFrequentWordsExtractor",
    "LexicalExtractor",
    "PunctuationExtractor",
    "SpecialCharacterExtractor",
    # Data
    "DEFAULT_GERMAN_FUNCTION_WORDS",
    # Factory
    "create_extractor",
    "create_extractor_for_corpus",
    "get_function_words",
]
