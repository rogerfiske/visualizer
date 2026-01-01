"""
CA5 Fantasy 5 - Optimal Range Analysis
Find the smallest number range that captures X% of draws for each position
"""
import csv
import os
from datetime import datetime
from collections import Counter

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
except ImportError:
    print("ERROR: matplotlib and numpy required. Install with: pip install matplotlib numpy")
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

def get_percentile_range(values, lower_pct=5, upper_pct=95):
    """Get the value range containing central X% of draws"""
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    lower_idx = int(n * lower_pct / 100)
    upper_idx = int(n * upper_pct / 100) - 1
    return sorted_vals[lower_idx], sorted_vals[upper_idx]

def find_optimal_contiguous_range(values, target_capture=0.90):
    """Find smallest contiguous number range capturing target % of draws"""
    distribution = Counter(values)
    total = len(values)
    target_count = int(total * target_capture)

    # Try all possible contiguous ranges
    best_range = None
    best_span = 40  # Max possible span

    for start in range(1, 40):
        cumsum = 0
        for end in range(start, 40):
            cumsum += distribution.get(end, 0)
            if cumsum >= target_count:
                span = end - start + 1
                if span < best_span:
                    best_span = span
                    best_range = (start, end, cumsum, cumsum/total*100)
                break

    return best_range

def analyze_capture_tradeoffs(values):
    """Analyze range size vs capture rate tradeoffs"""
    results = []
    for target in [0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 0.99]:
        optimal = find_optimal_contiguous_range(values, target)
        if optimal:
            start, end, count, actual_pct = optimal
            span = end - start + 1
            pool_reduction = (39 - span) / 39 * 100
            results.append({
                'target': target * 100,
                'range': f"{start}-{end}",
                'span': span,
                'captured': count,
                'actual_pct': actual_pct,
                'pool_reduction': pool_reduction
            })
    return results

def print_analysis(data, period_name, days):
    """Print comprehensive optimal range analysis"""
    columns = ['N_1', 'N_2', 'N_3', 'N_4', 'N_5']

    print(f"\n{'='*80}")
    print(f"  OPTIMAL RANGE ANALYSIS: {period_name} ({days} draws)")
    print(f"{'='*80}")

    # Summary table
    print(f"\n  90% CAPTURE RANGES (Central ranges capturing 90% of draws)")
    print(f"  {'-'*70}")
    print(f"  {'Position':<10} {'5th-95th %ile':<15} {'Optimal Range':<15} {'Span':<8} {'Pool Reduction':<15}")
    print(f"  {'-'*70}")

    for col in columns:
        values = [row[col] for row in data]

        # Percentile range
        p5, p95 = get_percentile_range(values, 5, 95)
        pct_range = f"{p5}-{p95}"

        # Optimal contiguous range
        optimal = find_optimal_contiguous_range(values, 0.90)
        if optimal:
            start, end, count, actual_pct = optimal
            opt_range = f"{start}-{end}"
            span = end - start + 1
            reduction = (39 - span) / 39 * 100
        else:
            opt_range = "N/A"
            span = 39
            reduction = 0

        print(f"  {col:<10} {pct_range:<15} {opt_range:<15} {span:<8} {reduction:>5.1f}%")

    # Detailed tradeoff analysis for each column
    print(f"\n  CAPTURE RATE vs POOL SIZE TRADEOFFS")
    print(f"  {'-'*70}")

    for col in columns:
        values = [row[col] for row in data]
        tradeoffs = analyze_capture_tradeoffs(values)

        print(f"\n  {col}:")
        print(f"    {'Target %':<10} {'Range':<12} {'Span':<8} {'Actual %':<12} {'Pool Reduction':<15}")
        for t in tradeoffs:
            print(f"    {t['target']:<10.0f} {t['range']:<12} {t['span']:<8} {t['actual_pct']:<12.1f} {t['pool_reduction']:>5.1f}%")

