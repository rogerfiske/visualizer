"""
VLA Contact Bias Analysis
Quantifies the inherent positional bias in the contact-based prediction methodology
"""
import csv
import os

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
except ImportError:
    print("ERROR: matplotlib and numpy required")
    exit(1)

# VLA Standard Matrix Layout (6 rows x 7 cols, 39 numbers)
MATRIX = [
    [1,  7,  13, 19, 25, 31, 37],
    [2,  8,  14, 20, 26, 32, 38],
    [3,  9,  15, 21, 27, 33, 39],
    [4,  10, 16, 22, 28, 34, None],
    [5,  11, 17, 23, 29, 35, None],
    [6,  12, 18, 24, 30, 36, None],
]

def get_position(num):
    """Get (row, col) position of a number in the matrix"""
    for r, row in enumerate(MATRIX):
        for c, val in enumerate(row):
            if val == num:
                return (r, c)
    return None

def get_neighbors(num):
    """Get all adjacent numbers (8-directional) for a given number"""
    pos = get_position(num)
    if not pos:
        return []

    r, c = pos
    neighbors = []

    # All 8 directions
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 6 and 0 <= nc < 7:
            val = MATRIX[nr][nc]
            if val is not None:
                neighbors.append(val)

    return neighbors

def calculate_contact_exposure():
    """Calculate contact exposure (neighbor count) for each number"""
    exposure = {}
    for num in range(1, 40):
        neighbors = get_neighbors(num)
        exposure[num] = {
            'count': len(neighbors),
            'neighbors': neighbors,
            'position': get_position(num)
        }
    return exposure

def classify_position(num):
    """Classify number as corner, edge, or interior"""
    pos = get_position(num)
    if not pos:
        return "invalid"

    r, c = pos

    # Check if corner
    is_top = (r == 0)
    is_bottom = (r == 5) or (c == 6 and r == 2)  # Row 6 or last valid in col 7
    is_left = (c == 0)
    is_right = (c == 6) or (MATRIX[r][c+1] is None if c < 6 else True)

    corner_count = sum([is_top, is_bottom, is_left, is_right])

    if corner_count >= 2:
        return "corner"
    elif corner_count == 1:
        return "edge"
    else:
        return "interior"

def print_analysis():
    """Print detailed contact exposure analysis"""
    exposure = calculate_contact_exposure()

    print("=" * 80)
    print("  VLA CONTACT BIAS ANALYSIS")
    print("=" * 80)

    # Print matrix with exposure counts
    print("\n  MATRIX WITH CONTACT EXPOSURE (neighbor count):\n")
    print("       Col1   Col2   Col3   Col4   Col5   Col6   Col7")
    print("      " + "-" * 49)

    for r in range(6):
        row_str = f"  R{r+1} |"
        for c in range(7):
            val = MATRIX[r][c]
            if val:
                exp = exposure[val]['count']
                row_str += f"  {val:2d}({exp}) "
            else:
                row_str += "   --   "
        print(row_str)

    # Summary by position type
    print("\n  EXPOSURE BY POSITION TYPE:")
    print("  " + "-" * 50)

    corners = []
    edges = []
    interiors = []

    for num in range(1, 40):
        pos_type = classify_position(num)
        exp = exposure[num]['count']

        if pos_type == "corner":
            corners.append((num, exp))
        elif pos_type == "edge":
            edges.append((num, exp))
        else:
            interiors.append((num, exp))

    print(f"\n  CORNERS ({len(corners)} numbers): Avg {sum(e for _,e in corners)/len(corners):.1f} contacts")
    for num, exp in sorted(corners):
        print(f"    {num:2d}: {exp} neighbors -> {exposure[num]['neighbors']}")

    print(f"\n  EDGES ({len(edges)} numbers): Avg {sum(e for _,e in edges)/len(edges):.1f} contacts")
    for num, exp in sorted(edges):
        print(f"    {num:2d}: {exp} neighbors")

    print(f"\n  INTERIOR ({len(interiors)} numbers): Avg {sum(e for _,e in interiors)/len(interiors):.1f} contacts")
    for num, exp in sorted(interiors):
        print(f"    {num:2d}: {exp} neighbors")

    # Bias quantification
    print("\n  BIAS QUANTIFICATION:")
    print("  " + "-" * 50)

    avg_corner = sum(e for _,e in corners) / len(corners)
    avg_edge = sum(e for _,e in edges) / len(edges)
    avg_interior = sum(e for _,e in interiors) / len(interiors)

    print(f"\n  Interior numbers are {avg_interior/avg_corner:.1f}x more likely to be 'in contact'")
    print(f"  than corner numbers purely due to geometry.")
    print(f"\n  Contact probability (uniform random draw):")
    print(f"    Corner number:   {avg_corner/8*100:.1f}% base contact rate")
    print(f"    Edge number:     {avg_edge/8*100:.1f}% base contact rate")
    print(f"    Interior number: {avg_interior/8*100:.1f}% base contact rate")

    return exposure

