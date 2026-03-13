"""Pydantic models for stilwerk configuration validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator


class CorpusConfig(BaseModel):
    """Configuration for corpus input."""

    directories: list[str] = Field(
        default_factory=list, description="Directories containing corpus texts"
    )
    files: list[str] = Field(
        default_factory=list, description="Individual corpus files"
    )
    pattern: str = Field(
        default="*.txt", description="Glob pattern for finding files in directories"
    )


class FeaturesConfig(BaseModel):
    """Configuration for feature extraction."""

    method: str = Field(
        default="mfw",
        description="Feature extraction method: mfw, function_words, lexical, punctuation, all",
    )
    mfw_count: int = Field(
        default=100, description="Number of most frequent words (for mfw method)"
    )
    function_words_file: str | None = Field(
        default=None, description="Path to function words file (uses language defaults if null)"
    )
    ngram_size: int = Field(default=1, description="N-gram size for feature extraction")
    include_punctuation: bool = Field(
        default=True, description="Include punctuation features"
    )

    @field_validator("method")
    @classmethod
    def validate_method(cls, v: str) -> str:
        """Validate feature extraction method."""
        valid = {"mfw", "function_words", "lexical", "punctuation", "all"}
        if v not in valid:
            raise ValueError(f"Invalid feature method: {v}. Must be one of {valid}")
        return v


class DistanceConfig(BaseModel):
    """Configuration for distance calculation."""

    measure: str = Field(
        default="burrows_delta",
        description="Distance measure: burrows_delta, cosine_delta, eder_delta, manhattan, euclidean",
    )
    normalize: bool = Field(
        default=True, description="Apply z-score normalization to features"
    )

    @field_validator("measure")
    @classmethod
    def validate_measure(cls, v: str) -> str:
        """Validate distance measure."""
        valid = {"burrows_delta", "cosine_delta", "eder_delta", "manhattan", "euclidean"}
        if v not in valid:
            raise ValueError(f"Invalid distance measure: {v}. Must be one of {valid}")
        return v


class ClusteringConfig(BaseModel):
    """Configuration for clustering."""

    method: str = Field(
        default="ward",
        description="Linkage method: ward, complete, average, single, weighted",
    )

    @field_validator("method")
    @classmethod
    def validate_method(cls, v: str) -> str:
        """Validate linkage method."""
        valid = {"ward", "complete", "average", "single", "weighted"}
        if v not in valid:
            raise ValueError(f"Invalid linkage method: {v}. Must be one of {valid}")
        return v


class StyloExportConfig(BaseModel):
    """Configuration for R stylo export."""

    output_dir: str = Field(
        default="./corpus/stylo", description="Output directory for stylo corpus"
    )
    mfw_min: int = Field(default=50, description="Minimum most frequent words")
    mfw_max: int = Field(default=200, description="Maximum most frequent words")
    mfw_incr: int = Field(default=50, description="MFW increment step")
    sample_size: int = Field(default=5000, description="Sample size for analysis")
    corpus_lang: str = Field(default="German", description="Corpus language")
    analyzed_features: str = Field(
        default="w", description="Features to analyze: 'w' (words) or 'c' (characters)"
    )


class VisualizationConfig(BaseModel):
    """Configuration for visualization output."""

    format: str = Field(default="png", description="Output format: png, svg, pdf")
    dpi: int = Field(default=150, description="DPI for raster formats")
    width: int = Field(default=12, description="Figure width in inches")
    height: int = Field(default=8, description="Figure height in inches")
    font_size: int = Field(default=10, description="Base font size")


class ProjectConfig(BaseModel):
    """Complete project configuration."""

    name: str = Field(default="Untitled", description="Project name")
    language: str = Field(default="de", description="Primary language code (de, en, etc.)")
    output_dir: str = Field(default="./output", description="Output directory")

    corpus: CorpusConfig = Field(
        default_factory=CorpusConfig, description="Corpus input settings"
    )

    query_texts: list[str] = Field(
        default_factory=list, description="Paths to query texts for attribution"
    )

    features: FeaturesConfig = Field(
        default_factory=FeaturesConfig, description="Feature extraction settings"
    )

    distance: DistanceConfig = Field(
        default_factory=DistanceConfig, description="Distance calculation settings"
    )

    clustering: ClusteringConfig = Field(
        default_factory=ClusteringConfig, description="Clustering settings"
    )

    stylo_export: StyloExportConfig = Field(
        default_factory=StyloExportConfig, description="R stylo export settings"
    )

    visualization: VisualizationConfig = Field(
        default_factory=VisualizationConfig, description="Visualization settings"
    )

    def resolve_path(self, path: str, base_dir: Path | None = None) -> Path:
        """Resolve a relative path against base directory.

        Args:
            path: Path to resolve.
            base_dir: Base directory for relative paths.

        Returns:
            Resolved absolute path.
        """
        p = Path(path)
        if p.is_absolute():
            return p
        if base_dir is None:
            base_dir = Path(".")
        return base_dir / p

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return self.model_dump()
