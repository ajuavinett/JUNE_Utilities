# JUNE_Utilities
Utilities for curating information about J Undergrad Neuro Ed papers

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ajuavinett/JUNE_Utilities/blob/main/01_build_inventory.ipynb)

--

This is the working repository for a 25th anniversary issue manuscript about *JUNE*. 

The workflow is a series of numbered notebooks. Run them in order; each one reads the CSV files the previous one wrote to `data/`. Click a notebook's name to open it in Google Colab (run its first code cell there to download the project files).

| Notebook | What it does | Writes |
|---|---|---|
| [`01_build_inventory.ipynb`](https://colab.research.google.com/github/ajuavinett/JUNE_Utilities/blob/main/01_build_inventory.ipynb) | Lists every JUNE item from funjournal.org (2002–Spring 2025) and CrossRef (Scholastica, Fall 2025 on) | `data/june_inventory.csv` |
| [`02_match_pubmed.ipynb`](https://colab.research.google.com/github/ajuavinett/JUNE_Utilities/blob/main/02_match_pubmed.ipynb) | Matches each item to PubMed; adds PubMed IDs, page numbers, abstracts, keywords, and CrossRef-checked DOIs. Hand corrections go in `manual_fixes.csv`. | `data/june_matched.csv`, `data/needs_review.csv` (the one file to review), `data/matching_details.csv` |
| [`03_citations.ipynb`](https://colab.research.google.com/github/ajuavinett/JUNE_Utilities/blob/main/03_citations.ipynb) | Total citations and citations in the first 5 years (OpenAlex, with NIH iCite as a cross-check) | `data/june_citations.csv` |
| [`04_topics.ipynb`](https://colab.research.google.com/github/ajuavinett/JUNE_Utilities/blob/main/04_topics.ipynb) | Keyword counts and automatic topic groups (from titles, keywords, and abstracts), by era | `data/june_topics.csv`, `data/topic_words.csv`, `data/keyword_counts.csv` |
| [`05_figures.ipynb`](https://colab.research.google.com/github/ajuavinett/JUNE_Utilities/blob/main/05_figures.ipynb) | Figures and tables for the manuscript; choices still under discussion are settings | `figures/` (PNG + PDF), `tables/` (CSV) |

Questions still to settle, and decisions already made, are in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).
