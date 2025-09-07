# deal-velocity-tracker

Measures how fast deals move through pipeline stages and surfaces where they stall.

## What it does

- Calculates days-in-stage for each deal (closed or still active)
- Computes per-stage average, min, and max cycle times
- Identifies the bottleneck stage with the highest average days
- Scores individual deals 0–100 by velocity relative to stage benchmarks
- Returns fast and slow deal cohorts for win/loss pattern analysis

## Usage

```python
from src.velocity import load_deals, deal_velocity_summary

deals = load_deals('data/deals.csv')
report = deal_velocity_summary(deals)
print(report['bottleneck_stage'])
print(report['stage_stats'])
```

## Sample output

```json
{
  "total_deals": 20,
  "avg_days_in_stage": 11.4,
  "bottleneck_stage": "negotiation",
  "stage_stats": {
    "demo":        {"count": 5, "avg_days": 9.2,  "max_days": 14, "min_days": 5},
    "proposal":    {"count": 4, "avg_days": 13.5, "max_days": 18, "min_days": 9},
    "negotiation": {"count": 3, "avg_days": 16.7, "max_days": 22, "min_days": 11}
  }
}
```

## Input format

`data/deals.csv` columns:

| Column | Description |
|--------|-------------|
| deal_id | Unique deal identifier |
| company | Account name |
| stage | Current or last pipeline stage |
| entered_date | YYYY-MM-DD when deal entered this stage |
| exited_date | YYYY-MM-DD when deal exited (blank if still active) |
| arr_usd | Annual recurring revenue |

Open deals (blank `exited_date`) are measured against today unless `reference_date` is supplied — useful for reproducible testing.

## Running tests

```bash
make test
```
