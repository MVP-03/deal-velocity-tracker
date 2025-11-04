from typing import Dict, List


def stage_summary_text(stats: Dict) -> str:
    lines = ['Stage Velocity Summary', '=' * 30]
    for stage, s in stats.items():
        lines.append(
            f"{stage:<14} avg: {s['avg_days']:>5.1f}d  "
            f"min: {s['min_days']:>3}d  max: {s['max_days']:>3}d  "
            f"n={s['count']}"
        )
    return '\n'.join(lines)


def forecast_summary_text(forecasted: List[Dict]) -> str:
    if not forecasted:
        return 'No active deals to forecast.'
    lines = ['Deal Forecast', '=' * 40]
    for deal in forecasted:
        pacing = deal.get('stage_pacing', 'unknown')
        close  = deal.get('forecast_close_date', 'TBD')
        lines.append(
            f"{deal['deal_id']:<10} {deal['company']:<20} "
            f"stage={deal['stage']:<12} pacing={pacing:<10} close≈{close}"
        )
    return '\n'.join(lines)
