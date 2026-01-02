# Start Here Tomorrow - January 2, 2026

## Quick Context
You built a complete lottery prediction system for CA Fantasy 5. Today you added a comprehensive 52-filter system, but discovered that **filters currently hurt performance**. The unfiltered predictor performs better.

---

## Immediate Commands

### Generate Today's Predictions
```bash
python -c "
import sys; sys.path.insert(0, '.')
from datetime import datetime
from src.predictor import CA5Predictor

p = CA5Predictor(matrix_type='proximity', capture_level='85', use_filters=False)
r = p.predict(num_tickets=50)
print(f'Predictions for {r[\"target_date_str\"]}')
print(f'Based on: {r[\"previous_draws\"][0]}')
for i, t in enumerate(r['tickets'][:10], 1):
    print(f'{i:2d}. {t}')
"
```

### Run Quick Backtest
```bash
python -c "
import sys; sys.path.insert(0, '.')
from datetime import datetime
from src.predictor import CA5Predictor

p = CA5Predictor(use_filters=False)
r = p.backtest_range(datetime(2025,12,1), datetime(2025,12,30), num_tickets=50)
print(f'Dec 2025: avg={r[\"summary\"][\"avg_best_match\"]:.2f}, hit={100*r[\"summary\"][\"days_with_3plus_match\"]/r[\"days_tested\"]:.1f}%')
"
```

---

## Current Best Configuration
```python
from src.predictor import CA5Predictor

predictor = CA5Predictor(
    matrix_type='proximity',   # Numerical proximity (unbiased)
    capture_level='85',        # 85% capture ranges
    use_filters=False          # Filters OFF (better performance)
)
```

**Performance**: 2.25 avg best match, 30.8% hit rate (3+ matches)

---

## System Architecture
```
src/
├── matrix/
│   ├── base.py              # ContactMatrix interface
│   ├── numerical_proximity.py  # Unbiased k=3 window
│   ├── weighted_adjacency.py   # VLA grid with bias correction
│   └── csv_matrix.py        # Generic CSV matrix loader
│
├── predictor/
│   ├── predictor.py         # CA5Predictor main class
│   ├── filters.py           # 52 filter functions + TicketFilter
│   ├── position_filter.py   # 85% capture ranges
│   ├── ticket_generator.py  # Generation strategies
│   └── data_loader.py       # DrawHistory class
```

---

## Key Files to Read

| Priority | File | Why |
|----------|------|-----|
| 1 | `CLAUDE.md` | Project overview and status |
| 2 | `src/predictor/predictor.py` | Main prediction logic |
| 3 | `src/predictor/filters.py` | Filter implementation |
| 4 | `docs/FILTER_STRATEGY.md` | Filter thresholds and rationale |
| 5 | `data/CA5_Optimal_Range_Analysis.md` | Position ranges |

---

## The Filter Problem

Filters were implemented correctly and validated against historical data (30.5% pass rate), but they **reduce prediction accuracy**:

| Config | Hit Rate |
|--------|----------|
| No filters | 35.4% |
| With filters | 23-24% |

**Possible solutions to explore:**
1. Use only 1-2 high-impact filters (odd/even, sum range)
2. Widen thresholds to reject fewer tickets
3. Make filters advisory (scoring) rather than eliminative
4. Test time-period specific effectiveness

---

## Data Status

| File | Records | Through |
|------|---------|---------|
| `data/raw/CA5_date.csv` | 11,663 | 1/1/2026 |
| `data/raw/CA5_raw_data.txt` | 11,663 | 1/1/2026 |

**To add new results**: Append to CA5_date.csv in format:
```
M/D/YYYY,N_1,N_2,N_3,N_4,N_5
1/2/2026,X,X,X,X,X
```

---

## Unfinished Business

### Should Do
- [ ] Test individual filters to find which help
- [ ] Try filters as scoring factors instead of eliminators
- [ ] Compare matrix types (proximity vs weighted) with more data

### Could Do
- [ ] Implement Daily 4 prediction
- [ ] Add prediction logging/tracking
- [ ] Create automated daily prediction script

---

## Git Status
```
Latest: 75d7202 Add comprehensive ticket filter system with 52 filter functions
Branch: main (pushed to origin)
```

---

## Filter Usage Reference

```python
from src.predictor import CA5Predictor, FilterConfig

# Custom filter configuration
config = FilterConfig(
    odd_min=2, odd_max=3,      # Allow 2-3 odd numbers
    low_min=2, low_max=3,      # Allow 2-3 low (1-19)
    sum_min=50, sum_max=140,   # Sum between 50-140
    decades_min=3,             # Require 3+ decades
    consecutive_max=2,         # Max 2 consecutive
    prime_min=1, prime_max=3,  # 1-3 prime numbers
    ac_min=4, ac_max=6,        # AC value 4-6
    span_min=20, span_max=38,  # Span 20-38
    same_last_max=2            # Max 2 same as last draw
)

# Use with predictor
predictor = CA5Predictor(
    use_filters=True,
    filter_config=config
)
```

---

## Matrix Visualization
```bash
# Compare all matrix types
python visualize_matrix.py --compare

# Show specific matrix
python visualize_matrix.py --matrix proximity
```

---

*Ready to continue: January 3, 2026*
