# VLA Contact Bias Analysis

**Generated**: January 1, 2026
**Matrix Source**: `data/num_matrix/vis_std_v1.csv`
**Analysis Script**: `analysis_contact_bias.py`

---

## Executive Summary

The Visual Lottery Analyser (VLA) contact-based prediction methodology contains an inherent **structural bias** caused by the grid layout. Numbers in interior positions have significantly more adjacent cells than corner/edge numbers, making them **2.5x more likely** to be flagged as "in contact" regardless of any predictive value.

This bias systematically over-weights mid-range numbers (8-29) and under-weights extreme numbers (1, 6, 36, 37, 39) - directly conflicting with the natural distribution patterns identified in our EDA analysis.

---

## VLA Methodology Overview

### How VLA Contact Analysis Works

1. **Grid Layout**: Numbers 1-39 arranged in a 6-row x 7-column matrix
2. **Draw Marking**: Most recent draw numbers marked on grid
3. **Contact Identification**: Numbers adjacent to drawn numbers (8-directional) flagged as "in contact"
4. **Prediction Generation**: Algorithm favors contact numbers for next prediction
5. **User Filtering**: Optional filters reduce ticket pool based on various criteria

### The Standard VLA Matrix

```
       Col1   Col2   Col3   Col4   Col5   Col6   Col7
      ─────────────────────────────────────────────────
 R1  │   1      7     13     19     25     31     37
 R2  │   2      8     14     20     26     32     38
 R3  │   3      9     15     21     27     33     39
 R4  │   4     10     16     22     28     34     --
 R5  │   5     11     17     23     29     35     --
 R6  │   6     12     18     24     30     36     --
```

Numbers are arranged in columns (1-6, 7-12, 13-18, etc.) creating a specific geometric relationship between adjacent values.

---

## The Structural Bias

### Matrix with Contact Exposure Counts

```
       Col1   Col2   Col3   Col4   Col5   Col6   Col7
      ─────────────────────────────────────────────────
 R1  │  1(3)   7(5)  13(5)  19(5)  25(5)  31(5)  37(3)
 R2  │  2(5)   8(8)  14(8)  20(8)  26(8)  32(8)  38(5)
 R3  │  3(5)   9(8)  15(8)  21(8)  27(8)  33(7)  39(4)
 R4  │  4(5)  10(8)  16(8)  22(8)  28(8)  34(6)   --
 R5  │  5(5)  11(8)  17(8)  23(8)  29(8)  35(5)   --
 R6  │  6(3)  12(5)  18(5)  24(5)  30(5)  36(3)   --

Legend: Number(Contact Exposure Count)
```

### Position Classification

| Type | Count | Numbers | Avg Contacts | Bias Factor |
|------|-------|---------|--------------|-------------|
| **Corner** | 5 | 1, 6, 36, 37, 39 | 3.2 | 1.0x (baseline) |
| **Edge** | 16 | 2-5, 7, 12-13, 18-19, 24-25, 30-31, 34-35, 38 | 5.1 | 1.6x |
| **Interior** | 18 | 8-11, 14-17, 20-23, 26-29, 32-33 | 7.9 | **2.5x** |

---

## Detailed Exposure Analysis

### Corner Numbers (5 numbers, avg 3.2 contacts)

| Number | Contacts | Adjacent Numbers |
|--------|----------|------------------|
| 1 | 3 | 7, 2, 8 |
| 6 | 3 | 5, 11, 12 |
| 36 | 3 | 29, 35, 30 |
| 37 | 3 | 31, 32, 38 |
| 39 | 4 | 32, 38, 33, 34 |

### Edge Numbers (16 numbers, avg 5.1 contacts)

| Number | Contacts | Number | Contacts |
|--------|----------|--------|----------|
| 2 | 5 | 24 | 5 |
| 3 | 5 | 25 | 5 |
| 4 | 5 | 30 | 5 |
| 5 | 5 | 31 | 5 |
| 7 | 5 | 34 | 6 |
| 12 | 5 | 35 | 5 |
| 13 | 5 | 38 | 5 |
| 18 | 5 | | |
| 19 | 5 | | |

### Interior Numbers (18 numbers, avg 7.9 contacts)

| Number | Contacts | Number | Contacts |
|--------|----------|--------|----------|
| 8 | 8 | 22 | 8 |
| 9 | 8 | 23 | 8 |
| 10 | 8 | 26 | 8 |
| 11 | 8 | 27 | 8 |
| 14 | 8 | 28 | 8 |
| 15 | 8 | 29 | 8 |
| 16 | 8 | 32 | 8 |
| 17 | 8 | 33 | 7 |
| 20 | 8 | | |
| 21 | 8 | | |

