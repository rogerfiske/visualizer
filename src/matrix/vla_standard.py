"""
VLA Standard Matrix (Baseline for Comparison)

This is the original VLA 6x7 grid layout WITHOUT any bias correction.
Used as a baseline to measure improvement from corrected approaches.

This is essentially WeightedAdjacencyMatrix with apply_correction=False,
but provided as a separate class for clarity.
"""

from typing import List, Dict, Tuple
from .base import ContactMatrix


# VLA Standard 6x7 Matrix Layout
VLA_MATRIX = [
    [1,  7,  13, 19, 25, 31, 37],
    [2,  8,  14, 20, 26, 32, 38],
    [3,  9,  15, 21, 27, 33, 39],
    [4,  10, 16, 22, 28, 34, None],
    [5,  11, 17, 23, 29, 35, None],
    [6,  12, 18, 24, 30, 36, None],
]

ROWS = 6
COLS = 7


class VLAStandardMatrix(ContactMatrix):
    """
    Original VLA grid matrix with NO bias correction.

    This implementation exhibits the documented bias:
    - Corner numbers (1, 6, 36, 37, 39): ~3.2 avg neighbors
    - Edge numbers: ~5.1 avg neighbors
    - Interior numbers: ~7.9 avg neighbors

    Use this as a baseline to measure improvement from corrected approaches.
    """

    def __init__(self):
        self._position_map = {}
        self._neighbor_cache = {}
        self._build_position_map()
        self._build_neighbor_cache()

    @property
    def name(self) -> str:
        return "VLAStandard(original)"

    def _build_position_map(self) -> None:
        """Build mapping from number to grid position."""
        for row in range(ROWS):
            for col in range(COLS):
                num = VLA_MATRIX[row][col]
                if num is not None:
                    self._position_map[num] = (row, col)

    def _build_neighbor_cache(self) -> None:
        """Pre-compute neighbors for all numbers."""
        for num in range(1, self.POOL_SIZE + 1):
            row, col = self._position_map[num]
            neighbors = []

            directions = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),          (0, 1),
                (1, -1),  (1, 0), (1, 1),
            ]

            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    neighbor_num = VLA_MATRIX[nr][nc]
                    if neighbor_num is not None:
                        neighbors.append(neighbor_num)

            self._neighbor_cache[num] = sorted(neighbors)

    def get_neighbors(self, number: int) -> List[int]:
        """Return 8-directionally adjacent numbers in VLA grid."""
        self._validate_number(number)
        return self._neighbor_cache[number].copy()

    def get_neighbor_count(self, number: int) -> int:
        """Return neighbor count (exhibits natural bias)."""
        self._validate_number(number)
        return len(self._neighbor_cache[number])

    def get_bias_factor(self, number: int) -> float:
        """
        Return bias factor (always 1.0 - no correction applied).

        This means corner numbers remain disadvantaged.
        """
        self._validate_number(number)
        return 1.0

    def get_position(self, number: int) -> Tuple[int, int]:
        """Return (row, col) position of number in VLA grid."""
        self._validate_number(number)
        return self._position_map[number]

    def get_position_type(self, number: int) -> str:
        """Classify number as corner, edge, or interior."""
        self._validate_number(number)
        neighbor_count = len(self._neighbor_cache[number])
        if neighbor_count <= 4:
            return "corner"
        elif neighbor_count <= 5:
            return "edge"
        elif neighbor_count <= 7:
            return "reduced_edge"
        else:
            return "interior"

    def get_corner_numbers(self) -> List[int]:
        """Return the 5 corner numbers that are most disadvantaged."""
        return [1, 6, 36, 37, 39]

    def get_bias_summary(self) -> Dict[str, Dict]:
        """Return bias statistics by position type."""
        types = {"corner": [], "edge": [], "reduced_edge": [], "interior": []}

        for n in range(1, self.POOL_SIZE + 1):
            pos_type = self.get_position_type(n)
            types[pos_type].append(self.get_neighbor_count(n))

        summary = {}
        for pos_type, counts in types.items():
            if counts:
                summary[pos_type] = {
                    'count': len(counts),
                    'avg_neighbors': sum(counts) / len(counts),
                    'min_neighbors': min(counts),
                    'max_neighbors': max(counts),
                }
        return summary


def create_default() -> VLAStandardMatrix:
    """Create a VLAStandardMatrix instance."""
    return VLAStandardMatrix()
