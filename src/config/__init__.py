"""Configuration management for stilwerk projects."""

from stilwerk.src.config.loader import load_config, save_config, merge_configs
from stilwerk.src.config.schema import (
    ProjectConfig,
    CorpusConfig,
    FeaturesConfig,
    DistanceConfig,
    ClusteringConfig,
    StyloExportConfig,
    VisualizationConfig,
)

__all__ = [
    "load_config",
    "save_config",
    "merge_configs",
    "ProjectConfig",
    "CorpusConfig",
    "FeaturesConfig",
    "DistanceConfig",
    "ClusteringConfig",
    "StyloExportConfig",
    "VisualizationConfig",
]
