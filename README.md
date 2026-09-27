# JUNE_Utilities
Utilities for curating information about J Undergrad Neuro Ed papers

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ajuavinett/JUNE_Utilities/blob/main/01_build_inventory.ipynb)

--

This is the working repository for a 25th anniversary issue manuscript about *JUNE*. 

The workflow is a series of numbered notebooks. Run them in order; each one reads the CSV files the previous one wrote to `data/`.

| Notebook | What it does | Writes |
|---|---|---|
| `01_build_inventory.ipynb` | Lists every JUNE item from funjournal.org (2002–Spring 2025) and CrossRef (Scholastica, Fall 2025 on) | `data/june_inventory.csv` |
| `02_match_pubmed.ipynb` *(next)* | Adds PubMed IDs, page numbers, abstracts, and keywords | |
| `03_citations.ipynb` *(planned)* | Total citations and citations in the first 5 years (OpenAlex, iCite) | |
| `04_topics.ipynb` *(planned)* | Topics from keywords, titles, and abstracts | |
| `05_figures.ipynb` *(planned)* | Figures and tables for the manuscript | |

Questions still to settle, and decisions already made, are in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).
