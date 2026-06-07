"""
Generate multi-tier cosmograph star positions for criterion 3.7 STRETCH.

Amended scope per gandalf 2026-06-07:
  Tier 1: 100 stars (baseline — original spec)
  Tier 2: 1,000 stars (production-min — /forge PROVISIONAL count)
  Tier 3: 15,000 stars (production-aspirational — drax Mode B Phase 2)

Positions are deterministic (golden-angle Fibonacci sphere per cluster).
Per-star attributes: id, x/y/z, tier(1-4), element_primary, color_hue, brightness, sprite_size_uu

Cluster layout scales with total count:
  6 clusters representing substrate archetype families
  Cluster spread scales with total_stars^0.4 (keeps cluster density consistent)
  Cluster spacing scales with spread to maintain separation

Output: Content/Data/CosmographSpike/cosmograph_tier{N}_star_data.json
"""

import json
import os
import math

CLUSTER_DEFS = [
    # (cx_norm, cy_norm, cz_norm, element, archetype)
    # Positions normalized; actual coords = norm * spacing
    ( 0.5,  0.4,  0.3, "fire",      "Ember"),
    (-0.6,  0.5, -0.1, "water",     "Tide"),
    ( 0.25, -0.7,  0.5, "shadow",   "Dusk"),
    (-0.5, -0.4, -0.6, "earth",     "Stone"),
    ( 0.75, -0.5, -0.4, "lightning", "Thunder"),
    (-0.25,  0.6,  0.75, "wind",    "Zephyr"),
]

ELEMENT_COLORS = {
    "fire":      [1.0, 0.3, 0.05],
    "water":     [0.0, 0.6, 1.0],
    "shadow":    [0.35, 0.0, 0.9],
    "earth":     [0.5, 0.35, 0.1],
    "lightning": [1.0, 0.9, 0.1],
    "wind":      [0.5, 1.0, 0.7],
}

TIERS = [1, 1, 1, 2, 2, 2, 3, 3, 4]


def golden_fibonacci_sphere(n, spread):
    """
    n points on sphere surface via golden angle spiral.
    Deterministic, evenly distributed, scaled by spread.
    """
    if n <= 1:
        return [(0.0, 0.0, 0.0)]
    points = []
    phi = math.pi * (3.0 - math.sqrt(5.0))
    for i in range(n):
        y = 1.0 - (i / float(n - 1)) * 2.0
        radius = math.sqrt(max(0.0, 1.0 - y * y))
        theta = phi * i
        x = math.cos(theta) * radius
        z = math.sin(theta) * radius
        # Non-uniform density: slightly pull extremes inward for cluster feel
        density = 0.5 + 0.5 * abs(y)
        points.append((x * spread * density, y * spread * 0.7, z * spread * density))
    return points


def compute_cluster_params(total_stars):
    """
    Compute cluster centers + spread based on total star count.
    Spread scales with total^0.4; spacing scales with spread.
    """
    n_clusters = len(CLUSTER_DEFS)
    # Stars per cluster (distribute evenly with slight variation)
    base = total_stars // n_clusters
    remainder = total_stars % n_clusters
    counts = [base + (1 if i < remainder else 0) for i in range(n_clusters)]

    # Spread and spacing scale with sqrt-ish of total
    spread = 8.0 * (total_stars / 100.0) ** 0.4
    spacing = spread * 4.5

    clusters = []
    for i, (nx, ny, nz, element, archetype) in enumerate(CLUSTER_DEFS):
        clusters.append({
            "cx": nx * spacing,
            "cy": ny * spacing,
            "cz": nz * spacing,
            "spread": spread,
            "count": counts[i],
            "element": element,
            "archetype": archetype,
        })
    return clusters


def generate_stars(total_stars):
    clusters = compute_cluster_params(total_stars)
    stars = []
    star_id = 1

    for ci, c in enumerate(clusters):
        cluster_letter = chr(ord('A') + ci)
        sphere_pts = golden_fibonacci_sphere(c["count"], c["spread"])

        for i, (dx, dy, dz) in enumerate(sphere_pts):
            tier = TIERS[i % len(TIERS)]
            brightness = 0.2 + tier * 0.2
            size = 0.5 + tier * 0.25

            star = {
                "star_id": f"S{star_id:05d}",
                "cluster": cluster_letter,
                "x": round(c["cx"] + dx, 2),
                "y": round(c["cy"] + dy, 2),
                "z": round(c["cz"] + dz, 2),
                "tier": tier,
                "element_primary": c["element"],
                "archetype_stub": c["archetype"],
                "color_hue": ELEMENT_COLORS[c["element"]],
                "brightness": round(brightness, 2),
                "sprite_size_uu": round(size, 2),
            }
            stars.append(star)
            star_id += 1

    return stars, clusters


