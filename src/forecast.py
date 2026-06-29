from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .velocity import days_in_stage, stage_stats


STAGE_ORDER = ['prospecting', 'discovery', 'evaluation', 'proposal', 'negotiation', 'closed']


def remaining_stages(current_stage: str, stage_order: List[str] = STAGE_ORDER) -> List[str]:
    try:
        idx = stage_order.index(current_stage.lower())
    except ValueError:
        return []
    return stage_order[idx + 1:]


def expected_close_date(
    deal: Dict,
    stats: Dict,
    reference_date=None,
) -> Optional[str]:
    from datetime import date
    ref = reference_date or date.today()
    remaining = remaining_stages(deal['stage'])
    if not remaining:
        return None

    days_left = sum(
        stats.get(s, {}).get('avg_days', 14)
        for s in remaining
    )
    close = ref + timedelta(days=int(days_left))
    return close.strftime('%Y-%m-%d')


def forecast_pipeline(deals: List[Dict], reference_date=None) -> List[Dict]:
    active = [d for d in deals if not d.get('exited_date')]
    if not active:
        return []

    stats = stage_stats(deals, reference_date)
    result = []
    for deal in active:
        close_date = expected_close_date(deal, stats, reference_date)
        days_spent = days_in_stage(deal, reference_date)
        bench = stats.get(deal['stage'], {}).get('avg_days', days_spent)
        pacing = 'ahead' if days_spent < bench * 0.8 else ('behind' if days_spent > bench * 1.2 else 'on-track')
        result.append({
            **deal,
            'days_in_current_stage': days_spent,
            'stage_pacing':          pacing,
            'forecast_close_date':   close_date,
        })
    return sorted(result, key=lambda x: x.get('forecast_close_date') or '')
