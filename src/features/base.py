"""Base classes for feature extraction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from numpy.typing import NDArray


@dataclass
class FeatureVector:
    """A vector of features extracted from text.

    Attributes:
        values: The feature values as a numpy array.
        feature_names: Names of the features.
        label: Label for this vector (e.g., document/voice ID).
        metadata: Additional metadata.
    """

    values: NDArray[np.float64]
    feature_names: list[str]
    label: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __len__(self) -> int:
        """Return number of features."""
        return len(self.values)

    def __getitem__(self, key: str | int) -> float:
        """Get feature value by name or index."""
        if isinstance(key, str):
            idx = self.feature_names.index(key)
            return float(self.values[idx])
        return float(self.values[key])

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "label": self.label,
            "feature_count": len(self.values),
            "features": dict(zip(self.feature_names, self.values.tolist())),
            "metadata": self.metadata,
        }

    def to_sparse_dict(self, threshold: float = 0.0) -> dict[str, float]:
        """Convert to sparse dictionary, omitting values below threshold."""
        return {
            name: float(val)
            for name, val in zip(self.feature_names, self.values)
            if abs(val) > threshold
        }


@dataclass
class FeatureMatrix:
    """A matrix of features for multiple texts.

    Attributes:
        values: 2D numpy array (rows=texts, cols=features).
        feature_names: Names of the features.
        labels: Labels for each row (text).
        metadata: Additional metadata.
    """

    values: NDArray[np.float64]
    feature_names: list[str]
    labels: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __len__(self) -> int:
        """Return number of texts."""
        return len(self.values)

    @property
    def shape(self) -> tuple[int, int]:
        """Return matrix shape (n_texts, n_features)."""
        return self.values.shape  # type: ignore

    def get_row(self, label: str) -> FeatureVector:
        """Get feature vector by label."""
        idx = self.labels.index(label)
        return FeatureVector(
            values=self.values[idx],
            feature_names=self.feature_names,
            label=label,
        )

    def get_column(self, feature: str) -> NDArray[np.float64]:
        """Get all values for a specific feature."""
        idx = self.feature_names.index(feature)
        return self.values[:, idx]

    def z_score_normalize(self) -> "FeatureMatrix":
        """Return a new matrix with z-score normalized features."""
        mean = np.mean(self.values, axis=0)
        std = np.std(self.values, axis=0)
        # Avoid division by zero
        std = np.where(std == 0, 1, std)
        normalized = (self.values - mean) / std

        return FeatureMatrix(
            values=normalized,
            feature_names=self.feature_names.copy(),
            labels=self.labels.copy(),
            metadata={**self.metadata, "normalized": "z_score"},
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "shape": list(self.shape),
            "labels": self.labels,
            "feature_names": self.feature_names,
            "values": self.values.tolist(),
            "metadata": self.metadata,
        }

    def to_dataframe(self) -> Any:
        """Convert to pandas DataFrame."""
        import pandas as pd

        return pd.DataFrame(
            self.values,
            index=self.labels,
            columns=self.feature_names,
        )

    @classmethod
    def from_vectors(cls, vectors: list[FeatureVector]) -> "FeatureMatrix":
        """Create matrix from a list of feature vectors."""
        if not vectors:
            raise ValueError("Cannot create matrix from empty list")

        feature_names = vectors[0].feature_names
        labels = [v.label for v in vectors]
        values = np.array([v.values for v in vectors])

        return cls(
            values=values,
            feature_names=feature_names,
            labels=labels,
        )


class FeatureExtractor(ABC):
    """Abstract base class for feature extractors."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this extractor."""
        ...

    @property
    @abstractmethod
    def feature_names(self) -> list[str]:
        """Return the names of features this extractor produces."""
        ...

    @abstractmethod
    def extract(self, text: str) -> FeatureVector:
        """Extract features from a single text.

        Args:
            text: Input text.

        Returns:
            FeatureVector with extracted features.
        """
        ...

    def extract_many(self, texts: dict[str, str]) -> FeatureMatrix:
        """Extract features from multiple texts.

        Args:
            texts: Dictionary mapping labels to text content.

        Returns:
            FeatureMatrix with all extracted features.
        """
        vectors = []
        for label, text in texts.items():
            vec = self.extract(text)
            vec.label = label
            vectors.append(vec)

        return FeatureMatrix.from_vectors(vectors)

    def to_dict(self) -> dict[str, Any]:
        """Convert extractor configuration to dictionary."""
        return {
            "name": self.name,
            "feature_count": len(self.feature_names),
            "feature_names": self.feature_names,
        }


class CompositeExtractor(FeatureExtractor):
    """Combines multiple extractors into one."""

    def __init__(self, extractors: list[FeatureExtractor]):
        """Initialize with a list of extractors.

        Args:
            extractors: List of feature extractors to combine.
        """
        self.extractors = extractors

    @property
    def name(self) -> str:
        """Return combined name."""
        return "composite"

    @property
    def feature_names(self) -> list[str]:
        """Return all feature names from all extractors."""
        names = []
        for extractor in self.extractors:
            for name in extractor.feature_names:
                prefix = extractor.name
                names.append(f"{prefix}:{name}")
        return names

    def extract(self, text: str) -> FeatureVector:
        """Extract features using all extractors.

        Args:
            text: Input text.

        Returns:
            Combined FeatureVector.
        """
        all_values: list[float] = []
        all_names: list[str] = []

        for extractor in self.extractors:
            vec = extractor.extract(text)
            prefix = extractor.name
            for name, val in zip(vec.feature_names, vec.values):
                all_names.append(f"{prefix}:{name}")
                all_values.append(float(val))

        return FeatureVector(
            values=np.array(all_values),
            feature_names=all_names,
        )
