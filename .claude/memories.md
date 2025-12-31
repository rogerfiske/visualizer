# Project Memories

## Session Log

### Session 1: 2025-12-31

**Objective**: Set up VLA backtesting framework

**Completed**:
1. Attempted to control VLA programmatically - discovered it's GUI-only, cannot be automated
2. Copied 6,666 VLA help files to `docs/` directory
3. Created categorized index of 273 English help files (`docs/INDEX.md`)
4. Conducted thorough audit of VLA documentation to understand methodology
5. Created `backtest.py` for single-day prediction scoring
6. Created `batch_backtest.py` for multi-day walk-forward analysis
7. Wrote comprehensive VLA methodology summary (`VLA_ANALYSIS_SUMMARY.md`)
8. Set up GitHub repository and pushed initial commit
9. Created session summary and continuation documents

**Key Discoveries**:
- VLA uses visual/geometric analysis on a grid-based "Ticket View"
- Each number belongs to multiple categories simultaneously (Contact/Outside, Hot/Cold, etc.)
- **Critical insight**: Good predictions always MIX number types - never all one category
- "One Step Analysis" is VLA's most productive feature (automated workflow)
- Pick-4 games use special "Pick Distribution Filters" (pairs, unmatched, all-same)

**Pending**:
- User needs to generate VLA predictions starting from 11/1/2025
- Actual backtesting not yet performed

---

## VLA Documentation Audit Findings

### Number Classification System

Every lottery number simultaneously belongs to:

1. **Contact vs Outside**
   - Contact = adjacent to previously drawn numbers (including drawn numbers)
   - Outside = all other numbers not touching drawn numbers
   - Rule: Mix both types

2. **Hot vs Cold**
   - Hot = drawn in recent past
   - Cold = not drawn recently
   - Rule: Balance hot and cold

3. **Odd vs Even**
   - Standard classification
   - Rule: Maintain balance

4. **Connected vs Unconnected vs Disconnected**
   - Connected = touching other drawn numbers in grid
   - Unconnected = drawn but not touching other drawn
   - Disconnected = not drawn, far from any drawn
   - Rule: Spread across grid

5. **Line Positions**
   - Horizontal lines (rows in grid)
   - Vertical lines (columns)
   - Slant lines (diagonals)
   - Rule: Don't cluster on one line

6. **Blocks**
   - Groups of 10 (1-10, 11-20, 21-30, etc.)
   - Rule: Draw from multiple blocks

### VLA Analysis Methods

| Category | Methods |
|----------|---------|
| Types of Numbers | Contact/Outside, Hot/Cold, Odd/Even, Connected |
| Numbers | Occurrences, Repetitions, Distribution |
| Grouped Numbers | Blocks, Similar Groups (same last digit) |
| Lines | Horizontal, Vertical, Slant Right, Slant Left |
| Between | Above First, Between Numbers, Below Last |
| In Contact | Various contact zone analyses |

### Pick-4 Specific

Daily 4 uses Pick Distribution Filters:
- Unmatched (all different digits)
- Pairs (two same digits)
- All-Same (e.g., 5555)
- Slant lines

---

## Data Formats

### CA Fantasy 5
```
date,L_1,L_2,L_3,L_4,L_5
12/30/2025,10,12,22,28,37
```
- 5 numbers from pool of 1-39
- Data file: `C:\Users\Minis\CascadeProjects\c5_scrapper\data\raw\CA5_raw_data.txt`

### CA Daily 4
```
date,QS1,QS2,QS3,QS4
12/30/2025,6,0,8,2
```
- 4 digits, each 0-9 (can repeat)
- Data file: `C:\Users\Minis\CascadeProjects\CA-4_scrapper\data\raw\CA_Daily_4_dat.csv`

---

## User Context

- Has Visual Lottery Analyser software installed
- Experiences difficulty navigating VLA's GUI
- Goal: Systematically test VLA effectiveness through backtesting
- Starting date for analysis: November 1, 2025
- Wants 20+ predictions per day per game

---

## Technical Notes

### VLA Cannot Be Automated
- VLA is a Windows GUI application
- No CLI interface or API available
- User must manually:
  1. Set date in VLA
  2. Run analysis
  3. Export predictions to file

### Prediction File Convention
```
predictions/{game}_{YYYY-MM-DD}.csv
predictions/fantasy5_2025-11-01.csv
predictions/daily4_2025-11-01.csv
```

### Backtest Scoring

**Fantasy 5**:
| Matches | Result |
|---------|--------|
| 5 | Jackpot |
| 4 | Major prize |
| 3 | Minor prize |
| 2 | Free play |
| 0-1 | No win |

**Daily 4**:
| Match Type | Description |
|------------|-------------|
| Straight | Exact match (all 4 in order) |
| Box | All digits match (any order) |
| Positional | Count of correct positions |
