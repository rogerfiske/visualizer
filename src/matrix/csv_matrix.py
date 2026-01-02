"""
Generic CSV Matrix Loader

Loads any grid-based matrix from CSV and computes:
- 8-directional neighbor relationships
- Bias factors based on neighbor counts
- Weighted correction factors for bias mitigation
"""

import csv
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from .base import ContactMatrix


class CSVGridMatrix(ContactMatrix):
    """
    Generic matrix loader for any CSV grid layout.

    Computes 8-directional adjacency based on grid positions.
    Supports weighted correction to eliminate positional bias.
    """

    def __init__(
        self,
        csv_path: Path,
        name: Optional[str] = None,
        apply_correction: bool = False
    ):
        """
        Load matrix from CSV file.

        Args:
            csv_path: Path to CSV file with grid layout
            name: Display name for this matrix
            apply_correction: If True, apply bias correction factors
        """
        self.csv_path = Path(csv_path)
        self._name = name or self.csv_path.stem
        self.apply_correction = apply_correction

        # Grid storage
        self.grid: List[List[Optional[int]]] = []
        self.num_rows = 0
        self.num_cols = 0

        # Position lookup: number -> (row, col)
        self._positions: Dict[int, Tuple[int, int]] = {}

        # Neighbor cache
        self._neighbor_cache: Dict[int, List[int]] = {}

        # Correction factors
        self._correction_factors: Dict[int, float] = {}

        # Load and process
        self._load_csv()
        self._build_neighbor_cache()
        self._compute_correction_factors()

    @property
    def name(self) -> str:
        suffix = "(corrected)" if self.apply_correction else "(original)"
        return f"{self._name} {suffix}"

    def _load_csv(self) -> None:
        """Load grid from CSV file."""
        with open(self.csv_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                grid_row = []
                for cell in row:
                    cell = cell.strip()
                    if cell and cell.isdigit():
                        num = int(cell)
                        grid_row.append(num)
                    else:
                        grid_row.append(None)

                # Only add non-empty rows
                if any(cell is not None for cell in grid_row):
                    self.grid.append(grid_row)

        self.num_rows = len(self.grid)
        self.num_cols = max(len(row) for row in self.grid) if self.grid else 0

        # Pad rows to equal length
        for row in self.grid:
            while len(row) < self.num_cols:
                row.append(None)

        # Build position lookup
        for r, row in enumerate(self.grid):
            for c, num in enumerate(row):
                if num is not None:
                    self._positions[num] = (r, c)

    def _build_neighbor_cache(self) -> None:
        """Build 8-directional neighbor relationships."""
        # 8 directions: N, NE, E, SE, S, SW, W, NW
        directions = [
            (-1, 0), (-1, 1), (0, 1), (1, 1),
            (1, 0), (1, -1), (0, -1), (-1, -1)
        ]

        for num in range(1, self.POOL_SIZE + 1):
            if num not in self._positions:
                # Number not in grid - no neighbors
                self._neighbor_cache[num] = []
                continue

            row, col = self._positions[num]
            neighbors = []

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc

                # Check bounds
                if 0 <= new_row < self.num_rows and 0 <= new_col < self.num_cols:
                    neighbor = self.grid[new_row][new_col]
                    if neighbor is not None:
                        neighbors.append(neighbor)

            self._neighbor_cache[num] = sorted(neighbors)

    def _compute_correction_factors(self) -> None:
        """Compute correction factors to equalize effective contacts."""
        if not self.apply_correction:
            # No correction - all factors = 1.0
            for num in range(1, self.POOL_SIZE + 1):
                self._correction_factors[num] = 1.0
            return

        # Find maximum neighbor count (target)
        max_neighbors = max(
            len(self._neighbor_cache.get(n, []))
            for n in range(1, self.POOL_SIZE + 1)
        )

        if max_neighbors == 0:
            max_neighbors = 1  # Avoid division by zero

        # Compute factors: target / actual
        for num in range(1, self.POOL_SIZE + 1):
            actual = len(self._neighbor_cache.get(num, []))
            if actual > 0:
                self._correction_factors[num] = max_neighbors / actual
            else:
                self._correction_factors[num] = 1.0

    def get_neighbors(self, number: int) -> List[int]:
        """Get adjacent numbers in the grid."""
        return self._neighbor_cache.get(number, [])

    def get_neighbor_count(self, number: int) -> int:
        """Get count of adjacent numbers."""
        return len(self._neighbor_cache.get(number, []))

    def get_bias_factor(self, number: int) -> float:
        """Get bias correction factor."""
        return self._correction_factors.get(number, 1.0)

    def get_position(self, number: int) -> Optional[Tuple[int, int]]:
        """Get grid position (row, col) for a number."""
        return self._positions.get(number)

    def get_grid_display(self) -> str:
        """Return ASCII representation of the grid."""
        lines = []

        # Header
        lines.append(f"       " + "  ".join(f"Col{c+1}" for c in range(self.num_cols)))
        lines.append("      " + "-" * (self.num_cols * 6 + 1))

        for r, row in enumerate(self.grid):
            line = f"  R{r+1}  |"
            for cell in row:
                if cell is None:
                    line += "  --  "
                else:
                    line += f"  {cell:2d}  "
            line += "|"
            lines.append(line)

        lines.append("      " + "-" * (self.num_cols * 6 + 1))

        return "\n".join(lines)

    def export_neighbors_csv(self, output_path: Path) -> None:
        """Export neighbor data to CSV."""
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['number', 'neighbor_count', 'bias_factor', 'effective_contacts', 'neighbors'])

            for num in range(1, self.POOL_SIZE + 1):
                neighbors = self.get_neighbors(num)
                count = len(neighbors)
                factor = self.get_bias_factor(num)
                effective = count * factor
                neighbors_str = ' '.join(map(str, neighbors))
                writer.writerow([num, count, f'{factor:.3f}', f'{effective:.1f}', neighbors_str])


def analyze_matrix(csv_path: Path, name: str = None) -> Dict:
    """
    Analyze a matrix CSV file for bias characteristics.

    Returns dict with:
    - grid_display: ASCII grid
    - bias_stats: Statistics about bias
    - position_types: Classification of each number
    """
    # Load without correction to see raw bias
    matrix = CSVGridMatrix(csv_path, name=name, apply_correction=False)

    # Collect stats
    neighbor_counts = {}
    for num in range(1, matrix.POOL_SIZE + 1):
        count = matrix.get_neighbor_count(num)
        neighbor_counts[num] = count

    # Group by neighbor count
    by_count = {}
    for num, count in neighbor_counts.items():
        if count not in by_count:
            by_count[count] = []
        by_count[count].append(num)

    # Calculate variance
    counts = list(neighbor_counts.values())
    if counts:
        mean = sum(counts) / len(counts)
        variance = sum((c - mean) ** 2 for c in counts) / len(counts)
    else:
        mean = variance = 0

    # Find min/max
    min_count = min(counts) if counts else 0
    max_count = max(counts) if counts else 0

    return {
        'name': matrix._name,
        'grid_display': matrix.get_grid_display(),
        'num_rows': matrix.num_rows,
        'num_cols': matrix.num_cols,
        'neighbor_counts': neighbor_counts,
        'by_count': by_count,
        'mean_neighbors': mean,
        'variance': variance,
        'min_neighbors': min_count,
        'max_neighbors': max_count,
        'bias_ratio': max_count / min_count if min_count > 0 else float('inf'),
        'numbers_in_grid': len(matrix._positions),
    }
