"""
Batch Backtesting - Walk Forward Analysis
Processes multiple prediction files across date range

Usage:
    python batch_backtest.py --game fantasy5 --predictions-dir ./predictions --start-date 2025-11-01 --end-date 2025-11-30
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
from backtest import load_actual_results, parse_predictions, analyze_predictions

# Prediction file naming convention expected:
# fantasy5_2025-11-01.csv or daily4_11-01-2025.txt


def find_prediction_file(predictions_dir: Path, game: str, target_date: datetime) -> Path:
    """Find prediction file for a specific date."""
    date_formats = [
        target_date.strftime("%Y-%m-%d"),
        target_date.strftime("%m-%d-%Y"),
        target_date.strftime("%m_%d_%Y"),
        target_date.strftime("%Y%m%d"),
    ]

    for date_str in date_formats:
        for ext in ['.csv', '.txt']:
            patterns = [
                f"{game}_{date_str}{ext}",
                f"{game}{date_str}{ext}",
                f"{date_str}_{game}{ext}",
                f"{date_str}{ext}",
            ]
            for pattern in patterns:
                file_path = predictions_dir / pattern
                if file_path.exists():
                    return file_path

    return None


def run_batch_backtest(game: str, predictions_dir: Path,
                       start_date: datetime, end_date: datetime) -> Dict:
    """Run backtest for date range."""
    all_results = []
    current_date = start_date

    total_days = 0
    days_with_data = 0
    total_predictions = 0
    aggregate_stats = {
        "fantasy5": {"match_0": 0, "match_1": 0, "match_2": 0,
                     "match_3": 0, "match_4": 0, "match_5": 0},
        "daily4": {"exact": 0, "box": 0, "none": 0}
    }

    print(f"\n{'='*70}")
    print(f"BATCH BACKTEST: {game.upper()}")
    print(f"Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"{'='*70}\n")

    while current_date <= end_date:
        total_days += 1
        date_str = current_date.strftime("%Y-%m-%d")

        # Load actual results
        actual, actual_date = load_actual_results(game, current_date)

        if not actual:
            print(f"  {date_str}: No drawing data")
            current_date += timedelta(days=1)
            continue

        # Find prediction file
        pred_file = find_prediction_file(predictions_dir, game, current_date)

        if not pred_file:
            print(f"  {date_str}: Actual={actual} | NO PREDICTIONS FILE")
            current_date += timedelta(days=1)
            continue

        # Parse and analyze predictions
        predictions = parse_predictions(pred_file, game)

        if not predictions:
            print(f"  {date_str}: Actual={actual} | NO VALID PREDICTIONS IN FILE")
            current_date += timedelta(days=1)
            continue

        days_with_data += 1
        total_predictions += len(predictions)

        results = analyze_predictions(game, predictions, actual)
        all_results.append({
            "date": date_str,
            "actual": actual,
            "num_predictions": len(predictions),
            "best_match": results["best_match"],
            "summary": results["summary"]
        })

        # Update aggregate stats
        if game == "fantasy5":
            for i in range(6):
                key = f"match_{i}"
                aggregate_stats["fantasy5"][key] += results["summary"]["match_distribution"].get(i, 0)

            best = results["best_match"]
            match_info = f"Best: {best}"
            if best >= 3:
                match_info = f"*** {best} MATCHES! ***"
        else:
            if results["summary"]["exact_matches"] > 0:
                aggregate_stats["daily4"]["exact"] += results["summary"]["exact_matches"]
                match_info = "*** EXACT MATCH! ***"
            elif results["summary"]["box_matches"] > 0:
                aggregate_stats["daily4"]["box"] += results["summary"]["box_matches"]
                match_info = "*** BOX MATCH! ***"
            else:
                aggregate_stats["daily4"]["none"] += 1
                match_info = f"Best pos: {results['best_match']}"

        print(f"  {date_str}: Actual={actual} | {len(predictions)} tickets | {match_info}")

        current_date += timedelta(days=1)

    # Print summary
    print(f"\n{'='*70}")
    print("AGGREGATE RESULTS")
    print(f"{'='*70}")
    print(f"Total Days: {total_days}")
    print(f"Days with Predictions: {days_with_data}")
    print(f"Total Tickets Analyzed: {total_predictions}")

    if game == "fantasy5":
        stats = aggregate_stats["fantasy5"]
        print(f"\nMatch Distribution Across All Tickets:")
        for i in range(6):
            count = stats[f"match_{i}"]
            pct = (count / total_predictions * 100) if total_predictions > 0 else 0
            bar = "#" * int(pct / 2)
            print(f"  {i} matches: {count:5d} ({pct:5.1f}%) {bar}")

        total_3plus = stats["match_3"] + stats["match_4"] + stats["match_5"]
        print(f"\n  3+ matches: {total_3plus} tickets")
        print(f"  4+ matches: {stats['match_4'] + stats['match_5']} tickets")
        print(f"  5  matches: {stats['match_5']} tickets (JACKPOT)")

    else:  # daily4
        stats = aggregate_stats["daily4"]
        print(f"\nWin Summary:")
        print(f"  Exact Matches (Straight): {stats['exact']}")
        print(f"  Box Matches: {stats['box']}")
        print(f"  No Match Days: {stats['none']}")

    print(f"{'='*70}\n")

    return {
        "game": game,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "total_days": total_days,
        "days_with_data": days_with_data,
        "total_predictions": total_predictions,
        "aggregate_stats": aggregate_stats[game],
        "daily_results": all_results
    }


def main():
    parser = argparse.ArgumentParser(description="Batch backtest VLA predictions")
    parser.add_argument("--game", choices=["fantasy5", "daily4"], required=True,
                        help="Game type")
    parser.add_argument("--predictions-dir", type=Path, required=True,
                        help="Directory containing prediction files")
    parser.add_argument("--start-date", required=True,
                        help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True,
                        help="End date (YYYY-MM-DD)")
    parser.add_argument("--output", type=Path, default=None,
                        help="Save results to JSON file")

    args = parser.parse_args()

    start = datetime.strptime(args.start_date, "%Y-%m-%d")
    end = datetime.strptime(args.end_date, "%Y-%m-%d")

    results = run_batch_backtest(args.game, args.predictions_dir, start, end)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()
