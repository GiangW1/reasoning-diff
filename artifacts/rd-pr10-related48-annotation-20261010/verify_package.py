"""Offline integrity checks only; no model calls or semantic adjudication."""
import argparse
from collections import Counter, defaultdict
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
SOURCE = 'artifacts/rd-pr10-server-recurrence-review-20261010/'
SHA = 'c20e0461c7158ec66b1f69abfd8d132cd6b275c8'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-manifest', action='store_true',
                        help='Write initial upload manifest; omit when independently verifying.')
    args = parser.parse_args()
    manifest_path = ROOT / 'SHA256.json'
    if args.write_manifest:
        assert not manifest_path.exists(), 'Do not replace the original snapshot manifest'
        manifest_path.write_text(json.dumps({str(p.relative_to(ROOT)): digest(p)
            for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts},
            indent=2) + '\n')
    for base, manifest in [(ROOT, manifest_path),
                           (ROOT/'related48', ROOT/'related48/manifest.json')]:
        for name, expected in json.loads(manifest.read_text()).items():
            assert digest(base/name) == expected, name

    archive_bytes = subprocess.check_output(['git', 'archive', SHA, SOURCE], cwd=REPO)
    with tarfile.open(fileobj=io.BytesIO(archive_bytes)) as archive:
        source = {m.name: archive.extractfile(m).read() for m in archive.getmembers() if m.isfile()}
    original = [json.loads(s) for s in source[SOURCE+'records.jsonl'].decode().splitlines()]
    original = {r['code']: r for r in original if r['condition'] == 'related_noop'}
    data = json.loads((ROOT/'related48/annotations.json').read_text())
    records = data['records']
    assert data['source_commit'] == SHA
    assert len(records) == len(original) == 48
    assert {r['code'] for r in records} == set(original)
    assert dict(Counter(r['category'] for r in records)) == data['categories']
    pairs = defaultdict(list)
    anchors = 0
    for r in records:
        code = r['code']; prior = original[code]
        raw = (ROOT/'related48/raw'/f'{code}.txt').read_bytes()
        assert raw == source[r['source_file']]
        assert hashlib.sha256(raw).hexdigest() == r['text_sha256'] == prior['text_sha256']
        assert (r['task_id'], r['seed'], r['role']) == (
            prior['meta']['base_group_id'], prior['meta']['seed'], prior['meta']['role'])
        text = raw.decode()
        paragraphs = list(re.finditer(r'[^\n]+(?:\n(?!\n)[^\n]+)*', text))
        assert len(paragraphs) == r['paragraph_count']
        for e in r['events']:
            p = paragraphs[e['paragraph']-1]
            assert (p.start(), p.end(), p.group()) == (e['start'], e['end'], e['quote'])
            assert text[e['start']:e['end']] == e['quote']
            anchors += 1
        assert (ROOT/'related48/cases'/f'{code}.md').is_file()
        assert (ROOT/'related48/paragraphs'/f'{code}.txt').is_file()
        pairs[r['task_id']].append(r['seed'])
    assert len(pairs) == 24 and all(sorted(xs) == [0, 3] for xs in pairs.values())

    links = 0
    for p in ROOT.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if '://' in target:
                continue
            target = target.split('#')[0]
            if target:
                assert (p.parent/target).exists(), (p, target)
                links += 1
    print(json.dumps(dict(records=48, base_tasks=24, source_commit=SHA,
        source_texts_equal=True, evidence_anchors_checked=anchors, local_links_checked=links,
        manifests_verified=True, no_new_model_experiments=True,
        semantic_labels_verified=False), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
