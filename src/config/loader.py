"""YAML configuration loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from stilwerk.src.config.schema import ProjectConfig


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file and return its contents as a dictionary.

    Args:
        path: Path to the YAML file.

    Returns:
        Dictionary containing the YAML contents.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the file is not valid YAML.
    """
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data if data is not None else {}


def load_config(path: str | Path) -> ProjectConfig:
    """Load and validate a project configuration from YAML.

    Args:
        path: Path to the configuration YAML file.

    Returns:
        Validated ProjectConfig instance.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        pydantic.ValidationError: If the configuration is invalid.
    """
    path = Path(path)
    data = load_yaml(path)

    # Store the config file's directory for resolving relative paths
    config_dir = path.parent.absolute()

    # Resolve function words file path if specified
    if "features" in data and "function_words_file" in data["features"]:
        fw = data["features"]["function_words_file"]
        if fw and not Path(fw).is_absolute():
            data["features"]["function_words_file"] = str(config_dir / fw)

    # Create and validate the config
    config = ProjectConfig(**data)

    return config


def load_function_words(path: str | Path) -> list[str]:
    """Load function words from a YAML file.

    Args:
        path: Path to the function words YAML file.

    Returns:
        List of function words.
    """
    path = Path(path)
    data = load_yaml(path)
    return data.get("words", [])


def save_config(config: ProjectConfig, path: str | Path) -> None:
    """Save a project configuration to YAML.

    Args:
        config: ProjectConfig instance to save.
        path: Path to save the configuration to.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = config.model_dump(exclude_none=True)

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def merge_configs(base: ProjectConfig, override: dict[str, Any]) -> ProjectConfig:
    """Merge override values into a base configuration.

    Args:
        base: Base ProjectConfig instance.
        override: Dictionary of values to override.

    Returns:
        New ProjectConfig with merged values.
    """
    base_dict = base.model_dump()

    def deep_merge(d1: dict, d2: dict) -> dict:
        """Deep merge two dictionaries."""
        result = d1.copy()
        for k, v in d2.items():
            if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = deep_merge(result[k], v)
            else:
                result[k] = v
        return result

    merged = deep_merge(base_dict, override)
    return ProjectConfig(**merged)
