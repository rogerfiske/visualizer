# Start Here Tomorrow

**Last Session**: December 31, 2025
**Project**: VLA Visualizer - Lottery Backtesting Framework
**Repo**: https://github.com/rogerfiske/visualizer

---

## Quick Context (30 seconds)

This project backtests **Visual Lottery Analyser (VLA)** predictions against actual California lottery results for:
- **CA Fantasy 5** (5 numbers from 1-39)
- **CA Daily 4** (4 digits, each 0-9)

VLA is a GUI-based lottery analysis tool that uses geometric/visual pattern analysis. We cannot control it programmatically - the user runs it manually and exports predictions.

---

## Current Status

| Item | Status |
|------|--------|
| VLA documentation audit | ✅ Complete |
| Backtest scripts | ✅ Complete |
| Project documentation | ✅ Complete |
| GitHub repo | ✅ Pushed |
| **VLA predictions** | ❌ Not yet generated |
| **Backtesting** | ❌ Waiting for predictions |

---

## Immediate Next Steps

### Step 1: User Generates VLA Predictions

User needs to:
1. Open Visual Lottery Analyser
2. Select **CA Fantasy 5** game
3. Set analysis date to **November 1, 2025**
4. Run "One Step Analysis"
5. Export 20+ tickets to `predictions/fantasy5_2025-11-01.csv`
6. Repeat for **CA Daily 4** → `predictions/daily4_2025-11-01.csv`

### Step 2: Run Backtest

Once files are in `predictions/`:
```bash
cd C:\Users\Minis\CascadeProjects\visualizer

# Fantasy 5
python backtest.py --game fantasy5 --predictions predictions/fantasy5_2025-11-01.csv --date 2025-11-01

# Daily 4
python backtest.py --game daily4 --predictions predictions/daily4_2025-11-01.csv --date 2025-11-01
```

### Step 3: Walk Forward

Repeat for subsequent dates (11/2, 11/3, etc.) to build statistical profile.

---

## Key Files to Know

| File | Purpose |
|------|---------|
| `backtest.py` | Score single day predictions |
| `batch_backtest.py` | Score multiple days at once |
| `VLA_ANALYSIS_SUMMARY.md` | Complete VLA methodology reference |
| `docs/INDEX.md` | Index of 273 VLA help files |
| `CLAUDE.md` | Quick project context |

---

## Data Locations

```
# Actual lottery results (updated through 12/30/2025)
Fantasy 5: C:\Users\Minis\CascadeProjects\c5_scrapper\data\raw\CA5_raw_data.txt
Daily 4:   C:\Users\Minis\CascadeProjects\CA-4_scrapper\data\raw\CA_Daily_4_dat.csv

# VLA software
C:\Program Files\Sprintbit Software\Visual Lottery Analyser\VisualLotteryAnalyser.exe

# VLA help docs (local copy)
C:\Users\Minis\CascadeProjects\visualizer\docs\
```

---

## VLA Key Concepts (Quick Reference)

**The Golden Rule**: Good predictions mix number types. Never all one category.

| Concept | Description |
|---------|-------------|
| Contact/Outside | Adjacent to drawn numbers vs distant |
| Hot/Cold | Recently drawn vs not recent |
| Lines | Horizontal, vertical, slant positions in grid |
| Blocks | Groups of 10 (1-10, 11-20, etc.) |
| One Step Analysis | VLA's automated prediction workflow |

---

## Prediction File Format

**CSV** (comma-separated):
```
1,5,12,23,39
3,8,15,28,35
7,14,21,30,38
```

**Naming**: `{game}_{YYYY-MM-DD}.csv`
- `fantasy5_2025-11-01.csv`
- `daily4_2025-11-01.csv`

---

## Possible Conversation Starters

- "I have VLA predictions for 11/1/2025, let's backtest them"
- "Let's run the batch backtest for November"
- "Help me understand this VLA analysis method: [method name]"
- "Let's improve the backtest scoring system"

---

## Session History

| Date | Summary |
|------|---------|
| 2025-12-31 | Initial setup: VLA docs audit, backtest framework, GitHub repo |

---

## Don't Forget

- VLA help files are in `docs/` locally but excluded from git (too large)
- `docs/INDEX.md` provides categorized access to all 273 English help topics
- Lottery data scraper projects are separate repos (`c5_scrapper`, `CA-4_scrapper`)
