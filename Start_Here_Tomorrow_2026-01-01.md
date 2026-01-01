# Start Here Tomorrow

**Last Session**: January 1, 2026
**Project**: VLA Visualizer - Custom Lottery Prediction System
**Repo**: https://github.com/rogerfiske/visualizer

---

## Quick Context (60 seconds)

This project is evolving from **backtesting VLA predictions** to **building our own prediction system** that:
1. Uses EDA-derived optimal ranges for each number position
2. Eliminates the structural bias found in VLA's contact methodology
3. Fully automates prediction generation and optimization

**Key Discovery This Session**: VLA's grid-based contact analysis has a **2.5x bias** favoring interior numbers over corner numbers - this works against optimal predictions for N_1 and N_5 positions.

---

## Current Status

| Item | Status |
|------|--------|
| Historical data (11,664 draws) | ✅ Loaded and analyzed |
| EDA complete | ✅ All statistics calculated |
| Optimal ranges identified | ✅ 85% capture recommended |
| VLA bias quantified | ✅ 2.5x interior bias confirmed |
| Alternative matrix design | ❌ **Next step** |
| Bias impact quantification | ❌ Planned |
| Custom prediction system | ❌ Planned |

---

## Tomorrow's Three Priorities

### Priority 1: Alternative Matrix Layouts

**Goal**: Design matrix that reduces/eliminates positional bias

**Approaches to explore**:
1. **Weighted adjacency**: Give corner/edge numbers bonus contact points
2. **Circular layout**: Wrap edges to eliminate corners
3. **Variable neighborhood**: Different contact definitions by position
4. **Non-geometric**: Pure frequency/recency-based (no grid)

**Key constraint**: New matrix should not disadvantage numbers 1, 6, 36, 37, 39

### Priority 2: Quantify Historical Bias Impact

**Goal**: Measure how much VLA's bias affected prediction accuracy

**Analysis approach**:
1. Score historical draws against VLA-style contact predictions
2. Score same draws against position-optimized predictions
3. Compare accuracy rates
4. Identify patterns in misses (are corners under-predicted?)

### Priority 3: Build Custom Prediction System

**Goal**: Automated predictor using optimized methodology

**Components needed**:
1. **Data loader**: Read CA5_date.csv
2. **Matrix engine**: Configurable grid layout with bias correction
3. **Contact analyzer**: Identify in-contact numbers with weighting
4. **Position filter**: Apply optimal range constraints per N_i
5. **Ticket generator**: Create N tickets meeting all criteria
6. **Backtester**: Score predictions against actual results
7. **Optimizer**: Tune parameters for best accuracy

---

## Key Files to Know

### Documentation
| File | Description |
|------|-------------|
| `data/CA5_EDA_Results.md` | Full EDA statistics |
| `data/CA5_Optimal_Range_Analysis.md` | **Optimal ranges - READ THIS** |
| `data/VLA_Contact_Bias_Analysis.md` | **Bias analysis - READ THIS** |
| `VLA_ANALYSIS_SUMMARY.md` | How VLA works |

### Analysis Scripts
| File | Description |
|------|-------------|
| `eda_optimal_range.py` | Generates optimal range analysis |
| `analysis_contact_bias.py` | Quantifies matrix bias |

### Data
| File | Description |
|------|-------------|
| `data/raw/CA5_date.csv` | 11,664 historical draws |
| `data/num_matrix/vis_std_v1.csv` | VLA standard matrix |
| `data/charts/*.png` | 50 visualization charts |

---

## Critical Numbers to Remember

### Optimal 85% Capture Ranges (Recommended)
```
N_1 (Lowest):  1-13   (span 13, 67% pool reduction)
N_2:           3-21   (span 19, 51% pool reduction)
N_3 (Middle):  9-29   (span 21, 46% pool reduction)
N_4:          18-36   (span 19, 51% pool reduction)
N_5 (Highest): 28-39  (span 12, 69% pool reduction)
```

### VLA Bias Factors
```
Corner numbers (1,6,36,37,39):  3.2 avg contacts → UNDERWEIGHTED
Edge numbers (16 total):        5.1 avg contacts → Slightly underweighted
Interior numbers (18 total):    7.9 avg contacts → OVERWEIGHTED (2.5x)
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

---

## How VLA Works (Reference)

### Step-by-Step Operation
1. **Load game**: Select CA Fantasy 5 (or other game)
2. **Set date**: Can be current or historical (for backtesting)
3. **Run analysis**: "One Step Analysis" or manual
4. **View matrix**: Numbers displayed on grid with draw markers
5. **Generate tickets**: Algorithm creates predictions based on:
   - Contact numbers (adjacent to recent draws)
   - Hot/cold analysis
   - User-selected filters
6. **Export**: Save tickets to CSV/TXT

### VLA Contact Definition
- 8-directional adjacency (including diagonals)
- Most recent draw marked, optionally previous day
- Numbers touching marked cells = "in contact"
- Algorithm favors contact numbers (exact weighting unknown)

### VLA Filters Available
- Contact/Outside ratio
- Hot/Cold balance
- Odd/Even distribution
- Line spread (horizontal, vertical, diagonal)
- Block distribution (1-10, 11-20, etc.)
- Include/Exclude specific numbers

---

## Conversation Starters

1. "Let's design an alternative matrix layout that eliminates the corner bias"
2. "Quantify how VLA's bias affected historical predictions"
3. "Start building the custom prediction system architecture"
4. "Compare VLA contact scoring vs our optimal range filtering"
5. "Test a circular matrix layout"

---

## Commands Reference

```bash
# View optimal range analysis
python eda_optimal_range.py

# View bias analysis
python analysis_contact_bias.py

# Run basic EDA
python eda_ca5.py

# Generate charts (already done, but for reference)
python eda_charts.py
```

---

## Session History

| Date | Summary |
|------|---------|
| 2025-12-31 | Initial setup: VLA docs audit, backtest framework, GitHub repo |
| 2026-01-01 | EDA complete, optimal ranges identified, VLA bias quantified |

---

## Don't Forget

- VLA help files in `docs/` (6,666 files, excluded from git)
- `docs/INDEX.md` has categorized access to 273 English help topics
- Historical data goes back to 1992 (33+ years)
- Numbers are PRE-SORTED in data (N_1 < N_2 < N_3 < N_4 < N_5)
- 39-day analysis window matches pool size (1-39)

---

## Architecture Vision (For Custom System)

```
┌─────────────────────────────────────────────────────────┐
│                    DATA LAYER                           │
│  CA5_date.csv → DataLoader → Processed Draw History     │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   MATRIX ENGINE                         │
│  Configurable Layout → Bias-Corrected Contact Scoring   │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                  PREDICTION LAYER                       │
│  Position Filters → Contact Analysis → Ticket Generator │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                  VALIDATION LAYER                       │
│  Backtester → Accuracy Metrics → Parameter Optimizer    │
└─────────────────────────────────────────────────────────┘
```

---

*Ready to build something better than VLA!*
