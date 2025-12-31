# Project Memories

## VLA Documentation Audit (2025-12-31)

### Key Findings

1. **VLA's Core Innovation**: Visual/geometric analysis using grid-based "Ticket View" instead of raw number analysis

2. **Number Classification System**: Each lottery number simultaneously belongs to multiple categories:
   - Contact vs Outside (proximity to drawn numbers)
   - Hot vs Cold (recency of draws)
   - Odd vs Even
   - Connected vs Unconnected vs Disconnected
   - Line positions (horizontal, vertical, slant)
   - Block membership (groups of 10)
   - Similar groups (same last digit)

3. **Primary Rule**: Good predictions ALWAYS mix number types. Never use all-contact, all-hot, all-same-line, etc.

4. **Most Productive Feature**: "One Step Analysis" - automated workflow that:
   - Downloads latest numbers
   - Runs analysis
   - Generates tickets
   - Exports for use

5. **Pick-4 Specific**: Daily 4 uses Pick Distribution Filters:
   - Unmatched (all different digits)
   - Pairs (two same digits)
   - All-Same (e.g., 5555)
   - Slant lines

### Data Formats

**Fantasy 5**: `date,L_1,L_2,L_3,L_4,L_5` (e.g., `12/30/2025,10,12,22,28,37`)

**Daily 4**: `date,QS1,QS2,QS3,QS4` (e.g., `12/30/2025,6,0,8,2`)

### User Context

- User has difficulty with VLA's GUI interface
- Goal: Backtest VLA effectiveness by comparing predictions to actual results
- Starting date: 11/1/2025, walking forward day by day
- Need 20+ predictions per day per game

## Files Created

| File | Purpose |
|------|---------|
| `docs/` | 6,666 VLA help files copied from original location |
| `docs/INDEX.md` | Categorized index of 273 English help files |
| `VLA_ANALYSIS_SUMMARY.md` | Complete methodology documentation |
| `backtest.py` | Single-day prediction scorer |
| `batch_backtest.py` | Multi-day walk-forward analysis |
| `README.md` | Project documentation |
