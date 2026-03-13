"""Generate transformation instructions for AI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from stilwerk.src.profile import StyleProfile, Example
from stilwerk.src.compare import ComparisonResult, Status
from stilwerk.src.extract import extract_excerpt


def generate_instructions(
    text: str,
    profile: StyleProfile,
    comparison: ComparisonResult,
) -> str:
    """Generate transformation instructions for AI.

    Args:
        text: Original text to transform.
        profile: Target style profile.
        comparison: Gap analysis result.

    Returns:
        Complete instruction prompt for AI.
    """
    sections = []

    # Header
    sections.append(_generate_header(profile, comparison))

    # Priority adjustments
    sections.append(_generate_adjustments(profile, comparison))

    # Blacklist eliminations
    if comparison.blacklist_violations:
        sections.append(_generate_blacklist_section(comparison))

    # Examples
    if profile.examples:
        sections.append(_generate_examples_section(profile))

    # Anti-examples
    if profile.anti_examples:
        sections.append(_generate_anti_examples_section(profile))

    # Original text
    sections.append(_generate_text_section(text))

    return "\n\n".join(sections)


def _generate_header(profile: StyleProfile, comparison: ComparisonResult) -> str:
    """Generate instruction header."""
    return f"""# Style Transformation Instructions

Transform the following text to match the **"{profile.name}"** style.

**Current fit:** {comparison.overall_fit:.0%}
**Target fit:** {profile.settings.fit_threshold:.0%}

{profile.description}"""


def _generate_adjustments(
    profile: StyleProfile,
    comparison: ComparisonResult,
) -> str:
    """Generate priority adjustments section."""
    lines = ["## Priority Adjustments"]
    priority = 1

    # Metrics that need adjustment
    for metric_id, metric in comparison.metrics.items():
        if metric.status != Status.OK:
            rule = profile.get_whitelist_rule(metric_id) or profile.get_blacklist_rule(metric_id)

            lines.append(f"\n### {priority}. {metric.name} ({metric.id})")
            lines.append(f"**Current:** {metric.current:.2f}")

            if metric.target:
                lines.append(f"**Target:** {metric.target[0]:.2f} - {metric.target[1]:.2f}")
            elif metric.max:
                lines.append(f"**Maximum:** {metric.max:.2f}")

            lines.append(f"**Status:** {metric.status.value}")
            lines.append(f"**Gap:** {metric.gap}")

            if rule and rule.instruction:
                lines.append(f"\n**Action:** {rule.instruction}")

            priority += 1

    # Whitelist gaps (qualitative)
    for gap in comparison.whitelist_gaps:
        rule = profile.get_whitelist_rule(gap.rule_id)

        lines.append(f"\n### {priority}. {gap.rule_name} ({gap.rule_id})")
        lines.append(f"**Issue:** {gap.issue}")

        if rule and rule.instruction:
            lines.append(f"\n**Action:** {rule.instruction}")

        priority += 1

    if priority == 1:
        lines.append("\nNo metric adjustments needed.")

    return "\n".join(lines)


def _generate_blacklist_section(comparison: ComparisonResult) -> str:
    """Generate blacklist elimination section."""
    lines = ["## Patterns to Eliminate"]

    for violation in comparison.blacklist_violations:
        lines.append(f"\n### {violation.rule_name} ({violation.rule_id})")
        lines.append(f"**Found {violation.count} instances:**")

        for found in violation.found[:5]:  # Show up to 5
            lines.append(f"- \"{found}\" → remove or rephrase")

    return "\n".join(lines)


def _generate_examples_section(profile: StyleProfile) -> str:
    """Generate examples section with excerpts."""
    lines = ["## Style Exemplars"]
    lines.append("\nWrite like these examples:")

    for example in profile.examples:
        if not example.include:
            continue

        lines.append(f"\n### {example.note or example.path}")

        # Load excerpt if not already loaded
        excerpt = example.excerpt
        if not excerpt:
            example_path = profile.resolve_example_path(example)
            if example_path.exists():
                text = example_path.read_text(encoding="utf-8")
                excerpt = extract_excerpt(text, profile.settings.excerpt_length)

        if excerpt:
            lines.append(f"\n> {excerpt}")

    return "\n".join(lines)


def _generate_anti_examples_section(profile: StyleProfile) -> str:
    """Generate anti-examples section."""
    lines = ["## Avoid This Style"]
    lines.append("\nDo NOT write like these examples:")

    for example in profile.anti_examples:
        if not example.include:
            continue

        lines.append(f"\n### {example.note or example.path}")

        # Load excerpt
        example_path = profile.resolve_example_path(example)
        if example_path.exists():
            text = example_path.read_text(encoding="utf-8")
            excerpt = extract_excerpt(text, profile.settings.excerpt_length)
            if excerpt:
                lines.append(f"\n> {excerpt}")

    return "\n".join(lines)


def _generate_text_section(text: str) -> str:
    """Generate the original text section."""
    return f"""## Text to Transform

```
{text}
```

## Instructions

Transform the text above according to the style adjustments specified. Maintain the core meaning and information while changing the style. Return only the transformed text."""


def generate_instructions_file(
    text_path: Path,
    profile: StyleProfile,
    comparison: ComparisonResult,
    output_path: Path | None = None,
) -> str:
    """Generate instructions and optionally save to file.

    Args:
        text_path: Path to original text.
        profile: Target style profile.
        comparison: Gap analysis result.
        output_path: Optional path to save instructions.

    Returns:
        Generated instructions.
    """
    text = Path(text_path).read_text(encoding="utf-8")
    instructions = generate_instructions(text, profile, comparison)

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(instructions, encoding="utf-8")

    return instructions
