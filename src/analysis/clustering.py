"""Hierarchical clustering for stylometric analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.cluster.hierarchy import fcluster, linkage

from stilwerk.src.analysis.distance import DistanceMatrix


class LinkageMethod(Enum):
    """Linkage methods for hierarchical clustering."""

    WARD = "ward"
    COMPLETE = "complete"
    AVERAGE = "average"
    SINGLE = "single"
    WEIGHTED = "weighted"


@dataclass
class ClusterNode:
    """A node in the cluster hierarchy."""

    id: int
    label: str | None = None
    left: "ClusterNode | None" = None
    right: "ClusterNode | None" = None
    distance: float = 0.0
    count: int = 1

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def get_leaves(self) -> list["ClusterNode"]:
        if self.is_leaf:
            return [self]
        leaves = []
        if self.left:
            leaves.extend(self.left.get_leaves())
        if self.right:
            leaves.extend(self.right.get_leaves())
        return leaves

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "id": self.id,
            "label": self.label,
            "distance": self.distance,
            "count": self.count,
            "is_leaf": self.is_leaf,
        }
        if not self.is_leaf:
            result["left"] = self.left.to_dict() if self.left else None
            result["right"] = self.right.to_dict() if self.right else None
        return result


@dataclass
class ClusteringResult:
    """Result of hierarchical clustering."""

    linkage_matrix: NDArray[np.float64]
    labels: list[str]
    method: str = ""
    root: ClusterNode | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def cut_tree(self, n_clusters: int) -> dict[str, int]:
        """Cut the tree to produce N clusters."""
        cluster_ids = fcluster(self.linkage_matrix, n_clusters, criterion="maxclust")
        return dict(zip(self.labels, cluster_ids))

    def cut_at_distance(self, threshold: float) -> dict[str, int]:
        """Cut the tree at a distance threshold."""
        cluster_ids = fcluster(self.linkage_matrix, threshold, criterion="distance")
        return dict(zip(self.labels, cluster_ids))

    def get_merge_order(self) -> list[tuple[str, str, float]]:
        """Get the order in which clusters were merged."""
        n = len(self.labels)
        cluster_labels: dict[int, list[str]] = {i: [self.labels[i]] for i in range(n)}
        merges = []
        for i, row in enumerate(self.linkage_matrix):
            c1, c2, dist, _ = row
            c1, c2 = int(c1), int(c2)
            labels1 = cluster_labels.get(c1, [])
            labels2 = cluster_labels.get(c2, [])
            l1 = labels1[0] if labels1 else f"cluster_{c1}"
            l2 = labels2[0] if labels2 else f"cluster_{c2}"
            merges.append((l1, l2, float(dist)))
            new_cluster_id = n + i
            cluster_labels[new_cluster_id] = labels1 + labels2
        return merges

    def to_newick(self) -> str:
        """Convert to Newick tree format."""
        if self.root is None:
            return ""

        def _to_newick(node: ClusterNode) -> str:
            if node.is_leaf:
                return node.label or f"node_{node.id}"
            left_str = _to_newick(node.left) if node.left else ""
            right_str = _to_newick(node.right) if node.right else ""
            return f"({left_str}:{node.distance:.4f},{right_str}:{node.distance:.4f})"

        return _to_newick(self.root) + ";"

    def to_dict(self) -> dict[str, Any]:
        return {
            "labels": self.labels,
            "method": self.method,
            "linkage_matrix": self.linkage_matrix.tolist(),
            "tree": self.root.to_dict() if self.root else None,
            "metadata": self.metadata,
        }


class HierarchicalClustering:
    """Perform hierarchical clustering on distance matrices."""

    def __init__(self, method: str | LinkageMethod = LinkageMethod.WARD):
        if isinstance(method, str):
            method = LinkageMethod(method)
        self.method = method

    def cluster(self, distances: DistanceMatrix) -> ClusteringResult:
        """Perform hierarchical clustering."""
        condensed = distances.to_condensed()
        Z = linkage(condensed, method=self.method.value)
        root = self._build_tree(Z, distances.labels)

        return ClusteringResult(
            linkage_matrix=Z,
            labels=distances.labels.copy(),
            method=self.method.value,
            root=root,
            metadata={"distance_measure": distances.measure},
        )

    def _build_tree(self, Z: NDArray[np.float64], labels: list[str]) -> ClusterNode:
        """Build cluster tree from linkage matrix."""
        n = len(labels)
        nodes: dict[int, ClusterNode] = {}

        for i, label in enumerate(labels):
            nodes[i] = ClusterNode(id=i, label=label, count=1)

        for i, row in enumerate(Z):
            c1, c2, dist, count = row
            c1, c2, count = int(c1), int(c2), int(count)
            node = ClusterNode(
                id=n + i,
                left=nodes[c1],
                right=nodes[c2],
                distance=float(dist),
                count=count,
            )
            nodes[n + i] = node

        return nodes[2 * n - 2]

    def cluster_from_features(
        self, features: Any, distance_measure: str = "burrows_delta"
    ) -> ClusteringResult:
        """Cluster directly from features."""
        from stilwerk.src.analysis.distance import DistanceCalculator

        calculator = DistanceCalculator(measure=distance_measure)
        distances = calculator.calculate(features)
        return self.cluster(distances)

    def to_dict(self) -> dict[str, Any]:
        return {"method": self.method.value}
