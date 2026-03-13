"""Distance measures for stylometric analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.spatial.distance import cdist, pdist, squareform

from stilwerk.src.features.base import FeatureMatrix


class DistanceMeasure(Enum):
    """Available distance measures."""

    BURROWS_DELTA = "burrows_delta"
    COSINE_DELTA = "cosine_delta"
    EDER_DELTA = "eder_delta"
    MANHATTAN = "manhattan"
    EUCLIDEAN = "euclidean"


@dataclass
class DistanceMatrix:
    """A matrix of pairwise distances between texts."""

    values: NDArray[np.float64]
    labels: list[str]
    measure: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, key: tuple[str, str]) -> float:
        """Get distance between two texts by label."""
        i = self.labels.index(key[0])
        j = self.labels.index(key[1])
        return float(self.values[i, j])

    def get(self, label1: str, label2: str) -> float:
        """Get distance between two texts."""
        return self[(label1, label2)]

    def nearest_neighbors(self, label: str, n: int = 5) -> list[tuple[str, float]]:
        """Find the N nearest neighbors to a text."""
        idx = self.labels.index(label)
        distances = self.values[idx]
        sorted_indices = np.argsort(distances)
        neighbors = []
        for i in sorted_indices:
            if self.labels[i] != label:
                neighbors.append((self.labels[i], float(distances[i])))
                if len(neighbors) >= n:
                    break
        return neighbors

    def farthest_from(self, label: str) -> tuple[str, float]:
        """Find the farthest text from a given text."""
        idx = self.labels.index(label)
        distances = self.values[idx]
        farthest_idx = np.argmax(
            np.where(np.arange(len(distances)) != idx, distances, -np.inf)
        )
        return self.labels[farthest_idx], float(distances[farthest_idx])

    def average_distance(self, label: str) -> float:
        """Calculate average distance from a text to all others."""
        idx = self.labels.index(label)
        distances = self.values[idx]
        other_distances = distances[np.arange(len(distances)) != idx]
        return float(np.mean(other_distances))

    def to_condensed(self) -> NDArray[np.float64]:
        """Convert to condensed distance vector (for scipy clustering)."""
        n = len(self.labels)
        condensed = []
        for i in range(n):
            for j in range(i + 1, n):
                condensed.append(self.values[i, j])
        return np.array(condensed)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "labels": self.labels,
            "measure": self.measure,
            "values": self.values.tolist(),
            "metadata": self.metadata,
        }

    def save_csv(self, path: str) -> None:
        """Save to CSV file."""
        import pandas as pd
        df = pd.DataFrame(self.values, index=self.labels, columns=self.labels)
        df.to_csv(path)

    @classmethod
    def from_csv(cls, path: str, measure: str = "") -> "DistanceMatrix":
        """Load from CSV file."""
        import pandas as pd
        df = pd.read_csv(path, index_col=0)
        return cls(values=df.values, labels=list(df.index), measure=measure)


class DistanceCalculator:
    """Calculate distances between texts using various measures."""

    def __init__(
        self,
        measure: str | DistanceMeasure = DistanceMeasure.BURROWS_DELTA,
        z_score_normalize: bool = True,
    ):
        if isinstance(measure, str):
            measure = DistanceMeasure(measure)
        self.measure = measure
        self.z_score_normalize = z_score_normalize

    def calculate(self, features: FeatureMatrix) -> DistanceMatrix:
        """Calculate pairwise distances for a feature matrix."""
        values = features.values

        if self.z_score_normalize and self.measure in {
            DistanceMeasure.BURROWS_DELTA,
            DistanceMeasure.COSINE_DELTA,
            DistanceMeasure.EDER_DELTA,
        }:
            mean = np.mean(values, axis=0)
            std = np.std(values, axis=0)
            std = np.where(std == 0, 1, std)
            values = (values - mean) / std

        if self.measure == DistanceMeasure.BURROWS_DELTA:
            distances = self._burrows_delta(values)
        elif self.measure == DistanceMeasure.COSINE_DELTA:
            distances = self._cosine_delta(values)
        elif self.measure == DistanceMeasure.EDER_DELTA:
            distances = self._eder_delta(values)
        elif self.measure == DistanceMeasure.MANHATTAN:
            distances = squareform(pdist(values, metric="cityblock"))
        elif self.measure == DistanceMeasure.EUCLIDEAN:
            distances = squareform(pdist(values, metric="euclidean"))
        else:
            raise ValueError(f"Unknown measure: {self.measure}")

        return DistanceMatrix(
            values=distances,
            labels=features.labels.copy(),
            measure=self.measure.value,
            metadata={"z_score_normalized": self.z_score_normalize, "feature_count": len(features.feature_names)},
        )

    def _burrows_delta(self, values: NDArray[np.float64]) -> NDArray[np.float64]:
        """Calculate Burrows' Delta."""
        n = len(values)
        distances = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                d = np.mean(np.abs(values[i] - values[j]))
                distances[i, j] = d
                distances[j, i] = d
        return distances

    def _cosine_delta(self, values: NDArray[np.float64]) -> NDArray[np.float64]:
        """Calculate Cosine Delta."""
        condensed = pdist(values, metric="cosine")
        return squareform(condensed)

    def _eder_delta(self, values: NDArray[np.float64]) -> NDArray[np.float64]:
        """Calculate Eder's Simple Distance."""
        n = len(values)
        num_features = values.shape[1]
        distances = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                d = np.sqrt(np.sum((values[i] - values[j]) ** 2) / num_features)
                distances[i, j] = d
                distances[j, i] = d
        return distances

    def calculate_between(
        self, features1: FeatureMatrix, features2: FeatureMatrix
    ) -> NDArray[np.float64]:
        """Calculate distances between two sets of texts."""
        values1 = features1.values
        values2 = features2.values

        if self.z_score_normalize:
            combined = np.vstack([values1, values2])
            mean = np.mean(combined, axis=0)
            std = np.std(combined, axis=0)
            std = np.where(std == 0, 1, std)
            values1 = (values1 - mean) / std
            values2 = (values2 - mean) / std

        if self.measure == DistanceMeasure.BURROWS_DELTA:
            return cdist(values1, values2, metric="cityblock") / values1.shape[1]
        elif self.measure == DistanceMeasure.COSINE_DELTA:
            return cdist(values1, values2, metric="cosine")
        elif self.measure == DistanceMeasure.EUCLIDEAN:
            return cdist(values1, values2, metric="euclidean")
        else:
            return cdist(values1, values2, metric="cityblock")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {"measure": self.measure.value, "z_score_normalize": self.z_score_normalize}
