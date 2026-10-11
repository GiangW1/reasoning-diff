"""Show exact paragraphs for human/assistant review; no semantic labels."""
import argparse
import json
from pathlib import Path
import re

OUT = Path('/mnt/mydata/wja/reasoning-diff/reports/pr10-server-recurrence-review-20261010')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('codes', nargs='+')
    ap.add_argument('--paragraphs')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()
    lookup = {r['code']: r for r in map(json.loads, (OUT/'records.jsonl').read_text().splitlines())}
    pattern = re.compile(r'souvenir|\blabels?\b|first sentence|initial(?:ly| value| statement|ly given)|misread|contradict|inconsisten|\bconflict|\bassum|\bsuppos|given.{0,30}\b17\b|\b17\b.{0,30}given|\bmistake\b|\bwrong\b', re.I)
    for code in args.codes:
        row = lookup[code]
        text = (OUT/'fulltexts'/f'{code}.txt').read_text()
        paragraphs = list(re.finditer(r'[^\n]+(?:\n(?!\n)[^\n]+)*', text))
        selected = {int(s) for s in args.paragraphs.split(',')} if args.paragraphs else None
        print('\nTRACE',code,row['meta']['task_id'],'seed',row['meta']['seed'],'role',row['meta']['role'],'gold',row['task']['answer_spec'])
        for i,p in enumerate(paragraphs,1):
            if selected is not None:
                include = i in selected
            elif args.all:
                include = p.end() > row['body_start']
            else:
                # Omit copies of the whole question after verifying source text.
                is_question_copy = len(p.group())>1200 and p.group().count('The number of')>=6
                include = p.end()>row['body_start'] and bool(pattern.search(p.group())) and not is_question_copy
            if include:print(f'[P{i:03} chars {p.start()}:{p.end()}]\n{p.group()}\n')


if __name__=='__main__':
    main()
