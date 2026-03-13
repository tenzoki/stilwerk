"""CLI for stilwerk style analysis and transformation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Stilwerk - Style analysis, attribution, and transformation",
        prog="stilwerk",
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Profile commands
    profile_parser = subparsers.add_parser("profile", help="Profile management")
    profile_sub = profile_parser.add_subparsers(dest="profile_command")

    profile_list = profile_sub.add_parser("list", help="List available profiles")
    profile_list.add_argument(
        "--dir", "-d",
        default="./profiles",
        help="Profiles directory",
    )

    profile_show = profile_sub.add_parser("show", help="Show profile details")
    profile_show.add_argument("name", help="Profile name")
    profile_show.add_argument("--dir", "-d", default="./profiles")

    # Learn command (NEW: from stilo integration)
    learn_parser = subparsers.add_parser("learn", help="Learn style profile from corpus")
    learn_parser.add_argument("corpus_dir", help="Directory containing exemplar texts")
    learn_parser.add_argument("--name", "-n", help="Profile name (defaults to directory name)")
    learn_parser.add_argument("--output", "-o", help="Output path for profile YAML")
    learn_parser.add_argument("--language", "-l", default="de", help="Language code (de, en)")
    learn_parser.add_argument("--pattern", default="*.txt", help="Glob pattern for text files")

    # Analyze command (NEW: from stilo integration)
    analyze_parser = subparsers.add_parser("analyze", help="Full stylometric analysis of corpus")
    analyze_parser.add_argument("config", help="Project config YAML file")
    analyze_parser.add_argument("--output", "-o", help="Output path for results JSON")
    analyze_parser.add_argument("--json", "-j", action="store_true", help="JSON output to stdout")

    # Attribute command (NEW: from stilo integration)
    attribute_parser = subparsers.add_parser("attribute", help="Attribute text authorship")
    attribute_parser.add_argument("query_text", help="Text file to attribute")
    attribute_parser.add_argument("--corpus", "-c", required=True, help="Corpus directory with known authors")
    attribute_parser.add_argument("--n-features", "-n", type=int, default=100, help="Number of MFW features")
    attribute_parser.add_argument("--language", "-l", default="de", help="Language code")
    attribute_parser.add_argument("--json", "-j", action="store_true", help="JSON output")

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare text against profile")
    compare_parser.add_argument("text", help="Text file to analyze")
    compare_parser.add_argument("--profile", "-p", required=True, help="Profile name")
    compare_parser.add_argument("--profiles-dir", "-d", default="./profiles")
    compare_parser.add_argument("--json", "-j", action="store_true", help="JSON output")

    # Instruct command
    instruct_parser = subparsers.add_parser("instruct", help="Generate transformation instructions")
    instruct_parser.add_argument("text", help="Text file to transform")
    instruct_parser.add_argument("--profile", "-p", required=True, help="Profile name")
    instruct_parser.add_argument("--profiles-dir", "-d", default="./profiles")
    instruct_parser.add_argument("--output", "-o", help="Output file for instructions")

    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify transformed text")
    verify_parser.add_argument("text", help="Transformed text file")
    verify_parser.add_argument("--profile", "-p", required=True, help="Profile name")
    verify_parser.add_argument("--profiles-dir", "-d", default="./profiles")
    verify_parser.add_argument("--json", "-j", action="store_true", help="JSON output")

    args = parser.parse_args()

    if args.command == "profile":
        handle_profile(args)
    elif args.command == "learn":
        handle_learn(args)
    elif args.command == "analyze":
        handle_analyze(args)
    elif args.command == "attribute":
        handle_attribute(args)
    elif args.command == "compare":
        handle_compare(args)
    elif args.command == "instruct":
        handle_instruct(args)
    elif args.command == "verify":
        handle_verify(args)
    else:
        parser.print_help()
        sys.exit(1)


def handle_profile(args):
    """Handle profile subcommands."""
    from stilwerk.src.profile import list_profiles, StyleProfile

    if args.profile_command == "list":
        profiles = list_profiles(Path(args.dir))
        print("Available profiles:")
        for name in profiles:
            print(f"  - {name}")

    elif args.profile_command == "show":
        profile_path = Path(args.dir) / f"{args.name}.yaml"
        profile = StyleProfile.load(profile_path)

        print(f"Profile: {profile.name}")
        print(f"Description: {profile.description}")
        if profile.extends:
            print(f"Extends: {profile.extends}")
        print(f"\nWhitelist rules: {len(profile.whitelist)}")
        for rule in profile.whitelist:
            target = f" (target: {rule.target})" if rule.target else ""
            print(f"  - {rule.id}: {rule.name}{target}")
        print(f"\nBlacklist rules: {len(profile.blacklist)}")
        for rule in profile.blacklist:
            print(f"  - {rule.id}: {rule.name}")
        print(f"\nSettings:")
        print(f"  fit_threshold: {profile.settings.fit_threshold}")
        print(f"  max_iterations: {profile.settings.max_iterations}")


def handle_learn(args):
    """Handle learn command - learn style from corpus."""
    from stilwerk.src.learn import learn_style, save_profile

    corpus_dir = Path(args.corpus_dir)
    if not corpus_dir.exists():
        print(f"Error: Corpus directory not found: {corpus_dir}", file=sys.stderr)
        sys.exit(1)

    name = args.name or corpus_dir.name
    output_path = Path(args.output) if args.output else Path(f"./profiles/{name}.yaml")

    print(f"Learning style from: {corpus_dir}")
    print(f"Language: {args.language}")
    print(f"Pattern: {args.pattern}")

    profile = learn_style(
        corpus_dir=corpus_dir,
        name=name,
        language=args.language,
        pattern=args.pattern,
    )

    save_profile(profile, output_path)
    print(f"\nProfile saved to: {output_path}")
    print(f"  Name: {profile.name}")
    print(f"  Description: {profile.description}")
    print(f"  Whitelist rules: {len(profile.whitelist)}")
    print(f"  Blacklist rules: {len(profile.blacklist)}")


def handle_analyze(args):
    """Handle analyze command - full stylometric analysis."""
    from stilwerk.src.config import load_config
    from stilwerk.src.analysis import analyze

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading config: {config_path}")
    config = load_config(config_path)

    print(f"Analyzing corpus: {config.corpus.path}")
    result = analyze(config)

    if args.json:
        import json
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    elif args.output:
        result.save_json(args.output)
        print(f"Results saved to: {args.output}")
    else:
        # Summary output
        print(f"\nAnalysis complete:")
        print(f"  Documents: {len(result.labels)}")
        if result.features:
            print(f"  Features: {len(result.features.feature_names)}")
        if result.clustering:
            print(f"  Clustering method: {result.clustering.method}")
            print(f"  Merge order (first 5):")
            for l1, l2, dist in result.clustering.get_merge_order()[:5]:
                print(f"    {l1} + {l2} (distance: {dist:.4f})")
        if result.pca:
            print(f"  PCA variance explained: {result.pca.explained_variance_ratio[0]:.1%}, {result.pca.explained_variance_ratio[1]:.1%}")


def handle_attribute(args):
    """Handle attribute command - authorship attribution."""
    import numpy as np
    from stilwerk.src.corpus import Corpus
    from stilwerk.src.features.function_words import MostFrequentWordsExtractor
    from stilwerk.src.analysis.distance import DistanceCalculator

    query_path = Path(args.query_text)
    corpus_dir = Path(args.corpus)

    if not query_path.exists():
        print(f"Error: Query text not found: {query_path}", file=sys.stderr)
        sys.exit(1)
    if not corpus_dir.exists():
        print(f"Error: Corpus directory not found: {corpus_dir}", file=sys.stderr)
        sys.exit(1)

    # Load query text
    query_text = query_path.read_text(encoding="utf-8")

    # Load corpus
    corpus = Corpus.from_directory(corpus_dir, pattern="**/*.txt")
    if len(corpus) == 0:
        print(f"Error: No texts found in corpus: {corpus_dir}", file=sys.stderr)
        sys.exit(1)

    texts = {doc.label: doc.text for doc in corpus}

    # Extract features using MFW
    extractor = MostFrequentWordsExtractor(
        n_features=args.n_features,
        language=args.language,
    )
    extractor.fit(texts)
    features = extractor.extract_many(texts)

    # Extract query features
    query_vec = extractor.extract(query_text)

    # Calculate distances to all corpus texts
    distances = []
    for i, label in enumerate(features.labels):
        dist = float(np.mean(np.abs(query_vec.values - features.values[i])))
        distances.append((label, dist))

    distances.sort(key=lambda x: x[1])

    if args.json:
        import json
        result = {
            "query": query_path.name,
            "attribution": distances[0][0] if distances else None,
            "confidence": 1.0 - distances[0][1] if distances else 0,
            "nearest_neighbors": [
                {"label": l, "distance": round(d, 4)}
                for l, d in distances[:10]
            ],
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Query: {query_path.name}")
        print(f"Corpus: {len(corpus)} texts")
        print(f"\nAttribution:")
        if distances:
            print(f"  Most likely author: {distances[0][0]}")
            print(f"  Distance: {distances[0][1]:.4f}")
            print(f"\nNearest neighbors:")
            for label, dist in distances[:5]:
                print(f"  {label}: {dist:.4f}")


def handle_compare(args):
    """Handle compare command."""
    from stilwerk.src.profile import StyleProfile
    from stilwerk.src.compare import compare_file

    profile_path = Path(args.profiles_dir) / f"{args.profile}.yaml"
    profile = StyleProfile.load(profile_path)

    result = compare_file(Path(args.text), profile)

    if args.json:
        import json
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"Profile: {result.profile_name}")
        print(f"Overall fit: {result.overall_fit:.0%}")
        print(f"\nMetrics:")
        for metric in result.metrics.values():
            status_icon = "✓" if metric.status.value == "OK" else "✗"
            print(f"  {status_icon} {metric.id}: {metric.current:.2f} ({metric.status.value})")
            if metric.gap:
                print(f"      {metric.gap}")

        if result.blacklist_violations:
            print(f"\nBlacklist violations:")
            for v in result.blacklist_violations:
                print(f"  - {v.rule_id}: {v.count} instances")
                for found in v.found[:3]:
                    print(f"      \"{found}\"")

        if result.whitelist_gaps:
            print(f"\nWhitelist gaps:")
            for g in result.whitelist_gaps:
                print(f"  - {g.rule_id}: {g.issue}")


def handle_instruct(args):
    """Handle instruct command."""
    from stilwerk.src.profile import StyleProfile
    from stilwerk.src.compare import compare_file
    from stilwerk.src.instruct import generate_instructions_file

    profile_path = Path(args.profiles_dir) / f"{args.profile}.yaml"
    profile = StyleProfile.load(profile_path)

    comparison = compare_file(Path(args.text), profile)

    output_path = Path(args.output) if args.output else None
    instructions = generate_instructions_file(
        Path(args.text),
        profile,
        comparison,
        output_path,
    )

    if not args.output:
        print(instructions)
    else:
        print(f"Instructions written to: {output_path}")


def handle_verify(args):
    """Handle verify command."""
    from stilwerk.src.profile import StyleProfile
    from stilwerk.src.verify import verify_file

    profile_path = Path(args.profiles_dir) / f"{args.profile}.yaml"
    profile = StyleProfile.load(profile_path)

    result = verify_file(Path(args.text), profile)

    if args.json:
        import json
        print(json.dumps(result.to_dict(), indent=2))
    else:
        status = "✓ PASS" if result.meets_threshold else "✗ FAIL"
        print(f"Verification: {status}")
        print(f"Overall fit: {result.overall_fit:.0%} (threshold: {profile.settings.fit_threshold:.0%})")
        print(f"\nMetrics: {result.metrics_ok} OK, {result.metrics_off} off-target")
        print(f"Violations remaining: {result.violations_remaining}")
        print(f"Gaps remaining: {result.gaps_remaining}")

        if result.remaining_issues:
            print(f"\nRemaining issues:")
            for issue in result.remaining_issues:
                print(f"  - {issue}")


if __name__ == "__main__":
    main()
