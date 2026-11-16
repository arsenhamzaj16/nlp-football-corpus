import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
entries = json.loads((ROOT/'sources.json').read_text(encoding='utf-8'))
assert len(entries) >= 8, 'At least eight texts required'
assert len({e['kind'] for e in entries}) >= 3, 'At least three text genres required'
missing = [e['file'] for e in entries if not (ROOT/'corpus'/e['file']).exists()]
if missing:
    print('Missing downloaded corpus files:', ', '.join(missing))
    raise SystemExit(1)
for e in entries:
    contents = (ROOT/'corpus'/e['file']).read_text(encoding='utf-8')
    assert len(contents.split()) >= 200, f"Not enough words: {e['file']}"
print('Corpus passes: ', len(entries), 'UTF-8 files,', len({e['kind'] for e in entries}), 'genres, each >=200 words.')
