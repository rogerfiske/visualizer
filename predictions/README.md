# Predictions Directory

Place VLA-generated prediction files here for backtesting.

## File Naming Convention

```
{game}_{date}.{ext}
```

Examples:
- `fantasy5_2025-11-01.csv`
- `daily4_2025-11-01.txt`

## Supported Formats

### CSV (comma-separated)
```csv
1,5,12,23,39
3,8,15,28,35
7,14,21,30,38
```

### TXT (space-separated)
```
1 5 12 23 39
3 8 15 28 35
7 14 21 30 38
```

## How to Export from VLA

1. Open Visual Lottery Analyser
2. Select game and set date
3. Run "One Step Analysis" or Tickets Generator
4. Use Export/Print menu to save as CSV or TXT
5. Save file to this directory with proper naming

## Usage

Once files are here, run backtest:

```bash
# Single day
python ../backtest.py --game fantasy5 --predictions fantasy5_2025-11-01.csv --date 2025-11-01

# Batch (all files in directory)
python ../batch_backtest.py --game fantasy5 --predictions-dir . --start-date 2025-11-01 --end-date 2025-11-30
```
