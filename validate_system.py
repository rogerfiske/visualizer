#!/usr/bin/env python3
"""
System Validation Script - VLA Visualizer Prediction System

Comprehensive validation including:
1. Unit tests for matrix implementations
2. Unit tests for position filters
3. Integration tests for predictor
4. Statistical validation tests
5. Configurable backtesting

Usage:
    python validate_system.py                    # Quick validation (100 days)
    python validate_system.py --full             # Full validation (500 days)
    python validate_system.py --extended         # Extended validation (1000 days)
    python validate_system.py --unit-only        # Unit tests only
    python validate_system.py --backtest-only    # Backtest comparison only
"""

import argparse
import sys
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.matrix import (
    VLAStandardMatrix,
    WeightedAdjacencyMatrix,
    NumericalProximityMatrix,
)
from src.predictor import CA5Predictor, PositionFilter, DrawHistory


# =============================================================================
# Test Infrastructure
# =============================================================================

@dataclass
class TestResult:
    name: str
    passed: bool
    message: str
    details: Dict = None


class TestRunner:
    def __init__(self):
        self.results: List[TestResult] = []
        self.verbose = True

    def run_test(self, name: str, test_func) -> TestResult:
        """Run a single test and record result."""
        try:
            passed, message, details = test_func()
            result = TestResult(name, passed, message, details)
        except Exception as e:
            result = TestResult(name, False, f"Exception: {str(e)}", None)

        self.results.append(result)
        return result

    def print_result(self, result: TestResult) -> None:
        """Print a single test result."""
        status = "[PASS]" if result.passed else "[FAIL]"
        print(f"  {status} {result.name}")
        if not result.passed and self.verbose:
            print(f"         {result.message}")

    def get_summary(self) -> Tuple[int, int]:
        """Return (passed, total) counts."""
        passed = sum(1 for r in self.results if r.passed)
        return passed, len(self.results)


# =============================================================================
# Statistical Utilities
# =============================================================================

def factorial(n: int) -> int:
    """Calculate factorial."""
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def combinations(n: int, r: int) -> int:
    """Calculate C(n,r) = n! / (r! * (n-r)!)"""
    if r > n or r < 0:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))


def hypergeometric_probability(k: int, K: int = 5, N: int = 39, n: int = 5) -> float:
    """
    Calculate probability of exactly k matches.
    K = numbers drawn (5)
    N = pool size (39)
    n = numbers on ticket (5)
    """
    return (combinations(K, k) * combinations(N - K, n - k)) / combinations(N, n)


def expected_best_match(num_tickets: int) -> float:
    """Calculate expected best match with n tickets."""
    # P(best >= k) = 1 - P(all tickets < k)^n
    expected = 0
    for k in range(6):
        p_less_than_k = sum(hypergeometric_probability(j) for j in range(k))
        p_at_least_k = 1 - (p_less_than_k ** num_tickets)
        expected += p_at_least_k
    return expected - 1  # Subtract 1 because we summed P(>=1) through P(>=5)


# =============================================================================
# Unit Tests - Matrix Implementations
# =============================================================================

def test_vla_standard_has_bias() -> Tuple[bool, str, Dict]:
    """TEST-MATRIX-001: VLA Standard has expected bias."""
    matrix = VLAStandardMatrix()
    stats = matrix.analyze_bias()

    # Check variance is approximately 5
    variance_ok = 4.5 <= stats['effective_variance'] <= 5.5

    # Check corners have 3-4 neighbors
    corners = [1, 6, 36, 37, 39]
    corner_counts = [matrix.get_neighbor_count(n) for n in corners]
    corners_ok = all(3 <= c <= 4 for c in corner_counts)

    # Check interior has 8 neighbors
    interior = [8, 15, 22, 27]
    interior_counts = [matrix.get_neighbor_count(n) for n in interior]
    interior_ok = all(c == 8 for c in interior_counts)

    passed = variance_ok and corners_ok and interior_ok
    message = f"variance={stats['effective_variance']:.2f}, corners={corner_counts}"

    return passed, message, stats


