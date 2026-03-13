"""Analysis result container."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, TYPE_CHECKING
import numpy as np
from stilwerk.src.analysis.clustering import ClusteringResult
from stilwerk.src.analysis.distance import DistanceMatrix
from stilwerk.src.analysis.pca import PCAResult
from stilwerk.src.features.base import FeatureMatrix, FeatureExtractor

if TYPE_CHECKING:
    from stilwerk.src.config.schema import ProjectConfig
    from stilwerk.src.corpus.loader import Corpus

@dataclass
class QueryResult:
    label: str
    nearest_neighbors: list[tuple[str, float]] = field(default_factory=list)
    cluster: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"label": self.label, "nearest_neighbors": [{"label": l, "distance": d} for l, d in self.nearest_neighbors], "attribution": self.nearest_neighbors[0][0] if self.nearest_neighbors else None}

@dataclass
class AnalysisResult:
    features: FeatureMatrix | None = None
    distances: DistanceMatrix | None = None
    clustering: ClusteringResult | None = None
    pca: PCAResult | None = None
    query_results: dict[str, QueryResult] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    labels: list[str] = field(default_factory=list)
    extractor_name: str = ""
    files: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result = {"timestamp": self.timestamp, "labels": self.labels}
        if self.features: result["features"] = self.features.to_dict()
        if self.distances: result["distances"] = self.distances.to_dict()
        if self.clustering: result["clustering"] = self.clustering.to_dict()
        if self.pca: result["pca"] = self.pca.to_dict()
        if self.query_results: result["query_results"] = {k: v.to_dict() for k, v in self.query_results.items()}
        return result

    def save_json(self, path: str | Path) -> None:
        import json
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

def analyze(config: "ProjectConfig", corpus: "Corpus | None" = None, query_texts: dict[str, str] | None = None, extractor: FeatureExtractor | None = None) -> AnalysisResult:
    from stilwerk.src.analysis.clustering import HierarchicalClustering
    from stilwerk.src.analysis.distance import DistanceCalculator
    from stilwerk.src.analysis.pca import PCAProjection
    from stilwerk.src.corpus.loader import Corpus
    from stilwerk.src.features.factory import create_extractor

    if corpus is None:
        corpus = Corpus.from_config(config)
    texts = {doc.label: doc.text for doc in corpus}
    if query_texts is None and config.query_texts:
        query_texts = {}
        for p in config.query_texts:
            path = Path(p)
            if path.exists(): query_texts[path.stem] = path.read_text(encoding="utf-8")
    if extractor is None:
        extractor = create_extractor(config.features, corpus=corpus, language=config.language)
    features = extractor.extract_many(texts)
    calculator = DistanceCalculator(measure=config.distance.measure, z_score_normalize=config.distance.normalize)
    distances = calculator.calculate(features)
    clustering = HierarchicalClustering(method=config.clustering.method).cluster(distances)
    pca = PCAProjection(n_components=2).fit_transform(features)
    result = AnalysisResult(features=features, distances=distances, clustering=clustering, pca=pca, labels=list(texts.keys()), extractor_name=extractor.name)
    if query_texts:
        for label, text in query_texts.items():
            qv = extractor.extract(text)
            dists = [(cl, float(np.mean(np.abs(qv.values - features.values[i])))) for i, cl in enumerate(features.labels)]
            dists.sort(key=lambda x: x[1])
            result.query_results[label] = QueryResult(label=label, nearest_neighbors=dists[:10])
    return result
