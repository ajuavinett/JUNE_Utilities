#!/usr/bin/env python3
"""
Fetch article-level citation metrics and usage data for JUNE articles.

Data sources
------------
1. NIH iCite API (https://icite.od.nih.gov/api/pubs)
     citation_count, citations_per_year, relative_citation_ratio,
     nih_percentile, ref_count

2. Europe PMC REST API (https://www.ebi.ac.uk/europepmc/webservices/rest/)
     independent citation count for cross-checking

Note on PMC views / downloads
------------------------------
NCBI does not expose article-level view or download counts through any public
API.  The bulk usage-stats files that used to live on the NCBI FTP were removed
during the 2026 PMC reorganisation, and the new PMC article viewer loads stats
dynamically (JavaScript-rendered, not scrape-friendly).

If you need per-article view/download figures you can:
  a) Export them directly from your Scholastica publisher dashboard.
  b) Request a COUNTER report from NCBI/PMC (email pubmedcentral@ncbi.nlm.nih.gov).
  c) Check the "Article metrics" panel on each PMC article page manually.

This script leaves a Views_PMC and Downloads_PMC column in the output CSV so
you can paste in those numbers once obtained.

Reads PMIDs and PMCIDs from june_pmids.csv (produced by june_pmid_search.py).
Outputs a timestamped CSV with all metrics combined.
"""

import requests
import csv
import time
from datetime import datetime

# ── API endpoints ─────────────────────────────────────────────────────────────
ICITE_API_URL    = "https://icite.od.nih.gov/api/pubs"
EUROPE_PMC_URL   = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


# ── iCite ─────────────────────────────────────────────────────────────────────

