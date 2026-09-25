# %% [markdown]
# # JUNE 25th-anniversary analysis — Step 1: build the article inventory
#
# **What this does:** visits every issue page in the funjournal.org archive
# (2002 through Spring 2025), and writes one row per published item to
# `june_inventory.csv`.
#
# **What you need to do:** run each cell from top to bottom
# (in Google Colab: Runtime → Run all). The whole thing takes ~5 minutes
# the first time. Web pages are saved in a `cache/` folder, so re-running
# is fast and doesn't re-download anything.
#
# **What comes out:**
# - `june_inventory.csv` — the master table (open it in Excel / Google Sheets)
# - `june_inventory_flags.csv` — only the rows a human should double-check
# - `june_issue_summary.csv` — number of items per issue, to spot gaps
#
# Issues from Fall 2025 onward live on Scholastica and are **not** covered here.

# %% [markdown]
# ## Settings — the only cell you should normally need to edit

# %%
ARCHIVE_HOME = "https://www.funjournal.org/"

# Issue pages to add even if they're missing from the site's Archives menu.
EXTRA_ISSUE_URLS = []

# Issue pages to skip (e.g., empty placeholder pages).
SKIP_ISSUE_URLS = [
    "https://www.funjournal.org/2025-volume-25-issue-1/",  # empty template page
]

# Newer issues (~2020s) link to an article page rather than straight to the PDF.
# Those pages carry the DOI and abstract, so we visit them too.
FETCH_ARTICLE_PAGES = True

SECONDS_BETWEEN_REQUESTS = 1.0   # be polite to the server
CACHE_DIR = "cache"
OUTPUT_CSV = "june_inventory.csv"

# %% [markdown]
# ## Setup (no need to edit below this line)

# %%
import hashlib
import os
import re
import time
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

HEADERS = {"User-Agent": "JUNE-25th-anniversary-inventory (academic, non-commercial)"}


