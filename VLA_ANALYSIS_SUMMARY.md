# Visual Lottery Analyser - Complete Analysis Summary

## Overview

Visual Lottery Analyser (VLA) uses **visual/geometric analysis** to identify patterns in lottery data. Instead of analyzing raw numbers, it visualizes occurrences as **wave diagrams** where each point represents a draw outcome.

---

## Core Concept: The Ticket View

The game numbers are arranged in a **square grid** (e.g., 7x7 for a 49-number game). This allows:
- Visualization of number relationships
- Identification of patterns across horizontal, vertical, and diagonal lines
- Tracking of "contact" zones around drawn numbers

### Key Terminology
- **Ticket Number**: Any number from the game pool (e.g., 1-39 for Fantasy 5)
- **Draw Number**: One of the numbers actually drawn in a single draw

---

## Number Type Classifications

Each number in the game pool belongs to multiple categories simultaneously:

### 1. Contact vs Outside Numbers
- **Contact**: Numbers adjacent to previously drawn numbers (including drawn numbers themselves)
- **Outside**: All other numbers not touching drawn numbers

**Rule**: Good tickets have a MIX of contact and outside numbers. All-contact or all-outside tickets rarely win.

### 2. Hot vs Cold Numbers
- **Hot**: Numbers drawn recently (within last few draws)
- **Cold**: Numbers not drawn in recent draws

**Rule**: Good tickets have a MIX of hot and cold numbers. All-hot or all-cold tickets rarely win.

### 3. Odd vs Even Numbers
- Standard odd/even classification

**Rule**: Good tickets have balanced odd/even distribution.

### 4. Connected vs Unconnected vs Disconnected
- **Connected**: Numbers adjacent to other drawn numbers in the grid
- **Unconnected**: Drawn numbers that don't touch other drawn numbers
- **Disconnected**: Non-drawn numbers far from any drawn number

---

## Game Layout Analysis Methods

### Lines Analysis
1. **Horizontal Lines** - Numbers grouped by horizontal rows in the grid
2. **Vertical Lines** - Numbers grouped by vertical columns
3. **Slant Lines Right** - Diagonal lines going left to right (/)
4. **Slant Lines Left** - Diagonal lines going right to left (\)

**Rule**: Numbers shouldn't cluster on one line. Spread across multiple lines is preferred.

### Blocks Analysis
- Numbers grouped into blocks of 10 (1-10, 11-20, 21-30, etc.)
- **Rule**: Good tickets draw from multiple blocks, not concentrated in one

### Similar Groups (Last Digit)
- Numbers grouped by their last digit (1,11,21,31... or 2,12,22,32...)
- Analyzes distribution patterns of same-ending numbers

### Between Numbers Analysis
- **Above First**: Numbers above the lowest drawn number
- **Below Last**: Numbers below the highest drawn number
- **Between**: Numbers in the middle range

### In-Contact Analysis
- Tracks how new draws relate to contact zones of previous draws
- Analyzes by position (horizontal, vertical, slant lines)

---

## Analysis Diagram Interpretation

The visual diagrams show patterns over time:
- **X-axis**: Time (draws), most recent on the right
- **Y-axis**: Count of occurrences (0, 1, 2, 3...)

### Reading Patterns:
- Points in row **0** = No numbers from that category were drawn
- Points in row **1** = One number from that category was drawn
- Points in row **2** = Two numbers from that category were drawn
- etc.

### Prediction Logic:
1. Look at the wave pattern trend
2. Identify if the pattern is at a peak or trough
3. Expect regression to mean / pattern continuation

---

## Productive Features for Automation

### 1. One Step Analysis (MOST PRODUCTIVE)
Fully automated workflow:
1. Downloads latest lottery numbers
2. Runs automatic analysis
3. Generates tickets based on analysis
4. Saves to collection
5. Displays for printing/export

### 2. Tickets Generator
Four generation methods:
1. **Automatic Analysis** - Uses VLA's visual analysis rules
2. **Random** - Simple random generation
3. **Custom Numbers** - User-selected numbers
4. **Filtered** - Applies filters to generated numbers

### 3. Filters System
Filter categories:
- **Types of Numbers Filters**: Contact/Outside, Hot/Cold, Odd/Even, Connected
- **Game Layout Filters**: Lines, Blocks, Similar Groups, Between
- **Numbers Filters**: Include/Exclude, Repeats, Consecutive
- **Pick Distribution Filters**: (For Pick games) Unmatched, Pairs, All-Same, Slant

---

## Game-Specific Notes

### CA Fantasy 5 (Standard Lotto)
- **Format**: 5 numbers from 1-39
- **Grid**: Approximately 6x7 layout
- **Applicable Analysis**: All standard methods (lines, blocks, contact, hot/cold)

### CA Daily 4 (Pick-4 Game)
- **Format**: 4 digits, each 0-9
- **Special Characteristics**: Numbers can repeat (e.g., 7,7,4,1)
- **Applicable Analysis**:
  - Pick Distribution Filters
  - Pairs (two same digits)
  - All-Same (e.g., 5,5,5,5)
  - Unmatched (all different)
  - Slant Lines

---

## Key Strategy Rules (From Documentation)

1. **Balance is Key**: Never use all numbers of one type
   - Mix contact + outside
   - Mix hot + cold
   - Mix odd + even
   - Spread across lines/blocks

2. **Pattern Recognition**: Look for:
   - When a category hasn't hit (due for occurrence)
   - When a category is overdue (regression expected)
   - Cyclical patterns in the wave diagrams

3. **Avoid Common Mistakes**:
   - All numbers from same horizontal/vertical line
   - All numbers from one block (e.g., all 1-10)
   - All contact numbers (too clustered)
   - All outside numbers (too scattered)

---

## Backtesting Workflow

For our testing process:

1. **Set VLA date to historical date** (e.g., 11/1/2025)
2. **Run One Step Analysis** to generate predictions
3. **Export predictions** to CSV/TXT
4. **Compare against actual results** from:
   - CA Fantasy 5: `C:\Users\Minis\CascadeProjects\c5_scrapper\data\raw\CA5_raw_data.txt`
   - CA Daily 4: `C:\Users\Minis\CascadeProjects\CA-4_scrapper\data\raw\CA_Daily_4_dat.csv`
5. **Score predictions**:
   - Match count per ticket
   - Best match across all tickets
   - Any wins (3+, 4+, 5 match)
6. **Walk forward** one day and repeat

---

## Data Formats

### CA Fantasy 5
```
date,L_1,L_2,L_3,L_4,L_5
12/30/2025,10,12,22,28,37
```

### CA Daily 4
```
date,QS1,QS2,QS3,QS4
12/30/2025,6,0,8,2
```

---

## Next Steps

1. User runs VLA with date set to 11/1/2025
2. Generates 20+ tickets for each game
3. Exports to CSV/TXT
4. Provides files for comparison analysis
5. We score against actual results
6. Repeat for subsequent dates to build statistical profile
