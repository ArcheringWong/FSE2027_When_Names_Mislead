"""Public-only, full-surface label construction for Study-S v2.

This module deliberately has no gold, answer-key, model-output, provider, or
transport dependency.  Every transformation is a deterministic function of
public candidate entities, their types, a case identifier, and a frozen seed.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter, defaultdict
from typing import Any, Iterable


def stable_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _prefix(entity_type: str) -> str:
    kind = (entity_type or "entity").lower()
    if "service" in kind:
        return "svc"
    if "pod" in kind or "instance" in kind:
        return "pod"
    if "node" in kind:
        return "node"
    return "ent"


def build_public_label_map(public_entities: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Create stable candidate IDs and semantic/typed-opaque labels.

    The signature accepts only public entities.  Stable candidate IDs are
    assigned by canonical ID order, matching the canonical RCA infrastructure.
    """
    entities = sorted((dict(item) for item in public_entities), key=lambda x: x["canonical_id"])
    counters: Counter[str] = Counter()
    result: list[dict[str, Any]] = []
    for index, entity in enumerate(entities, 1):
        candidate_id = f"E{index:03d}"
        entity_type = str(entity.get("entity_type") or "entity")
        prefix = _prefix(entity_type)
        counters[prefix] += 1
        opaque = f"{prefix}_{counters[prefix]:03d}"
        semantic = str(entity.get("original_display_name") or candidate_id)
        if semantic.casefold() in opaque.casefold() or opaque.casefold() in semantic.casefold():
            opaque = f"{prefix}_x{counters[prefix]:03d}"
        result.append({
            "candidate_id": candidate_id,
            "canonical_id": str(entity["canonical_id"]),
            "source_entity_id": str(entity.get("source_entity_id") or ""),
            "source_specific_ids": dict(entity.get("source_specific_ids") or {}),
            "verified_aliases": sorted(str(x) for x in (entity.get("verified_aliases") or []) if x),
            "entity_type": entity_type,
            "semantic_label": semantic,
            "opaque_label": opaque,
        })
    if len({row["candidate_id"] for row in result}) != len(result):
        raise AssertionError("candidate IDs are not unique")
    return result


def _deranged_sources(labels: list[str], rng: random.Random) -> list[int]:
    """Return source index for each destination, with no value fixed point."""
    n = len(labels)
    if n < 2 or max(Counter(labels).values(), default=0) * 2 > n:
        raise ValueError("no complete value-level derangement exists")
    allowed: dict[int, list[int]] = {}
    for destination in range(n):
        choices = [source for source in range(n) if labels[source] != labels[destination]]
        rng.shuffle(choices)
        allowed[destination] = choices
    owner: dict[int, int] = {}

    def assign(destination: int, seen: set[int]) -> bool:
        for source in allowed[destination]:
            if source in seen:
                continue
            seen.add(source)
            if source not in owner or assign(owner[source], seen):
                owner[source] = destination
                return True
        return False

    for destination in sorted(range(n), key=lambda i: (len(allowed[i]), labels[i], i)):
        if not assign(destination, set()):
            raise ValueError("no complete value-level derangement exists")
    result = [-1] * n
    for source, destination in owner.items():
        result[destination] = source
    if any(index < 0 for index in result):
        raise AssertionError("incomplete derangement")
    return result


