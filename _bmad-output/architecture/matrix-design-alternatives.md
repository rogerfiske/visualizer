# Matrix Design Alternatives - Architecture Document

**Author**: Winston (Architect Agent)
**Date**: January 2, 2026
**Project**: VLA Visualizer - Custom Lottery Prediction System
**Status**: DRAFT - Pending Review

---

## 1. Problem Statement

### 1.1 Current State

VLA's contact-based prediction methodology uses a 6x7 grid matrix where numbers 1-39 are arranged in columns. The "contact" concept identifies numbers adjacent (8-directional) to recently drawn numbers.

**The Standard VLA Matrix**:
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

### 1.2 The Bias Problem

| Position Type | Count | Numbers | Avg Contacts | Bias Factor |
|---------------|-------|---------|--------------|-------------|
| **Corner** | 5 | 1, 6, 36, 37, 39 | 3.2 | 1.0x (baseline) |
| **Edge** | 16 | Various | 5.1 | 1.6x |
| **Interior** | 18 | 8-11, 14-17, 20-23, 26-29, 32-33 | 7.9 | **2.5x** |

### 1.3 Impact on Prediction Quality

| Position | Optimal 85% Range | Affected Corners | Bias Impact |
|----------|-------------------|------------------|-------------|
| **N_1** | 1-13 | 1, 6 | 2 corners underweighted |
| **N_5** | 28-39 | 36, 37, 39 | 3 corners underweighted |

**Critical Insight**: The numbers most important for predicting extreme positions (lowest/highest) are systematically disadvantaged by VLA's geometry.

### 1.4 Design Objectives

1. **Eliminate or Normalize Positional Bias** - All numbers should have equal contact opportunity
2. **Preserve Contact Concept** - The idea of "proximity to recent draws" has value
3. **Support Optimal Ranges** - Solution must work WITH positional filtering, not against it
4. **Practical Implementation** - Must be implementable in Python for backtesting

---

## 2. Alternative Approaches

### Overview

| Approach | Complexity | Bias Elimination | Preserves VLA Concept | Recommended |
|----------|------------|------------------|----------------------|-------------|
| **A: Weighted Adjacency** | Low | Normalized (corrected) | Yes | For VLA compatibility |
| **B: Toroidal Matrix** | Medium | Eliminated (geometric) | Yes | For clean redesign |
| **C: Numerical Proximity** | Low | Eliminated (no grid) | Partially | For pure statistical |

---

## 3. Approach A: Weighted Adjacency (Bias Correction)

### 3.1 Concept

Keep the existing VLA grid layout but apply **correction multipliers** to contact scores based on position type. This normalizes the expected contact rate across all numbers.

### 3.2 Correction Factors

To equalize opportunity:

| Position Type | Raw Contacts | Correction Factor | Effective Score |
|---------------|--------------|-------------------|-----------------|
| Corner | 3.2 avg | × 2.47 | 7.9 (normalized) |
| Edge | 5.1 avg | × 1.55 | 7.9 (normalized) |
| Interior | 7.9 avg | × 1.00 | 7.9 (baseline) |

### 3.3 Number-Specific Correction Map

```python
CORRECTION_FACTORS = {
    # Corners (3 neighbors)
    1: 2.63,   # 3 contacts → factor 8/3
    6: 2.63,
    37: 2.63,

    # Corner-ish (4 neighbors)
    36: 2.00,  # 4 contacts → factor 8/4
    39: 2.00,

    # Edges (5 neighbors)
    2: 1.60, 3: 1.60, 4: 1.60, 5: 1.60,
    7: 1.60, 12: 1.60, 13: 1.60, 18: 1.60,
    19: 1.60, 24: 1.60, 25: 1.60, 30: 1.60,
    31: 1.60, 38: 1.60,

    # Reduced edges (6-7 neighbors)
    34: 1.33, 35: 1.14, 33: 1.14,

    # Interior (8 neighbors) - baseline
    8: 1.00, 9: 1.00, 10: 1.00, 11: 1.00,
    14: 1.00, 15: 1.00, 16: 1.00, 17: 1.00,
    20: 1.00, 21: 1.00, 22: 1.00, 23: 1.00,
    26: 1.00, 27: 1.00, 28: 1.00, 29: 1.00,
    32: 1.00
}
```

