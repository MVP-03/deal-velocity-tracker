from typing import Dict, List
from datetime import datetime


def validate_deal_row(row: Dict) -> List[str]:
    errors = []
    if not row.get('deal_id'):
        errors.append('deal_id is required')
    try:
        datetime.strptime(row.get('entered_date', ''), '%Y-%m-%d')
    except ValueError:
        errors.append('entered_date must be YYYY-MM-DD')
    try:
        v = float(row.get('arr_usd', 0))
        if v < 0:
            errors.append('arr_usd must be >= 0')
    except (TypeError, ValueError):
        errors.append('arr_usd must be numeric')
    return errors
