"""
CA5 Fantasy 5 - Exploratory Data Analysis
Analyzes N_1 through N_5 columns for range, median, and distribution
"""
import csv
from datetime import datetime
from collections import Counter

def load_data(filepath):
    """Load CA5 data from CSV file"""
    data = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Parse date (M/D/YYYY format)
                date_str = row['date']
                date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                data.append({
                    'date': date_obj,
                    'N_1': int(row['N_1']),
                    'N_2': int(row['N_2']),
                    'N_3': int(row['N_3']),
                    'N_4': int(row['N_4']),
                    'N_5': int(row['N_5'])
                })
            except (ValueError, KeyError) as e:
                continue
    # Sort by date descending (most recent first)
    data.sort(key=lambda x: x['date'], reverse=True)
    return data

def calculate_stats(data, columns=['N_1', 'N_2', 'N_3', 'N_4', 'N_5']):
    """Calculate range, median for each column"""
    stats = {}
    for col in columns:
        values = [row[col] for row in data]
        values_sorted = sorted(values)
        n = len(values_sorted)

        min_val = min(values)
        max_val = max(values)

        # Median
        if n % 2 == 0:
            median = (values_sorted[n//2 - 1] + values_sorted[n//2]) / 2
        else:
            median = values_sorted[n//2]

        # Distribution (frequency count)
        distribution = Counter(values)

        stats[col] = {
            'min': min_val,
            'max': max_val,
            'range': f"{min_val}-{max_val}",
            'median': median,
            'count': n,
            'distribution': distribution
        }
    return stats

def print_histogram(distribution, col_name, max_width=50):
    """Print ASCII histogram for distribution"""
    # Group into bins for visualization (1-39 range)
    bins = {}
    for i in range(1, 40):
        bins[i] = distribution.get(i, 0)

    max_count = max(bins.values()) if bins else 1

    print(f"\n  Distribution for {col_name}:")
    print(f"  {'Number':<8} {'Count':<8} {'Bar'}")
    print(f"  {'-'*6}   {'-'*6}   {'-'*max_width}")

    for num in range(1, 40):
        count = bins[num]
        bar_length = int((count / max_count) * max_width) if max_count > 0 else 0
        bar = '#' * bar_length
        print(f"  {num:<8} {count:<8} {bar}")

def print_condensed_histogram(distribution, col_name, max_width=40):
    """Print condensed histogram grouped by ranges"""
    # Group into 10-number bins
    bins = {
        '1-10': sum(distribution.get(i, 0) for i in range(1, 11)),
        '11-20': sum(distribution.get(i, 0) for i in range(11, 21)),
        '21-30': sum(distribution.get(i, 0) for i in range(21, 31)),
        '31-39': sum(distribution.get(i, 0) for i in range(31, 40))
    }

    max_count = max(bins.values()) if bins else 1

    print(f"\n  Range Distribution for {col_name}:")
    for range_label, count in bins.items():
        bar_length = int((count / max_count) * max_width) if max_count > 0 else 0
        bar = '#' * bar_length
        pct = (count / sum(bins.values()) * 100) if sum(bins.values()) > 0 else 0
        print(f"    {range_label:<8}: {count:>5} ({pct:5.1f}%) |{bar}")

def print_stats_table(stats, period_name, show_full_dist=False):
    """Print statistics table"""
    print(f"\n{'='*70}")
    print(f"  {period_name}")
    print(f"{'='*70}")

    first_col = list(stats.keys())[0]
    print(f"  Total draws: {stats[first_col]['count']}")

    print(f"\n  {'Column':<10} {'Range':<12} {'Median':<10}")
    print(f"  {'-'*8}   {'-'*10}   {'-'*8}")

    for col, stat in stats.items():
        print(f"  {col:<10} {stat['range']:<12} {stat['median']:<10.1f}")

    # Print distribution diagrams
    for col, stat in stats.items():
        print_condensed_histogram(stat['distribution'], col)

    if show_full_dist:
        for col, stat in stats.items():
            print_histogram(stat['distribution'], col)

def main():
    filepath = r'C:\Users\Minis\CascadeProjects\visualizer\data\raw\CA5_date.csv'

    print("Loading CA5 Fantasy 5 data...")
    data = load_data(filepath)

    if not data:
        print("ERROR: No data loaded!")
        return

    print(f"Loaded {len(data)} draws")
    print(f"Date range: {data[-1]['date'].strftime('%m/%d/%Y')} to {data[0]['date'].strftime('%m/%d/%Y')}")

    # Full dataset
    print_stats_table(calculate_stats(data), f"FULL DATASET ({len(data)} draws)")

    # Recent periods
    periods = [
        (500, "LAST 500 DAYS"),
        (250, "LAST 250 DAYS"),
        (100, "LAST 100 DAYS"),
        (39, "LAST 39 DAYS")
    ]

    for days, label in periods:
        if len(data) >= days:
            subset = data[:days]
            print_stats_table(calculate_stats(subset), f"{label} ({days} draws)")
        else:
            print(f"\n{'='*70}")
            print(f"  {label}: Insufficient data (only {len(data)} draws available)")
            print(f"{'='*70}")

if __name__ == "__main__":
    main()