### 3.4 Algorithm

```
For each number N in 1-39:
    raw_contact_score = count_adjacent_to_recent_draws(N)
    corrected_score = raw_contact_score × CORRECTION_FACTORS[N]

Sort numbers by corrected_score DESC
Apply position filters (N_1: 1-13, N_5: 28-39, etc.)
Generate tickets from filtered, ranked numbers
```

### 3.5 Analysis

**Pros**:
- Minimal change to VLA conceptual model
- Easy to implement (simple lookup table)
- Can be applied post-hoc to existing VLA output
- Backwards compatible with VLA workflows

**Cons**:
- Still using arbitrary grid geometry
- Correction factors are empirically derived, not principled
- Doesn't address WHY grid arrangement is columns of 6

**Expected Bias After Correction**:
| Position Type | Bias Factor |
|---------------|-------------|
| Corner | 1.0x |
| Edge | 1.0x |
| Interior | 1.0x |

### 3.6 Implementation Effort

- **Complexity**: Low
- **Lines of Code**: ~50
- **Testing**: Verify normalized scores, backtest against historical data

---

## 4. Approach B: Toroidal (Wraparound) Matrix

### 4.1 Concept

Transform the flat grid into a **torus** where edges wrap around:
- Left edge connects to right edge
- Top edge connects to bottom edge

This eliminates corners and edges entirely - every position becomes "interior-like" with equal neighbor access.

### 4.2 Geometric Model

**Standard Grid** (flat):
```
[1] - 7 - 13 - 19 - 25 - 31 - [37]
 |    |    |    |    |    |     |
 2  - 8 - 14 - 20 - 26 - 32 - 38
 ...
```

**Toroidal Grid** (wrapped):
```
... 31 - 37 ←→ 1 - 7 - 13 ...  (left-right wrap)
     ↕         ↕
... 36 - -- ←→ 6 - 12 - 18 ... (top-bottom wrap)
```

### 4.3 Challenge: Incomplete Grid

The 6x7 matrix has 42 cells but only 39 numbers. The three empty cells (positions 40, 41, 42) create asymmetry.

**Solutions**:

**Option B1: Virtual Neighbors**
- Empty cells act as "pass-through" - adjacency extends to next real number
- Number 34 adjacent to 39 via virtual 40

**Option B2: Compressed Layout (7x6 with 3 gaps)**
- Redistribute gaps to minimize impact
- Place gaps in interior positions where they affect fewest adjacencies

**Option B3: Alternative Dimensions (13x3 = 39)**
- Perfect fit, no empty cells
- Different neighbor patterns

### 4.4 Proposed Layout: 13x3 Toroidal

```
Col:  1   2   3   4   5   6   7   8   9  10  11  12  13
    ─────────────────────────────────────────────────────
R1:   1   2   3   4   5   6   7   8   9  10  11  12  13
R2:  14  15  16  17  18  19  20  21  22  23  24  25  26
R3:  27  28  29  30  31  32  33  34  35  36  37  38  39
      ↑ wraps to ↓
```

**Neighbor Map (with wrap)**:

Every number has exactly **8 neighbors**:
- 2 horizontal (left, right - with wrap)
- 2 vertical (up, down - with wrap)
- 4 diagonal (with wrap)

**Example**: Number 1's neighbors:
- Left: 13 (wrap), Right: 2
- Up: 27 (wrap), Down: 14
- Diagonals: 39, 28, 15, 26 (all with wrap)

### 4.5 Analysis

**Pros**:
- **Perfect bias elimination** - all numbers have exactly 8 neighbors
- Clean mathematical model
- No correction factors needed
- Preserves contact concept with improved fairness

