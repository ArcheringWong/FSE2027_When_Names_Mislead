"""Offline consistency checks for the anonymous Study-S review package."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review_only"


def read_csv(name: str) -> list[dict[str, str]]:
    with (REVIEW / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def truth(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes"}


def verify_roots_and_holders() -> dict[str, int]:
    roots = read_csv("restricted_root_mapping.csv")
    holders = read_csv("repaired_typed_holder_mapping.csv")

    assert len(roots) == 87
    assert len({row["case_id"] for row in roots}) == 87
    assert all(row["root_id"] for row in roots)

    assert len(holders) == 261
    assert len({(row["case_id"], row["seed"]) for row in holders}) == 261
    required = (
        "root_unique",
        "holder_unique",
        "holder_not_root",
        "type_matches",
        "holder_received_root_label",
        "root_label_moved",
        "eligibility_match",
    )
    assert all(all(truth(row[field]) for field in required) for row in holders)
    return {"root_rows": len(roots), "typed_holder_rows": len(holders)}


def verify_sq1() -> dict[str, dict[str, int | float]]:
    rows = read_csv("sq1_case_level.csv")
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row["provider"], row["topology"])].append(row)

    expected = {
        ("QWEN", "on"): (13, 1),
        ("QWEN", "off"): (14, 2),
        ("DEEPSEEK", "on"): (4, 1),
        ("DEEPSEEK", "off"): (5, 1),
    }
    output: dict[str, dict[str, int | float]] = {}
    for key, (semantic_expected, opaque_expected) in expected.items():
        group = groups[key]
        assert len(group) == 87
        semantic = sum(int(row["semantic_correct"]) for row in group)
        opaque = sum(int(row["opaque_correct"]) for row in group)
        assert (semantic, opaque) == (semantic_expected, opaque_expected)
        output[f"{key[0]}_{key[1]}"] = {
            "semantic_correct": semantic,
            "opaque_correct": opaque,
            "difference": (semantic - opaque) / 87,
        }
    return output


def verify_sq2() -> dict[str, dict[str, int | float]]:
    rows = read_csv("sq2_case_seed_level.csv")
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row["provider"], row["topology"])].append(row)

    expected = {
        ("QWEN", "on"): (45, 1, 44, 6),
        ("QWEN", "off"): (33, 1, 32, 4),
        ("DEEPSEEK", "on"): (7, 1, 6, 0),
        ("DEEPSEEK", "off"): (6, 1, 5, 0),
    }
    output: dict[str, dict[str, int | float]] = {}
    for key, expected_counts in expected.items():
        group = groups[key]
        assert len(group) == 261
        counts = (
            sum(int(row["permuted_holder_selection"]) for row in group),
            sum(int(row["opaque_holder_selection"]) for row in group),
            sum(truth(row["new_switch"]) for row in group),
            sum(truth(row["strict_stable_switch"]) for row in group),
        )
        assert counts == expected_counts
        output[f"{key[0]}_{key[1]}"] = {
            "permuted_holder": counts[0],
            "opaque_holder": counts[1],
            "difference": (counts[0] - counts[1]) / 261,
            "new_switch": counts[2],
            "strict_stable_switch": counts[3],
        }
    return output


def main() -> None:
    result = {
        "status": "PASS",
        "mapping_integrity": verify_roots_and_holders(),
        "sq1": verify_sq1(),
        "sq2": verify_sq2(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