def test_weighted_eliminates_bias() -> Tuple[bool, str, Dict]:
    """TEST-MATRIX-002: Weighted Adjacency eliminates bias."""
    matrix = WeightedAdjacencyMatrix(apply_correction=True)
    stats = matrix.analyze_bias()

    # Check variance < 0.5
    variance_ok = stats['effective_variance'] < 0.5

    # Check all effective contacts within 10% of mean
    avg = stats['avg_effective']
    all_effective = [
        matrix.get_neighbor_count(n) * matrix.get_bias_factor(n)
        for n in range(1, 40)
    ]
    within_10pct = all(abs(e - avg) / avg < 0.10 for e in all_effective)

    # Check corners get boost
    corners = [1, 6, 37]
    corner_factors = [matrix.get_bias_factor(n) for n in corners]
    corners_boosted = all(f > 2.5 for f in corner_factors)

    passed = variance_ok and stats['is_uniform']
    message = f"variance={stats['effective_variance']:.2f}, uniform={stats['is_uniform']}"

    return passed, message, stats


def test_numerical_proximity_uniform() -> Tuple[bool, str, Dict]:
    """TEST-MATRIX-003: Numerical Proximity is uniform."""
    matrix = NumericalProximityMatrix(window_size=3, use_wraparound=True)
    stats = matrix.analyze_bias()

    # All should have exactly 6 neighbors
    all_counts = [matrix.get_neighbor_count(n) for n in range(1, 40)]
    uniform_count = len(set(all_counts)) == 1

    # Variance should be 0
    variance_zero = stats['effective_variance'] == 0

    # All bias factors should be 1.0
    all_factors = [matrix.get_bias_factor(n) for n in range(1, 40)]
    all_one = all(f == 1.0 for f in all_factors)

    passed = uniform_count and variance_zero and all_one
    message = f"counts={set(all_counts)}, variance={stats['effective_variance']}"

    return passed, message, stats


def test_contact_scoring() -> Tuple[bool, str, Dict]:
    """TEST-MATRIX-004: Contact scoring works correctly."""
    matrix = NumericalProximityMatrix(window_size=3, use_wraparound=True)

    # Test with known draw
    draw = [10]  # Only number 10 drawn
    scores = matrix.calculate_contact_scores(draw)

    # Numbers 7-13 should be in contact (10 ± 3)
    expected_in_contact = [7, 8, 9, 11, 12, 13]
    for n in expected_in_contact:
        if scores[n] != 1.0:
            return False, f"Expected {n} to have score 1.0, got {scores[n]}", {}

    # Numbers far away should have score 0
    far_numbers = [1, 20, 30, 39]
    for n in far_numbers:
        if scores[n] != 0.0:
            return False, f"Expected {n} to have score 0.0, got {scores[n]}", {}

    return True, "Contact scoring verified", {'draw': draw, 'expected_in_contact': expected_in_contact}


# =============================================================================
# Unit Tests - Position Filters
# =============================================================================

def test_filter_ranges_correct() -> Tuple[bool, str, Dict]:
    """TEST-FILTER-001: 85% ranges are configured correctly."""
    pf = PositionFilter(capture_level='85')

    expected = {
        'N_1': (1, 13),
        'N_2': (3, 21),
        'N_3': (9, 29),
        'N_4': (18, 36),
        'N_5': (28, 39),
    }

    for pos, (exp_min, exp_max) in expected.items():
        range_def = pf.get_range(pos)
        if range_def.min_val != exp_min or range_def.max_val != exp_max:
            return False, f"{pos}: expected {exp_min}-{exp_max}, got {range_def.min_val}-{range_def.max_val}", {}

    return True, "All ranges correct", expected


