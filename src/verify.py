"""Verify transformed text against profile."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from stilwerk.src.profile import StyleProfile
from stilwerk.src.compare import compare, ComparisonResult, Status


@dataclass
class VerificationResult:
    """Result of verifying transformed text."""

    profile_name: str
    overall_fit: float
    meets_threshold: bool
    comparison: ComparisonResult

    # Summary
    metrics_ok: int = 0
    metrics_off: int = 0
    violations_remaining: int = 0
    gaps_remaining: int = 0

    # Specific remaining issues
    remaining_issues: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "profile": self.profile_name,
            "overall_fit": round(self.overall_fit, 2),
            "meets_threshold": self.meets_threshold,
            "metrics_ok": self.metrics_ok,
            "metrics_off": self.metrics_off,
            "violations_remaining": self.violations_remaining,
            "gaps_remaining": self.gaps_remaining,
            "remaining_issues": self.remaining_issues,
        }


def verify(text: str, profile: StyleProfile) -> VerificationResult:
    """Verify if transformed text meets profile requirements.

    Args:
        text: Transformed text to verify.
        profile: Target style profile.

    Returns:
        VerificationResult with fit score and remaining issues.
    """
    # Run comparison
    comparison = compare(text, profile)

    # Count metrics
    metrics_ok = sum(
        1 for m in comparison.metrics.values()
        if m.status == Status.OK
    )
    metrics_off = sum(
        1 for m in comparison.metrics.values()
        if m.status != Status.OK
    )

    # Check threshold
    meets_threshold = comparison.overall_fit >= profile.settings.fit_threshold

    # Collect remaining issues
    remaining_issues = []

    for metric in comparison.metrics.values():
        if metric.status != Status.OK:
            remaining_issues.append(
                f"{metric.id}: {metric.status.value} ({metric.current:.2f})"
            )

    for violation in comparison.blacklist_violations:
        remaining_issues.append(
            f"{violation.rule_id}: {violation.count} violation(s) - {', '.join(violation.found[:2])}"
        )

    for gap in comparison.whitelist_gaps:
        remaining_issues.append(f"{gap.rule_id}: {gap.issue}")

    return VerificationResult(
        profile_name=profile.name,
        overall_fit=comparison.overall_fit,
        meets_threshold=meets_threshold,
        comparison=comparison,
        metrics_ok=metrics_ok,
        metrics_off=metrics_off,
        violations_remaining=len(comparison.blacklist_violations),
        gaps_remaining=len(comparison.whitelist_gaps),
        remaining_issues=remaining_issues,
    )


def verify_file(path: Path, profile: StyleProfile) -> VerificationResult:
    """Verify a file against a profile.

    Args:
        path: Path to transformed text file.
        profile: Target style profile.

    Returns:
        VerificationResult.
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    return verify(text, profile)
