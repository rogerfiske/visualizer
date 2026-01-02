# Validation Strategy - VLA Visualizer Prediction System

**Author**: Murat (TEA Agent)
**Date**: January 2, 2026
**Project**: VLA Visualizer - Custom Lottery Prediction System

---

## 1. Executive Summary

This document defines the validation strategy for the lottery prediction system.
The system makes statistical claims that must be rigorously validated:

1. **Bias Elimination**: Corrected matrices eliminate VLA's 2.5x interior bias
2. **Position Filtering**: 85% capture ranges actually capture 85% of draws
3. **Prediction Quality**: System performs better than random baseline

**Key Risk**: Lottery prediction is inherently probabilistic. We cannot prove the system
"works" - we can only prove it doesn't perform *worse* than expected by chance, and
that our bias corrections achieve their stated goals.

---

## 2. Success Criteria

### 2.1 Bias Elimination (MUST PASS)

| Metric | VLA Standard | Corrected Target | Pass Criteria |
|--------|--------------|------------------|---------------|
| Effective variance | 5.0 | < 0.5 | Variance reduced > 90% |
| Corner disadvantage | 2.5x | 1.0x (±10%) | Corners within 10% of average |
| Uniform distribution | NO | YES | `is_uniform = True` |

**Mathematical Proof Required**: For all numbers 1-39:
```
effective_contacts(n) = neighbor_count(n) × bias_factor(n)
max(effective) - min(effective) < 0.5
```

### 2.2 Position Filter Accuracy (MUST PASS)

| Position | Claimed Capture | Acceptable Range | Test Sample |
|----------|-----------------|------------------|-------------|
| N_1 (1-13) | 87% | 82-92% | 500+ draws |
| N_2 (3-21) | 86% | 81-91% | 500+ draws |
| N_3 (9-29) | 85% | 80-90% | 500+ draws |
| N_4 (18-36) | 86% | 81-91% | 500+ draws |
| N_5 (28-39) | 86% | 81-91% | 500+ draws |

### 2.3 Baseline Performance (INFORMATIONAL)

**Random Baseline Probabilities** (CA Fantasy 5: 5 from 39):
```
P(0 matches) = C(5,0) × C(34,5) / C(39,5) = 42.5%
P(1 match)   = C(5,1) × C(34,4) / C(39,5) = 42.4%
P(2 matches) = C(5,2) × C(34,3) / C(39,5) = 13.2%
P(3 matches) = C(5,3) × C(34,2) / C(39,5) = 1.75%
P(4 matches) = C(5,4) × C(34,1) / C(39,5) = 0.09%
P(5 matches) = C(5,5) × C(34,0) / C(39,5) = 0.0017%
```

**Per-Ticket Expected Matches**: 0.641 numbers

**With 20 Tickets**:
- Expected best match: ~2.3 numbers
- P(at least one 3-match): ~30%
- P(at least one 4-match): ~1.8%

### 2.4 System Performance Target (SHOULD MEET)

| Metric | Random Baseline | System Target | Significance |
|--------|-----------------|---------------|--------------|
| Avg best match | 2.3 | ≥ 2.3 | Not worse than random |
| Days with 3+ match | 30% | ≥ 35% | 5% improvement |
| Position compliance | N/A | 100% | All tickets valid |

**Note**: Due to lottery randomness, we expect high variance. A 500-day test
gives reasonable confidence; 1000+ days gives strong confidence.

---

## 3. Test Categories

### 3.1 Unit Tests - Matrix Implementations

```
TEST-MATRIX-001: VLA Standard has expected bias
  - Assert variance = 5.0
  - Assert corners have 3-4 neighbors
  - Assert interior has 8 neighbors

TEST-MATRIX-002: Weighted Adjacency eliminates bias
  - Assert effective variance < 0.5
  - Assert all effective contacts within 10% of mean
  - Assert corners get 2.67x correction

TEST-MATRIX-003: Numerical Proximity is uniform
  - Assert all numbers have exactly 6 neighbors
  - Assert variance = 0
  - Assert bias factor = 1.0 for all

TEST-MATRIX-004: Contact scoring works correctly
  - Given specific draws, verify contact scores
  - Verify bias factors applied correctly
```

### 3.2 Unit Tests - Position Filters

```
TEST-FILTER-001: 85% ranges are configured correctly
  - N_1: 1-13, N_2: 3-21, N_3: 9-29, N_4: 18-36, N_5: 28-39

TEST-FILTER-002: Filter validation works
  - Valid ticket [5, 10, 20, 30, 35] passes
  - Invalid ticket [1, 2, 3, 4, 5] fails (N_5 out of range)

TEST-FILTER-003: Historical capture rates match claims
  - Run against 500+ draws
  - Each position captures within ±5% of claimed rate
```

### 3.3 Integration Tests - Predictor

```
TEST-PRED-001: Predictor generates valid tickets
  - All tickets have 5 unique numbers
  - All numbers in range 1-39
  - Numbers are sorted ascending

TEST-PRED-002: All tickets pass position filter
  - Generate 100 tickets
  - All must pass position validation

TEST-PRED-003: Backtest returns correct match counts
  - Compare known draw against known tickets
  - Verify match counts are accurate

TEST-PRED-004: Different strategies produce different results
  - balanced vs contact_first vs random
  - Tickets should differ (not identical)
```

