# Project: VLA Visualizer

## Quick Summary
Backtesting framework for Visual Lottery Analyser (VLA) predictions against California lottery results.

## Status (as of 2025-12-31)
- ✅ VLA documentation audited (273 English help files indexed)
- ✅ Backtest scripts created (`backtest.py`, `batch_backtest.py`)
- ✅ Project documentation complete
- ✅ GitHub repo: https://github.com/rogerfiske/visualizer
- ❌ Waiting for user to generate VLA predictions

## Target Games
| Game | Format | Pool |
|------|--------|------|
| CA Fantasy 5 | 5 numbers | 1-39 |
| CA Daily 4 | 4 digits | 0-9 each |

## Key Files
| File | Purpose |
|------|---------|
| `backtest.py` | Single-day prediction scorer |
| `batch_backtest.py` | Multi-day walk-forward analysis |
| `VLA_ANALYSIS_SUMMARY.md` | Complete VLA methodology |
| `docs/INDEX.md` | Index of 273 VLA help files |
| `Start_Here_Tomorrow_2025-12-31.md` | Session continuation guide |

## External Data Sources
```
Fantasy 5: C:\Users\Minis\CascadeProjects\c5_scrapper\data\raw\CA5_raw_data.txt
Daily 4:   C:\Users\Minis\CascadeProjects\CA-4_scrapper\data\raw\CA_Daily_4_dat.csv
```
Data current through: **12/30/2025**

## VLA Software
```
Location: C:\Program Files\Sprintbit Software\Visual Lottery Analyser\VisualLotteryAnalyser.exe
Help docs: docs/ (6,666 files, excluded from git)
```
Cannot be controlled programmatically - user runs GUI manually.

## Backtesting Workflow
1. User sets VLA to historical date (starting 11/1/2025)
2. User runs "One Step Analysis" in VLA
3. User exports predictions to `predictions/{game}_{date}.csv`
4. We run `backtest.py` to score against actual results
5. Walk forward day by day, repeat

## Prediction File Format
```csv
# fantasy5_2025-11-01.csv
1,5,12,23,39
3,8,15,28,35
```

## VLA Core Concepts
- **Ticket View**: Grid representation of lottery numbers
- **Contact/Outside**: Numbers adjacent to vs distant from drawn numbers
- **Hot/Cold**: Recently drawn vs not drawn numbers
- **Golden Rule**: Good tickets MIX all number types, never all one category

## Commands
```bash
# Single day backtest
python backtest.py --game fantasy5 --predictions predictions/fantasy5_2025-11-01.csv --date 2025-11-01

# Batch backtest
python batch_backtest.py --game fantasy5 --predictions-dir ./predictions --start-date 2025-11-01 --end-date 2025-11-30
```

## Next Session
Read `Start_Here_Tomorrow_2025-12-31.md` for immediate next steps.
