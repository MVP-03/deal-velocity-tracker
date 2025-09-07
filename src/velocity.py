import csv
from datetime import datetime, date
from statistics import mean


def load_deals(path):
    deals = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            deals.append({
                'deal_id': row['deal_id'].strip(),
                'company': row['company'].strip(),
                'stage': row['stage'].strip(),
                'entered_date': row['entered_date'].strip(),
                'exited_date': row['exited_date'].strip() if row['exited_date'].strip() else None,
                'arr_usd': float(row['arr_usd']),
            })
    return deals


def days_in_stage(deal, reference_date=None):
    entered = datetime.strptime(deal['entered_date'], '%Y-%m-%d').date()
    if deal['exited_date']:
        exited = datetime.strptime(deal['exited_date'], '%Y-%m-%d').date()
    else:
        exited = reference_date or date.today()
    return (exited - entered).days


def stage_stats(deals, reference_date=None):
    by_stage = {}
    for d in deals:
        s = d['stage']
        if s not in by_stage:
            by_stage[s] = []
        by_stage[s].append(days_in_stage(d, reference_date))
    return {
        s: {
            'count': len(vals),
            'avg_days': round(mean(vals), 1),
            'max_days': max(vals),
            'min_days': min(vals),
        }
        for s, vals in by_stage.items()
    }


def bottleneck_stage(stats):
    return max(stats.items(), key=lambda x: x[1]['avg_days'])[0]


def velocity_score(deal, stage_benchmarks, reference_date=None):
    days = days_in_stage(deal, reference_date)
    bench = stage_benchmarks.get(deal['stage'], {'avg_days': days})
    avg = bench['avg_days']
    if avg == 0:
        return 100
    ratio = days / avg
    return max(0, min(100, int(100 / ratio)))


def deal_velocity_summary(deals, reference_date=None):
    stats = stage_stats(deals, reference_date)
    all_days = [days_in_stage(d, reference_date) for d in deals]
    return {
        'total_deals': len(deals),
        'avg_days_in_stage': round(mean(all_days), 1) if all_days else 0,
        'bottleneck_stage': bottleneck_stage(stats),
        'stage_stats': stats,
    }


def fast_deals(deals, percentile=25, reference_date=None):
    scored = [(d, days_in_stage(d, reference_date)) for d in deals]
    scored.sort(key=lambda x: x[1])
    cutoff = max(1, int(len(scored) * percentile / 100))
    return [d for d, _ in scored[:cutoff]]


def slow_deals(deals, percentile=25, reference_date=None):
    scored = [(d, days_in_stage(d, reference_date)) for d in deals]
    scored.sort(key=lambda x: x[1], reverse=True)
    cutoff = max(1, int(len(scored) * percentile / 100))
    return [d for d, _ in scored[:cutoff]]
