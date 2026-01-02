"""
Weighted Adjacency Matrix (Approach A)

Uses VLA's standard 6x7 grid layout but applies correction factors
to normalize contact scores across all positions.

Corner numbers get 2.5x boost, edges get 1.6x boost, interior stays at 1.0x.
This equalizes the expected contact opportunity for all numbers.
"""

from typing import List, Dict, Tuple
from .base import ContactMatrix


# VLA Standard 6x7 Matrix Layout
# Numbers arranged in columns: 1-6, 7-12, 13-18, etc.
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


class WeightedAdjacencyMatrix(ContactMatrix):
    """
    VLA grid matrix with bias correction factors applied.

    The standard VLA 6x7 grid creates positional bias:
    - Corner numbers: 3-4 neighbors (underweighted)
    - Edge numbers: 5 neighbors
    - Interior numbers: 8 neighbors (overweighted)

    This implementation applies correction factors to normalize scores.
    """

    # Correction factors computed dynamically based on actual neighbor count
    # Factor = 8 / actual_neighbor_count (normalizes all to 8 effective)
    CORRECTION_FACTORS = None  # Will be computed in __init__

    def __init__(self, apply_correction: bool = True):
        """
        Initialize the weighted adjacency matrix.

        Args:
            apply_correction: If True, apply bias correction factors.
                              If False, behave like standard VLA.
        """
        self.apply_correction = apply_correction
        self._position_map = {}  # number -> (row, col)
        self._neighbor_cache = {}
        self._correction_factors = {}
        self._build_position_map()
        self._build_neighbor_cache()
        self._compute_correction_factors()

    @property
    def name(self) -> str:
        if self.apply_correction:
            return "WeightedAdjacency(corrected)"
        return "WeightedAdjacency(raw)"

    def _build_position_map(self) -> None:
        """Build mapping from number to grid position."""
        for row in range(ROWS):
            for col in range(COLS):
                num = VLA_MATRIX[row][col]
                if num is not None:
                    self._position_map[num] = (row, col)

    def _build_neighbor_cache(self) -> None:
        """Pre-compute neighbors for all numbers using 8-directional adjacency."""
        for num in range(1, self.POOL_SIZE + 1):
            row, col = self._position_map[num]
            neighbors = []

            # 8 directions: horizontal, vertical, diagonal
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

    def _compute_correction_factors(self) -> None:
        """Compute correction factors based on actual neighbor counts."""
        # Target: normalize all numbers to 8 effective neighbors
        target_neighbors = 8.0
        for num in range(1, self.POOL_SIZE + 1):
            actual = len(self._neighbor_cache[num])
            if actual > 0:
                self._correction_factors[num] = target_neighbors / actual
            else:
                self._correction_factors[num] = 1.0

    def get_neighbors(self, number: int) -> List[int]:
        """Return 8-directionally adjacent numbers in VLA grid."""
        self._validate_number(number)
        return self._neighbor_cache[number].copy()

    def get_neighbor_count(self, number: int) -> int:
        """Return actual neighbor count (before correction)."""
        self._validate_number(number)
        return len(self._neighbor_cache[number])

    def get_bias_factor(self, number: int) -> float:
        """Return bias correction factor for this number."""
        self._validate_number(number)
        if self.apply_correction:
            return self._correction_factors.get(number, 1.0)
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

    def get_numbers_by_type(self) -> Dict[str, List[int]]:
        """Return numbers grouped by position type."""
        types = {"corner": [], "edge": [], "reduced_edge": [], "interior": []}
        for n in range(1, self.POOL_SIZE + 1):
            pos_type = self.get_position_type(n)
            types[pos_type].append(n)
        return types


def create_default() -> WeightedAdjacencyMatrix:
    """Create a WeightedAdjacencyMatrix with correction enabled."""
    return WeightedAdjacencyMatrix(apply_correction=True)


def create_uncorrected() -> WeightedAdjacencyMatrix:
    """Create a WeightedAdjacencyMatrix without correction (VLA-equivalent)."""
    return WeightedAdjacencyMatrix(apply_correction=False)
