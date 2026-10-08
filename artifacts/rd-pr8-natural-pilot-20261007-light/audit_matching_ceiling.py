"""An optimistic count bound on the SAVED PARSED events, not parser recall."""
import argparse
from collections import Counter
from pathlib import Path

from reasoning_diff.graphs import ancestors
from reasoning_diff.io import read_json, read_jsonl, write_json
from reasoning_diff.schema import Task, Trace

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--in-dir', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
traces = {row['id']: Trace.from_dict(row) for row in read_jsonl(args.in_dir / 'traces.jsonl')}
tasks = {row['task_id']: Task.from_dict(row) for row in read_jsonl(args.in_dir / 'tasks.jsonl')}
observations = read_jsonl(args.in_dir / 'observations.jsonl')
pairs = sorted({(o['reference_trace'], o['comparison_trace'], o['premise_id']) for o in observations
                if not o['rng_pair'].startswith('sham:')})

def events(trace):
    return [e for e in trace.events if e.event_region == 'thinking' and e.event_kind != 'restatement' and e.status == 'ok']

rows = []
for aid, bid, premise in pairs:
    a, b = traces[aid], traces[bid]
    parents = ancestors(tasks[a.task_id])
    aa = [e for e in events(a) if premise not in parents.get(e.node_id, set())]
    bb = events(b)
    ac, bc = Counter(e.node_id for e in aa), Counter(e.node_id for e in bb)
    stage = lambda e: (e.node_id, e.event_kind, e.event_phase)
    asc, bsc = Counter(map(stage, aa)), Counter(map(stage, bb))
    rows.append({'problem': a.task_id, 'premise': premise, 'reference': aid, 'comparison': bid,
                 'eligible': len(aa), 'reference_events': len(events(a)), 'comparison_events': len(bb),
                 'entity_only_one_to_one_ceiling': sum((ac & bc).values()),
                 'entity_kind_phase_one_to_one_ceiling': sum((asc & bsc).values())})
assert sum(r['eligible'] for r in rows) == read_json(args.in_dir / 'measurement_report.json')['overall']['eligible_cells']
write_json(args.out, {'interpretation': 'Optimistic count bound on this parsed event set, ignoring order, expressions and ambiguity. Not actual matches or a bound on all unparsed prose.', 'rows': rows})
