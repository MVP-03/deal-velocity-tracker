import pytest
from datetime import date
from src.velocity import (
    load_deals, days_in_stage, stage_stats, bottleneck_stage,
    velocity_score, deal_velocity_summary, fast_deals, slow_deals,
)

SAMPLE_DEALS = [
    {'deal_id': 'T001', 'company': 'Alpha', 'stage': 'demo',
     'entered_date': '2025-07-01', 'exited_date': '2025-07-08', 'arr_usd': 50000},
    {'deal_id': 'T002', 'company': 'Beta', 'stage': 'demo',
     'entered_date': '2025-07-01', 'exited_date': '2025-07-15', 'arr_usd': 60000},
    {'deal_id': 'T003', 'company': 'Gamma', 'stage': 'proposal',
     'entered_date': '2025-07-01', 'exited_date': '2025-07-20', 'arr_usd': 80000},
]


def test_days_in_stage_completed():
    deal = SAMPLE_DEALS[0]
    assert days_in_stage(deal) == 7


def test_days_in_stage_open_uses_reference_date():
    deal = {'deal_id': 'X', 'company': 'Y', 'stage': 'demo',
            'entered_date': '2025-07-01', 'exited_date': None, 'arr_usd': 0}
    assert days_in_stage(deal, reference_date=date(2025, 7, 11)) == 10


def test_stage_stats_avg_days():
    stats = stage_stats(SAMPLE_DEALS)
    assert stats['demo']['avg_days'] == 10.5


def test_stage_stats_count():
    stats = stage_stats(SAMPLE_DEALS)
    assert stats['demo']['count'] == 2


def test_stage_stats_max_min():
    stats = stage_stats(SAMPLE_DEALS)
    assert stats['demo']['max_days'] == 14
    assert stats['demo']['min_days'] == 7


def test_bottleneck_is_longest_avg():
    stats = stage_stats(SAMPLE_DEALS)
    assert bottleneck_stage(stats) == 'proposal'


def test_velocity_score_faster_is_higher():
    bench = {'demo': {'avg_days': 10.0}}
    fast = {'deal_id': 'F', 'company': 'X', 'stage': 'demo',
            'entered_date': '2025-07-01', 'exited_date': '2025-07-06', 'arr_usd': 0}
    slow = {'deal_id': 'S', 'company': 'X', 'stage': 'demo',
            'entered_date': '2025-07-01', 'exited_date': '2025-07-21', 'arr_usd': 0}
    assert velocity_score(fast, bench) > velocity_score(slow, bench)


def test_velocity_score_range():
    bench = {'demo': {'avg_days': 10.0}}
    deal = {'deal_id': 'X', 'company': 'Y', 'stage': 'demo',
            'entered_date': '2025-07-01', 'exited_date': '2025-07-11', 'arr_usd': 0}
    score = velocity_score(deal, bench)
    assert 0 <= score <= 100


def test_deal_velocity_summary_keys():
    s = deal_velocity_summary(SAMPLE_DEALS)
    for key in ('total_deals', 'avg_days_in_stage', 'bottleneck_stage', 'stage_stats'):
        assert key in s


def test_deal_velocity_summary_count():
    s = deal_velocity_summary(SAMPLE_DEALS)
    assert s['total_deals'] == 3


def test_fast_deals_returns_subset():
    fast = fast_deals(SAMPLE_DEALS, percentile=50)
    assert 1 <= len(fast) < len(SAMPLE_DEALS)


def test_slow_deals_returns_subset():
    slow = slow_deals(SAMPLE_DEALS, percentile=50)
    assert 1 <= len(slow) < len(SAMPLE_DEALS)


def test_load_deals_from_csv(tmp_path):
    p = tmp_path / 'deals.csv'
    p.write_text(
        'deal_id,company,stage,entered_date,exited_date,arr_usd\n'
        'D1,TestCo,demo,2025-07-01,2025-07-10,50000\n'
    )
    deals = load_deals(str(p))
    assert len(deals) == 1
    assert deals[0]['company'] == 'TestCo'
    assert deals[0]['arr_usd'] == 50000.0
