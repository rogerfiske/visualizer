# VLA Visualizer - Lottery Analysis Backtesting Project

A backtesting framework for evaluating Visual Lottery Analyser (VLA) predictions against actual California lottery results.

## Overview

This project provides tools to:
- Understand VLA's visual analysis methodology
- Backtest VLA predictions against historical lottery data
- Track prediction accuracy over time
- Identify optimal VLA settings and strategies

## Supported Games

| Game | Format | Data Source |
|------|--------|-------------|
| **CA Fantasy 5** | 5 numbers from 1-39 | `CA5_raw_data.txt` |
| **CA Daily 4** | 4 digits (0-9 each) | `CA_Daily_4_dat.csv` |

## Project Structure

```
visualizer/
├── README.md                    # This file
├── VLA_ANALYSIS_SUMMARY.md      # Complete VLA methodology documentation
├── backtest.py                  # Single-day prediction scorer
├── batch_backtest.py            # Multi-day walk-forward analysis
├── docs/                        # VLA help documentation (273 English files)
│   ├── INDEX.md                 # Categorized index of help files
│   ├── visualanalysisconcept.htm
│   ├── analysis-base.htm
│   └── ...
└── predictions/                 # Directory for VLA prediction exports
    ├── fantasy5_2025-11-01.csv
    └── daily4_2025-11-01.csv
```

## Quick Start

### 1. Generate Predictions in VLA

1. Open Visual Lottery Analyser
2. Select your game (CA Fantasy 5 or CA Daily 4)
3. Set the analysis date to your target date (e.g., 11/1/2025)
4. Run "One Step Analysis" or use Tickets Generator
5. Export tickets to CSV or TXT format

### 2. Run Single-Day Backtest

```bash
# Fantasy 5
python backtest.py --game fantasy5 --predictions predictions/fantasy5_2025-11-01.csv --date 2025-11-01

# Daily 4
python backtest.py --game daily4 --predictions predictions/daily4_2025-11-01.csv --date 2025-11-01
```

### 3. Run Batch Backtest (Multiple Days)

```bash
python batch_backtest.py \
    --game fantasy5 \
    --predictions-dir ./predictions \
    --start-date 2025-11-01 \
    --end-date 2025-11-30 \
    --output results.json
```

## Prediction File Formats

### CSV Format
```csv
1,5,12,23,39
3,8,15,28,35
...
```

### TXT Format (space-separated)
```
1 5 12 23 39
3 8 15 28 35
...
```

### File Naming Convention
- `fantasy5_YYYY-MM-DD.csv` or `fantasy5_YYYY-MM-DD.txt`
- `daily4_YYYY-MM-DD.csv` or `daily4_YYYY-MM-DD.txt`

## Scoring

### Fantasy 5
| Matches | Result |
|---------|--------|
| 5 | Jackpot |
| 4 | Major prize |
| 3 | Minor prize |
| 2 | Free play |
| 0-1 | No win |

### Daily 4
| Match Type | Description |
|------------|-------------|
| Straight | Exact match (all 4 digits in order) |
| Box | All digits match (any order) |
| Positional | Count of correct position matches |

## VLA Key Concepts

Visual Lottery Analyser uses geometric/visual analysis on a grid representation of lottery numbers. Key principles:

1. **Balance Number Types**: Mix contact/outside, hot/cold, odd/even
2. **Spread Across Grid**: Avoid clustering on single lines or blocks
3. **Pattern Recognition**: Use wave diagrams to predict trends
4. **Automated Analysis**: "One Step Analysis" applies all rules automatically

See `VLA_ANALYSIS_SUMMARY.md` for complete methodology documentation.

## Data Sources

Actual lottery results are maintained in separate scraper projects:

- **Fantasy 5**: `C:\Users\Minis\CascadeProjects\c5_scrapper\data\raw\CA5_raw_data.txt`
- **Daily 4**: `C:\Users\Minis\CascadeProjects\CA-4_scrapper\data\raw\CA_Daily_4_dat.csv`

## Requirements

- Python 3.7+
- No external dependencies (uses standard library only)

## License

Personal use project for lottery analysis research.

## Disclaimer

This project is for educational and research purposes only. Lottery games are games of chance. Past performance does not guarantee future results. Please gamble responsibly.