### 3.4 Statistical Validation Tests

```
TEST-STAT-001: Position filter capture rates
  - 500-day backtest per position
  - Chi-square test against claimed rates

TEST-STAT-002: System vs random baseline
  - 1000-day backtest
  - Compare average best match
  - t-test for significance

TEST-STAT-003: Corner numbers not disadvantaged
  - Track corner number appearances in predictions
  - Compare to expected frequency
```

---

## 4. Backtest Framework Design

### 4.1 Test Windows

| Window | Days | Purpose | Confidence |
|--------|------|---------|------------|
| Quick | 100 | Smoke test | Low |
| Standard | 500 | Development validation | Medium |
| Full | 1000 | Release validation | High |
| Complete | 5000+ | Research analysis | Very High |

### 4.2 Configuration Matrix

Test all combinations of:

| Parameter | Values |
|-----------|--------|
| Matrix | proximity, weighted |
| Capture | 85, 90 |
| Strategy | balanced, contact_first, position_first, random |
| Tickets | 20 |

**Total Configurations**: 2 × 2 × 4 = 16

### 4.3 Metrics to Collect

Per configuration:
```
- total_days_tested
- avg_best_match
- std_best_match
- days_with_0_match
- days_with_1_match
- days_with_2_match
- days_with_3plus_match
- days_with_4plus_match
- days_with_5_match (jackpot)
- total_3plus_tickets
- position_compliance_rate
- corner_number_frequency
```

### 4.4 Statistical Significance

For comparing configurations:
```python
# Two-sample t-test for avg_best_match
from scipy.stats import ttest_ind
t_stat, p_value = ttest_ind(config_a_results, config_b_results)
significant = p_value < 0.05
```

For comparing to baseline:
```python
# One-sample t-test against expected value
from scipy.stats import ttest_1samp
t_stat, p_value = ttest_1samp(results, expected_baseline)
```

---

## 5. Validation Script Requirements

### 5.1 `validate_system.py` Functionality

```
1. Run all unit tests (matrix, filter, predictor)
2. Run statistical validation tests
3. Run configurable backtest
4. Generate summary report with PASS/FAIL

Usage:
  python validate_system.py                    # Quick validation (100 days)
  python validate_system.py --full             # Full validation (1000 days)
  python validate_system.py --unit-only        # Unit tests only
  python validate_system.py --backtest-only    # Backtest only
```

### 5.2 Output Format

```
============================================================
  VALIDATION REPORT - VLA Visualizer Prediction System
============================================================

UNIT TESTS:
  [PASS] TEST-MATRIX-001: VLA Standard has expected bias
  [PASS] TEST-MATRIX-002: Weighted Adjacency eliminates bias
  [PASS] TEST-MATRIX-003: Numerical Proximity is uniform
  ...

STATISTICAL VALIDATION:
  [PASS] Position filter capture rates within tolerance
  [INFO] System vs baseline: +3.2% improvement (p=0.12, not significant)
  ...

BACKTEST SUMMARY (500 days):
  Best Configuration: proximity + 85% + balanced
  Avg Best Match: 2.41 (baseline: 2.30)
  Days with 3+ match: 34.2%

============================================================
  OVERALL: 12/12 tests PASSED
============================================================
```

---

## 6. Risk Assessment

### 6.1 What We CAN Prove

| Claim | Validation Method | Confidence |
|-------|-------------------|------------|
| Bias eliminated | Mathematical proof | 100% |
| Position filters accurate | Statistical test | 95% |
| No worse than random | Statistical test | 95% |

### 6.2 What We CANNOT Prove

| Claim | Why |
|-------|-----|
| System "beats" lottery | Lottery is random by design |
| Optimal configuration | Would need infinite testing |
| Future performance | Past ≠ future |

### 6.3 Recommended Disclaimers

Any output should include:
```
DISCLAIMER: This system is for research/entertainment purposes only.
Lottery outcomes are random. Past performance does not guarantee
future results. Please gamble responsibly.
```

---

## 7. Recommended Test Execution

### 7.1 During Development

```bash
# After any code change
python validate_system.py --unit-only

# Before committing
python validate_system.py  # Quick (100 days)
```

### 7.2 For Release

```bash
# Full validation
python validate_system.py --full  # 1000 days

# All tests must pass
# Backtest metrics should meet targets
```

### 7.3 For Research

```bash
# Extended analysis
python validate_system.py --days 5000 --compare-all
```

---

## 8. Appendix: Statistical Formulas

### 8.1 Hypergeometric Distribution (Match Probabilities)

```
P(k matches) = C(5,k) × C(34,5-k) / C(39,5)

Where:
  C(n,r) = n! / (r! × (n-r)!)
  5 = numbers drawn
  39 = pool size
  k = number of matches
```

### 8.2 Expected Best Match (Multiple Tickets)

```
P(best ≥ k with n tickets) = 1 - P(all tickets have < k matches)^n
                            = 1 - (1 - P(≥k))^n
```

### 8.3 Chi-Square Test for Capture Rates

```
χ² = Σ (observed - expected)² / expected

df = number_of_categories - 1
p_value = 1 - chi2.cdf(χ², df)
```

---

*Document prepared by Murat, Test Architect*
*Risk-based testing: depth scales with impact*
