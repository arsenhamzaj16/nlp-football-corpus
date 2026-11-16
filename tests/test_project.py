from pathlib import Path
import json
import nbformat

ROOT = Path(__file__).resolve().parents[1]


def test_sources():
    rows = json.loads((ROOT/'sources.json').read_text(encoding='utf-8'))
    assert len(rows) == 8
    assert len({row['kind'] for row in rows}) >= 3
    assert len({row['file'] for row in rows}) == len(rows)
    assert all(row['url'].startswith('https://') for row in rows)


def test_notebook():
    path = ROOT / 'notebooks' / 'football_corpus_analysis.ipynb'
    nb = nbformat.read(path, as_version=4)
    nbformat.validate(nb)
    sources = '\n'.join(cell.source for cell in nb.cells)
    for question in ['Task A', 'Task B', 'Task C', 'Task D',
                     'Task E', 'Task F', 'Task G', 'Task H', 'Final questions']:
        assert question in sources
    assert sources.count('Output explanation:') >= 10
    for cell in nb.cells:
        if cell.cell_type == 'code':
            compile(cell.source, '<notebook-cell>', 'exec')
