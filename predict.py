#!/usr/bin/env python3
"""
CA Fantasy 5 Prediction CLI

Generate predictions using bias-corrected matrix analysis and
EDA-derived optimal position ranges.

Usage:
    # Generate predictions for tomorrow (using latest draw)
    python predict.py

    # Generate predictions for a specific date
    python predict.py --date 2025-12-31

    # Backtest on a specific date
    python predict.py --backtest --date 2025-12-30

    # Backtest over a date range
    python predict.py --backtest --start 2025-12-01 --end 2025-12-31

    # Use different matrix and strategy
    python predict.py --matrix weighted --strategy contact_first --tickets 30
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.predictor import CA5Predictor


def parse_date(date_str: str) -> datetime:
    """Parse date from various formats."""
    for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y"]:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date: {date_str}")


def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_prediction_result(result: dict) -> None:
    """Print prediction results."""
    print_header("CA FANTASY 5 PREDICTIONS")

    print(f"\nTarget Date: {result['target_date_str']}")
    print(f"Based on draw(s): {result['previous_dates']}")
    print(f"Previous numbers: {result['previous_draws']}")

    print(f"\nConfiguration:")
    for k, v in result['config'].items():
        print(f"  {k}: {v}")

    print(f"\n{'-' * 40}")
    print(f"GENERATED TICKETS ({len(result['tickets'])} total):")
    print(f"{'-' * 40}")

    for i, ticket in enumerate(result['tickets'], 1):
        print(f"  {i:2d}. {ticket}")


def print_backtest_result(result: dict) -> None:
    """Print backtest results for a single date."""
    print_header("BACKTEST RESULT")

    print(f"\nTest Date: {result['target_date_str']}")
    print(f"Actual Draw: {result.get('actual', 'N/A')}")
    print(f"Based on: {result['previous_dates']}")

    if result.get('actual'):
        print(f"\nBest Match: {result['best_match']} numbers")
        print(f"Tickets with 3+ matches: {result['tickets_with_3plus']}")

        print(f"\n{'-' * 40}")
        print("TOP TICKETS:")
        for score in result['scores'][:10]:
            ticket = score['ticket']
            matches = score['matches']
            matching = score['matching_numbers']
            marker = "*" * matches if matches >= 3 else ""
            print(f"  {ticket} -> {matches} matches {matching} {marker}")

        print(f"\nMatch Distribution:")
        for matches, count in sorted(result['match_distribution'].items()):
            bar = "#" * count
            print(f"  {matches} matches: {count:3d} {bar}")
    else:
        print("\n  No actual results available for this date.")


def print_range_backtest_result(result: dict) -> None:
    """Print backtest results for a date range."""
    print_header("BACKTEST SUMMARY")

    print(f"\nDate Range: {result['start_date'].strftime('%Y-%m-%d')} to "
          f"{result['end_date'].strftime('%Y-%m-%d')}")
    print(f"Days Tested: {result['days_tested']}")

    print(f"\nConfiguration:")
    for k, v in result['config'].items():
        print(f"  {k}: {v}")

    summary = result['summary']
    print(f"\n{'-' * 40}")
    print("RESULTS:")
    print(f"  Average Best Match: {summary['avg_best_match']:.2f}")
    print(f"  Days with 5-match (jackpot): {summary['days_with_5_match']}")
    print(f"  Days with 4+ match: {summary['days_with_4plus_match']}")
    print(f"  Days with 3+ match: {summary['days_with_3plus_match']}")
    print(f"  Total 3+ tickets: {summary['total_3plus_tickets']}")

    # Calculate rates
    if result['days_tested'] > 0:
        rate_3plus = summary['days_with_3plus_match'] / result['days_tested'] * 100
        print(f"\n  Hit Rate (3+ on any ticket): {rate_3plus:.1f}%")


def main():
    parser = argparse.ArgumentParser(
        description="CA Fantasy 5 Prediction System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python predict.py                           # Predict for tomorrow
  python predict.py --date 2025-12-31         # Predict for specific date
  python predict.py --backtest --date 2025-12-30  # Backtest single day
  python predict.py --backtest --start 2025-12-01 --end 2025-12-31  # Range backtest
        """
    )

    # Mode
    parser.add_argument('--backtest', action='store_true',
                        help="Run in backtest mode")

    # Date options
    parser.add_argument('--date', type=str,
                        help="Target date (YYYY-MM-DD)")
    parser.add_argument('--start', type=str,
                        help="Start date for range backtest")
    parser.add_argument('--end', type=str,
                        help="End date for range backtest")

    # Configuration
    parser.add_argument('--matrix', choices=['proximity', 'weighted'],
                        default='proximity',
                        help="Matrix type (default: proximity)")
    parser.add_argument('--capture', choices=['80', '85', '90'],
                        default='85',
                        help="Capture level for position filter (default: 85)")
    parser.add_argument('--strategy',
                        choices=['balanced', 'contact_first', 'position_first', 'random'],
                        default='balanced',
                        help="Ticket generation strategy (default: balanced)")
    parser.add_argument('--tickets', type=int, default=20,
                        help="Number of tickets to generate (default: 20)")
    parser.add_argument('--lookback', type=int, default=1,
                        help="Number of previous draws for contact analysis (default: 1)")

    # Output
    parser.add_argument('--output', type=Path,
                        help="Export predictions to file")
    parser.add_argument('--format', choices=['csv', 'txt'], default='csv',
                        help="Output format (default: csv)")
    parser.add_argument('--quiet', action='store_true',
                        help="Minimal output")

    args = parser.parse_args()

    # Create predictor
    predictor = CA5Predictor(
        matrix_type=args.matrix,
        capture_level=args.capture,
        lookback_draws=args.lookback
    )

    if not args.quiet:
        info = predictor.get_info()
        print(f"\nPredictor initialized:")
        print(f"  Matrix: {info['matrix']}")
        print(f"  Data: {info['data_range']} ({info['total_draws']} draws)")

    if args.backtest:
        # Backtest mode
        if args.start and args.end:
            # Range backtest
            start_date = parse_date(args.start)
            end_date = parse_date(args.end)
            result = predictor.backtest_range(
                start_date=start_date,
                end_date=end_date,
                num_tickets=args.tickets,
                strategy=args.strategy
            )
            print_range_backtest_result(result)
        elif args.date:
            # Single date backtest
            target_date = parse_date(args.date)
            result = predictor.backtest_single(
                test_date=target_date,
                num_tickets=args.tickets,
                strategy=args.strategy
            )
            print_backtest_result(result)
        else:
            print("Error: --backtest requires --date or --start/--end")
            return 1
    else:
        # Prediction mode
        target_date = parse_date(args.date) if args.date else None
        result = predictor.predict(
            target_date=target_date,
            num_tickets=args.tickets,
            strategy=args.strategy
        )

        if not args.quiet:
            print_prediction_result(result)
        else:
            for ticket in result['tickets']:
                print(",".join(str(n) for n in ticket))

        # Export if requested
        if args.output:
            predictor.export_predictions(
                result['tickets'],
                args.output,
                format=args.format
            )
            print(f"\nExported to: {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
