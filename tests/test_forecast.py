import sys, os
from datetime import date
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from forecast import remaining_stages, expected_close_date, forecast_pipeline, STAGE_ORDER


def test_remaining_stages_middle():
    remaining = remaining_stages('evaluation')
    assert 'proposal' in remaining
    assert 'prospecting' not in remaining


def test_remaining_stages_unknown():
    assert remaining_stages('unknown_stage') == []


def test_expected_close_date():
    deal = {'stage': 'proposal', 'entered_date': '2026-01-01', 'exited_date': None, 'arr_usd': 10000}
    stats = {'negotiation': {'avg_days': 10}, 'closed': {'avg_days': 0}}
    ref = date(2026, 1, 10)
    close = expected_close_date(deal, stats, reference_date=ref)
    assert close is not None
    assert close > '2026-01-10'


def test_forecast_pipeline_active_only():
    deals = [
        {'deal_id': 'd1', 'company': 'A', 'stage': 'proposal',
         'entered_date': '2026-01-01', 'exited_date': None, 'arr_usd': 10000},
        {'deal_id': 'd2', 'company': 'B', 'stage': 'closed',
         'entered_date': '2025-12-01', 'exited_date': '2026-01-15', 'arr_usd': 5000},
    ]
    result = forecast_pipeline(deals, reference_date=date(2026, 1, 20))
    assert len(result) == 1
    assert result[0]['deal_id'] == 'd1'
