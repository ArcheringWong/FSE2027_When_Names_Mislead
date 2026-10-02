"""Restricted, outcome-free root and provenance-holder adjudication.

This module may read the frozen root mapping.  It never reads model responses
and it is intentionally separate from the public label generator.
"""

from __future__ import annotations

from typing import Any


def resolve_root_entity(public_label_map: list[dict[str, Any]], root_rows: list[dict[str, Any]]) -> str:
    identifiers: dict[str, set[str]] = {}
    for entity in public_label_map:
        values = {entity["canonical_id"], entity["source_entity_id"], *map(str, entity["source_specific_ids"].values())}
        for value in values:
            if value:
                identifiers.setdefault(value, set()).add(entity["candidate_id"])
    selected: set[str] = set()
    for row in root_rows:
        source_id = str(row.get("source_root_entity_id") or "")
        exact = identifiers.get(source_id, set())
        if len(exact) == 1:
            selected.update(exact)
            continue
        name = str(row.get("source_root_entity_name") or "").strip().casefold()
        expected_type = str(row.get("source_root_entity_type") or "")
        candidates = [
            entity["candidate_id"] for entity in public_label_map
            if name and entity["entity_type"] == expected_type and name in {
                entity["semantic_label"].casefold(), *(alias.casefold() for alias in entity["verified_aliases"])
            }
        ]
        if len(candidates) == 1:
            selected.add(candidates[0])
    if len(selected) != 1:
        raise ValueError(f"root source did not resolve uniquely: {sorted(selected)}")
    return next(iter(selected))


def adjudicate_typed_holder(
    public_label_map: list[dict[str, Any]], ownership_map: dict[str, Any], root_entity_id: str
) -> dict[str, Any]:
    by_id = {row["candidate_id"]: row for row in public_label_map}
    inverse = ownership_map["destination_by_source"]
    source_map = ownership_map["source_by_destination"]
    if root_entity_id not in inverse:
        raise ValueError("root absent from ownership map")
    holder = inverse[root_entity_id]
    root = by_id[root_entity_id]
    assigned_label = by_id[source_map[holder]]["semantic_label"]
    root_type_labels = [
        row["semantic_label"] for row in public_label_map if row["entity_type"] == root["entity_type"]
    ]
    return {
        "root_id": root_entity_id,
        "root_type": root["entity_type"],
        "holder_id": holder,
        "holder_type": by_id[holder]["entity_type"],
        "holder_is_unique": list(inverse).count(root_entity_id) == 1,
        "holder_is_wrong": holder != root_entity_id,
        "holder_type_matches_root": by_id[holder]["entity_type"] == root["entity_type"],
        "root_label_moved": holder != root_entity_id and assigned_label == root["semantic_label"],
        "root_label_unique_within_type": root_type_labels.count(root["semantic_label"]) == 1,
        "ownership_source": "destination_by_source_provenance",
    }
