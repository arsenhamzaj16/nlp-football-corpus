# Football Media Corpus — NLP Semester Project

**Course:** Natural Language Processing  
**Language:** English  
**Topic:** Football (soccer) media  
**Assignment:** NLP Tutorial 2, Part 2 — Your Corpus (Tasks A–H)

This repository contains a group corpus and a Jupyter notebook comparing three tokenizers: Python `split()`, NLTK, and spaCy. The texts are collected from openly licensed football sources, and the same corpus is reused across the analysis. More football documents can be added during the semester.

## Corpus

The starter collection is selected as follows:

| Type | Number | Sources |
|---|---:|---|
| Encyclopedia articles | 2 | English Wikipedia (association football and FIFA World Cup) |
| Match reports | 3 | English Wikinews (UEFA Champions League and 2018 FIFA World Cup) |
| Learning guides | 3 | English Wikibooks (football basics, history, leagues and teams) |
| **Total** | **8** | **Three different types** |

Every file must contain at least **200 words**, use **UTF-8**, and stay **uncleaned** for this lab: numbers, punctuation, dates, abbreviations, and other difficult characters must not be normalized or removed. Text is extracted from source HTML into visible article paragraphs; HTML layout and images are excluded. The downloader does not artificially insert tokens or manufacture text.

The manifest in [`sources.json`](sources.json) records the title, URL, article-author history, genre, and reuse license for all eight sources. [`ATTRIBUTION.md`](ATTRIBUTION.md) includes links and license information. The corpus texts are *not* the group's original writing; attribution remains with the Wikimedia contributors.

## Repository layout

```text
football-nlp-corpus/
├── corpus/                         # eight UTF-8 text files after collecting sources
├── notebooks/
│   └── football_corpus_analysis.ipynb
├── scripts/
│   ├── corpus_builder.py
│   └── validate_corpus.py
├── tests/
│   └── test_project.py
├── .github/workflows/checks.yml
├── sources.json
├── ATTRIBUTION.md
├── requirements.txt
└── README.md
```

## Run the project locally

Using Python 3.11 or later:

```bash
python -m pip install -r requirements.txt
python scripts/corpus_builder.py
python scripts/validate_corpus.py
jupyter notebook notebooks/football_corpus_analysis.ipynb
```

If Jupyter is not installed locally, install it with `python -m pip install notebook`, or open the notebook in Google Colab. **The notebook can also download missing source files itself** when opened alone in Colab. For GitHub tracking, however, download the texts on your own machine and commit the generated `corpus/*.txt` and `CORPUS_SOURCES.csv` files.

In the notebook, use **Run all**. It completes Tasks A–H and prints comparisons, tables, and short "Output explanation" notes. Output cells depend on the downloaded source snapshots, so no token counts or conclusions are faked in the uploaded notebook.

### Why source text is not included in the initial ZIP

This build environment could not access the pages directly to download and verify them. Instead, the project includes the exact URLs and an automatic downloader that will save the eight real articles on the first successful network-connected run, with a minimum-word check. Until that happens, the GitHub repository has the manifest and notebook, but **not the completed corpus**. Do not claim that the downloaded files are already present. No fake articles have been substituted.

## Task coverage

- **A:** One row for each source; genre, link, character count, whitespace tokens; three-sentence description.
- **B:** Search difficult strings, show categories and examples, compare difficulty by genre, select five difficult cases.
- **C:** Compare `split()`, NLTK, and spaCy across all eight texts (tokens, types, type/token ratio, punctuation tokens).
- **D:** Count whitespace tokens with leading/trailing punctuation and show the fifteen most frequent.
- **E:** Show sentences around five hard strings, compare all three tokenizers, and give a preference.
- **F:** Compare the five sentence-level token-count differences between NLTK and spaCy, with likely explanations.
- **G:** Mean, median and five longest sentence strings.
- **H:** English Wikipedia introduction for the 2022 FIFA World Cup, five differences where present, source link, saved extra `.txt` file.
- **Final questions:** Most difficult text type, tokenizer choice, and what was surprising.

**Important:** The auto-generated "our choice" columns are preliminary group judgements. For a course discussion, review the actual printed examples and change the judgement if the tokenizer does not split a particular expression correctly. Task F also reports *possible* causes, not guaranteed explanations.

## Working as a group on GitHub

The repository should be created as a **new repository**, separate from unrelated software projects.

1. One member creates a GitHub repository, for example `football-nlp-corpus`.
2. Every group member is added under **Settings → Collaborators**.
3. Commit the starter notebook and manifest.
4. Run the downloader, check the texts, and commit the eight source files as a separate commit.
5. Each member works on a separate branch and opens a pull request for review.
6. Continue adding new texts and analysis notebooks through the semester, using descriptive commit messages.

Example commits:

```text
Initialize football NLP corpus project
Collect eight licensed football source texts
Complete corpus statistics and tokenizer comparison
Review five difficult tokenization cases
Add Wiki summary and final discussion
```

Basic Git commands from the project folder (replace `YOUR_USERNAME`):

```bash
git init
git add .
git commit -m "Initialize football NLP corpus project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/football-nlp-corpus.git
git push -u origin main

# After the texts have been downloaded and checked:
git add corpus CORPUS_SOURCES.csv
git commit -m "Collect eight football corpus documents"
git push
```

## Verification

```bash
python -m pytest -q
python scripts/validate_corpus.py
```

CI checks the source manifest and notebook validity on each push. When downloaded corpus files are present, it also verifies that there are eight documents across three genres, each with 200+ whitespace words. It does not claim to check the correctness of human judgements in the discussions.

## Academic and licensing notes

Textual analysis is our work, but the Wikimedia articles remain attributable to their authors. Consult the source URLs and **View history** links in `sources.json` for contributors and source-specific licensing details. Do not paste restricted newspaper articles into the repository. We retain source details and do not silently replace unreachable pages with generated stories.