def fetch_icite_metrics(pmids):
    """
    Fetch citation metrics from the NIH iCite API (up to 100 PMIDs per call).

    Returns a dict keyed by PMID (str) containing at minimum:
      citation_count, citations_per_year, relative_citation_ratio,
      nih_percentile, ref_count, doi, provisional, year
    """
    if not pmids:
        return {}

    params = {"pmids": ",".join(str(p) for p in pmids)}
    try:
        r = requests.get(ICITE_API_URL, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        return {str(pub["pmid"]): pub for pub in data.get("data", [])}
    except Exception as e:
        print(f"  [iCite] Error: {e}")
        return {}


# ── Europe PMC ────────────────────────────────────────────────────────────────

def fetch_europepmc_citations(pmid):
    """
    Fetch the citation count from Europe PMC for a single PMID.
    Returns an integer or None on failure.
    """
    params = {
        "query":      f"EXT_ID:{pmid} AND SRC:MED",
        "format":     "json",
        "resultType": "lite",
        "pageSize":   1,
    }
    try:
        r = requests.get(EUROPE_PMC_URL, params=params, timeout=20)
        r.raise_for_status()
        results = r.json().get("resultList", {}).get("result", [])
        if results:
            return results[0].get("citedByCount", None)
    except Exception as e:
        print(f"  [EuropePMC] PMID {pmid}: {e}")
    return None


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 80)
    print("JUNE ARTICLE STATS: Citation Metrics")
    print("=" * 80)
    print()

    # ── Load input CSV ─────────────────────────────────────────────────────────
    input_file = "june_pmids.csv"
    try:
        with open(input_file, encoding="utf-8") as f:
            articles = list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"ERROR: {input_file} not found.")
        print("Run june_pmid_search.py first to generate it.")
        return

    print(f"Loaded {len(articles)} articles from {input_file}")
    print()

    pmids = [a["PMID"] for a in articles if a.get("PMID")]

    # ── Step 1: iCite (batch call – all PMIDs at once) ─────────────────────────
    print("─" * 60)
    print("Step 1: Fetching iCite citation metrics …")
    icite_data = fetch_icite_metrics(pmids)
    print(f"  Retrieved data for {len(icite_data)}/{len(pmids)} articles.")
    print()

    # ── Step 2: Europe PMC (per-article) ──────────────────────────────────────
    print("─" * 60)
    print("Step 2: Fetching Europe PMC citation counts …")
    epmc_data = {}
    for pmid in pmids:
        count = fetch_europepmc_citations(pmid)
        epmc_data[pmid] = count
        status = count if count is not None else "not found"
        print(f"  PMID {pmid}: {status} citation(s)")
        time.sleep(0.3)   # polite rate limiting
    print()

    # ── Step 3: Combine & output ───────────────────────────────────────────────
    print("─" * 60)
    print("Step 3: Combining results …")

    results = []
    for article in articles:
        pmid  = article.get("PMID", "")
        pmcid = article.get("PMC_ID", "")

        ic = icite_data.get(pmid, {})
        ep = epmc_data.get(pmid)

        # Round floats for readability
        def fmt_float(v, places=2):
            try:
                return round(float(v), places) if v != "" and v is not None else ""
            except (TypeError, ValueError):
                return v

        results.append({
            # ── Identifiers & metadata ──
            "PMID":                    pmid,
            "PMC_ID":                  pmcid,
            "Year":                    article.get("Year", ""),
            "Author":                  article.get("Author", ""),
            "Title":                   article.get("Title", ""),
            "Category":                article.get("Category", ""),
            "DOI":                     ic.get("doi", ""),
            # ── iCite citation metrics ──
            "iCite_Citation_Count":    ic.get("citation_count", ""),
            "iCite_Citations_Per_Year": fmt_float(ic.get("citations_per_year")),
            "iCite_RCR":               fmt_float(ic.get("relative_citation_ratio")),
            "iCite_NIH_Percentile":    fmt_float(ic.get("nih_percentile")),
            "iCite_Ref_Count":         ic.get("ref_count", ""),
            "iCite_Provisional":       ic.get("provisional", ""),
            # ── Europe PMC ──
            "EuropePMC_Citation_Count": ep if ep is not None else "",
            # ── PMC usage (fill manually from Scholastica / NCBI COUNTER report) ──
            "Views_PMC":               "",   # paste from NCBI COUNTER report or PMC article page
            "Downloads_PMC":           "",   # paste from NCBI COUNTER report or PMC article page
        })

    # ── Save CSV ──────────────────────────────────────────────────────────────
    timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"june_article_stats_{timestamp}.csv"

    fieldnames = [
        "PMID", "PMC_ID", "Year", "Author", "Title", "Category", "DOI",
        "iCite_Citation_Count", "iCite_Citations_Per_Year", "iCite_RCR",
        "iCite_NIH_Percentile", "iCite_Ref_Count", "iCite_Provisional",
        "EuropePMC_Citation_Count",
        "Views_PMC", "Downloads_PMC",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"  Saved results to: {output_file}")
    print()

    # ── Summary table ─────────────────────────────────────────────────────────
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"{'Author':<22} {'Year'} {'iCite Cites':>11} {'Cites/yr':>9} "
          f"{'RCR':>6} {'NIH%':>6} {'EPMC':>6}")
    print("-" * 72)

    for r in sorted(results, key=lambda x: (x.get("Year", ""), x.get("Author", "")), reverse=True):
        print(
            f"{r['Author']:<22} {r['Year']} "
            f"{str(r['iCite_Citation_Count']):>11} "
            f"{str(r['iCite_Citations_Per_Year']):>9} "
            f"{str(r['iCite_RCR']):>6} "
            f"{str(r['iCite_NIH_Percentile']):>6} "
            f"{str(r['EuropePMC_Citation_Count']):>6}"
        )

    print()
    print("Columns in output CSV:")
    print("  iCite_RCR          – Relative Citation Ratio (field-normalised impact)")
    print("  iCite_NIH_Percentile – Percentile rank vs. all NIH-funded papers (same year)")
    print("  iCite_Provisional   – True if citation data is still provisional (<2 yrs old)")
    print("  Views_PMC / Downloads_PMC – left blank; fill from NCBI COUNTER report or")
    print("                              Scholastica dashboard export.")
    print()
    print(f"Full results: {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