def create_optimal_range_chart(data, column, period_name, days, output_dir, target_capture=0.90):
    """Create chart highlighting optimal capture range"""
    values = [row[column] for row in data]
    distribution = Counter(values)

    # Ensure all numbers represented
    for i in range(1, 40):
        if i not in distribution:
            distribution[i] = 0

    # Find optimal range
    optimal = find_optimal_contiguous_range(values, target_capture)
    if optimal:
        opt_start, opt_end, opt_count, opt_pct = optimal
    else:
        opt_start, opt_end = 1, 39

    # Get percentile range
    p5, p95 = get_percentile_range(values, 5, 95)

    numbers = list(range(1, 40))
    counts = [distribution[n] for n in numbers]

    # Color coding: green for optimal range, blue for outside
    colors = ['#27AE60' if opt_start <= n <= opt_end else '#BDC3C7' for n in numbers]

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 7))

    bars = ax.bar(numbers, counts, color=colors, edgecolor='white', linewidth=0.5)

    # Mark the optimal range boundaries
    ax.axvline(x=opt_start - 0.5, color='#27AE60', linestyle='-', linewidth=3, alpha=0.8)
    ax.axvline(x=opt_end + 0.5, color='#27AE60', linestyle='-', linewidth=3, alpha=0.8)

    # Add shaded region for optimal range
    ax.axvspan(opt_start - 0.5, opt_end + 0.5, alpha=0.1, color='#27AE60')

    # Mark percentile range with dashed lines
    ax.axvline(x=p5, color='#E74C3C', linestyle='--', linewidth=2, alpha=0.7)
    ax.axvline(x=p95, color='#E74C3C', linestyle='--', linewidth=2, alpha=0.7)

    # Styling
    ax.set_xlabel('Number', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')

    span = opt_end - opt_start + 1
    reduction = (39 - span) / 39 * 100
    ax.set_title(f'CA5 Fantasy 5 - {column} Optimal Range Analysis\n{period_name} ({days} draws) | 90% Capture Range: {opt_start}-{opt_end} (span: {span}, {reduction:.0f}% pool reduction)',
                 fontsize=13, fontweight='bold', pad=15)

    ax.set_xticks(range(1, 40, 2))
    ax.set_xlim(0, 42)

    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # Legend
    optimal_patch = mpatches.Patch(color='#27AE60', label=f'90% Capture Range ({opt_start}-{opt_end})')
    outside_patch = mpatches.Patch(color='#BDC3C7', label='Outside optimal range')
    pct_line = plt.Line2D([0], [0], color='#E74C3C', linestyle='--', linewidth=2, label=f'5th-95th Percentile ({p5}-{p95})')
    ax.legend(handles=[optimal_patch, outside_patch, pct_line], loc='upper right', fontsize=10)

    # Stats box
    median_val = sorted(values)[len(values)//2]
    stats_text = f'Median: {median_val} | Range captured: {opt_count}/{len(values)} draws ({opt_pct:.1f}%)'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='#E8F8F5', alpha=0.8))

    plt.tight_layout()

    filename = f"{column}_{days}days_optimal.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    return filepath

def create_summary_chart(data, period_name, days, output_dir):
    """Create summary chart showing all N_i optimal ranges"""
    columns = ['N_1', 'N_2', 'N_3', 'N_4', 'N_5']

    fig, ax = plt.subplots(figsize=(14, 8))

    y_positions = [4, 3, 2, 1, 0]

    for col, y_pos in zip(columns, y_positions):
        values = [row[col] for row in data]
        optimal = find_optimal_contiguous_range(values, 0.90)

        if optimal:
            start, end, count, pct = optimal
            span = end - start + 1

            # Draw the full range bar (1-39) in light gray
            ax.barh(y_pos, 38, left=1, height=0.6, color='#EAEDED', edgecolor='#BDC3C7')

            # Draw the optimal range in green
            ax.barh(y_pos, span, left=start, height=0.6, color='#27AE60', edgecolor='#1E8449', linewidth=2)

            # Add range labels
            ax.text(start + span/2, y_pos, f'{start}-{end}', ha='center', va='center',
                    fontsize=11, fontweight='bold', color='white')

            # Add stats on right
            reduction = (39 - span) / 39 * 100
            ax.text(41, y_pos, f'Span: {span} | -{reduction:.0f}% pool', ha='left', va='center', fontsize=10)

    ax.set_yticks(y_positions)
    ax.set_yticklabels(columns, fontsize=12, fontweight='bold')
    ax.set_xlim(0, 55)
    ax.set_ylim(-0.5, 4.5)
    ax.set_xlabel('Number Range (1-39)', fontsize=12, fontweight='bold')
    ax.set_title(f'CA5 Fantasy 5 - 90% Capture Ranges Summary\n{period_name} ({days} draws)',
                 fontsize=14, fontweight='bold', pad=15)

    # Add x-axis ticks for number scale
    ax.set_xticks(range(1, 40, 5))
    ax.axvline(x=1, color='#BDC3C7', linestyle='-', linewidth=1)
    ax.axvline(x=39, color='#BDC3C7', linestyle='-', linewidth=1)

    ax.xaxis.grid(True, linestyle='--', alpha=0.3)

    plt.tight_layout()

    filename = f"summary_{days}days_optimal.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    return filepath

def main():
    data_path = r'C:\Users\Minis\CascadeProjects\visualizer\data\raw\CA5_date.csv'
    output_dir = r'C:\Users\Minis\CascadeProjects\visualizer\data\charts'

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

    # Print analysis for each period
    for days, period_name in periods:
        subset = data[:days]
        print_analysis(subset, period_name, days)

    # Generate charts
    print(f"\n{'='*80}")
    print("  GENERATING OPTIMAL RANGE CHARTS")
    print(f"{'='*80}")

    total_charts = len(columns) * len(periods) + len(periods)  # Individual + summary charts
    chart_count = 0

    for days, period_name in periods:
        subset = data[:days]

        # Summary chart
        filepath = create_summary_chart(subset, period_name, days, output_dir)
        chart_count += 1
        print(f"  [{chart_count}/{total_charts}] Created: {os.path.basename(filepath)}")

        # Individual charts
        for col in columns:
            filepath = create_optimal_range_chart(subset, col, period_name, days, output_dir)
            chart_count += 1
            print(f"  [{chart_count}/{total_charts}] Created: {os.path.basename(filepath)}")

    print(f"\n{'='*80}")
    print(f"  COMPLETE: {total_charts} charts saved to {output_dir}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
