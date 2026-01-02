"""
Position filters based on EDA-derived optimal ranges.

Filters candidate numbers for each sorted position (N_1 through N_5)
using ranges that capture 85% or 90% of historical draws.
"""

from typing import List, Dict, Set, Tuple
from dataclasses import dataclass


@dataclass
class PositionRange:
    """Defines the valid range for a sorted position."""
    position: str  # N_1, N_2, N_3, N_4, N_5
    min_val: int
    max_val: int
    capture_rate: float  # Expected % of draws captured
    pool_reduction: float  # % reduction in candidate pool


# Optimal ranges from EDA analysis (85% capture - recommended)
OPTIMAL_RANGES_85 = {
    'N_1': PositionRange('N_1', 1, 13, 0.87, 0.667),
    'N_2': PositionRange('N_2', 3, 21, 0.86, 0.513),
    'N_3': PositionRange('N_3', 9, 29, 0.85, 0.462),
    'N_4': PositionRange('N_4', 18, 36, 0.86, 0.513),
    'N_5': PositionRange('N_5', 28, 39, 0.86, 0.692),
}

# Conservative ranges (90% capture)
OPTIMAL_RANGES_90 = {
    'N_1': PositionRange('N_1', 1, 15, 0.93, 0.615),
    'N_2': PositionRange('N_2', 2, 22, 0.90, 0.462),
    'N_3': PositionRange('N_3', 7, 30, 0.91, 0.385),
    'N_4': PositionRange('N_4', 17, 37, 0.91, 0.462),
    'N_5': PositionRange('N_5', 26, 39, 0.91, 0.641),
}

# Aggressive ranges (80% capture)
OPTIMAL_RANGES_80 = {
    'N_1': PositionRange('N_1', 1, 11, 0.82, 0.718),
    'N_2': PositionRange('N_2', 3, 19, 0.80, 0.564),
    'N_3': PositionRange('N_3', 11, 29, 0.81, 0.513),
    'N_4': PositionRange('N_4', 18, 35, 0.82, 0.538),
    'N_5': PositionRange('N_5', 30, 39, 0.81, 0.744),
}


class PositionFilter:
    """
    Filters numbers based on optimal positional ranges.

    Given candidate numbers, returns only those that fall within
    the optimal range for each sorted position.
    """

    def __init__(self, capture_level: str = '85'):
        """
        Initialize with a capture level.

        Args:
            capture_level: '80', '85', or '90' for % capture target
        """
        if capture_level == '80':
            self.ranges = OPTIMAL_RANGES_80
        elif capture_level == '90':
            self.ranges = OPTIMAL_RANGES_90
        else:
            self.ranges = OPTIMAL_RANGES_85  # Default
        self.capture_level = capture_level

    def get_range(self, position: str) -> PositionRange:
        """Get the range for a specific position."""
        return self.ranges.get(position)

    def filter_for_position(self, numbers: List[int], position: str) -> List[int]:
        """
        Filter numbers valid for a specific position.

        Args:
            numbers: Candidate numbers
            position: Position name (N_1, N_2, N_3, N_4, N_5)

        Returns:
            Numbers that fall within the optimal range for that position
        """
        range_def = self.ranges.get(position)
        if not range_def:
            return numbers

        return [n for n in numbers if range_def.min_val <= n <= range_def.max_val]

    def get_candidates_by_position(self, pool: Set[int] = None) -> Dict[str, List[int]]:
        """
        Get all valid candidates for each position.

        Args:
            pool: Optional set of numbers to filter from.
                  Defaults to full pool (1-39).

        Returns:
            Dict mapping position to list of valid numbers
        """
        if pool is None:
            pool = set(range(1, 40))

        candidates = {}
        for pos, range_def in self.ranges.items():
            candidates[pos] = sorted([
                n for n in pool
                if range_def.min_val <= n <= range_def.max_val
            ])
        return candidates

    def validate_ticket(self, numbers: List[int]) -> Tuple[bool, Dict[str, bool]]:
        """
        Check if a 5-number ticket satisfies all position constraints.

        Args:
            numbers: List of 5 numbers (will be sorted)

        Returns:
            (is_valid, position_checks) where position_checks shows
            which positions passed/failed
        """
        if len(numbers) != 5:
            return False, {}

        sorted_nums = sorted(numbers)
        positions = ['N_1', 'N_2', 'N_3', 'N_4', 'N_5']
        checks = {}

        for i, pos in enumerate(positions):
            range_def = self.ranges[pos]
            num = sorted_nums[i]
            checks[pos] = range_def.min_val <= num <= range_def.max_val

        return all(checks.values()), checks

    def score_ticket(self, numbers: List[int]) -> float:
        """
        Score a ticket based on how well it fits position constraints.

        Args:
            numbers: List of 5 numbers

        Returns:
            Score from 0.0 to 1.0 (1.0 = all positions in range)
        """
        _, checks = self.validate_ticket(numbers)
        if not checks:
            return 0.0
        return sum(1 for v in checks.values() if v) / len(checks)

    def get_overlap_numbers(self) -> Set[int]:
        """
        Get numbers that are valid for multiple positions.

        These are flexible numbers that can fill different roles.
        """
        position_sets = {}
        for pos, range_def in self.ranges.items():
            position_sets[pos] = set(range(range_def.min_val, range_def.max_val + 1))

        # Find numbers in multiple ranges
        all_numbers = set(range(1, 40))
        overlap = set()

        for n in all_numbers:
            count = sum(1 for s in position_sets.values() if n in s)
            if count >= 2:
                overlap.add(n)

        return overlap

    def __str__(self) -> str:
        lines = [f"PositionFilter (capture={self.capture_level}%):"]
        for pos, r in self.ranges.items():
            lines.append(f"  {pos}: {r.min_val}-{r.max_val} "
                        f"(capture={r.capture_rate:.0%}, reduction={r.pool_reduction:.0%})")
        return "\n".join(lines)


def create_default() -> PositionFilter:
    """Create PositionFilter with recommended 85% capture."""
    return PositionFilter(capture_level='85')
