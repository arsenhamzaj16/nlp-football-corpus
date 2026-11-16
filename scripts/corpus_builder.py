"""Download openly licensed football pages as unchanged, readable source text.

Only HTML markup is stripped. Spelling, numbers, punctuation and source wording are not
normalized. Paragraphs are kept intact and separated by original paragraph boundaries.
"""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, unquote

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'sources.json'
CORPUS = ROOT / 'corpus'
HEADERS = {
    'User-Agent': 'FootballNLPStudentCorpus/1.0 (educational coursework; contact: academic project)',
    'Accept-Language': 'en',
}


def extract_article(html):
    soup = BeautifulSoup(html, 'html.parser')
    main = (soup.select_one('#mw-content-text .mw-parser-output')
            or soup.select_one('#mw-content-text')
            or soup.select_one('.mw-parser-output'))
    if main is None:
        raise ValueError('Article content container was not found')
    # Exclude website interface elements, but leave the wording inside article paragraphs.
    for element in main.select('style, script, .mw-editsection, '
                               '.navbox, .infobox, .reflist, .metadata, '
                               '.thumb, .hatnote, .vertical-navbox, .toc, '
                               '.noprint, .mw-collapsible'):
        element.decompose()
    pieces = []
    for elem in main.find_all(['p', 'li']):
        if elem.find_parent(['table', 'aside', 'figure']) is not None:
            continue
        if elem.name == 'li' and elem.find_parent('li') is not None:
            continue
        raw = elem.get_text(separator='', strip=False).strip()
        if len(raw.split()) < 6:
            continue
        pieces.append(raw)
    return '\n\n'.join(pieces)


def fetch_article(url):
    """Read the public page, falling back to the matching MediaWiki API."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=40)
        response.raise_for_status()
        return extract_article(response.text)
    except (requests.RequestException, ValueError):
        page = urlparse(url)
        title = unquote(page.path.split('/wiki/', 1)[-1]).replace('_', ' ')
        api_url = f'{page.scheme}://{page.netloc}/w/api.php'
        response = requests.get(api_url,
                                params={'action': 'parse', 'page': title,
                                        'prop': 'text', 'format': 'json', 'formatversion': '2'},
                                headers=HEADERS, timeout=40)
        response.raise_for_status()
        data = response.json()
        if 'parse' not in data:
            raise ValueError(f'Could not retrieve article: {url}')
        return extract_article(data['parse']['text'])


def download_corpus(root=ROOT, overwrite=False):
    root = Path(root)
    sources = json.loads((root / 'sources.json').read_text(encoding='utf-8'))
    corpus = root / 'corpus'
    corpus.mkdir(parents=True, exist_ok=True)
    rows = []
    for entry in sources:
        destination = corpus / entry['file']
        if destination.exists() and not overwrite:
            article = destination.read_text(encoding='utf-8')
            print('Using saved:', entry['file'])
        else:
            article = fetch_article(entry['url'])
            if len(article.split()) < 200:
                raise ValueError(f"{entry['file']}: only {len(article.split())} words. "
                                 'Check the source or extraction; no placeholder content written.')
            destination.write_text(article + '\n', encoding='utf-8')
            print('Downloaded:', entry['file'], '(', len(article.split()), 'words )')
        if len(article.split()) < 200:
            raise ValueError(f"{entry['file']}: only {len(article.split())} words")
        rows.append({
            'filename': entry['file'], 'title': entry['title'],
            'kind': entry['kind'], 'url': entry['url'],
            'license': entry['license'], 'author_history': entry['history'],
            'words': len(article.split()), 'sha256': hashlib.sha256(article.encode('utf-8')).hexdigest(),
        })
    with (root/'CORPUS_SOURCES.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Build the football NLP corpus')
    parser.add_argument('--refresh', action='store_true', help='Redownload source texts, replacing files')
    args = parser.parse_args()
    result = download_corpus(overwrite=args.refresh)
    print('\nCorpus ready:', len(result), 'files; updated', datetime.now(timezone.utc).isoformat())