def fetch_html(url):
    """Download a page, or read it from the cache if we've seen it before."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = hashlib.md5(url.encode()).hexdigest()
    path = os.path.join(CACHE_DIR, key + ".html")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    time.sleep(SECONDS_BETWEEN_REQUESTS)
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    with open(path, "w", encoding="utf-8") as f:
        f.write(resp.text)
    return resp.text


# %% [markdown]
# ## Turning a web page into simple lines of text
#
# The issue pages were made by different people over 20+ years, so their HTML
# varies a lot. Instead of relying on the HTML structure, we flatten each page
# into lines that look like this:
#
#     ## Articles
#     [Title of the article](https://link-to-pdf)
#     By Author A & Author B
#
# and then read those lines in order, like a person would.

# %%
BLOCK_TAGS = {"p", "div", "li", "ul", "ol", "section", "article", "table",
              "tr", "td", "header", "footer", "nav", "blockquote"}
HEADING_TAGS = {"h1": "# ", "h2": "## ", "h3": "## ", "h4": "## "}


def html_to_lines(html):
    soup = BeautifulSoup(html, "lxml")
    for bad in soup(["script", "style", "noscript"]):
        bad.decompose()
    out = []

    def walk(node):
        if isinstance(node, NavigableString):
            out.append(str(node))
            return
        if not isinstance(node, Tag):
            return
        name = node.name
        if name == "br":
            out.append("\n")
            return
        if name in HEADING_TAGS:
            out.append("\n" + HEADING_TAGS[name] + node.get_text(" ", strip=True) + "\n")
            return
        if name == "a" and node.get("href"):
            text = node.get_text(" ", strip=True)
            out.append(f"[{text}]({node['href']})" if text else "")
            return
        if name in BLOCK_TAGS:
            out.append("\n")
        for child in node.children:
            walk(child)
        if name in BLOCK_TAGS:
            out.append("\n")

    walk(soup.body or soup)
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in "".join(out).split("\n")]
    return [ln for ln in lines if ln]


# %% [markdown]
# ## Step A: find every issue page from the site's Archives menu

# %%
ISSUE_LINK_RE = re.compile(
    r"^\[(?P<year>(19|20)\d\d),?\s+Volume\s+(?P<vol>\d+)\s*:?\s*Issue\s+(?P<iss>\d+)\]\((?P<url>[^)]+)\)$",
    re.I,
)


def find_issue_pages(home_lines):
    issues, seen = [], set()
    for ln in home_lines:
        m = ISSUE_LINK_RE.match(ln.lstrip("*- ").strip())
        if not m:
            continue
        url = m["url"]
        if not url.endswith("/"):
            url += "/"
        if url in seen or url in SKIP_ISSUE_URLS:
            continue
        seen.add(url)
        issues.append({"year_label": int(m["year"]), "volume": int(m["vol"]),
                       "issue": int(m["iss"]), "issue_url": url})
    return issues


# %% [markdown]
# ## Step B: read one issue page into rows
#
# Rules the parser follows:
# - `## Something` starts a new section (Editorials, Articles, Media Reviews, …)
# - a line with a link to a PDF or an article page starts a new item
# - a line starting with "by" / "-by" / "By" right after it gives the authors
# - in Media Reviews, "reviewed by" = the JUNE author, plain "by" = author
#   of the book/media being reviewed
# - links or lines mentioning "Supplementary" or "Movie" are counted as
#   supplements, not separate items

# %%
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
SUPPLEMENT_WORDS = re.compile(r"supplement|movie|video|appendix|download pdf", re.I)
PAGE_PREFIX_NAMES = {"A": "article", "E": "editorial", "R": "review",
                     "C": "case study", "T": "technical"}


def is_item_link(text, href):
    """True if this link points to a published item (not nav, not a supplement)."""
    if SUPPLEMENT_WORDS.search(text) or re.search(r"-s\d{2,3}\.pdf$", href, re.I):
        return False
    path = urlparse(href).path.lower()
    if path.endswith(".pdf"):
        return True
    # Newer issues link to an article page such as /volume-23-issue-2-.../name-june-232-a35-a43/
    return "funjournal.org" in href and re.search(r"june-\d+[^/]*\d+/?$", path) is not None


def pages_from_url(href):
    """Pull the first (and, when available, last) page out of a PDF name or article URL."""
    path = urlparse(href).path.rstrip("/").lower()
    last = path.split("/")[-1]
    # Newer article pages: ...-june-232-a35-a43  or  ...-june-232e22-e25  or  a50-55
    m = re.search(r"june-\d+-?([a-z]?)(\d+)-([a-z]?)(\d+)$", last)
    if m:
        prefix = (m[1] or m[3] or "A").upper()
        return prefix, int(m[2]), int(m[4])
    # PDFs: june-12-e1.pdf, june-18-15.pdf, june-23-a35.pdf
    m = re.search(r"june-\d+-([a-z]?)(\d+)\.pdf$", last)
    if m:
        return (m[1] or "A").upper(), int(m[2]), None
    # Early PDFs: LomE1.pdf, GittisA1.pdf
    m = re.search(r"([aecrt])(\d+)\.pdf$", last)
    if m:
        return m[1].upper(), int(m[2]), None
    return None, None, None


def clean_authors(text):
    text = re.sub(r"^[-–—\s]*(reviewed\s+)?by\s+", "", text, flags=re.I)
    return text.strip(" ,;")


def first_author_surname(authors):
    """Best guess at the first author's surname.
    Handles 'AG Gittis', 'CA Paul, EM Goergen', 'Stavnezer AJ', 'Ogilvie, JM', 'Flint, Jr. RW'."""
    if not authors:
        return ""
    first = re.split(r"\s*(?:&|\band\b|\bet al\.?)", authors)[0]
    first = first.split(",")[0].strip()          # first comma-separated piece
    words = [w for w in first.split() if w not in {"Jr.", "Jr", "Sr.", "III", "II"}]
    if not words:
        return ""
    is_initials = lambda w: re.fullmatch(r"[A-Z]{1,3}\.?", w) is not None
    if is_initials(words[0]) and len(words) > 1:   # "AG Gittis"
        return words[-1]
    return words[0]                                # "Stavnezer AJ" or "Ogilvie"


def surname_from_early_pdf(href):
    """Early PDFs are named after the first author, e.g. LomE1.pdf -> 'Lom'."""
    m = re.search(r"/([A-Za-z\-]+?)[AECRT]\d+\.pdf$", href or "")
    return m[1] if m and not m[1].lower().startswith("june") else ""


def parse_issue_lines(lines, issue_meta):
    # Keep only the issue's own content: from its title (# line) to the footer.
    start = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), None)
    if start is None:
        start = next((i for i, ln in enumerate(lines) if ln.startswith("## ")), 0)
    end = next((i for i, ln in enumerate(lines) if i > start and ln.startswith("©")), len(lines))
    lines = lines[start:end]

    rows, section, pending_subtype, current = [], "", "", None
    for ln in lines:
        if ln.startswith("# "):
            continue
        if ln.startswith("## "):
            section, pending_subtype, current = ln[3:].strip(), "", None
            continue

        links = LINK_RE.findall(ln)
        item_links = [(t, h) for t, h in links if is_item_link(t, h)]

        if item_links:
            for title, href in item_links:
                before = ln.split("[" + title + "]")[0]
                prefix, p_start, p_end = pages_from_url(href)
                current = {
                    **issue_meta,
                    "section": section,
                    "subtype": pending_subtype,
                    "title": title.strip(),
                    "authors": "",
                    "reviewed_work_author": "",
                    "page_prefix": prefix,
                    "page_start": p_start,
                    "page_end": p_end,
                    "pdf_url": href if href.lower().endswith(".pdf") else "",
                    "article_page_url": "" if href.lower().endswith(".pdf") else href,
                    "n_supplements": 0,
                }
                # e.g. "Editorial by EP Wiertelak, Editor-in-Chief: [Title](...)"
                m = re.search(r"\bby\s+(.+?)(?:,\s*Editor.*)?:?\s*$", before, re.I)
                if m:
                    current["authors"] = m[1].strip(" :,")
                rows.append(current)
            pending_subtype = ""
            continue

        if current is None:
            # A short label line before an item, e.g. "Book Review"
            if not links and len(ln) < 40:
                pending_subtype = ln.strip("*_ ")
            continue

        # Supplements (linked or just italic text)
        if SUPPLEMENT_WORDS.search(ln):
            current["n_supplements"] += max(1, len(links))
            continue

        low = ln.lower().lstrip("-–— ")
        if low.startswith("reviewed by"):
            current["authors"] = clean_authors(ln)
        elif low.startswith("by "):
            if section.lower().startswith("media") and not current["reviewed_work_author"] \
                    and current["authors"] == "":
                # In media reviews, a plain "by" line names the book's author
                # — unless it's the only author line (fixed up below).
                current["reviewed_work_author"] = clean_authors(ln)
            elif not current["authors"]:
                current["authors"] = clean_authors(ln)
        elif not current["authors"] and not links and len(ln) < 300:
            # Newest pages sometimes list authors with no "By"
            current["authors"] = clean_authors(ln)
        elif not links and len(ln) < 40:
            pending_subtype = ln.strip("*_ ")

    for r in rows:
        # Media review with only a "by" line: that line is probably the reviewer.
        if r["section"].lower().startswith("media") and not r["authors"] and r["reviewed_work_author"]:
            r["authors"], r["reviewed_work_author"] = r["reviewed_work_author"], ""
        r["first_author"] = first_author_surname(r["authors"]) or surname_from_early_pdf(r["pdf_url"])
    return rows


# %% [markdown]
# ## Step C (newer issues): read the article page for DOI, abstract, and PDF

# %%
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"<>)*]+")


def parse_article_lines(lines):
    info = {"doi": "", "abstract": "", "pdf_url_from_page": ""}
    text = "\n".join(lines)
    m = DOI_RE.search(text)
    if m:
        info["doi"] = m[0].rstrip(".,;")
    abs_start = next((i for i, ln in enumerate(lines) if ln.strip().upper() == "ABSTRACT"), None)
    if abs_start is not None:
        body = []
        for ln in lines[abs_start + 1:]:
            if ln.startswith("[") or ln.startswith("©") or ln.upper().startswith("KEY WORDS"):
                break
            body.append(ln)
        info["abstract"] = " ".join(body).strip()
    for t, h in LINK_RE.findall(text):
        if h.lower().endswith(".pdf"):
            info["pdf_url_from_page"] = h
            break
    return info


# %% [markdown]
# ## Step D: quality checks
#
# Rather than silently trusting the parser, every row gets a `flags` column
# listing anything a human should look at. Nothing is deleted.

# %%
def add_flags(df):
    flags = [[] for _ in range(len(df))]
    expected_prefix = {"editorial": "E", "article": "A", "media": "R", "case": "C", "technical": "T"}
    for i, r in enumerate(df.itertuples()):
        if not r.authors:
            flags[i].append("no authors found")
        if r.page_start is None or pd.isna(r.page_start):
            flags[i].append("no page number")
        sec = str(r.section).lower()
        for key, pre in expected_prefix.items():
            if sec.startswith(key) and r.page_prefix and r.page_prefix != pre:
                flags[i].append(f"section '{r.section}' but page prefix {r.page_prefix}")
        if not r.pdf_url:
            flags[i].append("no PDF link")
        if r.section == "":
            flags[i].append("no section heading")
    df["flags"] = ["; ".join(f) for f in flags]

    dup = df.duplicated(subset=["volume", "page_prefix", "page_start"], keep=False) & df["page_start"].notna()
    df.loc[dup, "flags"] = df.loc[dup, "flags"].apply(lambda s: (s + "; " if s else "") + "duplicate volume+page")
    return df


def issue_completeness(issues):
    """List any volume whose issue numbers aren't 1, 2, (3) with no gaps."""
    problems = []
    by_vol = {}
    for it in issues:
        by_vol.setdefault(it["volume"], set()).add(it["issue"])
    for v in range(1, max(by_vol) + 1):
        got = by_vol.get(v, set())
        if not got:
            problems.append(f"Volume {v}: no issues found")
        elif sorted(got) != list(range(1, max(got) + 1)):
            problems.append(f"Volume {v}: issues found = {sorted(got)}")
    return problems


