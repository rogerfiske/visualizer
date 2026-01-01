# CA5 Fantasy 5 - Exploratory Data Analysis Results

**Generated**: January 1, 2026
**Data Source**: `data/raw/CA5_date.csv`
**Total Draws**: 11,664
**Date Range**: 02/04/1992 to 12/31/2025

---

## Summary Statistics Table

| Period | Draws | N_1 Range | N_1 Median | N_2 Range | N_2 Median | N_3 Range | N_3 Median | N_4 Range | N_4 Median | N_5 Range | N_5 Median |
|--------|-------|-----------|------------|-----------|------------|-----------|------------|-----------|------------|-----------|------------|
| **Full Dataset** | 11,664 | 1-30 | 5.0 | 2-35 | 12.0 | 3-37 | 20.0 | 4-38 | 27.0 | 9-39 | 35.0 |
| **Last 500 Days** | 500 | 1-30 | 6.0 | 2-32 | 13.0 | 3-37 | 20.0 | 8-38 | 28.0 | 13-39 | 35.0 |
| **Last 250 Days** | 250 | 1-27 | 6.0 | 2-31 | 13.0 | 3-37 | 20.0 | 8-38 | 28.0 | 15-39 | 34.5 |
| **Last 100 Days** | 100 | 1-26 | 6.0 | 2-31 | 13.0 | 5-37 | 20.0 | 8-38 | 28.0 | 15-39 | 34.5 |
| **Last 39 Days** | 39 | 1-16 | 7.0 | 2-31 | 14.0 | 5-33 | 20.0 | 8-36 | 27.0 | 17-39 | 34.0 |

---

## Key Observations

### Positional Distribution Pattern
Numbers are sorted (N_1 < N_2 < N_3 < N_4 < N_5), creating distinct ranges for each position:

| Position | Description | Primary Range | Concentration |
|----------|-------------|---------------|---------------|
| **N_1** | Lowest number | 1-10 | ~78-80% |
| **N_2** | 2nd lowest | 11-20 | ~45-48% |
| **N_3** | Middle number | 11-30 | ~40% each bin |
| **N_4** | 4th number | 21-30 | ~43-49% |
| **N_5** | Highest number | 31-39 | ~75-77% |

### Trend Analysis

1. **N_1 Range Tightening**: Maximum value dropped from 30 (historical) to 16 (last 39 days)
2. **N_5 Floor Rising**: Minimum increased from 9 (historical) to 17 (last 39 days)
3. **N_3 Stability**: Median remains constant at 20.0 across all time periods
4. **N_4 Upward Drift**: Slight increase in recent periods (27 → 28)

---

## Full Dataset Distribution (11,664 draws)

### N_1 (Lowest Number)
```
Range       Count    Pct     Distribution
1-10        9,284   79.6%   |########################################
11-20       2,130   18.3%   |#########
21-30         250    2.1%   |#
31-39           0    0.0%   |
```

### N_2 (2nd Lowest)
```
Range       Count    Pct     Distribution
1-10        4,563   39.1%   |##################################
11-20       5,320   45.6%   |########################################
21-30       1,690   14.5%   |############
31-39          91    0.8%   |
```

### N_3 (Middle Number)
```
Range       Count    Pct     Distribution
1-10        1,151    9.9%   |#########
11-20       5,004   42.9%   |########################################
21-30       4,710   40.4%   |#####################################
31-39         799    6.9%   |######
```

### N_4 (4th Number)
```
Range       Count    Pct     Distribution
1-10          139    1.2%   |
11-20       2,038   17.5%   |##############
21-30       5,694   48.8%   |########################################
31-39       3,793   32.5%   |##########################
```

### N_5 (Highest Number)
```
Range       Count    Pct     Distribution
1-10            3    0.0%   |
11-20         354    3.0%   |#
21-30       2,602   22.3%   |###########
31-39       8,705   74.6%   |########################################
```

---

## Last 500 Days Distribution

### N_1
```
Range       Count    Pct     Distribution
1-10          392   78.4%   |########################################
11-20         101   20.2%   |##########
21-30           7    1.4%   |
31-39           0    0.0%   |
```

### N_2
```
Range       Count    Pct     Distribution
1-10          196   39.2%   |##################################
11-20         225   45.0%   |########################################
21-30          76   15.2%   |#############
31-39           3    0.6%   |
```

### N_3
```
Range       Count    Pct     Distribution
1-10           48    9.6%   |#########
11-20         211   42.2%   |########################################
21-30         203   40.6%   |######################################
31-39          38    7.6%   |#######
```

