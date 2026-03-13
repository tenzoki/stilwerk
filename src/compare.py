"""Compare text against a style profile."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from stilwerk.src.extract import extract_metrics, extract_excerpt, ExtractionResult
from stilwerk.src.profile import StyleProfile, Rule, Example


class Status(str, Enum):
    """Metric status relative to target."""

    OK = "OK"
    LOW = "LOW"
    HIGH = "HIGH"
    MISSING = "MISSING"


@dataclass
class MetricComparison:
    """Comparison result for a single metric."""

    id: str
    name: str
    current: float
    target: tuple[float, float] | None = None
    max: float | None = None
    status: Status = Status.OK
    gap: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "current": round(self.current, 2),
            "target": list(self.target) if self.target else None,
            "max": self.max,
            "status": self.status.value,
            "gap": self.gap,
        }


@dataclass
class Violation:
    """A blacklist violation found in text."""

    rule_id: str
    rule_name: str
    found: list[str]  # Specific instances found
    count: int

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.rule_id,
            "name": self.rule_name,
            "found": self.found,
            "count": self.count,
        }


@dataclass
class Gap:
    """A whitelist gap (missing desired pattern)."""

    rule_id: str
    rule_name: str
    issue: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.rule_id,
            "name": self.rule_name,
            "issue": self.issue,
        }


@dataclass
class ComparisonResult:
    """Complete comparison result."""

    profile_name: str
    metrics: dict[str, MetricComparison] = field(default_factory=dict)
    blacklist_violations: list[Violation] = field(default_factory=list)
    whitelist_gaps: list[Gap] = field(default_factory=list)
    overall_fit: float = 0.0

    # Raw extraction data
    extraction: ExtractionResult | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for YAML/JSON output."""
        return {
            "profile": self.profile_name,
            "overall_fit": round(self.overall_fit, 2),
            "metrics": {k: v.to_dict() for k, v in self.metrics.items()},
            "blacklist_violations": [v.to_dict() for v in self.blacklist_violations],
            "whitelist_gaps": [g.to_dict() for g in self.whitelist_gaps],
        }


def compare(text: str, profile: StyleProfile) -> ComparisonResult:
    """Compare text against a style profile.

    Args:
        text: Text content to analyze.
        profile: Target style profile.

    Returns:
        ComparisonResult with gaps and fit score.
    """
    result = ComparisonResult(profile_name=profile.name)

    # Extract metrics from text
    extraction = extract_metrics(text)
    result.extraction = extraction

    # Compare metrics against whitelist targets
    for rule in profile.whitelist:
        if rule.target:
            current = extraction.get(rule.id, 0.0)
            comparison = _compare_metric(rule, current)
            result.metrics[rule.id] = comparison

    # Check blacklist violations
    for rule in profile.blacklist:
        violation = _check_blacklist(text, rule)
        if violation:
            result.blacklist_violations.append(violation)

        # Also check max threshold
        if rule.max is not None:
            current = extraction.get(rule.id, 0.0)
            if current > rule.max:
                comparison = MetricComparison(
                    id=rule.id,
                    name=rule.name,
                    current=current,
                    max=rule.max,
                    status=Status.HIGH,
                    gap=f"Reduce from {current:.2f} to below {rule.max}",
                )
                result.metrics[rule.id] = comparison

    # Check whitelist qualitative gaps
    for rule in profile.whitelist:
        if not rule.target:  # Qualitative rule
            gap = _check_whitelist_gap(text, rule, extraction)
            if gap:
                result.whitelist_gaps.append(gap)

    # Calculate overall fit score
    result.overall_fit = _calculate_fit(result, profile)

    return result


def _compare_metric(rule: Rule, current: float) -> MetricComparison:
    """Compare a metric against its target range."""
    target = rule.target
    if target is None:
        return MetricComparison(
            id=rule.id,
            name=rule.name,
            current=current,
            status=Status.OK,
        )

    min_val, max_val = target

    if current < min_val:
        gap = f"Increase from {current:.2f} to {min_val:.2f}-{max_val:.2f}"
        status = Status.LOW
    elif current > max_val:
        gap = f"Reduce from {current:.2f} to {min_val:.2f}-{max_val:.2f}"
        status = Status.HIGH
    else:
        gap = ""
        status = Status.OK

    return MetricComparison(
        id=rule.id,
        name=rule.name,
        current=current,
        target=target,
        status=status,
        gap=gap,
    )


def _check_blacklist(text: str, rule: Rule) -> Violation | None:
    """Check for blacklist violations in text."""
    if not rule.examples:
        return None

    text_lower = text.lower()
    found = []

    for example in rule.examples:
        example_lower = example.lower()
        # Find all occurrences
        if example_lower in text_lower:
            # Extract actual text (with original case)
            pattern = re.compile(re.escape(example), re.IGNORECASE)
            matches = pattern.findall(text)
            found.extend(matches[:3])  # Limit to 3 examples

    if found:
        return Violation(
            rule_id=rule.id,
            rule_name=rule.name,
            found=found,
            count=len(found),
        )

    return None


def _check_whitelist_gap(
    text: str,
    rule: Rule,
    extraction: ExtractionResult,
) -> Gap | None:
    """Check if a qualitative whitelist pattern is missing."""
    # Check based on rule ID
    if rule.id == "U05":  # First person
        rate = extraction.get("U05", 0.0)
        if rate < 1.0:
            return Gap(
                rule_id=rule.id,
                rule_name=rule.name,
                issue="No first-person perspective found",
            )

    if rule.id == "V03":  # Epistemic hedging
        hedges = ["i think", "probably", "perhaps", "maybe", "might",
                  "ich denke", "vielleicht", "wahrscheinlich", "möglicherweise"]
        text_lower = text.lower()
        if not any(h in text_lower for h in hedges):
            return Gap(
                rule_id=rule.id,
                rule_name=rule.name,
                issue="No epistemic hedging found (text sounds too certain)",
            )

    return None


def _calculate_fit(result: ComparisonResult, profile: StyleProfile) -> float:
    """Calculate overall fit score (0-1).

    Scoring:
    - Each metric in range: +1
    - Each metric out of range: -0.5
    - Each blacklist violation: -0.2
    - Each whitelist gap: -0.1
    """
    score = 1.0
    total_checks = 0

    # Metric scores
    for comparison in result.metrics.values():
        total_checks += 1
        if comparison.status == Status.OK:
            pass  # Full credit
        elif comparison.status in (Status.LOW, Status.HIGH):
            score -= 0.15

    # Blacklist penalties
    for violation in result.blacklist_violations:
        score -= 0.1 * min(violation.count, 3)  # Cap penalty

    # Whitelist gap penalties
    for gap in result.whitelist_gaps:
        score -= 0.1

    return max(0.0, min(1.0, score))


def compare_file(path: Path, profile: StyleProfile) -> ComparisonResult:
    """Compare a file against a profile.

    Args:
        path: Path to text file.
        profile: Target style profile.

    Returns:
        ComparisonResult.
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    return compare(text, profile)