# %% [markdown]
# ## Run everything

# %%
def build_inventory():
    home_lines = html_to_lines(fetch_html(ARCHIVE_HOME))
    issues = find_issue_pages(home_lines)
    for url in EXTRA_ISSUE_URLS:
        issues.append({"year_label": None, "volume": None, "issue": None, "issue_url": url})
    print(f"Found {len(issues)} issue pages.")
    for p in issue_completeness([i for i in issues if i["volume"]]):
        print("  ⚠", p)

    rows = []
    for n, meta in enumerate(sorted(issues, key=lambda d: (d["volume"] or 0, d["issue"] or 0)), 1):
        try:
            lines = html_to_lines(fetch_html(meta["issue_url"]))
        except Exception as e:
            print(f"  ✗ could not read {meta['issue_url']}: {e}")
            continue
        items = parse_issue_lines(lines, meta)
        print(f"[{n}/{len(issues)}] Vol {meta['volume']}({meta['issue']}) {meta['year_label']}: {len(items)} items")
        rows.extend(items)

    df = pd.DataFrame(rows)
    df["doi"], df["abstract"] = "", ""

    if FETCH_ARTICLE_PAGES:
        todo = df.index[df["article_page_url"] != ""]
        print(f"Reading {len(todo)} article pages for DOIs/abstracts…")
        for idx in todo:
            try:
                info = parse_article_lines(html_to_lines(fetch_html(df.at[idx, "article_page_url"])))
            except Exception as e:
                print(f"  ✗ {df.at[idx, 'article_page_url']}: {e}")
                continue
            df.at[idx, "doi"] = info["doi"]
            df.at[idx, "abstract"] = info["abstract"]
            if not df.at[idx, "pdf_url"]:
                df.at[idx, "pdf_url"] = info["pdf_url_from_page"]

    df["page_start"] = df["page_start"].astype("Int64")
    df["page_end"] = df["page_end"].astype("Int64")
    df["item_type_from_page"] = df["page_prefix"].map(PAGE_PREFIX_NAMES)
    df["item_id"] = df.apply(
        lambda r: f"JUNE-{r.volume}-{r.page_prefix or 'X'}{r.page_start if pd.notna(r.page_start) else 'NA'}",
        axis=1)
    df = add_flags(df)

    cols = ["item_id", "year_label", "volume", "issue", "section", "subtype",
            "item_type_from_page", "title", "authors", "first_author",
            "reviewed_work_author", "page_prefix", "page_start", "page_end",
            "doi", "pdf_url", "article_page_url", "issue_url",
            "n_supplements", "abstract", "flags"]
    df = df[cols]
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")  # utf-8-sig opens cleanly in Excel
    df[df["flags"] != ""].to_csv("june_inventory_flags.csv", index=False, encoding="utf-8-sig")
    (df.groupby(["year_label", "volume", "issue", "section"]).size()
       .unstack(fill_value=0).to_csv("june_issue_summary.csv", encoding="utf-8-sig"))

    print(f"\nDone: {len(df)} items → {OUTPUT_CSV}")
    print(f"{(df['flags'] != '').sum()} rows flagged for a human check → june_inventory_flags.csv")
    return df


if __name__ == "__main__":
    inventory = build_inventory()
