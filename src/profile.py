"""Style profile loading, inheritance, and validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Rule:
    """A whitelist or blacklist rule."""

    id: str
    name: str = ""
    target: tuple[float, float] | None = None  # [min, max] for metrics
    max: float | None = None  # For blacklist upper bounds
    instruction: str = ""
    examples: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Rule":
        """Create Rule from dictionary."""
        target = None
        if "target" in data:
            t = data["target"]
            target = (float(t[0]), float(t[1]))

        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            target=target,
            max=data.get("max"),
            instruction=data.get("instruction", ""),
            examples=data.get("examples", []),
        )


@dataclass
class Example:
    """A style example or anti-example."""

    path: str
    note: str = ""
    extract: bool = True  # Auto-extract metrics
    include: bool = True  # Include excerpt in prompt
    weight: float = 1.0  # Weight for averaging metrics

    # Extracted data (populated by extract.py)
    metrics: dict[str, float] = field(default_factory=dict)
    excerpt: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Example":
        """Create Example from dictionary."""
        return cls(
            path=data.get("path", ""),
            note=data.get("note", ""),
            extract=data.get("extract", True),
            include=data.get("include", True),
            weight=data.get("weight", 1.0),
        )


@dataclass
class Settings:
    """Profile settings."""

    fit_threshold: float = 0.85
    max_iterations: int = 5
    excerpt_length: int = 500

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Settings":
        """Create Settings from dictionary."""
        return cls(
            fit_threshold=data.get("fit_threshold", 0.85),
            max_iterations=data.get("max_iterations", 5),
            excerpt_length=data.get("excerpt_length", 500),
        )


@dataclass
class StyleProfile:
    """Complete style profile with rules, examples, and settings."""

    name: str
    description: str = ""
    extends: str | None = None
    whitelist: list[Rule] = field(default_factory=list)
    blacklist: list[Rule] = field(default_factory=list)
    examples: list[Example] = field(default_factory=list)
    anti_examples: list[Example] = field(default_factory=list)
    settings: Settings = field(default_factory=Settings)

    # Source path (for resolving relative paths)
    _path: Path | None = None

    @classmethod
    def load(cls, path: Path, profiles_dir: Path | None = None) -> "StyleProfile":
        """Load profile from YAML with inheritance resolution.

        Args:
            path: Path to profile YAML file.
            profiles_dir: Directory to search for base profiles.

        Returns:
            Fully resolved StyleProfile.
        """
        path = Path(path)
        if profiles_dir is None:
            profiles_dir = path.parent

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        profile = cls._from_dict(data, path)

        # Resolve inheritance
        if profile.extends:
            base_path = profiles_dir / f"{profile.extends}.yaml"
            if not base_path.exists():
                raise FileNotFoundError(f"Base profile not found: {base_path}")

            base = cls.load(base_path, profiles_dir)
            profile = profile._merge_with_base(base)

        return profile

    @classmethod
    def _from_dict(cls, data: dict[str, Any], path: Path) -> "StyleProfile":
        """Create profile from dictionary."""
        whitelist = [Rule.from_dict(r) for r in data.get("whitelist", [])]
        blacklist = [Rule.from_dict(r) for r in data.get("blacklist", [])]
        examples = [Example.from_dict(e) for e in data.get("examples", [])]
        anti_examples = [Example.from_dict(e) for e in data.get("anti_examples", [])]
        settings = Settings.from_dict(data.get("settings", {}))

        return cls(
            name=data.get("name", path.stem),
            description=data.get("description", ""),
            extends=data.get("extends"),
            whitelist=whitelist,
            blacklist=blacklist,
            examples=examples,
            anti_examples=anti_examples,
            settings=settings,
            _path=path,
        )

    def _merge_with_base(self, base: "StyleProfile") -> "StyleProfile":
        """Merge this profile with a base profile.

        Child rules override base rules with same ID.
        Examples are concatenated.
        Settings are merged (child overrides).
        """
        # Build ID -> Rule maps
        base_whitelist = {r.id: r for r in base.whitelist}
        base_blacklist = {r.id: r for r in base.blacklist}

        # Override with child rules
        for rule in self.whitelist:
            base_whitelist[rule.id] = rule
        for rule in self.blacklist:
            base_blacklist[rule.id] = rule

        # Merge settings
        merged_settings = Settings(
            fit_threshold=self.settings.fit_threshold or base.settings.fit_threshold,
            max_iterations=self.settings.max_iterations or base.settings.max_iterations,
            excerpt_length=self.settings.excerpt_length or base.settings.excerpt_length,
        )

        return StyleProfile(
            name=self.name,
            description=self.description or base.description,
            extends=None,  # Inheritance resolved
            whitelist=list(base_whitelist.values()),
            blacklist=list(base_blacklist.values()),
            examples=base.examples + self.examples,
            anti_examples=base.anti_examples + self.anti_examples,
            settings=merged_settings,
            _path=self._path,
        )

    def get_whitelist_rule(self, rule_id: str) -> Rule | None:
        """Get whitelist rule by ID."""
        for rule in self.whitelist:
            if rule.id == rule_id:
                return rule
        return None

    def get_blacklist_rule(self, rule_id: str) -> Rule | None:
        """Get blacklist rule by ID."""
        for rule in self.blacklist:
            if rule.id == rule_id:
                return rule
        return None

    def resolve_example_path(self, example: Example) -> Path:
        """Resolve example path relative to profile location."""
        if self._path is None:
            return Path(example.path)

        example_path = Path(example.path)
        if example_path.is_absolute():
            return example_path

        return self._path.parent / example_path

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "extends": self.extends,
            "whitelist": [
                {
                    "id": r.id,
                    "name": r.name,
                    "target": list(r.target) if r.target else None,
                    "max": r.max,
                    "instruction": r.instruction,
                    "examples": r.examples,
                }
                for r in self.whitelist
            ],
            "blacklist": [
                {
                    "id": r.id,
                    "name": r.name,
                    "max": r.max,
                    "instruction": r.instruction,
                    "examples": r.examples,
                }
                for r in self.blacklist
            ],
            "settings": {
                "fit_threshold": self.settings.fit_threshold,
                "max_iterations": self.settings.max_iterations,
                "excerpt_length": self.settings.excerpt_length,
            },
        }


def list_profiles(profiles_dir: Path) -> list[str]:
    """List available profiles in directory."""
    profiles_dir = Path(profiles_dir)
    if not profiles_dir.exists():
        return []

    return [p.stem for p in profiles_dir.glob("*.yaml")]
