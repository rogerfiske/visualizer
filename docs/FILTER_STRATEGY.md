# CA Fantasy 5 Filter Strategy

**Based on analysis of 11,664 historical draws (1992-2025)**

---

## Key Findings: Repeat Combinations

| Pattern | Repeats | Verdict |
|---------|---------|---------|
| Exact 5-number | 125 (1.07%) | LOW IMPACT - most unique |
| 4-number subsets | 31.4% repeat | MINIMAL IMPACT |
| 3-number subsets | 100% repeat (avg 12.8x) | NOT USEFUL |

**Conclusion**: Filtering by "previously drawn" has minimal impact. Use statistical filters instead.

---

## Recommended Filters (Validated Against Historical Data)

### TIER 1: High-Impact Filters (Use Always)

#### 1. Odd/Even Ratio
```
Most Common:
  3:2 -> 34.8%
  2:3 -> 31.5%

Combined: 66.3% of all draws

FILTER: Allow only 2:3 and 3:2 ratios
REDUCTION: Eliminates 33.7% of candidates
```

#### 2. High/Low Ratio (1-19 low, 20-39 high)
```
Most Common:
  L2:H3 -> 33.7%
  L3:H2 -> 32.1%

Combined: 65.8% of all draws

FILTER: Allow only L2:H3 and L3:H2 ratios
REDUCTION: Eliminates 34.2% of candidates
```

#### 3. Sum Range
```
Optimal Range: 50-140
Captures: 93.6% of historical draws

Distribution:
   70-90:  23.1%
   90-110: 31.3%  <- Peak
  110-130: 23.5%

FILTER: Require sum between 50-140
REDUCTION: Eliminates 6.4% of candidates
```

#### 4. Decade Spread
```
Distribution:
  1 decade:  0.1% (AVOID)
  2 decades: 14.4%
  3 decades: 58.5% <- Most common
  4 decades: 26.9%

FILTER: Require 3+ decades represented
REDUCTION: Eliminates 14.5% of candidates
```

### TIER 2: Medium-Impact Filters

#### 5. Consecutive Number Limit
```
Distribution:
  No consecutive: 56.8%
  Max 2 consecutive: 39.3%
  Max 3+ consecutive: 3.9%

FILTER: Allow max 2 consecutive numbers
REDUCTION: Eliminates 3.9% of candidates
```

#### 6. Prime Number Count
```
Distribution:
  0 primes: 14.1%
  1 prime:  35.5%
  2 primes: 34.1%
  3 primes: 13.8%
  4+ primes: 2.5%

Primes in pool (1-39): 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37

FILTER: Require 1-3 prime numbers
REDUCTION: Eliminates 16.6% of candidates
```

### TIER 3: Advanced Filters (Fine-Tuning)

#### 7. AC Value (Arithmetic Complexity)
From documentation: AC value of 5 or 6 covers 90%+ of draws.

#### 8. First-Last Distance
The span between lowest and highest number in the ticket.

#### 9. Unit Digit Analysis
Ending digits (0-9) patterns across the 5 numbers.

---

## Filter Pipeline Design

### Stage 1: Position Filter (Already Implemented)
```
Uses 85% capture ranges:
  N_1: 1-13, N_2: 3-21, N_3: 9-29, N_4: 18-36, N_5: 28-39
```

### Stage 2: Statistical Filters
```python
def apply_filters(tickets):
    filtered = []
    for ticket in tickets:
        # Odd/Even: 2:3 or 3:2
        odd = sum(1 for n in ticket if n % 2 == 1)
        if odd not in [2, 3]:
            continue

        # High/Low: L2:H3 or L3:H2
        low = sum(1 for n in ticket if n <= 19)
        if low not in [2, 3]:
            continue

        # Sum: 50-140
        if not (50 <= sum(ticket) <= 140):
            continue

        # Decades: 3+ represented
        decades = len(set(n // 10 for n in ticket))
        if decades < 3:
            continue

        # Consecutive: max 2
        max_consec = calc_max_consecutive(ticket)
        if max_consec > 2:
            continue

        filtered.append(ticket)
    return filtered
```

### Stage 3: Scoring & Ranking
After filtering, rank remaining tickets by:
1. Contact score (from matrix analysis)
2. Position compliance score
3. Historical pattern match

---

## Recommended Workflow

```
1. Generate large pool (200-1000 tickets)
   ↓
2. Apply Position Filter (85% ranges)
   ↓
3. Apply Tier 1 filters (Odd/Even, High/Low, Sum, Decade)
   ↓
4. Apply Tier 2 filters (Consecutive, Prime)
   ↓
5. Rank by contact score
   ↓
6. Select top 40-50 tickets
```

### Expected Reduction Rates

| Stage | Input | Output | Reduction |
|-------|-------|--------|-----------|
| Generate | - | 1000 | - |
| Position | 1000 | ~850 | 15% |
| Odd/Even | 850 | ~566 | 33% |
| High/Low | 566 | ~373 | 34% |
| Sum | 373 | ~350 | 6% |
| Decades | 350 | ~299 | 14% |
| Consecutive | 299 | ~287 | 4% |
| Prime | 287 | ~239 | 17% |
| **Final selection** | 239 | **40** | Top ranked |

---

## Things to AVOID

1. **All odd or all even**: Only 4.6% of draws
2. **All from one decade**: Only 0.1% of draws
3. **5 consecutive numbers**: Essentially never (0.02%)
4. **Extreme sums** (<50 or >140): Only 6.4% of draws
5. **Previously drawn exact combinations**: Minimal impact but easy to check

---

## Next Steps

1. Implement filter functions in `src/predictor/filters.py`
2. Add filter configuration to predictor
3. Backtest different filter combinations
4. Find optimal initial pool size for 40-ticket target
