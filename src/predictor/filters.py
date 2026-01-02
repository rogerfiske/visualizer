"""
Lottery Ticket Filters

Comprehensive filter implementation based on 52 standard lottery filters.
Reference: imported_docs/FILTERING.txt

Filters are organized into categories:
- Basic Composition (odd/even, high/low, prime/composite)
- Sum & Average
- Consecutive/Successive patterns
- Distance metrics
- Unit digit analysis
- Decade analysis
- AC Value (Arithmetic Complexity)
- Historical comparison
"""

from typing import List, Dict, Tuple, Set, Optional, Callable
from dataclasses import dataclass
from math import sqrt


# Constants for CA Fantasy 5
POOL_SIZE = 39
PICK_SIZE = 5
LOW_HIGH_SPLIT = 19  # 1-19 low, 20-39 high
PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}
COMPOSITES = {4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39}


# =============================================================================
# BASIC COMPOSITION FILTERS (1-5, 52)
# =============================================================================

def odd_count(ticket: List[int]) -> int:
    """Filter 1: Count of odd numbers in combination."""
    return sum(1 for n in ticket if n % 2 == 1)


def even_count(ticket: List[int]) -> int:
    """Filter 2: Count of even numbers in combination."""
    return sum(1 for n in ticket if n % 2 == 0)


def high_count(ticket: List[int], split: int = LOW_HIGH_SPLIT) -> int:
    """Filter 3: Count of high numbers (> split)."""
    return sum(1 for n in ticket if n > split)


def low_count(ticket: List[int], split: int = LOW_HIGH_SPLIT) -> int:
    """Filter 4: Count of low numbers (<= split)."""
    return sum(1 for n in ticket if n <= split)


def prime_count(ticket: List[int]) -> int:
    """Filter 5: Count of prime numbers."""
    return sum(1 for n in ticket if n in PRIMES)


def composite_count(ticket: List[int]) -> int:
    """Filter 52: Count of composite numbers."""
    return sum(1 for n in ticket if n in COMPOSITES)


# =============================================================================
# SUM & AVERAGE FILTERS (6-8, 22, 49-50)
# =============================================================================

def number_sum(ticket: List[int]) -> int:
    """Filter 6: Sum of all numbers."""
    return sum(ticket)


def average_value(ticket: List[int]) -> float:
    """Filter 7: Average of all numbers."""
    return sum(ticket) / len(ticket)


def unit_number_sum(ticket: List[int]) -> int:
    """Filter 8: Sum of unit digits (last digit of each number)."""
    return sum(n % 10 for n in ticket)


def sum_value_even_odd(ticket: List[int]) -> int:
    """Filter 22: 0 if sum is even, 1 if sum is odd."""
    return sum(ticket) % 2


def root_sum(ticket: List[int]) -> int:
    """Filter 49: Digital root of the sum (repeatedly sum digits until single digit)."""
    s = sum(ticket)
    while s >= 10:
        s = sum(int(d) for d in str(s))
    return s


