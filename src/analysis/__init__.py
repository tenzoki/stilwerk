"""Analysis components: distance measures, clustering, PCA."""

from stilwerk.src.analysis.distance import DistanceCalculator, DistanceMatrix, DistanceMeasure
from stilwerk.src.analysis.clustering import HierarchicalClustering, ClusteringResult, LinkageMethod
from stilwerk.src.analysis.pca import PCAProjection, PCAResult, pca_from_distance
from stilwerk.src.analysis.results import AnalysisResult, QueryResult, analyze

__all__ = [
    "DistanceCalculator",
    "DistanceMatrix",
    "DistanceMeasure",
    "HierarchicalClustering",
    "ClusteringResult",
    "LinkageMethod",
    "PCAProjection",
    "PCAResult",
    "pca_from_distance",
    "AnalysisResult",
    "QueryResult",
    "analyze",
]
