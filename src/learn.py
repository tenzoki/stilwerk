"""Learn style from corpus and generate profile."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import numpy as np

from stilwerk.src.corpus.loader import Corpus
from stilwerk.src.features.lexical import LexicalExtractor
from stilwerk.src.features.function_words import MostFrequentWordsExtractor
from stilwerk.src.profile import StyleProfile, Rule, Settings


def learn_style(
    corpus_dir: Path | str,
    name: str,
    language: str = "de",
    pattern: str = "*.txt",
) -> StyleProfile:
    """Learn style characteristics from a corpus directory.

    Analyzes texts in the corpus to extract statistical features
    and generates a style profile with appropriate target ranges.

    Args:
        corpus_dir: Directory containing exemplar texts.
        name: Name for the generated profile.
        language: Language code (de, en).
        pattern: Glob pattern for text files.

    Returns:
        StyleProfile with learned targets.
    """
    corpus_dir = Path(corpus_dir)
    corpus = Corpus.from_directory(corpus_dir, pattern=pattern, name=name)

    if len(corpus) == 0:
        raise ValueError(f"No texts found in {corpus_dir} matching {pattern}")

    # Extract features from all texts
    lexical = LexicalExtractor()
    metrics = {
        "avg_sentence_length": [],
        "sentence_variance": [],
        "type_token_ratio": [],
        "avg_word_length": [],
    }

    for doc in corpus:
        vec = lexical.extract(doc.text)
        metrics["avg_sentence_length"].append(vec["avg_sentence_length"])
        metrics["type_token_ratio"].append(vec["type_token_ratio"])
        metrics["avg_word_length"].append(vec["avg_word_length"])

        # Calculate sentence variance manually
        from stilwerk.src.extract import _extract_sentence_variance
        metrics["sentence_variance"].append(_extract_sentence_variance(doc.text))

    # Calculate target ranges (mean ± 1 std, bounded)
    def calc_range(values: list[float], min_val: float = 0, max_val: float = 100) -> tuple[float, float]:
        arr = np.array(values)
        mean = float(np.mean(arr))
        std = float(np.std(arr))
        low = max(min_val, mean - std)
        high = min(max_val, mean + std)
        return (round(low, 1), round(high, 1))

    # Build whitelist rules from learned metrics
    whitelist = [
        Rule(
            id="U01",
            name="Sentence variance",
            target=calc_range(metrics["sentence_variance"], 3, 25),
            instruction="Vary sentence length to match corpus style.",
        ),
        Rule(
            id="TTR",
            name="Type-token ratio",
            target=calc_range(metrics["type_token_ratio"], 0.3, 0.9),
            instruction="Maintain vocabulary diversity matching corpus.",
        ),
    ]

    # Add first-person rate if detected
    from stilwerk.src.extract import _extract_first_person_rate
    fp_rates = [_extract_first_person_rate(doc.text) for doc in corpus]
    if np.mean(fp_rates) > 1.0:  # If corpus uses first person
        whitelist.append(Rule(
            id="U05",
            name="First person",
            target=calc_range(fp_rates, 0, 50),
            instruction="Use first-person perspective as in corpus.",
        ))

    # Default blacklist (can be customized)
    blacklist = [
        Rule(
            id="AI01",
            name="AI phrases",
            instruction="Remove characteristic AI patterns.",
            examples=[
                "Let's dive into", "It's important to note",
                "In this comprehensive guide", "Whether you're a beginner or expert",
            ] if language == "en" else [
                "Es ist wichtig zu beachten", "Lass uns eintauchen",
                "In diesem umfassenden Leitfaden",
            ],
        ),
    ]

    return StyleProfile(
        name=name,
        description=f"Style learned from {len(corpus)} texts in {corpus_dir.name}",
        whitelist=whitelist,
        blacklist=blacklist,
        settings=Settings(fit_threshold=0.85, max_iterations=5),
    )


def save_profile(profile: StyleProfile, path: Path | str) -> None:
    """Save a learned profile to YAML.

    Args:
        profile: StyleProfile to save.
        path: Output path.
    """
    import yaml

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "name": profile.name,
        "description": profile.description,
        "whitelist": [
            {
                "id": r.id,
                "name": r.name,
                "target": list(r.target) if r.target else None,
                "instruction": r.instruction,
            }
            for r in profile.whitelist
        ],
        "blacklist": [
            {
                "id": r.id,
                "name": r.name,
                "instruction": r.instruction,
                "examples": r.examples if r.examples else None,
            }
            for r in profile.blacklist
        ],
        "settings": {
            "fit_threshold": profile.settings.fit_threshold,
            "max_iterations": profile.settings.max_iterations,
        },
    }

    # Remove None values
    def clean(d):
        if isinstance(d, dict):
            return {k: clean(v) for k, v in d.items() if v is not None}
        elif isinstance(d, list):
            return [clean(i) for i in d]
        return d

    data = clean(data)

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def learn_and_save(
    corpus_dir: Path | str,
    output_path: Path | str,
    name: str | None = None,
    language: str = "de",
) -> StyleProfile:
    """Learn style from corpus and save to file.

    Args:
        corpus_dir: Directory with exemplar texts.
        output_path: Where to save the profile.
        name: Profile name (defaults to directory name).
        language: Language code.

    Returns:
        The generated StyleProfile.
    """
    corpus_dir = Path(corpus_dir)
    if name is None:
        name = corpus_dir.name

    profile = learn_style(corpus_dir, name, language)
    save_profile(profile, output_path)
    return profile