### N_4
```
Range       Count    Pct     Distribution
1-10            5    1.0%   |
11-20          92   18.4%   |################
21-30         225   45.0%   |########################################
31-39         178   35.6%   |###############################
```

### N_5
```
Range       Count    Pct     Distribution
1-10            0    0.0%   |
11-20          21    4.2%   |##
21-30         100   20.0%   |##########
31-39         379   75.8%   |########################################
```

---

## Last 250 Days Distribution

### N_1
```
Range       Count    Pct     Distribution
1-10          196   78.4%   |########################################
11-20          51   20.4%   |##########
21-30           3    1.2%   |
31-39           0    0.0%   |
```

### N_2
```
Range       Count    Pct     Distribution
1-10           89   35.6%   |#############################
11-20         120   48.0%   |########################################
21-30          40   16.0%   |#############
31-39           1    0.4%   |
```

### N_3
```
Range       Count    Pct     Distribution
1-10           24    9.6%   |########
11-20         102   40.8%   |######################################
21-30         107   42.8%   |########################################
31-39          17    6.8%   |######
```

### N_4
```
Range       Count    Pct     Distribution
1-10            2    0.8%   |
11-20          45   18.0%   |################
21-30         109   43.6%   |########################################
31-39          94   37.6%   |##################################
```

### N_5
```
Range       Count    Pct     Distribution
1-10            0    0.0%   |
11-20          10    4.0%   |##
21-30          53   21.2%   |###########
31-39         187   74.8%   |########################################
```

---

## Last 100 Days Distribution

### N_1
```
Range       Count    Pct     Distribution
1-10           78   78.0%   |########################################
11-20          21   21.0%   |##########
21-30           1    1.0%   |
31-39           0    0.0%   |
```

### N_2
```
Range       Count    Pct     Distribution
1-10           36   36.0%   |############################
11-20          50   50.0%   |########################################
21-30          13   13.0%   |##########
31-39           1    1.0%   |
```

### N_3
```
Range       Count    Pct     Distribution
1-10           11   11.0%   |##########
11-20          43   43.0%   |########################################
21-30          41   41.0%   |######################################
31-39           5    5.0%   |####
```

### N_4
```
Range       Count    Pct     Distribution
1-10            2    2.0%   |#
11-20          21   21.0%   |###################
21-30          43   43.0%   |########################################
31-39          34   34.0%   |###############################
```

### N_5
```
Range       Count    Pct     Distribution
1-10            0    0.0%   |
11-20           5    5.0%   |##
21-30          20   20.0%   |##########
31-39          75   75.0%   |########################################
```

---

## Last 39 Days Distribution

### N_1
```
Range       Count    Pct     Distribution
1-10           30   76.9%   |########################################
11-20           9   23.1%   |############
21-30           0    0.0%   |
31-39           0    0.0%   |
```

### N_2
```
Range       Count    Pct     Distribution
1-10           14   35.9%   |###############################
11-20          18   46.2%   |########################################
21-30           6   15.4%   |#############
31-39           1    2.6%   |##
```

### N_3
```
Range       Count    Pct     Distribution
1-10            5   12.8%   |###########
11-20          16   41.0%   |#####################################
21-30          17   43.6%   |########################################
31-39           1    2.6%   |##
```

### N_4
```
Range       Count    Pct     Distribution
1-10            2    5.1%   |#####
11-20          10   25.6%   |##########################
21-30          15   38.5%   |########################################
31-39          12   30.8%   |################################
```

### N_5
```
Range       Count    Pct     Distribution
1-10            0    0.0%   |
11-20           3    7.7%   |####
21-30           6   15.4%   |########
31-39          30   76.9%   |########################################
```

---

## Analytical Notes

### Why 39 Days?
The 39-day window matches the Fantasy 5 number pool size (1-39), representing approximately one full "cycle" where each number has statistically equal opportunity to appear.

### Distribution Consistency
The positional distributions remain remarkably stable across all time periods, suggesting:
- Sorted number positions follow predictable probability distributions
- N_1 and N_5 show strongest concentration (lowest/highest ranges)
- N_3 shows most uniform spread across middle ranges

### Implications for VLA Analysis
These baseline statistics can inform VLA filter settings:
- **Contact/Outside analysis** should account for positional bias
- **Hot/Cold tracking** may be more meaningful for middle positions (N_2, N_3, N_4)
- **Range filters** could leverage positional probability distributions

---

*Analysis performed using `eda_ca5.py`*