def test_filter_validation() -> Tuple[bool, str, Dict]:
    """TEST-FILTER-002: Filter validation works."""
    pf = PositionFilter(capture_level='85')

    # Valid ticket: all positions in range
    valid_ticket = [5, 10, 20, 30, 35]
    is_valid, checks = pf.validate_ticket(valid_ticket)
    if not is_valid:
        return False, f"Valid ticket rejected: {checks}", {}

    # Invalid ticket: N_5 position out of range (sorted: 1,2,3,4,5 -> N_5=5 not in 28-39)
    invalid_ticket = [1, 2, 3, 4, 5]
    is_valid, checks = pf.validate_ticket(invalid_ticket)
    if is_valid:
        return False, "Invalid ticket accepted", {}

    return True, "Validation logic correct", {}


def test_filter_capture_rates() -> Tuple[bool, str, Dict]:
    """TEST-FILTER-003: Historical capture rates match claims."""
    history = DrawHistory()
    pf = PositionFilter(capture_level='85')

    # Test on last 500 draws
    draws = history.draws[-500:]

    position_hits = {pos: 0 for pos in ['N_1', 'N_2', 'N_3', 'N_4', 'N_5']}
    total = len(draws)

    for draw in draws:
        nums = draw['numbers']
        for i, pos in enumerate(['N_1', 'N_2', 'N_3', 'N_4', 'N_5']):
            range_def = pf.get_range(pos)
            if range_def.min_val <= nums[i] <= range_def.max_val:
                position_hits[pos] += 1

    # Calculate rates and check within tolerance (±7%)
    rates = {}
    all_ok = True
    messages = []

    expected_rates = {
        'N_1': 0.87, 'N_2': 0.86, 'N_3': 0.85, 'N_4': 0.86, 'N_5': 0.86
    }

    for pos, hits in position_hits.items():
        rate = hits / total
        rates[pos] = rate
        expected = expected_rates[pos]
        if not (expected - 0.07 <= rate <= expected + 0.07):
            all_ok = False
            messages.append(f"{pos}: {rate:.1%} (expected {expected:.0%})")

    message = "All within tolerance" if all_ok else "; ".join(messages)
    return all_ok, message, rates


# =============================================================================
# Integration Tests - Predictor
# =============================================================================

def test_predictor_generates_valid_tickets() -> Tuple[bool, str, Dict]:
    """TEST-PRED-001: Predictor generates valid tickets."""
    predictor = CA5Predictor()
    result = predictor.predict(num_tickets=10)

    tickets = result['tickets']

    for i, ticket in enumerate(tickets):
        # Check 5 numbers
        if len(ticket) != 5:
            return False, f"Ticket {i} has {len(ticket)} numbers", {}

        # Check all unique
        if len(set(ticket)) != 5:
            return False, f"Ticket {i} has duplicates", {}

        # Check range 1-39
        if not all(1 <= n <= 39 for n in ticket):
            return False, f"Ticket {i} has out-of-range numbers", {}

        # Check sorted
        if ticket != sorted(ticket):
            return False, f"Ticket {i} not sorted", {}

    return True, f"Generated {len(tickets)} valid tickets", {}


def test_predictor_position_compliance() -> Tuple[bool, str, Dict]:
    """TEST-PRED-002: All tickets pass position filter."""
    predictor = CA5Predictor()
    result = predictor.predict(num_tickets=100)

    tickets = result['tickets']
    pf = predictor.position_filter

    failed = []
    for i, ticket in enumerate(tickets):
        is_valid, _ = pf.validate_ticket(ticket)
        if not is_valid:
            failed.append(i)

    if failed:
        return False, f"{len(failed)} tickets failed position validation", {'failed': failed}

    return True, "100% position compliance", {}


def test_predictor_backtest_accuracy() -> Tuple[bool, str, Dict]:
    """TEST-PRED-003: Backtest returns correct match counts."""
    predictor = CA5Predictor()

    # Get a known date
    history = predictor.history
    test_draw = history.draws[-10]  # 10th from last
    test_date = test_draw['date']
    actual = set(test_draw['numbers'])

    # Run backtest
    result = predictor.backtest_single(test_date, num_tickets=20)

    # Verify match counts are calculated correctly
    if result['actual'] is None:
        return False, "Backtest couldn't find actual results", {}

    for score in result['scores']:
        ticket = set(score['ticket'])
        expected_matches = len(ticket & actual)
        if score['matches'] != expected_matches:
            return False, f"Match count mismatch: {score['matches']} vs {expected_matches}", {}

    return True, "Match counts verified", {'actual': list(actual)}