**Cons**:
- Different from VLA's layout (loses direct comparability)
- Sequential numbers become adjacent (1-2-3... on same row)
- May change which numbers are "in contact" for same draws

**Expected Bias After Implementation**:
| Position Type | Count | Bias Factor |
|---------------|-------|-------------|
| All | 39 | 1.0x (uniform) |

### 4.6 Implementation Effort

- **Complexity**: Medium
- **Lines of Code**: ~100
- **Key Components**:
  1. New matrix layout (13x3)
  2. Wraparound neighbor calculation
  3. Contact analysis using toroidal adjacency

---

## 5. Approach C: Numerical Proximity (Non-Geometric)

### 5.1 Concept

Abandon the grid entirely. Define "contact" based on **numerical proximity** rather than spatial adjacency.

### 5.2 Proximity Definitions

**Option C1: Fixed Window**
```
A number N is "in contact" with drawn number D if:
    |N - D| <= k  (where k = 3 or 4)
```

Example with k=3: If 15 is drawn, numbers 12-18 are "in contact"

**Option C2: Percentage Window**
```
A number N is "in contact" with drawn number D if:
    |N - D| <= pool_size * p  (where p = 0.10 for 10%)
```

For pool 1-39 with p=0.10: window = ±4 numbers

**Option C3: Frequency-Based Co-occurrence**
```
Contact_score(N) = sum of historical co-occurrence with recent draws
```

This learns from actual draw patterns rather than imposing arbitrary geometry.

### 5.3 Analysis

**Pros**:
- **Complete bias elimination** - no geometry means no geometric bias
- Simple to understand and implement
- Naturally aligns with numerical ordering (useful for sorted positions)
- Can be tuned with parameter k

**Cons**:
- Loses "visual" aspect of VLA methodology
- Fixed window creates new edge effects (numbers 1-3 and 37-39 have fewer potential contacts)
- Co-occurrence approach requires significant computation

**Edge Effect in Fixed Window (k=3)**:
| Number | Possible Contacts |
|--------|-------------------|
| 1 | 2, 3, 4 (3 contacts) |
| 2 | 1, 3, 4, 5 (4 contacts) |
| 5-35 | 6 contacts each |
| 38 | 35, 36, 37, 39 (4 contacts) |
| 39 | 36, 37, 38 (3 contacts) |

**Mitigation**: Use wraparound for numerical proximity too:
- Number 1 also contacts 37, 38, 39
- Number 39 also contacts 1, 2, 3

### 5.4 Implementation Effort

- **Complexity**: Low
- **Lines of Code**: ~30
- **Key Components**:
  1. Proximity function with configurable window
  2. Optional wraparound for extreme numbers

---

## 6. Recommendation

### 6.1 Primary Recommendation: Hybrid Approach

Implement **two** approaches for comparison:

| Purpose | Approach | Rationale |
|---------|----------|-----------|
| **VLA Compatibility** | A: Weighted Adjacency | Allows direct comparison with VLA predictions |
| **Clean Baseline** | C: Numerical Proximity | Simple, unbiased reference point |

### 6.2 Implementation Priority

```
Phase 1: Implement Approach C (Numerical Proximity)
         - Simplest to implement
         - Provides unbiased baseline for comparison
         - 1-2 hours development

Phase 2: Implement Approach A (Weighted Adjacency)
         - Enables VLA comparison studies
         - Tests if bias correction improves accuracy
         - 2-3 hours development

Phase 3 (Optional): Implement Approach B (Toroidal)
         - If Approaches A/C show promise
         - More complex but mathematically elegant
         - 3-4 hours development
```

### 6.3 Success Criteria

For each approach, measure:

1. **Bias Elimination**: Contact probability should be uniform (±5%) across all numbers
2. **Prediction Accuracy**: Backtest against historical data
3. **Range Compatibility**: Must work with 85% optimal position filters
4. **Corner Performance**: Numbers 1, 6, 36, 37, 39 should NOT be disadvantaged

### 6.4 Decision Matrix

