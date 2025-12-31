# Project: VLA Visualizer

## Purpose
Backtesting framework for Visual Lottery Analyser (VLA) predictions against California lottery results.

## Target Games
- **CA Fantasy 5**: 5 numbers from 1-39 (standard lotto)
- **CA Daily 4**: 4 digits 0-9 each (pick-4 game)

## Key Files
- `backtest.py` - Single-day prediction scorer
- `batch_backtest.py` - Multi-day walk-forward analysis
- `VLA_ANALYSIS_SUMMARY.md` - Complete VLA methodology documentation
- `docs/INDEX.md` - Index of 273 English VLA help files

## External Data Sources
- Fantasy 5: `C:\Users\Minis\CascadeProjects\c5_scrapper\data\raw\CA5_raw_data.txt`
- Daily 4: `C:\Users\Minis\CascadeProjects\CA-4_scrapper\data\raw\CA_Daily_4_dat.csv`

## VLA Software
- Location: `C:\Program Files\Sprintbit Software\Visual Lottery Analyser\VisualLotteryAnalyser.exe`
- Help files copied to: `docs/` directory
- Cannot be controlled programmatically - user runs GUI manually

## Workflow
1. User sets VLA to historical date
2. User generates predictions via "One Step Analysis"
3. User exports predictions to CSV/TXT
4. We score predictions against actual results using backtest scripts

## Prediction File Convention
- `fantasy5_YYYY-MM-DD.csv` or `.txt`
- `daily4_YYYY-MM-DD.csv` or `.txt`
- Place in `predictions/` directory

## VLA Core Concepts
- **Ticket View**: Grid representation of lottery numbers
- **Contact/Outside**: Numbers adjacent to vs distant from drawn numbers
- **Hot/Cold**: Recently drawn vs not drawn numbers
- **Lines/Blocks**: Horizontal, vertical, diagonal groupings
- **Balance**: Good tickets mix all number types, not all one category
