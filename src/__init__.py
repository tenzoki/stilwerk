"""Stilwerk - Style analysis and transformation toolkit."""

__version__ = "0.2.0"

# Core imports for convenience
from stilwerk.src.config import load_config, ProjectConfig
from stilwerk.src.corpus import Corpus, Document
from stilwerk.src.analysis import analyze, AnalysisResult

__all__ = [
    "__version__",
    "load_config",
    "ProjectConfig",
    "Corpus",
    "Document",
    "analyze",
    "AnalysisResult",
]