| Criterion | Weight | Approach A | Approach B | Approach C |
|-----------|--------|------------|------------|------------|
| Implementation Speed | 20% | 9 | 6 | 10 |
| Bias Elimination | 30% | 7 | 10 | 9 |
| VLA Compatibility | 20% | 10 | 5 | 6 |
| Simplicity | 15% | 8 | 6 | 10 |
| Extensibility | 15% | 7 | 9 | 8 |
| **Weighted Score** | | **8.0** | **7.3** | **8.5** |

**Verdict**: Start with **Approach C** (Numerical Proximity) for speed and simplicity, then add **Approach A** (Weighted Adjacency) for VLA comparison capability.

---

## 7. Technical Specifications

### 7.1 Data Structures

```python
# Shared interface for all matrix approaches
class ContactMatrix:
    def get_neighbors(self, number: int) -> List[int]:
        """Return list of numbers considered 'adjacent' to given number"""
        pass

    def calculate_contact_scores(self, recent_draws: List[int]) -> Dict[int, float]:
        """Calculate contact score for all numbers 1-39"""
        pass

    def get_bias_factor(self, number: int) -> float:
        """Return bias correction factor (1.0 if unbiased)"""
        pass
```

### 7.2 File Structure

```
visualizer/
├── src/
│   └── matrix/
│       ├── __init__.py
│       ├── base.py              # ContactMatrix base class
│       ├── weighted_adjacency.py # Approach A
│       ├── toroidal.py          # Approach B
│       ├── numerical_proximity.py # Approach C
│       └── vla_standard.py      # Original VLA (for comparison)
```

### 7.3 Configuration

```yaml
# config/matrix_config.yaml
matrix_type: "numerical_proximity"  # or "weighted_adjacency", "toroidal", "vla_standard"

numerical_proximity:
  window_size: 3
  use_wraparound: true

weighted_adjacency:
  use_vla_layout: true

toroidal:
  dimensions: [13, 3]  # or [7, 6] with gaps
```

---

## 8. Next Steps

### For Dev Agent (Step 2)

1. **Create base matrix interface** (`src/matrix/base.py`)
2. **Implement Approach C** (`numerical_proximity.py`) - Priority 1
3. **Implement Approach A** (`weighted_adjacency.py`) - Priority 2
4. **Create bias analysis script** to verify implementations
5. **Backtest both approaches** against historical data

### For TEA Agent (Step 4)

1. Define acceptance criteria for bias elimination
2. Design comparison test suite (VLA vs Approach A vs Approach C)
3. Create backtest validation framework

---

## 9. Appendix

### A. Complete Neighbor Maps

#### VLA Standard Matrix (for reference)
```
Number  Contacts  Neighbors
------  --------  ---------
1       3         2, 7, 8
2       5         1, 3, 7, 8, 9
3       5         2, 4, 8, 9, 10
4       5         3, 5, 9, 10, 11
5       5         4, 6, 10, 11, 12
6       3         5, 11, 12
7       5         1, 2, 8, 13, 14
8       8         1, 2, 3, 7, 9, 13, 14, 15
...
37      3         31, 32, 38
38      5         31, 32, 33, 37, 39
39      4         32, 33, 34, 38
```

#### Numerical Proximity (k=3, with wrap)
```
Number  Contacts  Neighbors
------  --------  ---------
1       6         37, 38, 39, 2, 3, 4
2       6         38, 39, 1, 3, 4, 5
3       6         39, 1, 2, 4, 5, 6
...
37      6         34, 35, 36, 38, 39, 1
38      6         35, 36, 37, 39, 1, 2
39      6         36, 37, 38, 1, 2, 3
```

### B. Historical Context

The VLA software was designed for visual pattern recognition, where users look at the grid and identify clusters. The column-based layout (1-6, 7-12, etc.) creates visual groupings that may help human pattern recognition but introduce computational bias.

Our custom system prioritizes **computational fairness** over visual aesthetics, which is appropriate for an automated prediction pipeline.

---

*Document prepared by Winston, Architect Agent*
*Ready for DCOG99 review and Dev Agent implementation*
