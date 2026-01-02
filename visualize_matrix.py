#!/usr/bin/env python3
"""
Matrix Visualization Tool

Visualize contact matrices and draw analysis:
- ASCII grid display with contact highlighting
- Bias heatmap visualization
- Draw history overlay
- Comparison between matrix types

Usage:
    python visualize_matrix.py                     # Show VLA grid with latest draw
    python visualize_matrix.py --date 2025-12-30   # Show grid for specific date
    python visualize_matrix.py --compare           # Compare all matrix types
    python visualize_matrix.py --bias              # Show bias heatmap
    python visualize_matrix.py --chart             # Generate matplotlib charts
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Set

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.matrix import (
    VLAStandardMatrix,
    WeightedAdjacencyMatrix,
    NumericalProximityMatrix,
)
from src.predictor import DrawHistory

# ANSI color codes for terminal
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'


# VLA Matrix Layout (6 rows x 7 cols)
VLA_GRID = [
    [1,  7,  13, 19, 25, 31, 37],
    [2,  8,  14, 20, 26, 32, 38],
    [3,  9,  15, 21, 27, 33, 39],
    [4,  10, 16, 22, 28, 34, None],
    [5,  11, 17, 23, 29, 35, None],
    [6,  12, 18, 24, 30, 36, None],
]


def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def get_position_type(num: int, matrix: VLAStandardMatrix) -> str:
    """Get position type for coloring."""
    if num is None:
        return "empty"
    count = matrix.get_neighbor_count(num)
    if count <= 4:
        return "corner"
    elif count <= 5:
        return "edge"
    elif count <= 7:
        return "reduced"
    return "interior"


def display_vla_grid(
    drawn: Set[int] = None,
    in_contact: Set[int] = None,
    show_bias: bool = False,
    matrix: VLAStandardMatrix = None
) -> None:
    """
    Display the VLA 6x7 grid with optional highlighting.

    Args:
        drawn: Numbers that were drawn (highlighted in red)
        in_contact: Numbers in contact with draws (highlighted in yellow)
        show_bias: Show bias coloring by position type
        matrix: Matrix instance for bias calculations
    """
    if drawn is None:
        drawn = set()
    if in_contact is None:
        in_contact = set()
    if matrix is None:
        matrix = VLAStandardMatrix()

    print("\n    VLA STANDARD MATRIX (6x7 Grid)")
    print("    Columns fill top-to-bottom: 1-6, 7-12, 13-18, etc.")
    print()

    # Column headers
    print("       ", end="")
    for col in range(7):
        print(f"Col{col+1:1d}  ", end="")
    print()
    print("      " + "-" * 49)

    for row in range(6):
        print(f"  R{row+1}  |", end="")
        for col in range(7):
            num = VLA_GRID[row][col]

            if num is None:
                print("  --  ", end="")
            else:
                # Determine formatting
                if num in drawn:
                    # Drawn number - red background
                    formatted = f"{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}{num:3d}{Colors.RESET}"
                elif num in in_contact:
                    # In contact - yellow/cyan
                    formatted = f"{Colors.CYAN}{Colors.BOLD}{num:3d}{Colors.RESET}"
                elif show_bias:
                    # Show bias coloring
                    pos_type = get_position_type(num, matrix)
                    if pos_type == "corner":
                        formatted = f"{Colors.RED}{num:3d}{Colors.RESET}"
                    elif pos_type == "edge":
                        formatted = f"{Colors.YELLOW}{num:3d}{Colors.RESET}"
                    elif pos_type == "reduced":
                        formatted = f"{Colors.GREEN}{num:3d}{Colors.RESET}"
                    else:  # interior
                        formatted = f"{Colors.WHITE}{num:3d}{Colors.RESET}"
                else:
                    formatted = f"{num:3d}"

                print(f"  {formatted}  ", end="")
        print("|")

    print("      " + "-" * 49)

    # Legend
    if drawn or in_contact:
        print("\n  Legend:")
        if drawn:
            print(f"    {Colors.BG_RED}{Colors.WHITE}{Colors.BOLD} ## {Colors.RESET} = Drawn numbers")
        if in_contact:
            print(f"    {Colors.CYAN}{Colors.BOLD} ## {Colors.RESET} = In contact (adjacent to drawn)")

    if show_bias:
        print("\n  Bias Legend (neighbor count):")
        print(f"    {Colors.RED}###{Colors.RESET} = Corner (3-4 neighbors) - UNDERWEIGHTED")
        print(f"    {Colors.YELLOW}###{Colors.RESET} = Edge (5 neighbors)")
        print(f"    {Colors.GREEN}###{Colors.RESET} = Reduced edge (6-7 neighbors)")
        print(f"    {Colors.WHITE}###{Colors.RESET} = Interior (8 neighbors) - OVERWEIGHTED")


def display_numerical_proximity_grid(
    drawn: Set[int] = None,
    window_size: int = 3
) -> None:
    """
    Display numerical proximity as a linear representation.
    """
    if drawn is None:
        drawn = set()

    matrix = NumericalProximityMatrix(window_size=window_size, use_wraparound=True)

    print(f"\n    NUMERICAL PROXIMITY (k={window_size}, wraparound)")
    print("    Contact = within ±3 numbers (wraps at edges)")
    print()

    # Calculate in-contact numbers
    in_contact = set()
    for d in drawn:
        in_contact.update(matrix.get_neighbors(d))

    # Display as rows of 13 (matches 13x3 toroidal layout concept)
    print("      " + "-" * 66)
    for row_start in [1, 14, 27]:
        print("      |", end="")
        for num in range(row_start, min(row_start + 13, 40)):
            if num in drawn:
                formatted = f"{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}{num:3d}{Colors.RESET}"
            elif num in in_contact:
                formatted = f"{Colors.CYAN}{Colors.BOLD}{num:3d}{Colors.RESET}"
            else:
                formatted = f"{num:3d}"
            print(f" {formatted} ", end="")
        print(" |")
    print("      " + "-" * 66)

    print("\n  All numbers have exactly 6 neighbors (uniform, no bias)")


def display_contact_analysis(
    drawn: List[int],
    matrix_type: str = 'vla'
) -> None:
    """
    Show detailed contact analysis for a draw.
    """
    if matrix_type == 'vla':
        matrix = VLAStandardMatrix()
    elif matrix_type == 'weighted':
        matrix = WeightedAdjacencyMatrix(apply_correction=True)
    else:
        matrix = NumericalProximityMatrix(window_size=3, use_wraparound=True)

    print(f"\n  Contact Analysis ({matrix.name}):")
    print("  " + "-" * 50)

    scores = matrix.calculate_contact_scores(drawn)
    in_contact = matrix.get_in_contact_numbers(drawn)

    # Sort by score
    sorted_scores = sorted(scores.items(), key=lambda x: -x[1])

    print(f"\n  Drawn: {drawn}")
    print(f"  In Contact: {len(in_contact)} numbers")
    print(f"\n  Top 15 by Contact Score:")

    for i, (num, score) in enumerate(sorted_scores[:15], 1):
        bar = "#" * int(score * 5)
        in_draw = "*" if num in drawn else " "
        bias = matrix.get_bias_factor(num)
        print(f"    {in_draw}{num:3d}: {score:5.2f} (bias factor: {bias:.2f}) {bar}")


def display_bias_comparison() -> None:
    """
    Compare bias across all matrix types.
    """
    print_header("MATRIX BIAS COMPARISON")

    matrices = [
        VLAStandardMatrix(),
        WeightedAdjacencyMatrix(apply_correction=True),
        NumericalProximityMatrix(window_size=3, use_wraparound=True),
    ]

    # Header
    print(f"\n  {'Number':<8}", end="")
    for m in matrices:
        name = m.name[:18]
        print(f"{name:<20}", end="")
    print()
    print("  " + "-" * 68)

    # Show key numbers (corners and some interior)
    key_numbers = [1, 6, 8, 15, 22, 36, 37, 39]

    for num in key_numbers:
        print(f"  {num:<8}", end="")
        for m in matrices:
            count = m.get_neighbor_count(num)
            factor = m.get_bias_factor(num)
            effective = count * factor
            print(f"{count}n × {factor:.2f} = {effective:.1f}".ljust(20), end="")
        print()

    # Summary stats
    print("\n  " + "-" * 68)
    print(f"  {'Variance':<8}", end="")
    for m in matrices:
        stats = m.analyze_bias()
        var = stats['effective_variance']
        uniform = "YES" if stats['is_uniform'] else "NO"
        print(f"var={var:.2f} uniform={uniform}".ljust(20), end="")
    print()


def display_draw_history_overlay(
    history: DrawHistory,
    num_draws: int = 5
) -> None:
    """
    Show recent draws overlaid on the grid.
    """
    print_header(f"RECENT {num_draws} DRAWS OVERLAY")

    recent = history.draws[-num_draws:]
    matrix = VLAStandardMatrix()

    # Count how many times each number appeared
    appearance_count = {}
    for draw in recent:
        for num in draw['numbers']:
            appearance_count[num] = appearance_count.get(num, 0) + 1

    print(f"\n  Last {num_draws} draws:")
    for draw in recent:
        print(f"    {draw['date_str']}: {draw['numbers']}")

    print("\n  Appearance frequency on grid:")
    print()

    # Display grid with frequency
    print("       ", end="")
    for col in range(7):
        print(f"Col{col+1:1d}  ", end="")
    print()
    print("      " + "-" * 49)

    for row in range(6):
        print(f"  R{row+1}  |", end="")
        for col in range(7):
            num = VLA_GRID[row][col]

            if num is None:
                print("  --  ", end="")
            else:
                count = appearance_count.get(num, 0)
                if count >= 3:
                    formatted = f"{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}{num:3d}{Colors.RESET}"
                elif count == 2:
                    formatted = f"{Colors.YELLOW}{Colors.BOLD}{num:3d}{Colors.RESET}"
                elif count == 1:
                    formatted = f"{Colors.CYAN}{num:3d}{Colors.RESET}"
                else:
                    formatted = f"{num:3d}"

                print(f"  {formatted}  ", end="")
        print("|")

    print("      " + "-" * 49)
    print(f"\n  Legend: {Colors.BG_RED}{Colors.WHITE} 3+ {Colors.RESET}  {Colors.YELLOW} 2x {Colors.RESET}  {Colors.CYAN} 1x {Colors.RESET}  plain=0")


def generate_matplotlib_chart(
    drawn: List[int] = None,
    output_path: Path = None
) -> None:
    """
    Generate matplotlib visualization of the matrix.
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        import numpy as np
    except ImportError:
        print("  matplotlib not installed. Run: pip install matplotlib")
        return

    if drawn is None:
        drawn = []

    matrix = VLAStandardMatrix()
    drawn_set = set(drawn)
    in_contact = set(matrix.get_in_contact_numbers(drawn)) - drawn_set

    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    # Draw grid
    for row in range(6):
        for col in range(7):
            num = VLA_GRID[row][col]
            x, y = col, 5 - row  # Flip y for display

            if num is None:
                color = 'lightgray'
                text = '--'
            elif num in drawn_set:
                color = 'red'
                text = str(num)
            elif num in in_contact:
                color = 'yellow'
                text = str(num)
            else:
                # Color by bias
                neighbor_count = matrix.get_neighbor_count(num)
                if neighbor_count <= 4:
                    color = 'lightcoral'
                elif neighbor_count <= 5:
                    color = 'lightyellow'
                elif neighbor_count <= 7:
                    color = 'lightgreen'
                else:
                    color = 'lightblue'
                text = str(num)

            rect = patches.Rectangle((x, y), 1, 1, linewidth=1,
                                     edgecolor='black', facecolor=color)
            ax.add_patch(rect)
            ax.text(x + 0.5, y + 0.5, text, ha='center', va='center',
                   fontsize=12, fontweight='bold')

    ax.set_xlim(0, 7)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.set_xticks([i + 0.5 for i in range(7)])
    ax.set_xticklabels([f'Col{i+1}' for i in range(7)])
    ax.set_yticks([i + 0.5 for i in range(6)])
    ax.set_yticklabels([f'R{6-i}' for i in range(6)])

    title = 'VLA Matrix Grid'
    if drawn:
        title += f'\nDrawn: {drawn}'
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Legend
    legend_elements = [
        patches.Patch(facecolor='red', label='Drawn'),
        patches.Patch(facecolor='yellow', label='In Contact'),
        patches.Patch(facecolor='lightcoral', label='Corner (3-4 neighbors)'),
        patches.Patch(facecolor='lightyellow', label='Edge (5 neighbors)'),
        patches.Patch(facecolor='lightgreen', label='Reduced (6-7 neighbors)'),
        patches.Patch(facecolor='lightblue', label='Interior (8 neighbors)'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1))

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"  Chart saved to: {output_path}")
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Visualize contact matrices and draw analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--date', type=str, help="Show grid for specific date (YYYY-MM-DD)")
    parser.add_argument('--draw', type=str, help="Comma-separated numbers to highlight (e.g., 3,15,22,28,37)")
    parser.add_argument('--bias', action='store_true', help="Show bias coloring")
    parser.add_argument('--compare', action='store_true', help="Compare all matrix types")
    parser.add_argument('--proximity', action='store_true', help="Show numerical proximity grid")
    parser.add_argument('--history', type=int, default=0, help="Show last N draws overlay")
    parser.add_argument('--chart', action='store_true', help="Generate matplotlib chart")
    parser.add_argument('--output', type=Path, help="Save chart to file")

    args = parser.parse_args()

    # Load history
    history = DrawHistory()

    # Determine which draw to show
    if args.draw:
        drawn = [int(x.strip()) for x in args.draw.split(',')]
    elif args.date:
        for fmt in ["%Y-%m-%d", "%m/%d/%Y"]:
            try:
                date = datetime.strptime(args.date, fmt)
                break
            except ValueError:
                continue
        else:
            print(f"Cannot parse date: {args.date}")
            return 1

        draw = history.get_draw_by_date(date)
        if draw:
            drawn = draw['numbers']
            print(f"\nDraw for {args.date}: {drawn}")
        else:
            print(f"No draw found for {args.date}")
            return 1
    else:
        # Use latest draw
        draw = history.get_last_draw()
        drawn = draw['numbers']
        print(f"\nLatest draw ({draw['date_str']}): {drawn}")

    # Calculate in-contact numbers
    matrix = VLAStandardMatrix()
    in_contact = set(matrix.get_in_contact_numbers(drawn)) - set(drawn)

    # Display based on options
    if args.compare:
        display_bias_comparison()
    elif args.proximity:
        display_numerical_proximity_grid(set(drawn))
    elif args.history > 0:
        display_draw_history_overlay(history, args.history)
    elif args.chart:
        generate_matplotlib_chart(drawn, args.output)
    else:
        # Default: show VLA grid
        display_vla_grid(
            drawn=set(drawn),
            in_contact=in_contact,
            show_bias=args.bias,
            matrix=matrix
        )

        if not args.bias:
            # Also show contact analysis
            display_contact_analysis(drawn, 'vla')

    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
