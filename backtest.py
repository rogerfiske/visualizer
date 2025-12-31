"""
Visual Lottery Analyser Backtesting Framework
Compares VLA predictions against actual lottery results

Usage:
    python backtest.py --game fantasy5 --predictions predictions.csv --date 2025-11-01
    python backtest.py --game daily4 --predictions predictions.txt --date 2025-11-01
"""

import argparse
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple, Dict
import re

# Actual results file paths
FANTASY5_DATA = Path(r"C:\Users\Minis\CascadeProjects\c5_scrapper\data\raw\CA5_raw_data.txt")
DAILY4_DATA = Path(r"C:\Users\Minis\CascadeProjects\CA-4_scrapper\data\raw\CA_Daily_4_dat.csv")


def parse_date(date_str: str) -> datetime:
    """Parse date from various formats."""
    for fmt in ["%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y", "%d/%m/%Y"]:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date: {date_str}")


def load_actual_results(game: str, target_date: datetime) -> Tuple[List[int], str]:
    """Load actual lottery results for a specific date."""
    if game == "fantasy5":
        data_file = FANTASY5_DATA
        num_cols = 5
    elif game == "daily4":
        data_file = DAILY4_DATA
        num_cols = 4
    else:
        raise ValueError(f"Unknown game: {game}")

    with open(data_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header

        for row in reader:
            if len(row) < num_cols + 1:
                continue
            try:
                row_date = parse_date(row[0])
                if row_date.date() == target_date.date():
                    numbers = [int(row[i]) for i in range(1, num_cols + 1)]
                    return numbers, row[0]
            except (ValueError, IndexError):
                continue

    return [], ""


def parse_predictions(file_path: Path, game: str) -> List[List[int]]:
    """
    Parse prediction file. Supports multiple formats:
    - CSV: number1,number2,number3,number4,number5
    - TXT with spaces: 1 2 3 4 5
    - VLA export format
    """
    predictions = []

    with open(file_path, 'r') as f:
        content = f.read()

    # Try to detect format and parse
    lines = content.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or line.lower().startswith('date'):
            continue

        # Try comma-separated
        if ',' in line:
            parts = line.split(',')
            # Skip date column if present
            numbers = []
            for p in parts:
                p = p.strip()
                if p.isdigit():
                    numbers.append(int(p))
                elif re.match(r'^\d+$', p):
                    numbers.append(int(p))
        else:
            # Try space/tab separated
            parts = line.split()
            numbers = []
            for p in parts:
                if p.isdigit():
                    numbers.append(int(p))

        if game == "fantasy5" and len(numbers) >= 5:
            predictions.append(numbers[:5])
        elif game == "daily4" and len(numbers) >= 4:
            predictions.append(numbers[:4])
        elif len(numbers) > 0:
            predictions.append(numbers)

    return predictions


def score_fantasy5(prediction: List[int], actual: List[int]) -> int:
    """Score Fantasy 5 prediction - count matching numbers."""
    return len(set(prediction) & set(actual))


def score_daily4(prediction: List[int], actual: List[int]) -> Dict[str, bool]:
    """
    Score Daily 4 prediction.
    Returns match types: exact, any_order (box), pairs
    """
    results = {
        "exact": prediction == actual,
        "any_order": sorted(prediction) == sorted(actual),
        "match_3": False,
        "match_2": False,
        "match_count": 0
    }

    # Count positional matches
    match_count = sum(1 for i in range(min(len(prediction), len(actual)))
                      if prediction[i] == actual[i])
    results["match_count"] = match_count
    results["match_3"] = match_count >= 3
    results["match_2"] = match_count >= 2

    return results


def analyze_predictions(game: str, predictions: List[List[int]], actual: List[int]) -> Dict:
    """Analyze all predictions against actual results."""
    results = {
        "actual": actual,
        "total_predictions": len(predictions),
        "predictions": [],
        "best_match": 0,
        "summary": {}
    }

    if game == "fantasy5":
        match_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        for i, pred in enumerate(predictions):
            score = score_fantasy5(pred, actual)
            results["predictions"].append({
                "ticket": i + 1,
                "numbers": pred,
                "matches": score,
                "matching_numbers": list(set(pred) & set(actual))
            })
            match_counts[score] = match_counts.get(score, 0) + 1
            if score > results["best_match"]:
                results["best_match"] = score

        results["summary"] = {
            "match_distribution": match_counts,
            "any_match_3+": match_counts.get(3, 0) + match_counts.get(4, 0) + match_counts.get(5, 0),
            "any_match_4+": match_counts.get(4, 0) + match_counts.get(5, 0),
            "jackpot": match_counts.get(5, 0)
        }

    elif game == "daily4":
        exact_matches = 0
        box_matches = 0

        for i, pred in enumerate(predictions):
            score = score_daily4(pred, actual)
            results["predictions"].append({
                "ticket": i + 1,
                "numbers": pred,
                "exact_match": score["exact"],
                "box_match": score["any_order"],
                "positional_matches": score["match_count"]
            })
            if score["exact"]:
                exact_matches += 1
                results["best_match"] = 4
            if score["any_order"]:
                box_matches += 1
                if results["best_match"] < 4:
                    results["best_match"] = 3  # Use 3 to indicate box match

        results["summary"] = {
            "exact_matches": exact_matches,
            "box_matches": box_matches,
            "straight_win": exact_matches > 0,
            "box_win": box_matches > 0
        }

    return results


def print_report(game: str, date_str: str, results: Dict):
    """Print analysis report."""
    print("\n" + "=" * 60)
    print(f"BACKTEST REPORT: {game.upper()}")
    print(f"Date: {date_str}")
    print("=" * 60)

    print(f"\nActual Numbers: {results['actual']}")
    print(f"Total Predictions: {results['total_predictions']}")
    print(f"Best Match: {results['best_match']}")

    print("\n" + "-" * 40)
    print("SUMMARY:")
    for key, value in results['summary'].items():
        print(f"  {key}: {value}")

    print("\n" + "-" * 40)
    print("TOP PREDICTIONS:")

    # Sort predictions by match quality
    if game == "fantasy5":
        sorted_preds = sorted(results['predictions'],
                             key=lambda x: x['matches'], reverse=True)[:10]
        for pred in sorted_preds:
            matching = pred['matching_numbers']
            print(f"  Ticket {pred['ticket']:2d}: {pred['numbers']} "
                  f"-> {pred['matches']} matches {matching}")

    elif game == "daily4":
        for pred in results['predictions'][:10]:
            status = "EXACT!" if pred['exact_match'] else \
                     "BOX" if pred['box_match'] else \
                     f"{pred['positional_matches']} pos"
            print(f"  Ticket {pred['ticket']:2d}: {pred['numbers']} -> {status}")

    print("=" * 60)


def run_backtest(game: str, predictions_file: Path, target_date: datetime):
    """Run complete backtest analysis."""
    # Load actual results
    actual, date_str = load_actual_results(game, target_date)

    if not actual:
        print(f"No results found for {game} on {target_date.strftime('%Y-%m-%d')}")
        print("Check if the date has a drawing and data is available.")
        return None

    # Parse predictions
    predictions = parse_predictions(predictions_file, game)

    if not predictions:
        print(f"No valid predictions found in {predictions_file}")
        return None

    # Analyze
    results = analyze_predictions(game, predictions, actual)

    # Print report
    print_report(game, date_str, results)

    return results


def main():
    parser = argparse.ArgumentParser(description="Backtest VLA predictions")
    parser.add_argument("--game", choices=["fantasy5", "daily4"], required=True,
                        help="Game type")
    parser.add_argument("--predictions", type=Path, required=True,
                        help="Path to predictions file (CSV or TXT)")
    parser.add_argument("--date", required=True,
                        help="Target date (YYYY-MM-DD or MM/DD/YYYY)")

    args = parser.parse_args()

    target_date = parse_date(args.date)

    run_backtest(args.game, args.predictions, target_date)


if __name__ == "__main__":
    main()
