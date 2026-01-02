# Project: VLA Visualizer - Custom Lottery Prediction System

## Quick Summary
Custom lottery prediction system with bias-corrected contact analysis and EDA-derived optimal position filtering. Replaces VLA's biased methodology with mathematically proven unbiased approaches.

## Status (as of 2026-01-02)
- ✅ VLA documentation audited (273 English help files indexed)
- ✅ Backtest scripts created (`backtest.py`, `batch_backtest.py`)
- ✅ **EDA Complete**: 11,664 draws analyzed (1992-2025)
- ✅ **Optimal Ranges Identified**: 85% capture recommended
- ✅ **VLA Bias Quantified**: 2.5x interior bias confirmed
- ✅ **Bias-Corrected Matrices**: 3 implementations (variance 5.0 → 0.0)
- ✅ **Custom Prediction System**: Full MVP with CLI
- ✅ **Validation Framework**: 12/12 tests passing

## Target Games
| Game | Format | Pool |
|------|--------|------|
| CA Fantasy 5 | 5 numbers | 1-39 |
| CA Daily 4 | 4 digits | 0-9 each |

## Quick Start Commands
```bash
# Generate 20 predictions for tomorrow
python predict.py

# Backtest on specific date
python predict.py --backtest --date 2025-12-30

# Backtest date range
python predict.py --backtest --start 2025-12-01 --end 2025-12-31

# Validate system (12 tests)
python validate_system.py

# Compare matrix bias
python analysis_bias_comparison.py
```

## Prediction System Architecture

### Matrix Implementations (`src/matrix/`)
| Matrix | Bias | Use Case |
|--------|------|----------|
| `VLAStandardMatrix` | 2.5x interior bias | Baseline comparison |
| `WeightedAdjacencyMatrix` | Corrected (0.0 variance) | VLA-compatible |
| `NumericalProximityMatrix` | None (inherently uniform) | **Recommended** |

### Predictor Components (`src/predictor/`)
| Component | Purpose |
|-----------|---------|
| `DrawHistory` | Loads 11,664 draws (1992-2025) |
| `PositionFilter` | 80/85/90% capture ranges |
| `TicketGenerator` | 4 strategies available |
| `CA5Predictor` | Main predictor + backtest |

### Generation Strategies
| Strategy | Description |
|----------|-------------|
| `balanced` | Weighted mix of contact + position (default) |
| `contact_first` | Prioritize high contact scores |
| `position_first` | Strict position compliance |
| `random` | Random within position constraints |

## Key Findings

### Optimal 85% Capture Ranges
```
N_1 (Lowest):  1-13   (67% pool reduction)
N_2:           3-21   (51% pool reduction)
N_3 (Middle):  9-29   (46% pool reduction)
N_4:          18-36   (51% pool reduction)
N_5 (Highest): 28-39  (69% pool reduction)
```

### Bias Elimination Proof
```
VLA Standard:     variance = 5.0  (corners disadvantaged)
Weighted Adj:     variance = 0.0  (corrected)
Num. Proximity:   variance = 0.0  (inherently uniform)
```

### VLA Matrix Layout (Reference)
```
   1   7  13  19  25  31  37
   2   8  14  20  26  32  38
   3   9  15  21  27  33  39
   4  10  16  22  28  34  --
   5  11  17  23  29  35  --
   6  12  18  24  30  36  --
```

## Key Files

### Prediction System
| File | Purpose |
|------|---------|
| `predict.py` | **Main CLI** - predictions & backtests |
| `validate_system.py` | System validation (12 tests) |
| `analysis_bias_comparison.py` | Bias elimination proof |

### Source Modules
| Directory | Purpose |
|-----------|---------|
| `src/matrix/` | Contact matrix implementations |
| `src/predictor/` | Prediction pipeline components |

### Analysis & Documentation
| File | Purpose |
|------|---------|
| `data/CA5_Optimal_Range_Analysis.md` | EDA optimal ranges |
| `data/VLA_Contact_Bias_Analysis.md` | Bias quantification |
| `_bmad-output/architecture/matrix-design-alternatives.md` | Architecture doc |
| `_bmad-output/test-strategy/validation-strategy.md` | Test strategy |

### Data Files
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

## VLA Software (Legacy Reference)
```
Location: C:\Program Files\Sprintbit Software\Visual Lottery Analyser\VisualLotteryAnalyser.exe
Help docs: docs/ (6,666 files, excluded from git)
```
No longer needed - custom system replaces VLA functionality.

## CLI Reference

### predict.py Options
| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--date` | YYYY-MM-DD | tomorrow | Target date |
| `--tickets` | 1-100+ | 20 | Tickets to generate |
| `--matrix` | proximity, weighted | proximity | Matrix type |
| `--capture` | 80, 85, 90 | 85 | Capture level % |
| `--strategy` | balanced, contact_first, position_first, random | balanced | Generation strategy |
| `--backtest` | flag | - | Run backtest mode |
| `--start/--end` | dates | - | Backtest range |
| `--output` | path | - | Export to file |

### validate_system.py Options
| Option | Description |
|--------|-------------|
| (none) | Quick validation (100 days) |
| `--full` | Full validation (500 days) |
| `--extended` | Extended (1000 days) |
| `--unit-only` | Unit tests only (fast) |

## Validation Status
```
Matrix Tests:      4/4 PASS
Filter Tests:      3/3 PASS
Integration Tests: 4/4 PASS
Statistical Tests: 1/1 PASS
─────────────────────────
Total:            12/12 PASS
```

## Future Enhancements
1. Daily 4 support (currently Fantasy 5 only)
2. Parameter optimization via extended backtesting
3. Ensemble methods (combine multiple strategies)
4. Real-time data fetching

## Session History
| Date | Summary |
|------|---------|
| 2025-12-31 | Initial setup, VLA docs audit, backtest framework |
| 2026-01-01 | EDA complete, optimal ranges, VLA bias quantified |
| 2026-01-02 | **Custom prediction system MVP**, bias-corrected matrices, validation framework, 12/12 tests passing |