def create_heatmap(output_dir):
    """Create visual heatmap of contact exposure"""
    exposure = calculate_contact_exposure()

    fig, ax = plt.subplots(figsize=(12, 10))

    # Create grid
    grid = np.zeros((6, 7))
    for r in range(6):
        for c in range(7):
            val = MATRIX[r][c]
            if val:
                grid[r, c] = exposure[val]['count']
            else:
                grid[r, c] = np.nan

    # Custom colormap: red (low) -> yellow -> green (high)
    cmap = plt.cm.RdYlGn

    # Plot heatmap
    im = ax.imshow(grid, cmap=cmap, vmin=2, vmax=8)

    # Add text annotations
    for r in range(6):
        for c in range(7):
            val = MATRIX[r][c]
            if val:
                exp = exposure[val]['count']
                color = 'white' if exp <= 4 else 'black'
                ax.text(c, r, f'{val}\n({exp})', ha='center', va='center',
                       fontsize=12, fontweight='bold', color=color)

    # Styling
    ax.set_xticks(range(7))
    ax.set_yticks(range(6))
    ax.set_xticklabels([f'Col {i+1}' for i in range(7)], fontsize=10)
    ax.set_yticklabels([f'Row {i+1}' for i in range(6)], fontsize=10)

    ax.set_title('VLA Matrix Contact Exposure Bias\nNumber (Contact Count)',
                 fontsize=14, fontweight='bold', pad=15)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Number of Adjacent Cells (Contact Exposure)', fontsize=11)

    # Add legend
    legend_text = """
BIAS SUMMARY:
- Corner (red): 3 contacts
- Edge (yellow): 5 contacts
- Interior (green): 8 contacts

Interior numbers are 2.7x more likely
to be "in contact" than corners
purely due to grid geometry.
"""
    ax.text(1.25, 0.5, legend_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()

    filepath = os.path.join(output_dir, 'contact_bias_heatmap.png')
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    return filepath

def create_exposure_distribution(output_dir):
    """Create bar chart of exposure by number"""
    exposure = calculate_contact_exposure()

    fig, ax = plt.subplots(figsize=(14, 6))

    numbers = list(range(1, 40))
    counts = [exposure[n]['count'] for n in numbers]

    # Color by position type
    colors = []
    for n in numbers:
        pos_type = classify_position(n)
        if pos_type == "corner":
            colors.append('#E74C3C')  # Red
        elif pos_type == "edge":
            colors.append('#F39C12')  # Orange/Yellow
        else:
            colors.append('#27AE60')  # Green

    bars = ax.bar(numbers, counts, color=colors, edgecolor='white', linewidth=0.5)

    # Add reference lines
    ax.axhline(y=3, color='#E74C3C', linestyle='--', linewidth=1.5, alpha=0.5)
    ax.axhline(y=5, color='#F39C12', linestyle='--', linewidth=1.5, alpha=0.5)
    ax.axhline(y=8, color='#27AE60', linestyle='--', linewidth=1.5, alpha=0.5)

    ax.set_xlabel('Number', fontsize=12, fontweight='bold')
    ax.set_ylabel('Contact Exposure (Neighbor Count)', fontsize=12, fontweight='bold')
    ax.set_title('VLA Contact Exposure by Number\nStructural Bias in Contact-Based Prediction',
                 fontsize=14, fontweight='bold', pad=15)

    ax.set_xticks(range(1, 40, 2))
    ax.set_ylim(0, 10)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)

    # Legend
    corner_patch = mpatches.Patch(color='#E74C3C', label='Corner (3 contacts)')
    edge_patch = mpatches.Patch(color='#F39C12', label='Edge (5 contacts)')
    interior_patch = mpatches.Patch(color='#27AE60', label='Interior (8 contacts)')
    ax.legend(handles=[corner_patch, edge_patch, interior_patch], loc='upper right', fontsize=10)

    plt.tight_layout()

    filepath = os.path.join(output_dir, 'contact_exposure_by_number.png')
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    return filepath

def main():
    output_dir = r'C:\Users\Minis\CascadeProjects\visualizer\data\charts'
    os.makedirs(output_dir, exist_ok=True)

    # Print analysis
    print_analysis()

    # Generate charts
    print("\n" + "=" * 80)
    print("  GENERATING VISUALIZATIONS")
    print("=" * 80)

    path1 = create_heatmap(output_dir)
    print(f"  Created: {os.path.basename(path1)}")

    path2 = create_exposure_distribution(output_dir)
    print(f"  Created: {os.path.basename(path2)}")

    print("\n" + "=" * 80)
    print("  COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
