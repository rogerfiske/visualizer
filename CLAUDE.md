# Project: VLA Visualizer - Custom Lottery Prediction System

## Quick Summary
Evolved from VLA backtesting framework to building a custom prediction system using EDA-derived optimal ranges and bias-corrected methodology.

## Status (as of 2026-01-01)
- ✅ VLA documentation audited (273 English help files indexed)
- ✅ Backtest scripts created (`backtest.py`, `batch_backtest.py`)
- ✅ **EDA Complete**: 11,664 draws analyzed (1992-2025)
- ✅ **Optimal Ranges Identified**: 85% capture recommended
- ✅ **VLA Bias Quantified**: 2.5x interior bias confirmed
- ❌ Alternative matrix design (NEXT)
- ❌ Historical bias impact quantification
- ❌ Custom prediction system

## Target Games
| Game | Format | Pool |
|------|--------|------|
| CA Fantasy 5 | 5 numbers | 1-39 |
| CA Daily 4 | 4 digits | 0-9 each |

## Key Findings

### Optimal 85% Capture Ranges
```
N_1 (Lowest):  1-13   (67% pool reduction)
N_2:           3-21   (51% pool reduction)
N_3 (Middle):  9-29   (46% pool reduction)
N_4:          18-36   (51% pool reduction)
N_5 (Highest): 28-39  (69% pool reduction)
```

### VLA Contact Bias
```
Interior numbers (18): 7.9 avg contacts → 2.5x OVERWEIGHTED
Edge numbers (16):     5.1 avg contacts → 1.6x
Corner numbers (5):    3.2 avg contacts → UNDERWEIGHTED
  └─ Corners: 1, 6, 36, 37, 39 (conflicts with N_1/N_5 optimal ranges)
```

### VLA Matrix Layout
```
   1   7  13  19  25  31  37
   2   8  14  20  26  32  38
   3   9  15  21  27  33  39
   4  10  16  22  28  34  --
   5  11  17  23  29  35  --
   6  12  18  24  30  36  --
```

## Key Files
| File | Purpose |
|------|---------|
| `data/CA5_Optimal_Range_Analysis.md` | **READ FIRST** - Optimal ranges |
| `data/VLA_Contact_Bias_Analysis.md` | **READ FIRST** - Bias analysis |
| `data/CA5_EDA_Results.md` | Full EDA statistics |
| `eda_optimal_range.py` | Generates optimal range analysis |
| `analysis_contact_bias.py` | Quantifies matrix bias |
| `Start_Here_Tomorrow_2026-01-01.md` | Session continuation guide |

## Data Files
| File | Description |
|------|-------------|
| `data/raw/CA5_date.csv` | 11,664 historical draws (1992-2025) |
| `data/num_matrix/vis_std_v1.csv` | VLA standard 6x7 matrix |
| `data/charts/*.png` | 50 visualization charts |

## External Data Sources
```
Fantasy 5: C:\Users\Minis\CascadeProjects\c5_scrapper\data\raw\CA5_raw_data.txt
Daily 4:   C:\Users\Minis\CascadeProjects\CA-4_scrapper\data\raw\CA_Daily_4_dat.csv
```
Data current through: **12/31/2025**

## VLA Software
```
Location: C:\Program Files\Sprintbit Software\Visual Lottery Analyser\VisualLotteryAnalyser.exe
Help docs: docs/ (6,666 files, excluded from git)
```
Cannot be controlled programmatically - user runs GUI manually.

## How VLA Works
1. **Grid Layout**: Numbers 1-39 in 6x7 matrix (columns go down: 1-6, 7-12, etc.)
2. **Mark Draws**: Recent draw numbers marked on grid
3. **Contact Analysis**: Numbers adjacent (8-directional) to draws = "in contact"
4. **Generate Tickets**: Algorithm favors contact numbers
5. **Apply Filters**: User-selected filters refine output
6. **Export**: Save tickets to CSV/TXT

## Tomorrow's Priorities
1. **Alternative Matrix Design**: Reduce/eliminate positional bias
2. **Historical Bias Impact**: Quantify accuracy loss from VLA bias
3. **Custom Prediction System**: Build automated, optimized predictor

## Commands
```bash
# Optimal range analysis
python eda_optimal_range.py

# VLA bias analysis
python analysis_contact_bias.py

# Basic EDA
python eda_ca5.py
```

## Architecture Vision
```
Data → Bias-Corrected Matrix → Position Filters → Predictions → Backtesting → Optimization
```

## Next Session
Read `Start_Here_Tomorrow_2026-01-01.md` for immediate next steps.

## Session History
| Date | Summary |
|------|---------|
| 2025-12-31 | Initial setup, VLA docs audit, backtest framework |
| 2026-01-01 | EDA complete, optimal ranges, VLA bias quantified |
