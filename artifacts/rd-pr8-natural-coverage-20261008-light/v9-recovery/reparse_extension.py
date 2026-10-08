"""Reparse the completed fixed extension without changing generated trajectories."""
from pathlib import Path
from reasoning_diff import events
from reasoning_diff.artifacts import write_manifest
from reasoning_diff.io import file_digest, read_json, read_jsonl, write_json, write_jsonl
from reasoning_diff.schema import Task
from reparse_pr8 import reparse_trace
from extend_natural_pilot import measure, PAIRED_SEEDS, NOISE_SEEDS, source_hashes

source = Path('/mnt/mydata/wja/reasoning-diff/runs/pr8-natural-extension-3gpu-20261008')
root = Path('/mnt/mydata/wja/reasoning-diff/runs/pr8-v9-recovery-20261008/extension-r1')
if root.exists():
    raise ValueError('require a fresh output directory')
manifest = read_json(source / 'manifest.json')
for name, checksum in manifest['file_hashes'].items():
    assert file_digest(source / name) == checksum
old_report = read_json(source / 'measurement_report.json')
original = read_jsonl(source / 'traces.jsonl')
all_tasks = {row['task_id']: Task.from_dict(row) for row in read_jsonl(source / 'tasks.jsonl')}
base_ids = set(old_report['by_problem'])
tasks = [all_tasks[key] for key in sorted(base_ids)]
parser_hash = file_digest(Path(events.__file__))
rows = [reparse_trace(row, all_tasks[row['task_id']], parser_hash).to_dict() for row in original]
assert len(rows) == 128
for old, new in zip(original, rows):
    assert all(old[key] == new[key] for key in ('text', 'token_ids', 'offsets', 'answer', 'correct', 'status'))
report, observations, owners = measure(tasks, rows)
ablations = {}
for name, refs, noise in [('original_seed0', (0,), PAIRED_SEEDS),
                          ('seed0_extended_noise', (0,), NOISE_SEEDS),
                          ('all_paired_original_noise', PAIRED_SEEDS, PAIRED_SEEDS)]:
    ablations[name] = measure(tasks, rows, refs, noise)[0]
pilot = read_json(root.parent / 'pilot-r1/measurement_report.json')
assert ablations['original_seed0']['overall'] == pilot['overall']
report.update(ablations=ablations, posthoc_reparse=True, source_extension=str(source),
    parser_hash=parser_hash, measurement_source_hashes=source_hashes(),
    generation_protocol=old_report['protocol'], original_overall=old_report['overall'],
    n_traces=len(rows), n_reused=48, n_new=80, formal_launch_ready=False,
    original_natural_matching_resolved=False, scientific_conclusion=None)
report['checks']['extension_generation_complete'] = old_report['checks']['extension_generation_complete']
report['failures'] = [key for key, passed in report['checks'].items() if not passed]
report['passed'] = not report['failures']
for name, data in [('tasks.jsonl', owners), ('traces.jsonl', rows), ('observations.jsonl', observations)]:
    write_jsonl(root / name, data)
write_json(root / 'measurement_report.json', report)
files = ['tasks.jsonl', 'traces.jsonl', 'observations.jsonl', 'measurement_report.json']
write_manifest(root, [root / name for name in files], {'traces': len(rows), 'new_generated': 0})
print(report['overall'])
print(report['checks'])
for key, value in report['by_problem'].items():
    print(key, value)