def generate_constellation_edges(stars, max_edges_per_star=2):
    """
    Within-cluster constellation edges.
    For large tiers, cap edges per star to keep edge count manageable.
    For Tier 3 (15K stars): edges = 15K * 2 = 30K (manageable for Niagara ribbon).
    """
    edges = []
    by_cluster = {}
    for s in stars:
        by_cluster.setdefault(s["cluster"], []).append(s["star_id"])

    for cluster_letter, ids in by_cluster.items():
        n = len(ids)
        for i in range(n):
            # Always connect to next star (chain)
            edges.append({"from": ids[i], "to": ids[(i + 1) % n]})
            # Additional cross-link for larger clusters
            if max_edges_per_star >= 2 and n > 6:
                step = max(3, n // 8)
                edges.append({"from": ids[i], "to": ids[(i + step) % n]})

    return edges


def generate_tier(tier_num, total_stars, out_dir):
    """Generate one tier and write to JSON."""
    tier_label = {1: "BASELINE", 2: "PRODUCTION-MIN", 3: "PRODUCTION-ASPIRATIONAL"}[tier_num]
    print(f"\n--- Tier {tier_num} ({tier_label}): {total_stars:,} stars ---")

    stars, clusters = generate_stars(total_stars)

    # Cap edges for Tier 3 to avoid excessive file size
    max_edges = 2 if total_stars <= 1000 else 1
    edges = generate_constellation_edges(stars, max_edges_per_star=max_edges)

    xs = [s["x"] for s in stars]
    ys = [s["y"] for s in stars]
    zs = [s["z"] for s in stars]

    output = {
        "description": f"Criterion 3.7 cosmograph spike Tier {tier_num} — {total_stars:,} stars ({tier_label})",
        "tier": tier_num,
        "tier_label": tier_label,
        "star_count": len(stars),
        "cluster_count": len(clusters),
        "edge_count": len(edges),
        "amendment_source": "gandalf 2026-06-07 direct relay — scale progression",
        "coordinate_space": {
            "units": "UE_units",
            "scale_note": "1 UU = 1 cm in UE5; cluster spacing scales with tier",
            "origin": "cosmograph_center",
        },
        "bounding_box": {
            "x_min": round(min(xs), 1), "x_max": round(max(xs), 1),
            "y_min": round(min(ys), 1), "y_max": round(max(ys), 1),
            "z_min": round(min(zs), 1), "z_max": round(max(zs), 1),
        },
        "element_color_map": ELEMENT_COLORS,
        "tier_brightness_map": {"T1": 0.4, "T2": 0.6, "T3": 0.8, "T4": 1.0},
        "cluster_summary": [
            {
                "cluster": chr(ord('A') + i),
                "element": c["element"],
                "archetype": c["archetype"],
                "count": c["count"],
                "center": [round(c["cx"], 1), round(c["cy"], 1), round(c["cz"], 1)],
                "spread_uu": round(c["spread"], 1),
            }
            for i, c in enumerate(clusters)
        ],
        "stars": stars,
        "constellation_edges": edges,
    }

    fname = f"cosmograph_tier{tier_num}_{total_stars:06d}stars.json"
    out_path = os.path.join(out_dir, fname)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    fsize_kb = os.path.getsize(out_path) / 1024
    print(f"  Stars: {len(stars):,} | Edges: {len(edges):,} | File: {fname} ({fsize_kb:.0f} KB)")
    print(f"  Bounds X[{output['bounding_box']['x_min']}, {output['bounding_box']['x_max']}]  "
          f"Y[{output['bounding_box']['y_min']}, {output['bounding_box']['y_max']}]  "
          f"Z[{output['bounding_box']['z_min']}, {output['bounding_box']['z_max']}]")

    by_cluster = {}
    for s in stars:
        by_cluster.setdefault(s["cluster"], []).append(s)
    for c_letter in sorted(by_cluster.keys()):
        ss = by_cluster[c_letter]
        print(f"  Cluster {c_letter} ({ss[0]['element_primary']}): {len(ss):,} stars")

    return out_path, len(stars), len(edges), output["bounding_box"]


def main():
    out_dir = r"C:\dev\reincarnated-unreal\Reincarnated\Content\Data\CosmographSpike"
    os.makedirs(out_dir, exist_ok=True)

    print("=" * 60)
    print("Criterion 3.7 STRETCH — Multi-tier cosmograph data generation")
    print("Amendment: gandalf 2026-06-07 — 3-tier scale progression")
    print("=" * 60)

    # Note: Tier 1 (100 stars) already generated in earlier script run.
    # Re-generating for completeness and consistent format with Tier 2/3.
    results = []
    for tier_num, total_stars in [(1, 100), (2, 1000), (3, 15000)]:
        path, stars, edges, bbox = generate_tier(tier_num, total_stars, out_dir)
        results.append((tier_num, total_stars, stars, edges, path))

    print("\n" + "=" * 60)
    print("SUMMARY:")
    for tier_num, requested, actual, edges, path in results:
        fname = os.path.basename(path)
        print(f"  Tier {tier_num}: {actual:,} stars, {edges:,} edges -> {fname}")
    print("\nNiagara performance expectations:")
    print("  Tier 1 (100):    60fps PC expected; mobile OK")
    print("  Tier 2 (1,000):  60fps PC expected; mobile borderline")
    print("  Tier 3 (15,000): <60fps PC without LOD; LOD architecture needed for mobile")
    print("\nLOD recommendation (per drax Mode B Phase 2 spec):")
    print("  Low zoom: centroid dots only (1 sprite per cluster = 6 sprites)")
    print("  Mid zoom: cluster-level constellation shape (subset of lines)")
    print("  High zoom: full individual stars + all constellation edges")
    print("  Niagara LOD: Scalability Groups (r.Niagara.QualityLevel 0/1/2)")


main()
