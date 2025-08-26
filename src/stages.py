STAGE_ORDER = [
    'prospecting',
    'discovery',
    'evaluation',
    'proposal',
    'negotiation',
    'closed',
]

STAGE_BENCHMARKS = {
    'prospecting':  {'target_days': 7,  'warn_days': 14},
    'discovery':    {'target_days': 14, 'warn_days': 21},
    'evaluation':   {'target_days': 21, 'warn_days': 35},
    'proposal':     {'target_days': 10, 'warn_days': 21},
    'negotiation':  {'target_days': 14, 'warn_days': 30},
}

STAGE_COLORS = {
    'prospecting': '#6366f1',
    'discovery':   '#3b82f6',
    'evaluation':  '#f59e0b',
    'proposal':    '#10b981',
    'negotiation': '#f97316',
    'closed':      '#22c55e',
}
