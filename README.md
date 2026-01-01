# VLA Visualizer - Lottery Analysis & Prediction System

A comprehensive lottery analysis framework that started as a backtesting tool for Visual Lottery Analyser (VLA) predictions and is evolving into a custom prediction system with bias-corrected methodology.

## Project Evolution

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 1**: VLA Documentation | ✅ Complete | Audit and index VLA help files |
| **Phase 2**: Backtesting Framework | ✅ Complete | Score VLA predictions against results |
| **Phase 3**: Exploratory Data Analysis | ✅ Complete | Analyze 33 years of historical data |
| **Phase 4**: Custom Prediction System | 🔄 In Progress | Build bias-corrected predictor |

## Key Discoveries

### 1. Optimal Prediction Ranges
Analysis of 11,664 draws (1992-2025) identified optimal number ranges for each sorted position:

| Position | 85% Capture Range | Pool Reduction |
|----------|-------------------|----------------|
| N_1 (Lowest) | 1-13 | 67% |
| N_2 | 3-21 | 51% |
| N_3 (Middle) | 9-29 | 46% |
| N_4 | 18-36 | 51% |
| N_5 (Highest) | 28-39 | 69% |

### 2. VLA Structural Bias
VLA's contact-based methodology has inherent positional bias:
- **Interior numbers**: 2.5x more likely to be flagged as "in contact"
- **Corner numbers** (1, 6, 36, 37, 39): Systematically underweighted
- **Impact**: Conflicts with optimal N_1 and N_5 predictions

## Supported Games

| Game | Format | Data Source | Historical Data |
|------|--------|-------------|-----------------|
| **CA Fantasy 5** | 5 numbers from 1-39 | `CA5_date.csv` | 11,664 draws (1992-2025) |
| **CA Daily 4** | 4 digits (0-9 each) | `CA_Daily_4_dat.csv` | TBD |

## Project Structure

```
visualizer/
├── README.md                      # This file
├── CLAUDE.md                      # Claude Code context
├── VLA_ANALYSIS_SUMMARY.md        # VLA methodology reference
│
├── Analysis Scripts/
│   ├── eda_ca5.py                 # Basic EDA statistics
│   ├── eda_charts.py              # Distribution visualizations
│   ├── eda_optimal_range.py       # Optimal capture range analysis
│   └── analysis_contact_bias.py   # VLA matrix bias quantification
│
├── Backtesting Scripts/
│   ├── backtest.py                # Single-day prediction scorer
│   └── batch_backtest.py          # Multi-day walk-forward analysis
│
├── data/
│   ├── raw/                       # Historical lottery data
│   │   ├── CA5_date.csv           # 11,664 Fantasy 5 draws
│   │   └── CA5_raw_data.txt       # Alternative format
│   ├── num_matrix/                # Matrix layouts
│   │   └── vis_std_v1.csv         # VLA standard 6x7 matrix
│   ├── charts/                    # Generated visualizations (50 PNGs)
│   ├── CA5_EDA_Results.md         # EDA statistics
│   ├── CA5_Optimal_Range_Analysis.md  # Optimal ranges with trade-offs
│   └── VLA_Contact_Bias_Analysis.md   # Bias analysis
│
├── docs/                          # VLA help documentation
│   └── INDEX.md                   # Categorized index of 273 files
│
├── predictions/                   # VLA prediction exports
│
└── Session Documentation/
    ├── Session_Summary_*.md       # Session recaps
    └── Start_Here_Tomorrow_*.md   # Continuation guides
```

## Quick Start

### Run EDA Analysis
```bash
# Basic statistics
python eda_ca5.py

# Optimal range analysis with charts
python eda_optimal_range.py

# VLA bias analysis
python analysis_contact_bias.py
```

### Run Backtests
```bash
# Single day
python backtest.py --game fantasy5 --predictions predictions/fantasy5_2025-11-01.csv --date 2025-11-01

# Batch (multiple days)
python batch_backtest.py --game fantasy5 --predictions-dir ./predictions --start-date 2025-11-01 --end-date 2025-11-30
```

## How VLA Works

Visual Lottery Analyser uses a grid-based contact analysis:

### Matrix Layout
```
   Col1  Col2  Col3  Col4  Col5  Col6  Col7
   ────────────────────────────────────────
R1:  1     7    13    19    25    31    37
R2:  2     8    14    20    26    32    38
R3:  3     9    15    21    27    33    39
R4:  4    10    16    22    28    34    --
R5:  5    11    17    23    29    35    --
R6:  6    12    18    24    30    36    --
```

### Process
1. Mark recent draw numbers on grid
2. Identify "contact" numbers (8-directional adjacency)
3. Apply user-selected filters (hot/cold, odd/even, etc.)
4. Generate tickets favoring contact numbers

### The Bias Problem
- Interior cells have 8 neighbors
- Corner cells have only 3 neighbors
- This creates 2.5x bias favoring mid-range numbers

## Analysis Results

### Key Documentation
| Document | Description |
|----------|-------------|
| [CA5_EDA_Results.md](data/CA5_EDA_Results.md) | Full statistical analysis |
| [CA5_Optimal_Range_Analysis.md](data/CA5_Optimal_Range_Analysis.md) | Capture rate trade-offs |
| [VLA_Contact_Bias_Analysis.md](data/VLA_Contact_Bias_Analysis.md) | Structural bias deep-dive |

### Generated Charts
- Distribution charts for each position (N_1 through N_5)
- Optimal range visualizations with capture zones
- Contact bias heatmap and bar charts
- Summary charts by time period

## Roadmap

### Next Steps
1. **Alternative Matrix Design**: Layouts that reduce positional bias
2. **Historical Bias Impact**: Quantify accuracy loss from VLA bias
3. **Custom Prediction System**: Automated, optimized predictor

### Future Vision
```
Data → Bias-Corrected Matrix → Position Filters → Optimized Predictions → Backtesting → Parameter Tuning
```

## Requirements

- Python 3.7+
- matplotlib
- numpy

## Data Sources

| Data | Location | Updated Through |
|------|----------|-----------------|
| Fantasy 5 (project) | `data/raw/CA5_date.csv` | 12/31/2025 |
| Fantasy 5 (external) | `C:\Users\Minis\CascadeProjects\c5_scrapper\data\raw\` | 12/30/2025 |
| Daily 4 (external) | `C:\Users\Minis\CascadeProjects\CA-4_scrapper\data\raw\` | 12/30/2025 |

## VLA Software

```
Location: C:\Program Files\Sprintbit Software\Visual Lottery Analyser\VisualLotteryAnalyser.exe
```
GUI-based application - cannot be controlled programmatically.

## License

Personal use project for lottery analysis research.

## Disclaimer

This project is for educational and research purposes only. Lottery games are games of chance. Past performance does not guarantee future results. Please gamble responsibly.

---

*Last updated: January 1, 2026*
