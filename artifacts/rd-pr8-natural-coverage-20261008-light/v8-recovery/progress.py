from collections import Counter
from pathlib import Path
from reasoning_diff.io import read_json, write_json
from extend_natural_pilot import load_source, measure

root = Path('/mnt/mydata/wja/reasoning-diff/runs/pr8-natural-extension-20261008')
protocol = read_json(root / 'protocol.json')
state = read_json(root / 'pipeline.json')
print(state)
added = [read_json(f)['trace'] for f in (root / 'responses').glob('*.json')]
counts = Counter(r['base_group_id'] for r in added)
print('statuses', dict(Counter(r['status'] for r in added)), 'by_problem', dict(sorted(counts.items())))
previous_path = root / 'partial_by_problem.json'
previous = read_json(previous_path)['problems'] if previous_path.exists() else {}
pending = {problem for problem, count in counts.items() if count == 10 and problem not in previous}
if pending:
    tasks, original, _, _ = load_source(Path(protocol['source']))
    for task in tasks:
        if task.task_id not in pending:
            continue
        report = measure([task], original + added)[0]
        previous[task.task_id] = {key: report[key] for key in ('overall', 'checks', 'passed')}
        print('NEW_COMPLETE_PROBLEM', task.task_id, previous[task.task_id])
    write_json(previous_path, {'cohort_complete': False, 'new_requests_complete': len(added), 'problems': previous})
