#!/usr/bin/env python3
"""
Bias Comparison Analysis

Compares the three matrix implementations to verify bias elimination:
1. VLA Standard (baseline with bias)
2. Weighted Adjacency (VLA grid with correction factors)
3. Numerical Proximity (non-geometric, inherently unbiased)

Outputs:
- Neighbor count statistics for each approach
- Effective contact opportunity (after bias correction)
- Corner number analysis (1, 6, 36, 37, 39)
- Verification that corrected approaches eliminate bias
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.matrix import (
    VLAStandardMatrix,
    WeightedAdjacencyMatrix,
    NumericalProximityMatrix,
)


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_subheader(title: str) -> None:
    """Print a formatted subsection header."""
    print(f"\n--- {title} ---")


def analyze_matrix(matrix) -> dict:
    """Analyze a matrix implementation and return statistics."""
    stats = matrix.analyze_bias()

    # Get detailed per-number info
    neighbor_counts = {}
    effective_scores = {}
    for n in range(1, 40):
        neighbor_counts[n] = matrix.get_neighbor_count(n)
        effective_scores[n] = neighbor_counts[n] * matrix.get_bias_factor(n)

    stats['neighbor_counts'] = neighbor_counts
    stats['effective_scores'] = effective_scores

    return stats


def print_corner_analysis(matrices: list) -> None:
    """Print detailed analysis for corner numbers."""
    print_subheader("Corner Number Analysis (1, 6, 36, 37, 39)")
    print("These numbers are critical for N_1 and N_5 optimal ranges.")
    print()

    corners = [1, 6, 36, 37, 39]

    # Header
    print(f"{'Number':<8}", end="")
    for m in matrices:
        name = m.name[:20]
        print(f"{name:<25}", end="")
    print()
    print("-" * (8 + 25 * len(matrices)))

    # Data rows
    for corner in corners:
        print(f"{corner:<8}", end="")
        for m in matrices:
            count = m.get_neighbor_count(corner)
            factor = m.get_bias_factor(corner)
            effective = count * factor
            print(f"{count} neighbors × {factor:.2f} = {effective:.1f}".ljust(25), end="")
        print()


def print_bias_summary(matrices: list) -> None:
    """Print bias summary comparison."""
    print_subheader("Bias Summary by Matrix Type")
    print()

    for matrix in matrices:
        stats = matrix.analyze_bias()
        print(f"\n{matrix.name}:")
        print(f"  Raw neighbors:      min={stats['min_neighbors']}, max={stats['max_neighbors']}, avg={stats['avg_neighbors']:.1f}")
        print(f"  Effective contacts: min={stats['min_effective']:.1f}, max={stats['max_effective']:.1f}, avg={stats['avg_effective']:.1f}")
        print(f"  Variance (max-min): raw={stats['neighbor_variance']}, effective={stats['effective_variance']:.2f}")
        print(f"  Is Uniform (var<0.5): {'YES' if stats['is_uniform'] else 'NO'}")


def print_full_neighbor_table(matrix) -> None:
    """Print complete neighbor table for a matrix."""
    print_subheader(f"Full Neighbor Table: {matrix.name}")

    print(f"{'Num':<5}{'Neighbors':<8}{'Factor':<8}{'Effective':<10}{'Position':<12}")
    print("-" * 45)

    for n in range(1, 40):
        count = matrix.get_neighbor_count(n)
        factor = matrix.get_bias_factor(n)
        effective = count * factor

        # Determine position type if available
        if hasattr(matrix, 'get_position_type'):
            pos_type = matrix.get_position_type(n)
        else:
            pos_type = "n/a"

        print(f"{n:<5}{count:<8}{factor:<8.2f}{effective:<10.1f}{pos_type:<12}")


def print_contact_score_example(matrices: list) -> None:
    """Show example contact scores for a sample draw."""
    print_subheader("Example: Contact Scores for Draw [3, 15, 22, 28, 37]")
    print()

    sample_draw = [3, 15, 22, 28, 37]

    for matrix in matrices:
        scores = matrix.calculate_contact_scores(sample_draw)
        in_contact = matrix.get_in_contact_numbers(sample_draw)

        # Sort by score descending
        sorted_scores = sorted(scores.items(), key=lambda x: -x[1])
        top_10 = sorted_scores[:10]

        print(f"\n{matrix.name}:")
        print(f"  Numbers in contact: {len(in_contact)} total")
        print(f"  Top 10 by contact score:")
        for num, score in top_10:
            in_draw = "*" if num in sample_draw else " "
            print(f"    {in_draw} {num:2d}: {score:.2f}")


def verify_bias_elimination() -> bool:
    """Verify that corrected matrices eliminate bias. Return True if passed."""
    print_header("BIAS ELIMINATION VERIFICATION")

    vla = VLAStandardMatrix()
    weighted = WeightedAdjacencyMatrix(apply_correction=True)
    proximity = NumericalProximityMatrix(window_size=3, use_wraparound=True)

    all_passed = True

    # Test 1: VLA should have high variance (bias)
    vla_stats = vla.analyze_bias()
    vla_has_bias = vla_stats['effective_variance'] > 4.0
    print(f"\n1. VLA Standard has bias (variance > 4.0): ", end="")
    print("PASS" if vla_has_bias else "FAIL")
    print(f"   Actual variance: {vla_stats['effective_variance']:.2f}")
    if not vla_has_bias:
        all_passed = False

    # Test 2: Weighted should have low variance (corrected)
    weighted_stats = weighted.analyze_bias()
    weighted_corrected = weighted_stats['effective_variance'] < 1.0
    print(f"\n2. Weighted Adjacency is corrected (variance < 1.0): ", end="")
    print("PASS" if weighted_corrected else "FAIL")
    print(f"   Actual variance: {weighted_stats['effective_variance']:.2f}")
    if not weighted_corrected:
        all_passed = False

    # Test 3: Numerical Proximity should be uniform
    proximity_stats = proximity.analyze_bias()
    proximity_uniform = proximity_stats['is_uniform']
    print(f"\n3. Numerical Proximity is uniform (variance < 0.5): ", end="")
    print("PASS" if proximity_uniform else "FAIL")
    print(f"   Actual variance: {proximity_stats['effective_variance']:.2f}")
    if not proximity_uniform:
        all_passed = False

    # Test 4: Corner numbers should not be disadvantaged in corrected matrices
    corners = [1, 6, 36, 37, 39]
    print(f"\n4. Corner numbers (1,6,36,37,39) not disadvantaged:")

    for matrix in [weighted, proximity]:
        effective_scores = [matrix.get_neighbor_count(n) * matrix.get_bias_factor(n) for n in range(1, 40)]
        avg_effective = sum(effective_scores) / len(effective_scores)

        corner_effective = [matrix.get_neighbor_count(n) * matrix.get_bias_factor(n) for n in corners]
        avg_corner = sum(corner_effective) / len(corner_effective)

        # Corners should be within 20% of average
        corner_ok = abs(avg_corner - avg_effective) / avg_effective < 0.20
        print(f"   {matrix.name}: avg_corner={avg_corner:.1f}, avg_all={avg_effective:.1f} - ", end="")
        print("PASS" if corner_ok else "FAIL")
        if not corner_ok:
            all_passed = False

    return all_passed


def main():
    """Run the full bias comparison analysis."""
    print("\n" + "=" * 60)
    print("  MATRIX BIAS COMPARISON ANALYSIS")
    print("  VLA Visualizer Project")
    print("=" * 60)

    # Create matrix instances
    vla = VLAStandardMatrix()
    weighted_corrected = WeightedAdjacencyMatrix(apply_correction=True)
    weighted_raw = WeightedAdjacencyMatrix(apply_correction=False)
    proximity = NumericalProximityMatrix(window_size=3, use_wraparound=True)

    matrices = [vla, weighted_corrected, proximity]

    # Run verification tests
    all_passed = verify_bias_elimination()

    # Print detailed analysis
    print_bias_summary(matrices)
    print_corner_analysis(matrices)
    print_contact_score_example(matrices)

    # Print full table for VLA to show the bias
    print_full_neighbor_table(vla)

    # Summary
    print_header("SUMMARY")
    print()
    print("Matrix Implementations Created:")
    print("  1. VLAStandardMatrix      - Original VLA (baseline with bias)")
    print("  2. WeightedAdjacencyMatrix - VLA grid + correction factors")
    print("  3. NumericalProximityMatrix - Non-geometric (no bias)")
    print()

    if all_passed:
        print("RESULT: All verification tests PASSED")
        print("        Bias has been successfully eliminated/normalized.")
    else:
        print("RESULT: Some verification tests FAILED")
        print("        Review the output above for details.")

    print()
    print("Files created:")
    print("  src/matrix/base.py               - Base ContactMatrix interface")
    print("  src/matrix/vla_standard.py       - VLA baseline (biased)")
    print("  src/matrix/weighted_adjacency.py - Approach A (corrected)")
    print("  src/matrix/numerical_proximity.py - Approach C (unbiased)")
    print("  src/matrix/__init__.py           - Module exports")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