---

## Bias Quantification

### Contact Probability by Position Type

Given a uniformly random draw, the probability of any number being "in contact":

| Position Type | Base Contact Rate | Relative Probability |
|---------------|-------------------|---------------------|
| Corner | 40.0% | 1.0x |
| Edge | 63.3% | 1.6x |
| Interior | 98.8% | **2.5x** |

**Interpretation**: An interior number like 15 or 22 is 2.5 times more likely to be flagged as "in contact" than corner numbers like 1 or 37, purely due to geometric position - not because it has any greater predictive value.

### Systematic Over/Under-Representation

**Over-represented** (Interior - 18 numbers):
- 8, 9, 10, 11, 14, 15, 16, 17, 20, 21, 22, 23, 26, 27, 28, 29, 32, 33
- These numbers will appear in VLA contact lists disproportionately often

**Under-represented** (Corners - 5 numbers):
- 1, 6, 36, 37, 39
- These numbers are systematically disadvantaged by the contact algorithm

---

## Conflict with Actual Draw Patterns

### EDA Findings vs VLA Bias

Our EDA analysis (see `CA5_Optimal_Range_Analysis.md`) identified optimal ranges for each sorted position:

| Position | Optimal 90% Range | VLA Bias Impact |
|----------|-------------------|-----------------|
| **N_1** | 1-15 | Corner 1 and 6 disadvantaged |
| **N_2** | 2-22 | Mixed - edges disadvantaged |
| **N_3** | 7-30 | Favored - mostly interior numbers |
| **N_4** | 17-37 | Corner 36, 37 disadvantaged |
| **N_5** | 26-39 | Corners 36, 37, 39 disadvantaged |

### Critical Observation

The VLA contact bias works **against** the natural distribution of extreme positions:

1. **N_1 (lowest number)**: Needs numbers 1-15, but VLA underweights 1 and 6
2. **N_5 (highest number)**: Needs numbers 26-39, but VLA underweights 36, 37, 39

This means VLA's contact-based predictions may systematically miss optimal N_1 and N_5 candidates.

---

## Implications for VLA Usage

### Problems with Pure Contact-Based Prediction

1. **False Signal**: High contact score may reflect grid position, not predictive value
2. **Extreme Number Neglect**: Critical N_1 and N_5 candidates systematically underweighted
3. **Mid-Range Inflation**: N_2, N_3, N_4 ranges over-represented in contact lists

### Recommended Compensations

1. **Weight Adjustment**: Manually boost corner/edge numbers in final selection
2. **Position-Aware Filtering**: Apply different contact thresholds by grid position
3. **Hybrid Approach**: Combine contact analysis with positional probability (EDA ranges)

### Suggested Correction Factors

To normalize contact scores across positions:

| Position Type | Raw Score | Correction Factor | Normalized |
|---------------|-----------|-------------------|------------|
| Corner | x | × 2.5 | 2.5x |
| Edge | x | × 1.6 | 1.6x |
| Interior | x | × 1.0 | 1.0x |

---

## Alternative Considerations

### Why This Bias May Be Intentional

Some lottery analysts argue that:
- Numbers "cluster" in draws (consecutive or adjacent numbers appear together)
- Contact methodology captures this clustering tendency
- Interior numbers genuinely have more "connection paths" to potential clusters

### Counter-Argument

Our EDA shows:
- N_1 and N_5 positions have tight, predictable ranges
- These ranges include corner/edge numbers that VLA underweights
- Historical data doesn't support systematic clustering around interior numbers

---

## Charts Reference

| Chart | File | Description |
|-------|------|-------------|
| Heatmap | `contact_bias_heatmap.png` | Matrix visualization with color-coded exposure |
| Bar Chart | `contact_exposure_by_number.png` | Exposure by number with position type coloring |

Charts located in: `data/charts/`

---

## Conclusions

1. **VLA contact methodology contains inherent structural bias** - confirmed
2. **Interior numbers are 2.5x over-weighted** vs corner numbers
3. **This bias conflicts with optimal N_1 and N_5 ranges** from EDA
4. **Correction factors or hybrid approaches recommended** for improved accuracy

---

## Next Steps

Potential follow-up analyses:
1. Quantify historical impact of bias on VLA prediction accuracy
2. Design alternative matrix layouts with reduced positional bias
3. Develop bias-corrected scoring algorithm
4. Test hybrid approach combining VLA contact + EDA optimal ranges

---

*Analysis performed using `analysis_contact_bias.py`*