def build_full_surface_permutation(
    public_label_map: list[dict[str, Any]], seed: int, *, case_id: str
) -> dict[str, Any]:
    """Build a complete typed ownership bijection without restricted inputs."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in public_label_map:
        groups[entry["entity_type"]].append(entry)
    source_by_destination: dict[str, str] = {}
    type_status: dict[str, dict[str, Any]] = {}
    for entity_type in sorted(groups):
        members = groups[entity_type]
        labels = [row["semantic_label"] for row in members]
        carry_reason = ""
        try:
            material = {"case_id": case_id, "seed": int(seed), "entity_type": entity_type}
            rng = random.Random(int(stable_hash(material)[:16], 16))
            indices = _deranged_sources(labels, rng)
        except ValueError as exc:
            indices = list(range(len(members)))
            carry_reason = str(exc)
        for destination, source_index in zip(members, indices):
            source_by_destination[destination["candidate_id"]] = members[source_index]["candidate_id"]
        type_status[entity_type] = {
            "mode": "identity_carry" if carry_reason else "deranged",
            "reason": carry_reason,
            "candidate_count": len(members),
            "distinct_label_count": len(set(labels)),
        }

    destination_by_source = {source: destination for destination, source in source_by_destination.items()}
    ids = [row["candidate_id"] for row in public_label_map]
    by_id = {row["candidate_id"]: row for row in public_label_map}
    if set(source_by_destination) != set(ids) or set(source_by_destination.values()) != set(ids):
        raise AssertionError("ownership mapping is not a full candidate bijection")
    if len(destination_by_source) != len(ids):
        raise AssertionError("ownership inverse is not bijective")
    if any(destination_by_source[source] != destination for destination, source in source_by_destination.items()):
        raise AssertionError("ownership mappings are not inverse")
    if any(by_id[destination]["entity_type"] != by_id[source]["entity_type"] for destination, source in source_by_destination.items()):
        raise AssertionError("ownership mapping crosses entity types")

    permuted = []
    moved = 0
    for destination in ids:
        source = source_by_destination[destination]
        if source != destination:
            moved += 1
        permuted.append({
            "candidate_id": destination,
            "display_name": by_id[source]["semantic_label"],
            "entity_type": by_id[destination]["entity_type"],
            "label_source_entity_id": source,
        })
    original_multisets = {
        kind: Counter(row["semantic_label"] for row in rows) for kind, rows in groups.items()
    }
    assigned_multisets = {
        kind: Counter(row["display_name"] for row in permuted if row["entity_type"] == kind)
        for kind in groups
    }
    if original_multisets != assigned_multisets:
        raise AssertionError("within-type label multiset changed")
    for kind, status in type_status.items():
        rows = [row for row in permuted if row["entity_type"] == kind]
        if status["mode"] == "deranged" and any(
            row["display_name"] == by_id[row["candidate_id"]]["semantic_label"] for row in rows
        ):
            raise AssertionError("value-level fixed point in deranged type")
        if status["mode"] == "identity_carry" and any(
            source_by_destination[row["candidate_id"]] != row["candidate_id"] for row in rows
        ):
            raise AssertionError("identity-carry type was changed")
    return {
        "case_id": case_id,
        "seed": int(seed),
        "candidate_ids": ids,
        "source_by_destination": source_by_destination,
        "destination_by_source": destination_by_source,
        "permuted_labels": permuted,
        "type_status": type_status,
        "moved_candidate_count": moved,
        "movement_coverage": moved / len(ids) if ids else 0.0,
        "identity_carry_types": sorted(kind for kind, value in type_status.items() if value["mode"] == "identity_carry"),
        "deranged_types": sorted(kind for kind, value in type_status.items() if value["mode"] == "deranged"),
    }


def semantic_active_labels(public_label_map: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"candidate_id": row["candidate_id"], "display_name": row["semantic_label"], "entity_type": row["entity_type"]} for row in public_label_map]


def opaque_active_labels(public_label_map: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"candidate_id": row["candidate_id"], "display_name": row["opaque_label"], "entity_type": row["entity_type"]} for row in public_label_map]


def mapping_hamming(first: dict[str, str], second: dict[str, str], surface: set[str] | None = None) -> float:
    ids = sorted(surface if surface is not None else set(first))
    if not ids or any(entity_id not in first or entity_id not in second for entity_id in ids):
        return 0.0
    return sum(first[entity_id] != second[entity_id] for entity_id in ids) / len(ids)