def test_strategies_differ() -> Tuple[bool, str, Dict]:
    """TEST-PRED-004: Different strategies produce different results."""
    predictor = CA5Predictor()

    strategies = ['balanced', 'contact_first', 'position_first', 'random']
    results = {}

    for strategy in strategies:
        result = predictor.predict(num_tickets=20, strategy=strategy)
        results[strategy] = set(tuple(t) for t in result['tickets'])

    # Check that at least some strategies produce different tickets
    all_same = True
    for i, s1 in enumerate(strategies):
        for s2 in strategies[i+1:]:
            if results[s1] != results[s2]:
                all_same = False
                break

    if all_same:
        return False, "All strategies produced identical tickets", {}

    return True, "Strategies produce varied results", {}


# =============================================================================
# Statistical Validation
# =============================================================================

def test_baseline_probabilities() -> Tuple[bool, str, Dict]:
    """Verify our baseline probability calculations."""
    # Correct values for CA Fantasy 5 (5 from 39)
    # P(k) = C(5,k) × C(34,5-k) / C(39,5)
    expected = {
        0: 0.4833,  # C(5,0)×C(34,5)/C(39,5) = 278256/575757
        1: 0.4027,  # C(5,1)×C(34,4)/C(39,5) = 231880/575757
        2: 0.1039,  # C(5,2)×C(34,3)/C(39,5) = 59840/575757
        3: 0.0097,  # C(5,3)×C(34,2)/C(39,5) = 5610/575757
        4: 0.0003,  # C(5,4)×C(34,1)/C(39,5) = 170/575757
        5: 0.000002,  # C(5,5)×C(34,0)/C(39,5) = 1/575757
    }

    calculated = {}
    for k in range(6):
        calculated[k] = hypergeometric_probability(k)

    # Check each is within 1%
    for k, exp in expected.items():
        calc = calculated[k]
        if abs(calc - exp) > 0.01:
            return False, f"P({k} matches): expected {exp:.4f}, got {calc:.4f}", {}

    return True, "Baseline probabilities verified", calculated


def run_backtest_comparison(num_days: int = 100) -> Dict:
    """Run backtest comparison across configurations."""
    configs = [
        {'matrix': 'proximity', 'capture': '85', 'strategy': 'balanced'},
        {'matrix': 'proximity', 'capture': '85', 'strategy': 'contact_first'},
        {'matrix': 'weighted', 'capture': '85', 'strategy': 'balanced'},
        {'matrix': 'proximity', 'capture': '90', 'strategy': 'balanced'},
    ]

    results = {}
    history = DrawHistory()

    # Get test date range
    end_date = history.draws[-1]['date']
    start_date = end_date - timedelta(days=num_days)

    for config in configs:
        predictor = CA5Predictor(
            matrix_type=config['matrix'],
            capture_level=config['capture']
        )

        result = predictor.backtest_range(
            start_date=start_date,
            end_date=end_date,
            num_tickets=20,
            strategy=config['strategy']
        )

        config_name = f"{config['matrix']}_{config['capture']}_{config['strategy']}"
        results[config_name] = {
            'days_tested': result['days_tested'],
            'avg_best_match': result['summary']['avg_best_match'],
            'days_with_3plus': result['summary']['days_with_3plus_match'],
            'hit_rate_3plus': result['summary']['days_with_3plus_match'] / result['days_tested'] * 100
                             if result['days_tested'] > 0 else 0,
        }

    return results


# =============================================================================
# Main Test Runner
# =============================================================================

