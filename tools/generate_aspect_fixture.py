"""Generate contracts/aspects/detection.json from the documented rule.

This is a deliberately small, independent reference implementation of the
aspect-detection convention in CONVENTIONS.md (section "Aspects"). Both the
Rust app and the Python sidecar must reproduce its output exactly (as sets).

Inputs are the Horizons reference positions (mean equinox of date) plus a few
synthetic points that exercise structurally locked pairs and the inclusive
orb boundary. Standard library only.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACTS = ROOT / "contracts"
LOCKED_PAIRS = {frozenset(p) for p in (("asc", "desc"), ("ic", "mc"), ("north_node", "south_node"))}


def shortest_arc(a, b):
    d = abs(a - b) % 360.0
    return 360.0 - d if d > 180.0 else d


def detect(angle, catalog, orbs):
    for entry in catalog:
        exact = entry["angle"]
        normalized = 360.0 - exact if exact > 180.0 else exact
        orb = abs(angle - normalized)
        if orb <= orbs.get(entry["id"], entry["default_orb"]):
            return entry["id"], orb
    return None


def chart_aspects(positions, catalog, orbs):
    ids = sorted(positions)
    out = []
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if frozenset((a, b)) in LOCKED_PAIRS:
                continue
            hit = detect(shortest_arc(positions[a], positions[b]), catalog, orbs)
            if hit:
                out.append({"from": a, "to": b, "type": hit[0], "orb": round(hit[1], 9)})
    return out


def cross_aspects(transiting, transited, catalog, orbs):
    out = []
    for a in sorted(transiting):
        for b in sorted(transited):
            hit = detect(shortest_arc(transiting[a], transited[b]), catalog, orbs)
            if hit:
                out.append({"from": a, "to": b, "type": hit[0], "orb": round(hit[1], 9)})
    return out


def main():
    catalog = json.loads((CONTRACTS / "catalogs/aspects.json").read_text())["aspects"]
    horizons = json.loads((CONTRACTS / "reference/positions-horizons.json").read_text())
    nutation = json.loads((CONTRACTS / "reference/earth-orientation-erfa.json").read_text())["epochs"]
    bodies = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]

    def mean_positions(index):
        dpsi = nutation[index]["nutation_longitude_deg"]
        return {b: round((horizons["positions"][b][index]["lon_true_deg"] - dpsi) % 360.0, 7) for b in bodies}

    radix = mean_positions(3)  # 2024-01-01T12:00Z
    radix.update({"asc": 120.0, "desc": 300.0, "mc": 30.0, "ic": 210.0,
                  "north_node": 15.0, "south_node": 195.0})
    transit = mean_positions(4)  # 2024-10-17T18:00Z
    boundary = {"a": 0.0, "b": 96.0, "c": 216.0000001}  # a-b: square at exactly 6.0 deg orb (inclusive)
    cases = [
        {"id": "chart-2024-01-01-all-aspects", "kind": "chart", "positions": radix, "aspect_orbs": {},
         "expected": chart_aspects(radix, catalog, {})},
        {"id": "chart-orb-boundary", "kind": "chart", "positions": boundary, "aspect_orbs": {},
         "expected": chart_aspects(boundary, catalog, {})},
        {"id": "chart-orb-override", "kind": "chart", "positions": boundary, "aspect_orbs": {"square": 5.0},
         "expected": chart_aspects(boundary, catalog, {"square": 5.0})},
        {"id": "cross-2024-10-17-over-2024-01-01", "kind": "cross",
         "transiting": transit, "transited": {b: radix[b] for b in bodies}, "aspect_orbs": {},
         "expected": cross_aspects(transit, {b: radix[b] for b in bodies}, catalog, {})},
    ]
    doc = {
        "schema_version": 1,
        "catalog": "catalogs/aspects.json",
        "description": "Expected aspects for the documented detection rule (CONVENTIONS.md, 'Aspects'). Compare as sets of (unordered pair for 'chart', ordered pair for 'cross', type); orb to 1e-6 deg.",
        "generated_by": "tools/generate_aspect_fixture.py",
        "cases": cases,
    }
    out = CONTRACTS / "aspects/detection.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(doc, indent=2) + "\n")
    print({c["id"]: len(c["expected"]) for c in cases})


if __name__ == "__main__":
    main()