def first_and_second_unit_sum(ticket: List[int]) -> int:
    """Filter 50: Sum of all tens digits + sum of all unit digits."""
    tens_sum = sum(n // 10 for n in ticket)
    units_sum = sum(n % 10 for n in ticket)
    return tens_sum + units_sum


# =============================================================================
# CONSECUTIVE/SUCCESSIVE FILTERS (10-13, 37)
# =============================================================================

def successive(ticket: List[int]) -> int:
    """Filter 10: Maximum consecutive sequence length."""
    if not ticket:
        return 0
    sorted_t = sorted(ticket)
    max_consec = 1
    current = 1
    for i in range(1, len(sorted_t)):
        if sorted_t[i] == sorted_t[i-1] + 1:
            current += 1
            max_consec = max(max_consec, current)
        else:
            current = 1
    return max_consec


def successive_groups(ticket: List[int]) -> int:
    """Filter 11: Number of consecutive groups."""
    if not ticket:
        return 0
    sorted_t = sorted(ticket)
    groups = 0
    in_group = False
    for i in range(1, len(sorted_t)):
        if sorted_t[i] == sorted_t[i-1] + 1:
            if not in_group:
                groups += 1
                in_group = True
        else:
            in_group = False
    return groups


def odd_successive(ticket: List[int]) -> int:
    """Filter 12: Maximum consecutive odd numbers in sequence."""
    odds = sorted([n for n in ticket if n % 2 == 1])
    if not odds:
        return 0
    max_consec = 1
    current = 1
    for i in range(1, len(odds)):
        if odds[i] == odds[i-1] + 2:  # Odd numbers differ by 2
            current += 1
            max_consec = max(max_consec, current)
        else:
            current = 1
    return max_consec


def even_successive(ticket: List[int]) -> int:
    """Filter 13: Maximum consecutive even numbers in sequence."""
    evens = sorted([n for n in ticket if n % 2 == 0])
    if not evens:
        return 0
    max_consec = 1
    current = 1
    for i in range(1, len(evens)):
        if evens[i] == evens[i-1] + 2:  # Even numbers differ by 2
            current += 1
            max_consec = max(max_consec, current)
        else:
            current = 1
    return max_consec


def successive_end_units(ticket: List[int]) -> int:
    """Filter 37: Maximum consecutive unit digits."""
    units = sorted([n % 10 for n in ticket])
    if not units:
        return 0
    max_consec = 1
    current = 1
    for i in range(1, len(units)):
        if units[i] == units[i-1] + 1:
            current += 1
            max_consec = max(max_consec, current)
        else:
            current = 1
    return max_consec


# =============================================================================
# MIN/MAX & DISTANCE FILTERS (14-19, 51)
# =============================================================================

def minimum_number(ticket: List[int]) -> int:
    """Filter 14: Smallest number in combination."""
    return min(ticket)


def maximum_number(ticket: List[int]) -> int:
    """Filter 15: Largest number in combination."""
    return max(ticket)


def first_last_distance(ticket: List[int]) -> int:
    """Filter 16: Span between min and max."""
    return max(ticket) - min(ticket)


def get_distances(ticket: List[int]) -> List[int]:
    """Helper: Get all adjacent distances."""
    sorted_t = sorted(ticket)
    return [sorted_t[i] - sorted_t[i-1] for i in range(1, len(sorted_t))]


def max_distance(ticket: List[int]) -> int:
    """Filter 17: Maximum gap between adjacent numbers."""
    distances = get_distances(ticket)
    return max(distances) if distances else 0


def min_distance(ticket: List[int]) -> int:
    """Filter 51: Minimum gap between adjacent numbers."""
    distances = get_distances(ticket)
    return min(distances) if distances else 0


def average_distance(ticket: List[int]) -> float:
    """Filter 18: Average gap between adjacent numbers."""
    distances = get_distances(ticket)
    return sum(distances) / len(distances) if distances else 0


def different_distance(ticket: List[int]) -> int:
    """Filter 19: Count of unique distances."""
    distances = get_distances(ticket)
    return len(set(distances))


# =============================================================================
# AC VALUE (ARITHMETIC COMPLEXITY) - Filter 20
# =============================================================================

def ac_value(ticket: List[int]) -> int:
    """
    Filter 20: Arithmetic Complexity value.

    AC = number of unique differences between all pairs - (n-1)
    where n is the count of numbers.

    Higher AC means more varied spacing, lower means arithmetic progression.
    For 5 numbers: AC ranges from 0 (arithmetic sequence) to 6 (max variation)
    """
    sorted_t = sorted(ticket)
    n = len(sorted_t)

    # Calculate all pairwise differences
    differences = set()
    for i in range(n):
        for j in range(i + 1, n):
            differences.add(sorted_t[j] - sorted_t[i])

    # AC = unique differences - (n-1)
    return len(differences) - (n - 1)


# =============================================================================
# UNIT DIGIT ANALYSIS FILTERS (9, 23, 27-36, 38-48)
# =============================================================================

def unit_number_different(ticket: List[int]) -> int:
    """Filter 9: Count of unique unit digits."""
    return len(set(n % 10 for n in ticket))


def unit_number_group_count(ticket: List[int]) -> int:
    """Filter 23: Count of consecutive unit digit groups."""
    units = sorted(set(n % 10 for n in ticket))
    if not units:
        return 0
    groups = 1
    for i in range(1, len(units)):
        if units[i] != units[i-1] + 1:
            groups += 1
    return groups


def high_units_count(ticket: List[int]) -> int:
    """Filter 27: Count of high unit digits (6,7,8,9)."""
    return sum(1 for n in ticket if n % 10 >= 6)


def odd_units_count(ticket: List[int]) -> int:
    """Filter 28: Count of odd unit digits (1,3,5,7,9)."""
    return sum(1 for n in ticket if n % 10 in {1, 3, 5, 7, 9})


def even_units_count(ticket: List[int]) -> int:
    """Filter 34: Count of even unit digits (0,2,4,6,8)."""
    return sum(1 for n in ticket if n % 10 in {0, 2, 4, 6, 8})


def lowest_4_units_count(ticket: List[int]) -> int:
    """Filter 29: Count of unit digits 1,2,3,4 (not 0)."""
    return sum(1 for n in ticket if n % 10 in {1, 2, 3, 4})


def count_123_units(ticket: List[int]) -> int:
    """Filter 33: Count of unit digits 1, 2, or 3."""
    return sum(1 for n in ticket if n % 10 in {1, 2, 3})


def successive_paired_units_count(ticket: List[int]) -> int:
    """Filter 30: Count of numbers with successive paired unit digits (01,12,23,34,45,56,67,78,89)."""
    successive_pairs = {(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9)}
    count = 0
    for n in ticket:
        tens = n // 10
        units = n % 10
        if (tens, units) in successive_pairs or (units, tens) in successive_pairs:
            count += 1
    return count


def pairs_odd_even_units(ticket: List[int]) -> int:
    """Filter 31: Count of numbers with one odd and one even digit."""
    count = 0
    for n in ticket:
        tens = n // 10
        units = n % 10
        if (tens % 2) != (units % 2):  # One odd, one even
            count += 1
    return count


def interchangeable_units_count(ticket: List[int], pool_max: int = POOL_SIZE) -> int:
    """Filter 32: Count of numbers whose reversed digits are also valid."""
    count = 0
    for n in ticket:
        tens = n // 10
        units = n % 10
        if tens != units:  # Not palindromic (11, 22, 33...)
            reversed_n = units * 10 + tens
            if 1 <= reversed_n <= pool_max:
                count += 1
    return count


def pairs_even_units_only(ticket: List[int]) -> int:
    """Filter 35: Count of numbers where both digits are even."""
    count = 0
    for n in ticket:
        tens = n // 10
        units = n % 10
        if tens % 2 == 0 and units % 2 == 0:
            count += 1
    return count


def pairs_odd_units_only(ticket: List[int]) -> int:
    """Filter 38: Count of numbers where both digits are odd."""
    count = 0
    for n in ticket:
        tens = n // 10
        units = n % 10
        if tens % 2 == 1 and units % 2 == 1:
            count += 1
    return count


def pairs_123_units(ticket: List[int]) -> int:
    """Filter 36: Count of numbers where both digits are 1, 2, or 3."""
    valid_digits = {1, 2, 3}
    count = 0
    for n in ticket:
        tens = n // 10
        units = n % 10
        if tens in valid_digits and units in valid_digits:
            count += 1
    return count


def units_digit_count(ticket: List[int], digit: int) -> int:
    """Filters 39-48: Count of specific digit (0-9) appearances in all positions."""
    count = 0
    for n in ticket:
        if n // 10 == digit:
            count += 1
        if n % 10 == digit:
            count += 1
    return count


# =============================================================================
# DECADE ANALYSIS FILTERS (24-25)
# =============================================================================

def get_decades(ticket: List[int]) -> List[int]:
    """Helper: Get decade for each number (0=1-9, 1=10-19, 2=20-29, 3=30-39)."""
    return [n // 10 for n in ticket]


def decade_group_count(ticket: List[int]) -> int:
    """Filter 24: Count of consecutive decade groups."""
    decades = sorted(set(get_decades(ticket)))
    if not decades:
        return 0
    groups = 1
    for i in range(1, len(decades)):
        if decades[i] != decades[i-1] + 1:
            groups += 1
    return groups


def different_decade_count(ticket: List[int]) -> int:
    """Filter 25: Count of unique decades represented."""
    return len(set(get_decades(ticket)))


# =============================================================================
# HISTORICAL COMPARISON FILTERS (21, 26)
# =============================================================================

def same_last_drawn(ticket: List[int], last_draw: List[int]) -> int:
    """Filter 21: Count of numbers that match the previous draw."""
    return len(set(ticket) & set(last_draw))


def same_end_units_with_last(ticket: List[int], last_draw: List[int]) -> int:
    """Filter 26: Count of numbers sharing unit digit with previous draw."""
    last_units = set(n % 10 for n in last_draw)
    return sum(1 for n in ticket if n % 10 in last_units)


# =============================================================================
# FILTER CONFIGURATION & PIPELINE
# =============================================================================

@dataclass
class FilterConfig:
    """Configuration for filter thresholds based on CA Fantasy 5 historical analysis."""

    # Odd/Even (most common: 2:3 or 3:2 = 66%)
    odd_min: int = 2
    odd_max: int = 3

    # High/Low (most common: L2:H3 or L3:H2 = 66%)
    low_min: int = 2
    low_max: int = 3

    # Sum (captures 93.6% of historical draws)
    sum_min: int = 50
    sum_max: int = 140

    # Decades (3+ covers 85.4%)
    decades_min: int = 3

    # Consecutive (max 2 covers 96.1%)
    consecutive_max: int = 2

    # Prime count (1-3 covers 83.4%)
    prime_min: int = 1
    prime_max: int = 3

    # AC value (4-6 covers 94% of draws; max possible for 5 numbers is 6)
    ac_min: int = 4
    ac_max: int = 6

    # Distance constraints
    min_distance_min: int = 1  # No duplicates
    span_min: int = 20  # Min first-last distance
    span_max: int = 38  # Max first-last distance

    # Same as last draw (0-2 typical)
    same_last_max: int = 2


class TicketFilter:
    """
    Multi-stage ticket filter pipeline.

    Usage:
        config = FilterConfig()
        filter = TicketFilter(config)
        filtered_tickets = filter.apply(tickets, last_draw=[1,5,15,25,35])
    """

    def __init__(self, config: FilterConfig = None):
        self.config = config or FilterConfig()
        self.stats = {}  # Track filter rejection stats

    def reset_stats(self):
        """Reset filter statistics."""
        self.stats = {
            'input': 0,
            'odd_even': 0,
            'high_low': 0,
            'sum_range': 0,
            'decades': 0,
            'consecutive': 0,
            'prime': 0,
            'ac_value': 0,
            'distance': 0,
            'same_last': 0,
            'output': 0
        }

    def passes_odd_even(self, ticket: List[int]) -> bool:
        """Check odd/even ratio filter."""
        odd = odd_count(ticket)
        return self.config.odd_min <= odd <= self.config.odd_max

    def passes_high_low(self, ticket: List[int]) -> bool:
        """Check high/low ratio filter."""
        low = low_count(ticket)
        return self.config.low_min <= low <= self.config.low_max

    def passes_sum_range(self, ticket: List[int]) -> bool:
        """Check sum range filter."""
        s = number_sum(ticket)
        return self.config.sum_min <= s <= self.config.sum_max

    def passes_decades(self, ticket: List[int]) -> bool:
        """Check decade spread filter."""
        return different_decade_count(ticket) >= self.config.decades_min

    def passes_consecutive(self, ticket: List[int]) -> bool:
        """Check consecutive numbers filter."""
        return successive(ticket) <= self.config.consecutive_max

    def passes_prime(self, ticket: List[int]) -> bool:
        """Check prime count filter."""
        p = prime_count(ticket)
        return self.config.prime_min <= p <= self.config.prime_max

    def passes_ac_value(self, ticket: List[int]) -> bool:
        """Check AC value filter."""
        ac = ac_value(ticket)
        return self.config.ac_min <= ac <= self.config.ac_max

    def passes_distance(self, ticket: List[int]) -> bool:
        """Check distance constraints."""
        if min_distance(ticket) < self.config.min_distance_min:
            return False
        span = first_last_distance(ticket)
        return self.config.span_min <= span <= self.config.span_max

    def passes_same_last(self, ticket: List[int], last_draw: List[int]) -> bool:
        """Check same-as-last-draw filter."""
        if not last_draw:
            return True
        return same_last_drawn(ticket, last_draw) <= self.config.same_last_max

    def filter_single(self, ticket: List[int], last_draw: List[int] = None) -> bool:
        """
        Apply all filters to a single ticket.

        Returns True if ticket passes all filters.
        """
        if not self.passes_odd_even(ticket):
            return False
        if not self.passes_high_low(ticket):
            return False
        if not self.passes_sum_range(ticket):
            return False
        if not self.passes_decades(ticket):
            return False
        if not self.passes_consecutive(ticket):
            return False
        if not self.passes_prime(ticket):
            return False
        if not self.passes_ac_value(ticket):
            return False
        if not self.passes_distance(ticket):
            return False
        if not self.passes_same_last(ticket, last_draw):
            return False
        return True

    def apply(self, tickets: List[List[int]], last_draw: List[int] = None,
              track_stats: bool = False) -> List[List[int]]:
        """
        Apply all filters to a list of tickets.

        Args:
            tickets: List of tickets to filter
            last_draw: Previous draw numbers (for same-last filter)
            track_stats: If True, track rejection statistics

        Returns:
            List of tickets that pass all filters
        """
        if track_stats:
            self.reset_stats()
            self.stats['input'] = len(tickets)

        filtered = []
        for ticket in tickets:
            if track_stats:
                # Track which filter rejected each ticket
                if not self.passes_odd_even(ticket):
                    self.stats['odd_even'] += 1
                    continue
                if not self.passes_high_low(ticket):
                    self.stats['high_low'] += 1
                    continue
                if not self.passes_sum_range(ticket):
                    self.stats['sum_range'] += 1
                    continue
                if not self.passes_decades(ticket):
                    self.stats['decades'] += 1
                    continue
                if not self.passes_consecutive(ticket):
                    self.stats['consecutive'] += 1
                    continue
                if not self.passes_prime(ticket):
                    self.stats['prime'] += 1
                    continue
                if not self.passes_ac_value(ticket):
                    self.stats['ac_value'] += 1
                    continue
                if not self.passes_distance(ticket):
                    self.stats['distance'] += 1
                    continue
                if not self.passes_same_last(ticket, last_draw):
                    self.stats['same_last'] += 1
                    continue
                filtered.append(ticket)
            else:
                if self.filter_single(ticket, last_draw):
                    filtered.append(ticket)

        if track_stats:
            self.stats['output'] = len(filtered)

        return filtered

    def get_stats_report(self) -> str:
        """Get formatted statistics report."""
        if not self.stats:
            return "No statistics available. Run apply() with track_stats=True."

        lines = ["Filter Statistics:", "-" * 40]
        lines.append(f"  Input tickets:     {self.stats['input']}")
        lines.append(f"  Rejected by:")
        lines.append(f"    Odd/Even:        {self.stats['odd_even']}")
        lines.append(f"    High/Low:        {self.stats['high_low']}")
        lines.append(f"    Sum Range:       {self.stats['sum_range']}")
        lines.append(f"    Decades:         {self.stats['decades']}")
        lines.append(f"    Consecutive:     {self.stats['consecutive']}")
        lines.append(f"    Prime Count:     {self.stats['prime']}")
        lines.append(f"    AC Value:        {self.stats['ac_value']}")
        lines.append(f"    Distance:        {self.stats['distance']}")
        lines.append(f"    Same Last:       {self.stats['same_last']}")
        lines.append(f"  Output tickets:    {self.stats['output']}")

        if self.stats['input'] > 0:
            pass_rate = self.stats['output'] / self.stats['input'] * 100
            lines.append(f"  Pass rate:         {pass_rate:.1f}%")

        return "\n".join(lines)


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_ticket(ticket: List[int], last_draw: List[int] = None) -> Dict:
    """
    Compute all filter values for a ticket.

    Returns dict with all 52 filter values.
    """
    result = {
        # Basic composition
        'odd_count': odd_count(ticket),
        'even_count': even_count(ticket),
        'high_count': high_count(ticket),
        'low_count': low_count(ticket),
        'prime_count': prime_count(ticket),
        'composite_count': composite_count(ticket),

        # Sum & average
        'number_sum': number_sum(ticket),
        'average_value': average_value(ticket),
        'unit_number_sum': unit_number_sum(ticket),
        'sum_value_even_odd': sum_value_even_odd(ticket),
        'root_sum': root_sum(ticket),
        'first_second_unit_sum': first_and_second_unit_sum(ticket),

        # Consecutive
        'successive': successive(ticket),
        'successive_groups': successive_groups(ticket),
        'odd_successive': odd_successive(ticket),
        'even_successive': even_successive(ticket),
        'successive_end_units': successive_end_units(ticket),

        # Min/max & distance
        'minimum_number': minimum_number(ticket),
        'maximum_number': maximum_number(ticket),
        'first_last_distance': first_last_distance(ticket),
        'max_distance': max_distance(ticket),
        'min_distance': min_distance(ticket),
        'average_distance': average_distance(ticket),
        'different_distance': different_distance(ticket),

        # AC value
        'ac_value': ac_value(ticket),

        # Unit analysis
        'unit_number_different': unit_number_different(ticket),
        'unit_number_group_count': unit_number_group_count(ticket),
        'high_units_count': high_units_count(ticket),
        'odd_units_count': odd_units_count(ticket),
        'even_units_count': even_units_count(ticket),
        'lowest_4_units_count': lowest_4_units_count(ticket),
        'count_123_units': count_123_units(ticket),
        'successive_paired_units': successive_paired_units_count(ticket),
        'pairs_odd_even_units': pairs_odd_even_units(ticket),
        'interchangeable_units': interchangeable_units_count(ticket),
        'pairs_even_only': pairs_even_units_only(ticket),
        'pairs_odd_only': pairs_odd_units_only(ticket),
        'pairs_123_units': pairs_123_units(ticket),

        # Decade analysis
        'decade_group_count': decade_group_count(ticket),
        'different_decade_count': different_decade_count(ticket),
    }

    # Unit digit counts (0-9)
    for digit in range(10):
        result[f'units_{digit}_count'] = units_digit_count(ticket, digit)

    # Historical comparison (if last_draw provided)
    if last_draw:
        result['same_last_drawn'] = same_last_drawn(ticket, last_draw)
        result['same_end_units_last'] = same_end_units_with_last(ticket, last_draw)

    return result


def validate_against_history(draws: List[List[int]], config: FilterConfig = None) -> Dict:
    """
    Validate filter configuration against historical draws.

    Returns dict with capture rates for each filter.
    """
    config = config or FilterConfig()
    filter_obj = TicketFilter(config)

    total = len(draws)
    passes = {
        'odd_even': 0,
        'high_low': 0,
        'sum_range': 0,
        'decades': 0,
        'consecutive': 0,
        'prime': 0,
        'ac_value': 0,
        'distance': 0,
        'all_filters': 0
    }

    for draw in draws:
        if filter_obj.passes_odd_even(draw):
            passes['odd_even'] += 1
        if filter_obj.passes_high_low(draw):
            passes['high_low'] += 1
        if filter_obj.passes_sum_range(draw):
            passes['sum_range'] += 1
        if filter_obj.passes_decades(draw):
            passes['decades'] += 1
        if filter_obj.passes_consecutive(draw):
            passes['consecutive'] += 1
        if filter_obj.passes_prime(draw):
            passes['prime'] += 1
        if filter_obj.passes_ac_value(draw):
            passes['ac_value'] += 1
        if filter_obj.passes_distance(draw):
            passes['distance'] += 1
        if filter_obj.filter_single(draw):
            passes['all_filters'] += 1

    return {k: {'count': v, 'rate': v / total * 100} for k, v in passes.items()}
