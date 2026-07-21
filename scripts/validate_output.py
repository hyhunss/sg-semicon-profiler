#!/usr/bin/env python3
"""Validate a canonical plugin output against its declared JSON schema."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ModuleNotFoundError:
    print(
        "Validation requires the 'jsonschema' Python package. "
        "Install it or perform the schema self-check described in the skill.",
        file=sys.stderr,
    )
    raise SystemExit(2)


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATHS = {
    "capability_profile": PLUGIN_ROOT
    / "skills/map-sme-capability/schema/capability-profile.schema.json",
    "prospect_discovery": PLUGIN_ROOT
    / "skills/us-prospect-discovery/schema/prospect-discovery.schema.json",
    "qualified_prospects": PLUGIN_ROOT
    / "skills/qualify-us-prospects/schema/qualified-prospects.schema.json",
}


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"File not found: {path}", file=sys.stderr)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {path}: {exc}", file=sys.stderr)
    except OSError as exc:
        print(f"Could not read {path}: {exc}", file=sys.stderr)
    raise SystemExit(1)


def format_location(parts: list[object]) -> str:
    return "$" + "".join(
        f"[{part}]" if isinstance(part, int) else f".{part}" for part in parts
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a capability, prospect, or qualified-prospect JSON output."
    )
    parser.add_argument("output", type=Path, help="Path to the JSON output file")
    args = parser.parse_args()

    output_path = args.output.resolve()
    record = load_json(output_path)
    if not isinstance(record, dict):
        print("The output must be a JSON object.", file=sys.stderr)
        return 1

    schema_name = record.get("schema_name")
    schema_path = SCHEMA_PATHS.get(schema_name)
    if schema_path is None:
        supported = ", ".join(sorted(SCHEMA_PATHS))
        print(
            f"Unsupported or missing schema_name {schema_name!r}. "
            f"Expected one of: {supported}.",
            file=sys.stderr,
        )
        return 1

    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(record),
        key=lambda error: tuple(str(part) for part in error.path),
    )
    if errors:
        print(f"Validation failed for {output_path}:", file=sys.stderr)
        for error in errors:
            location = format_location(list(error.absolute_path))
            print(f"- {location}: {error.message}", file=sys.stderr)
        return 1

    print(f"Valid {schema_name}: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
