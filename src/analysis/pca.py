"""PCA projection for stylometric visualization."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import numpy as np
from numpy.typing import NDArray
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from stilwerk.src.features.base import FeatureMatrix

@dataclass
class PCAResult:
    coordinates: NDArray[np.float64]
    labels: list[str]
    explained_variance: NDArray[np.float64]
    explained_variance_ratio: NDArray[np.float64]
    components: NDArray[np.float64]
    feature_names: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def n_components(self) -> int:
        return self.coordinates.shape[1]

    def get_coordinates(self, label: str) -> NDArray[np.float64]:
        return self.coordinates[self.labels.index(label)]

    def to_dict(self) -> dict[str, Any]:
        return {"labels": self.labels, "coordinates": self.coordinates.tolist(), "explained_variance_ratio": self.explained_variance_ratio.tolist()}

class PCAProjection:
    def __init__(self, n_components: int = 2, standardize: bool = True):
        self.n_components = n_components
        self.standardize = standardize
        self._pca: PCA | None = None
        self._scaler: StandardScaler | None = None

    def fit_transform(self, features: FeatureMatrix) -> PCAResult:
        values = features.values
        if self.standardize:
            self._scaler = StandardScaler()
            values = self._scaler.fit_transform(values)
        self._pca = PCA(n_components=self.n_components)
        coordinates = self._pca.fit_transform(values)
        return PCAResult(coordinates=coordinates, labels=features.labels.copy(), explained_variance=self._pca.explained_variance_, explained_variance_ratio=self._pca.explained_variance_ratio_, components=self._pca.components_, feature_names=features.feature_names.copy())

def pca_from_distance(distances: Any, n_components: int = 2) -> PCAResult:
    from sklearn.manifold import MDS
    mds = MDS(n_components=n_components, dissimilarity="precomputed", random_state=42, normalized_stress="auto")
    coordinates = mds.fit_transform(distances.values)
    return PCAResult(coordinates=coordinates, labels=distances.labels.copy(), explained_variance=np.zeros(n_components), explained_variance_ratio=np.zeros(n_components), components=np.zeros((n_components, n_components)), metadata={"method": "MDS"})
