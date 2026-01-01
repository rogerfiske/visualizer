# CA5 Fantasy 5 - Optimal Range Analysis

**Generated**: January 1, 2026
**Data Source**: `data/raw/CA5_date.csv`
**Total Draws Analyzed**: 11,664
**Analysis Periods**: 500, 250, 100, 39 days

---

## Executive Summary

This analysis identifies the **smallest contiguous number ranges** that capture a target percentage of actual lottery draws for each sorted position (N_1 through N_5). The goal is to reduce the prediction pool while maintaining high probability of capturing the correct numbers.

**Key Finding**: The 85% capture rate offers the optimal balance between pool reduction and prediction accuracy.

---

## 90% Capture Ranges by Period

### Last 500 Days

| Position | Optimal Range | Span | Pool Reduction | Actual Capture |
|----------|---------------|------|----------------|----------------|
| **N_1** (Lowest) | 1-15 | 15 | 61.5% | 92.6% |
| **N_2** | 2-22 | 21 | 46.2% | 90.2% |
| **N_3** (Middle) | 7-30 | 24 | 38.5% | 90.6% |
| **N_4** | 17-37 | 21 | 46.2% | 90.8% |
| **N_5** (Highest) | 26-39 | 14 | 64.1% | 91.0% |

### Last 250 Days

| Position | Optimal Range | Span | Pool Reduction | Actual Capture |
|----------|---------------|------|----------------|----------------|
| **N_1** | 1-14 | 14 | 64.1% | 91.2% |
| **N_2** | 2-22 | 21 | 46.2% | 90.8% |
| **N_3** | 7-30 | 24 | 38.5% | 91.6% |
| **N_4** | 17-37 | 21 | 46.2% | 90.8% |
| **N_5** | 26-39 | 14 | 64.1% | 91.2% |

### Last 100 Days

| Position | Optimal Range | Span | Pool Reduction | Actual Capture |
|----------|---------------|------|----------------|----------------|
| **N_1** | 1-14 | 14 | 64.1% | 90.0% |
| **N_2** | 2-21 | 20 | 48.7% | 90.0% |
| **N_3** | 7-29 | 23 | 41.0% | 91.0% |
| **N_4** | 16-37 | 22 | 43.6% | 90.0% |
| **N_5** | 25-39 | 15 | 61.5% | 90.0% |

### Last 39 Days

| Position | Optimal Range | Span | Pool Reduction | Actual Capture |
|----------|---------------|------|----------------|----------------|
| **N_1** | 1-14 | 14 | 64.1% | 92.3% |
| **N_2** | 2-23 | 22 | 43.6% | 89.7% |
| **N_3** | 7-28 | 22 | 43.6% | 89.7% |
| **N_4** | 17-36 | 20 | 48.7% | 89.7% |
| **N_5** | 24-39 | 16 | 59.0% | 89.7% |

---

## Capture Rate vs Pool Size Tradeoffs

### N_1 (Lowest Number)

| Target % | Range | Span | Actual % | Pool Reduction |
|----------|-------|------|----------|----------------|
| 70% | 1-9 | 9 | 71.8% | **76.9%** |
| 75% | 1-10 | 10 | 78.4% | 74.4% |
| 80% | 1-11 | 11 | 82.0% | 71.8% |
| **85%** | **1-13** | **13** | **87.0%** | **66.7%** |
| 90% | 1-15 | 15 | 92.6% | 61.5% |
| 95% | 1-17 | 17 | 95.2% | 56.4% |
| 99% | 1-22 | 22 | 99.0% | 43.6% |

### N_2 (2nd Lowest)

| Target % | Range | Span | Actual % | Pool Reduction |
|----------|-------|------|----------|----------------|
| 70% | 4-17 | 14 | 70.4% | 64.1% |
| 75% | 5-19 | 15 | 75.2% | 61.5% |
| 80% | 3-19 | 17 | 80.4% | 56.4% |
| **85%** | **3-21** | **19** | **86.4%** | **51.3%** |
| 90% | 2-22 | 21 | 90.2% | 46.2% |
| 95% | 2-25 | 24 | 96.0% | 38.5% |
| 99% | 2-30 | 29 | 99.4% | 25.6% |

### N_3 (Middle Number)

| Target % | Range | Span | Actual % | Pool Reduction |
|----------|-------|------|----------|----------------|
| 70% | 9-25 | 17 | 71.0% | 56.4% |
| 75% | 10-27 | 18 | 75.4% | 53.8% |
| 80% | 11-29 | 19 | 80.6% | 51.3% |
| **85%** | **9-29** | **21** | **85.2%** | **46.2%** |
| 90% | 7-30 | 24 | 90.6% | 38.5% |
| 95% | 7-33 | 27 | 96.2% | 30.8% |
| 99% | 4-34 | 31 | 99.0% | 20.5% |

### N_4 (4th Number)

| Target % | Range | Span | Actual % | Pool Reduction |
|----------|-------|------|----------|----------------|
| 70% | 20-34 | 15 | 70.2% | 61.5% |
| 75% | 20-35 | 16 | 75.6% | 59.0% |
| 80% | 18-35 | 18 | 82.0% | 53.8% |
| **85%** | **18-36** | **19** | **86.2%** | **51.3%** |
| 90% | 17-37 | 21 | 90.8% | 46.2% |
| 95% | 14-37 | 24 | 95.4% | 38.5% |
| 99% | 11-38 | 28 | 99.0% | 28.2% |

### N_5 (Highest Number)