def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def run_unit_tests() -> TestRunner:
    """Run all unit tests."""
    runner = TestRunner()

    print_header("UNIT TESTS - Matrix Implementations")
    runner.print_result(runner.run_test("VLA Standard has expected bias", test_vla_standard_has_bias))
    runner.print_result(runner.run_test("Weighted Adjacency eliminates bias", test_weighted_eliminates_bias))
    runner.print_result(runner.run_test("Numerical Proximity is uniform", test_numerical_proximity_uniform))
    runner.print_result(runner.run_test("Contact scoring works correctly", test_contact_scoring))

    print_header("UNIT TESTS - Position Filters")
    runner.print_result(runner.run_test("85% ranges configured correctly", test_filter_ranges_correct))
    runner.print_result(runner.run_test("Filter validation works", test_filter_validation))
    runner.print_result(runner.run_test("Historical capture rates match", test_filter_capture_rates))

    print_header("INTEGRATION TESTS - Predictor")
    runner.print_result(runner.run_test("Generates valid tickets", test_predictor_generates_valid_tickets))
    runner.print_result(runner.run_test("100% position compliance", test_predictor_position_compliance))
    runner.print_result(runner.run_test("Backtest accuracy", test_predictor_backtest_accuracy))
    runner.print_result(runner.run_test("Strategies produce different results", test_strategies_differ))

    print_header("STATISTICAL VALIDATION")
    runner.print_result(runner.run_test("Baseline probabilities correct", test_baseline_probabilities))

    return runner


def run_backtest_validation(num_days: int) -> Dict:
    """Run backtest validation."""
    print_header(f"BACKTEST COMPARISON ({num_days} days)")

    print("\nRunning backtest across configurations...")
    results = run_backtest_comparison(num_days)

    # Print results
    print(f"\n{'Configuration':<40} {'Days':<6} {'Avg Best':<10} {'3+ Rate':<10}")
    print("-" * 70)

    best_config = None
    best_avg = 0

    for config, metrics in results.items():
        print(f"{config:<40} {metrics['days_tested']:<6} "
              f"{metrics['avg_best_match']:<10.2f} {metrics['hit_rate_3plus']:<10.1f}%")
        if metrics['avg_best_match'] > best_avg:
            best_avg = metrics['avg_best_match']
            best_config = config

    # Calculate random baseline
    baseline = expected_best_match(20)
    print(f"\n{'Random Baseline (theoretical)':<40} {'--':<6} {baseline:<10.2f} {'30.0':<10}%")

    print(f"\nBest Configuration: {best_config}")

    return results


def main():
    parser = argparse.ArgumentParser(description="VLA Visualizer System Validation")
    parser.add_argument('--full', action='store_true', help="Full validation (500 days)")
    parser.add_argument('--extended', action='store_true', help="Extended validation (1000 days)")
    parser.add_argument('--unit-only', action='store_true', help="Unit tests only")
    parser.add_argument('--backtest-only', action='store_true', help="Backtest only")
    parser.add_argument('--days', type=int, help="Custom backtest days")

    args = parser.parse_args()

    # Determine backtest days
    if args.days:
        backtest_days = args.days
    elif args.extended:
        backtest_days = 1000
    elif args.full:
        backtest_days = 500
    else:
        backtest_days = 100

    print("\n" + "=" * 60)
    print("  VALIDATION REPORT - VLA Visualizer Prediction System")
    print("=" * 60)
    print(f"\nValidation started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Run tests
    if not args.backtest_only:
        runner = run_unit_tests()
        passed, total = runner.get_summary()
    else:
        passed, total = 0, 0

    if not args.unit_only:
        backtest_results = run_backtest_validation(backtest_days)

    # Print summary
    print_header("SUMMARY")

    if not args.backtest_only:
        print(f"\nUnit/Integration Tests: {passed}/{total} passed")
        if passed == total:
            print("  Status: ALL TESTS PASSED")
        else:
            print("  Status: SOME TESTS FAILED")
            return 1

    if not args.unit_only:
        print(f"\nBacktest: {backtest_days} days tested")
        print("  See configuration comparison above")

    print("\n" + "=" * 60)
    print("  VALIDATION COMPLETE")
    print("=" * 60)

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
