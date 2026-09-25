#!/usr/bin/env python3
"""
Fetch citation counts and metadata for all JUNE articles registered with CrossRef.

Uses the CrossRef REST API (https://api.crossref.org) with the FUN member ID
(38466) and DOI prefix 10.59390 to retrieve all works and their citation counts.

CrossRef resolution statistics (DOI click counts) are NOT available via the
public API — those are in your monthly member email and the member portal at
https://doi.crossref.org.  This script collects everything CrossRef DOES expose
publicly:
  - is-referenced-by-count  (citations received)
  - reference-count         (references made in the article)
  - title, authors, type, volume, issue, page, published date

Output: timestamped CSV  june_crossref_citations_YYYYMMDD_HHMMSS.csv

Polite API usage: tool name + email are sent in the User-Agent header so
CrossRef can contact you if there's a problem. No API key needed.
"""

import requests
import csv
import time
from datetime import datetime

# ── Config ─────────────────────────────────────────────────────────────────────
CROSSREF_API   = "https://api.crossref.org/works"
MEMBER_ID      = "38466"          # Faculty for Undergraduate Neuroscience
CONTACT_EMAIL  = "ashleyjuavinett@gmail.com"
PAGE_SIZE      = 100              # CrossRef max rows per request
POLITE_DELAY   = 0.5             # seconds between paginated requests

HEADERS = {
    "User-Agent": f"JUNE-citation-tool/1.0 (mailto:{CONTACT_EMAIL})"
}


# ── Fetch ───────────────────────────────────────────────────────────────────────

def fetch_all_works():
    """
    Page through all CrossRef works for JUNE (member 38466) and return
    a flat list of raw work dicts.
    """
    all_items = []
    offset    = 0

    while True:
        params = {
            "filter":  f"member:{MEMBER_ID}",
            "rows":    PAGE_SIZE,
            "offset":  offset,
            "sort":    "published",
            "order":   "desc",
        }

        try:
            r = requests.get(CROSSREF_API, params=params, headers=HEADERS, timeout=30)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"  [CrossRef] Request error at offset {offset}: {e}")
            break

        msg   = r.json()["message"]
        items = msg["items"]
        total = msg["total-results"]

        if offset == 0:
            print(f"  Total works in CrossRef: {total}")

        all_items.extend(items)
        print(f"  Fetched {len(all_items)}/{total} …")

        if len(all_items) >= total or not items:
            break

        offset += PAGE_SIZE
        time.sleep(POLITE_DELAY)

    return all_items


# ── Parse ───────────────────────────────────────────────────────────────────────

def parse_work(item):
    """
    Extract the fields we care about from a CrossRef work record.
    """
    # Title
    title = " ".join(item.get("title", [])).strip()

    # Authors: "Last, First; Last, First; …"
    authors_raw = item.get("author", [])
    authors = "; ".join(
        f"{a.get('family', '')} {a.get('given', '')}".strip()
        for a in authors_raw
    )

    # Published year (prefer published-online, fall back to issued)
    pub = item.get("published-online") or item.get("published") or item.get("issued") or {}
    date_parts = pub.get("date-parts", [[None]])
    year  = date_parts[0][0] if date_parts and date_parts[0] else ""
    month = date_parts[0][1] if date_parts and len(date_parts[0]) > 1 else ""

    return {
        "DOI":              item.get("DOI", ""),
        "URL":              item.get("URL", ""),
        "Type":             item.get("type", ""),
        "Year":             year,
        "Month":            month,
        "Volume":           item.get("volume", ""),
        "Issue":            item.get("issue", ""),
        "Page":             item.get("page", ""),
        "Title":            title,
        "Authors":          authors,
        "Citations_CrossRef": item.get("is-referenced-by-count", 0),
        "References_Count": item.get("reference-count", 0),
    }


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 80)
    print("JUNE CrossRef Citation Data")
    print("=" * 80)
    print()

    print("Fetching all works from CrossRef …")
    raw_works = fetch_all_works()
    print(f"  Done — {len(raw_works)} works retrieved.")
    print()

    works = [parse_work(w) for w in raw_works]

    # ── Save CSV ────────────────────────────────────────────────────────────────
    timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"june_crossref_citations_{timestamp}.csv"

    fieldnames = [
        "DOI", "URL", "Type", "Year", "Month",
        "Volume", "Issue", "Page",
        "Title", "Authors",
        "Citations_CrossRef", "References_Count",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(works)

    print(f"Saved {len(works)} records to: {output_file}")
    print()

    # ── Summary ─────────────────────────────────────────────────────────────────
    total_citations = sum(w["Citations_CrossRef"] for w in works)
    cited_works     = [w for w in works if w["Citations_CrossRef"] > 0]

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"  Total articles in CrossRef : {len(works)}")
    print(f"  Articles with ≥1 citation  : {len(cited_works)}")
    print(f"  Total citations (all works): {total_citations}")
    print()

    if cited_works:
        print(f"  {'Citations':>9}  {'Year'}  Title")
        print("  " + "-" * 70)
        for w in sorted(cited_works, key=lambda x: x["Citations_CrossRef"], reverse=True):
            print(f"  {w['Citations_CrossRef']:>9}  {str(w['Year']):<4}  {w['Title'][:60]}")

    print()
    print(f"Full results: {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
