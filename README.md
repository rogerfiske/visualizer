# VLA Visualizer - Lottery Analysis & Prediction System

A comprehensive lottery analysis framework that started as a backtesting tool for Visual Lottery Analyser (VLA) predictions and is evolving into a custom prediction system with bias-corrected methodology.

## Project Evolution

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 1**: VLA Documentation | ✅ Complete | Audit and index VLA help files |
| **Phase 2**: Backtesting Framework | ✅ Complete | Score VLA predictions against results |
| **Phase 3**: Exploratory Data Analysis | ✅ Complete | Analyze 33 years of historical data |
| **Phase 4**: Custom Prediction System | ✅ Complete | Bias-corrected predictor with CLI |
| **Phase 5**: Filter System | ✅ Complete | 52 filters implemented (tuning needed) |

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

### 3. Filter System Performance
52 statistical filters implemented but currently **reduce** performance:

| Configuration | Avg Best Match | Hit Rate (3+) |
|---------------|----------------|---------------|
| **No filters** | 2.25 | **30.8%** |
| With filters | 2.05 | 24.2% |

Filters need tuning - currently too aggressive.

## Supported Games

| Game | Format | Data Source | Historical Data |
|------|--------|-------------|-----------------|
| **CA Fantasy 5** | 5 numbers from 1-39 | `CA5_date.csv` | 11,663 draws (1992-2026) |
| **CA Daily 4** | 4 digits (0-9 each) | `CA_Daily_4_dat.csv` | TBD |

## Project Structure

```
visualizer/
├── README.md                      # This file
├── CLAUDE.md                      # Claude Code context
├── predict.py                     # Main CLI for predictions
├── validate_system.py             # System validation (12 tests)
├── visualize_matrix.py            # Matrix visualization tool
│
├── src/
│   ├── matrix/                    # Contact matrix implementations
│   │   ├── base.py                # ContactMatrix interface
│   │   ├── numerical_proximity.py # Unbiased k=3 window (recommended)
│   │   ├── weighted_adjacency.py  # VLA with bias correction
│   │   └── csv_matrix.py          # Generic CSV matrix loader
│   │
│   └── predictor/                 # Prediction pipeline
│       ├── predictor.py           # CA5Predictor main class
│       ├── filters.py             # 52 filter functions
│       ├── position_filter.py     # 85% capture ranges
│       ├── ticket_generator.py    # Generation strategies
│       └── data_loader.py         # DrawHistory class
│
├── Analysis Scripts/
│   ├── eda_ca5.py                 # Basic EDA statistics
│   ├── eda_optimal_range.py       # Optimal capture range analysis
│   └── analysis_bias_comparison.py # Matrix bias comparison
│
├── data/
│   ├── raw/                       # Historical lottery data
│   │   └── CA5_date.csv           # 11,663 Fantasy 5 draws (1992-2026)
│   ├── num_matrix/                # Matrix layouts and neighbor CSVs
│   └── charts/                    # Generated visualizations (50 PNGs)
│
├── docs/                          # VLA help documentation
│   ├── INDEX.md                   # Categorized index of 273 files
│   └── FILTER_STRATEGY.md         # Filter thresholds and rationale
│
├── imported_docs/                 # VLA reference documentation
│   └── FILTERING.txt              # 52 filter definitions
│
└── Session Documentation/
    ├── Session_Summary_*.md       # Session recaps
    └── Start_Here_Tomorrow_*.md   # Continuation guides
```

## Quick Start

### Generate Predictions
```bash
# Generate 50 predictions for tomorrow
python predict.py --tickets 50

# Generate for specific date
python predict.py --date 2026-01-03 --tickets 50
```

### Run Backtests
```bash
# Backtest specific date
python predict.py --backtest --date 2025-12-30

# Backtest date range
python predict.py --backtest --start 2025-01-01 --end 2025-12-31 --tickets 50
```

### Python API
```python
from src.predictor import CA5Predictor

# Create predictor (best configuration)
predictor = CA5Predictor(
    matrix_type='proximity',
    capture_level='85',
    use_filters=False  # Filters currently reduce performance
)

# Generate predictions
result = predictor.predict(num_tickets=50)
for ticket in result['tickets'][:10]:
    print(ticket)
```

### Validate System
```bash
python validate_system.py        # Quick (100 days)
python validate_system.py --full # Full (500 days)
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
1. **Filter Tuning**: Test individual filters to find which improve performance
2. **Daily 4 Support**: Extend system to Daily 4 game
3. **Automated Daily Predictions**: Scheduled prediction generation

### Future Vision
```
Data → Bias-Corrected Matrix → Position Filters → [Tuned Filters] → Predictions → Tracking
```

## Requirements

- Python 3.7+
- matplotlib
- numpy

## Data Sources

| Data | Location | Updated Through |
|------|----------|-----------------|
| Fantasy 5 (project) | `data/raw/CA5_date.csv` | 1/1/2026 |
| Fantasy 5 (external) | `C:\Users\Minis\CascadeProjects\c5_scrapper\data\raw\` | 1/1/2026 |
| Daily 4 (external) | `C:\Users\Minis\CascadeProjects\CA-4_scrapper\data\raw\` | TBD |

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

*Last updated: January 2, 2026*
