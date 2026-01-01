"""
CA5 Fantasy 5 - EDA Chart Generator
Creates PNG distribution diagrams with 90th percentile highlighting
"""
import csv
import os
from datetime import datetime
from collections import Counter

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    print("ERROR: matplotlib is required. Install with: pip install matplotlib")
    exit(1)

def load_data(filepath):
    """Load CA5 data from CSV file"""
    data = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
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
            except (ValueError, KeyError):
                continue
    data.sort(key=lambda x: x['date'], reverse=True)
    return data

def get_distribution(data, column):
    """Get frequency distribution for a column"""
    values = [row[column] for row in data]
    distribution = Counter(values)
    # Ensure all numbers 1-39 are represented
    for i in range(1, 40):
        if i not in distribution:
            distribution[i] = 0
    return distribution

def calculate_90th_percentile_threshold(distribution):
    """Calculate the count threshold for 90th percentile"""
    counts = sorted(distribution.values(), reverse=True)
    if not counts:
        return 0
    idx = int(len(counts) * 0.10)  # Top 10% = 90th percentile
    return counts[idx] if idx < len(counts) else counts[-1]

def create_chart(data, column, period_name, period_days, output_dir):
    """Create a single distribution chart with 90th percentile highlighting"""
    distribution = get_distribution(data, column)

    # Get numbers and counts
    numbers = list(range(1, 40))
    counts = [distribution[n] for n in numbers]

    # Calculate 90th percentile threshold
    threshold = calculate_90th_percentile_threshold(distribution)

    # Assign colors: blue for normal, red/orange for 90th percentile
    colors = ['#E74C3C' if distribution[n] >= threshold else '#3498DB' for n in numbers]

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))

    # Create bar chart
    bars = ax.bar(numbers, counts, color=colors, edgecolor='white', linewidth=0.5)

    # Add 90th percentile line
    ax.axhline(y=threshold, color='#E74C3C', linestyle='--', linewidth=2, alpha=0.7)
    ax.text(40.5, threshold, f'90th %ile ({threshold})', va='center', ha='left',
            color='#E74C3C', fontsize=10, fontweight='bold')

    # Styling
    ax.set_xlabel('Number', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax.set_title(f'CA5 Fantasy 5 - {column} Distribution\n{period_name} ({period_days} draws)',
                 fontsize=14, fontweight='bold', pad=15)

    # Set x-axis ticks
    ax.set_xticks(range(1, 40, 2))
    ax.set_xlim(0, 42)

    # Grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # Legend
    normal_patch = mpatches.Patch(color='#3498DB', label='Below 90th percentile')
    high_patch = mpatches.Patch(color='#E74C3C', label='90th percentile and above')
    ax.legend(handles=[normal_patch, high_patch], loc='upper right', fontsize=10)

    # Stats annotation
    values = [row[column] for row in data]
    median_val = sorted(values)[len(values)//2]
    min_val = min(values)
    max_val = max(values)

    stats_text = f'Range: {min_val}-{max_val}  |  Median: {median_val}'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()

    # Save
    filename = f"{column}_{period_days}days.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    return filepath

def main():
    data_path = r'C:\Users\Minis\CascadeProjects\visualizer\data\raw\CA5_date.csv'
    output_dir = r'C:\Users\Minis\CascadeProjects\visualizer\data\charts'

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print("Loading CA5 Fantasy 5 data...")
    data = load_data(data_path)
    print(f"Loaded {len(data)} draws")

    columns = ['N_1', 'N_2', 'N_3', 'N_4', 'N_5']
    periods = [
        (500, "Last 500 Days"),
        (250, "Last 250 Days"),
        (100, "Last 100 Days"),
        (39, "Last 39 Days")
    ]

    total_charts = len(columns) * len(periods)
    chart_count = 0

    for days, period_name in periods:
        subset = data[:days]
        print(f"\nGenerating charts for {period_name}...")

        for col in columns:
            filepath = create_chart(subset, col, period_name, days, output_dir)
            chart_count += 1
            print(f"  [{chart_count}/{total_charts}] Created: {os.path.basename(filepath)}")

    print(f"\n{'='*60}")
    print(f"COMPLETE: {total_charts} charts saved to:")
    print(f"  {output_dir}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
