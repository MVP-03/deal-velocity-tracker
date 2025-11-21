import pytest
from datetime import date


@pytest.fixture
def sample_deals():
    return [
        {'deal_id': 'd1', 'company': 'Alpha', 'stage': 'proposal',
         'entered_date': '2026-01-01', 'exited_date': None, 'arr_usd': 50000},
        {'deal_id': 'd2', 'company': 'Beta',  'stage': 'discovery',
         'entered_date': '2026-01-05', 'exited_date': '2026-01-20', 'arr_usd': 25000},
        {'deal_id': 'd3', 'company': 'Gamma', 'stage': 'negotiation',
         'entered_date': '2026-01-10', 'exited_date': None, 'arr_usd': 100000},
    ]


@pytest.fixture
def reference_date():
    return date(2026, 2, 1)