| Target % | Range | Span | Actual % | Pool Reduction |
|----------|-------|------|----------|----------------|
| 70% | 32-39 | 8 | 72.2% | **79.5%** |
| 75% | 31-39 | 9 | 75.8% | 76.9% |
| 80% | 30-39 | 10 | 80.8% | 74.4% |
| **85%** | **28-39** | **12** | **86.4%** | **69.2%** |
| 90% | 26-39 | 14 | 91.0% | 64.1% |
| 95% | 21-39 | 19 | 95.8% | 51.3% |
| 99% | 17-39 | 23 | 99.0% | 41.0% |

---

## Expert Recommendation

### Why 85% Capture Rate is Optimal

The 85% capture rate offers the best risk/reward balance:

1. **Extreme Positions Benefit Most**: N_1 and N_5 achieve 67-69% pool reduction
2. **Acceptable Miss Rate**: Only 15% chance of missing vs 10% for 90%
3. **Significantly Tighter Ranges**: Especially for N_1 (13 vs 15) and N_5 (12 vs 14)
4. **Stable Across Time Periods**: Results consistent from 39 to 500 days

### Recommended Filter Sets

#### Aggressive Filter (80% Capture)
*Use when generating many tickets and can afford some misses*

| Position | Range | Span | Pool Reduction |
|----------|-------|------|----------------|
| N_1 | 1-11 | 11 | 71.8% |
| N_2 | 3-19 | 17 | 56.4% |
| N_3 | 11-29 | 19 | 51.3% |
| N_4 | 18-35 | 18 | 53.8% |
| N_5 | 30-39 | 10 | 74.4% |

**Combined Pool Reduction**: ~61% average

#### Balanced Filter (85% Capture) - RECOMMENDED
*Default choice for most prediction scenarios*

| Position | Range | Span | Pool Reduction |
|----------|-------|------|----------------|
| N_1 | 1-13 | 13 | 66.7% |
| N_2 | 3-21 | 19 | 51.3% |
| N_3 | 9-29 | 21 | 46.2% |
| N_4 | 18-36 | 19 | 51.3% |
| N_5 | 28-39 | 12 | 69.2% |

**Combined Pool Reduction**: ~57% average

#### Conservative Filter (90% Capture)
*Use when accuracy is paramount*

| Position | Range | Span | Pool Reduction |
|----------|-------|------|----------------|
| N_1 | 1-15 | 15 | 61.5% |
| N_2 | 2-22 | 21 | 46.2% |
| N_3 | 7-30 | 24 | 38.5% |
| N_4 | 17-37 | 21 | 46.2% |
| N_5 | 26-39 | 14 | 64.1% |

**Combined Pool Reduction**: ~51% average

---

## Position-Specific Insights

### N_1 (Lowest Number)
- **Tightest natural distribution** - heavily concentrated 1-10
- Best candidate for aggressive filtering (80% at span 11)
- Rarely exceeds 20 in historical data

### N_2 (2nd Lowest)
- **Moderate spread** - centered around 11-20
- Benefits from filtering but less dramatically than N_1/N_5
- Optimal range shifts slightly based on time period

### N_3 (Middle Number)
- **Widest natural spread** - least constrained by position
- Pool reduction potential limited (~38-46%)
- Consider focusing filter efforts on other positions

### N_4 (4th Number)
- **Mirror of N_2** - similar characteristics, opposite end
- Consistent optimal ranges across time periods
- Good candidate for balanced filtering

### N_5 (Highest Number)
- **Tightest high-end distribution** - concentrated 31-39
- Best candidate for aggressive filtering alongside N_1
- 80% capture achieved with only 10 numbers (30-39)

---

## Strategic Application for VLA

### Using Ranges as VLA Filters

1. **Pre-Generation Filter**: Configure VLA to only generate tickets with numbers in optimal ranges
2. **Post-Generation Filter**: Score generated tickets against range compliance
3. **Hybrid Approach**: Use 85% ranges for generation, 90% for validation

### Combining with VLA Analysis

The optimal ranges complement VLA's existing methodologies:

- **Contact/Outside**: Apply range filter AFTER contact analysis
- **Hot/Cold**: Range filter should take precedence (structural constraint)
- **Lines/Blocks**: Range compliance is independent of grid position

### Expected Outcomes

With 85% capture filter applied to all positions:
- **~57% reduction** in number combinations to consider
- **~85% probability** of capturing all 5 drawn numbers
- **~44% compound probability** of missing at least one number (1 - 0.85^5)

For better compound capture:
- 90% individual capture = 59% compound capture (all 5 correct)
- 95% individual capture = 77% compound capture (all 5 correct)

---

## Charts Reference

### Summary Charts
| Period | File |
|--------|------|
| 500 Days | `summary_500days_optimal.png` |
| 250 Days | `summary_250days_optimal.png` |
| 100 Days | `summary_100days_optimal.png` |
| 39 Days | `summary_39days_optimal.png` |

### Individual Position Charts (per period)
- `N_1_{days}days_optimal.png`
- `N_2_{days}days_optimal.png`
- `N_3_{days}days_optimal.png`
- `N_4_{days}days_optimal.png`
- `N_5_{days}days_optimal.png`

All charts located in: `data/charts/`

---

## Methodology

### Optimal Contiguous Range Algorithm

For each position and target capture rate:
1. Calculate frequency distribution of drawn numbers (1-39)
2. For each possible starting number (1 to 39):
   - Accumulate frequencies until target capture rate reached
   - Record the range span
3. Select the range with smallest span meeting target capture rate

### Data Notes

- Numbers are pre-sorted (N_1 < N_2 < N_3 < N_4 < N_5)
- This creates natural positional constraints
- Historical patterns remarkably stable across time periods
- 39-day window chosen to match pool size (1 cycle)

---

*Analysis performed using `eda_optimal_range.py`*
