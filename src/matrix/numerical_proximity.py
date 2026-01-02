"""
Numerical Proximity Matrix (Approach C)

Non-geometric contact definition based on numerical distance.
A number N is "in contact" with drawn number D if |N - D| <= k.

With wraparound enabled, extreme numbers (1-3 and 37-39) also
contact numbers at the opposite end of the pool.

Key benefit: All numbers have exactly 2*k neighbors (uniform bias).
"""

from typing import List
from .base import ContactMatrix


class NumericalProximityMatrix(ContactMatrix):
    """
    Contact matrix using numerical proximity instead of grid geometry.

    Args:
        window_size: Number of positions in each direction (default 3)
        use_wraparound: If True, pool wraps (1 contacts 39, etc.)
    """

    def __init__(self, window_size: int = 3, use_wraparound: bool = True):
        self.window_size = window_size
        self.use_wraparound = use_wraparound
        self._neighbor_cache = {}
        self._build_neighbor_cache()

    @property
    def name(self) -> str:
        wrap_str = "wrap" if self.use_wraparound else "nowrap"
        return f"NumericalProximity(k={self.window_size}, {wrap_str})"

    def _build_neighbor_cache(self) -> None:
        """Pre-compute neighbors for all numbers."""
        for n in range(1, self.POOL_SIZE + 1):
            neighbors = []

            for offset in range(-self.window_size, self.window_size + 1):
                if offset == 0:
                    continue  # Skip self

                neighbor = n + offset

                if 1 <= neighbor <= self.POOL_SIZE:
                    neighbors.append(neighbor)
                elif self.use_wraparound:
                    # Wrap around the pool
                    if neighbor < 1:
                        wrapped = self.POOL_SIZE + neighbor
                        if wrapped >= 1:
                            neighbors.append(wrapped)
                    elif neighbor > self.POOL_SIZE:
                        wrapped = neighbor - self.POOL_SIZE
                        if wrapped <= self.POOL_SIZE:
                            neighbors.append(wrapped)

            self._neighbor_cache[n] = sorted(set(neighbors))

    def get_neighbors(self, number: int) -> List[int]:
        """Return numbers within window_size distance."""
        self._validate_number(number)
        return self._neighbor_cache[number].copy()

    def get_neighbor_count(self, number: int) -> int:
        """Return count of neighbors (always 2*k with wraparound)."""
        self._validate_number(number)
        return len(self._neighbor_cache[number])

    def get_bias_factor(self, number: int) -> float:
        """
        Return bias correction factor.

        With wraparound enabled, all numbers have equal neighbors,
        so no correction is needed (factor = 1.0).

        Without wraparound, edge numbers have fewer neighbors and
        need boosting to normalize.
        """
        self._validate_number(number)

        if self.use_wraparound:
            # All numbers have equal neighbors - no bias
            return 1.0
        else:
            # Calculate correction factor based on neighbor count
            max_neighbors = 2 * self.window_size
            actual_neighbors = len(self._neighbor_cache[number])
            if actual_neighbors == 0:
                return 1.0
            return max_neighbors / actual_neighbors


def create_default() -> NumericalProximityMatrix:
    """Create a NumericalProximityMatrix with recommended settings."""
    return NumericalProximityMatrix(window_size=3, use_wraparound=True)
