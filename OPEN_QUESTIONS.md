# Open questions and decisions

A running list for Ashley and Barbara to discuss. When a question is settled,
move it to **Decisions** with the date and the answer.

## Open questions

5. **Media reviews not indexed in PubMed:** most have no abstract. Include them
   in the topic analysis using the title only, or leave them out?
   - *Waiting on:* Ashley to ask Elaine, Erik, and Bill why media reviews
     aren't indexed in PubMed.
9. **Name the topic groups.** `04_topics.ipynb` found 15 groups of articles
   by their words; the computer doesn't name them. Read the top words and
   example titles in `data/topic_words.csv` and agree on a short name for
   each, then put them in `TOPIC_NAMES` in the notebook's Settings cell.
   Topic 10 ("science, interdisciplinary, curriculum…") looks like a
   catch-all; decide whether to report it as "general/curriculum".
10. **Are these the right eras?** Notebook 04 uses five-volume eras
    (1–5, 6–10, 11–15, 16–20, 21–24). Other options: by decade, or around
    events such as the move to Scholastica or the pandemic.
11. **Automatic groups, or a hand-built list of topics?** The automatic
    groups are a good way to *discover* themes. For the manuscript, we could
    instead define our own list of topics (e.g., "active learning",
    "CUREs", "DEI") with the words that signal each, and count articles
    per topic. That's easier to explain and defend, but takes more of our
    time.

## Notes for the journal (not decisions for us)

- **Wrong DOIs in PubMed** (the publisher can ask NLM to correct them):
  - 22(1) "A Versatile Semester-Long Course-Based Undergraduate Research
    Experience…" is listed with 10.59390/XZQL5300; correct is 10.59390/MEDI5423
  - 22(1) "PopScience: Teaching Students to Communicate Scientific Findings…"
    is listed with 10.59390/KCBV9244; correct is 10.59390/KYOE5906
- **Title typo on the funjournal.org 20(2) issue page:** "Why Students Cheat
  and How Understanding This Can H Reduce…" should read "Can Help Reduce"
  (the article's own page is correct). Corrected for our analysis in
  `manual_fixes.csv`.
- **Wrong pages in PubMed:** 21(2) "Comparing Student Performance in Emergency
  Remote and Face-to-Face Collaborative Learning Courses" (PMID 37588654) is
  listed as A126–A125; the website shows A117–A125. (Corrected for our
  analysis in `manual_fixes.csv`.)

## Decisions

- **2026-09-25 — Count by volume, not calendar year.** Volumes span two
  calendar years (e.g., 1(1) is 2002 and 1(2) is 2003).
- **2026-09-25 — FUN workshop issues:** 8(1) 2008 Macalester, 11(1) 2011
  Pomona, 13(3) 2014 Ithaca, 16(3) 2017, 20(2) 2020 Virtual Meeting, and
  22(2) 2023 Western Washington. 22(3) is *not* a workshop issue.
  Workshop status is tagged per article, since an issue may also contain
  regular articles.
- **2026-09-25 — Workshop articles are counted separately** from the
  per-volume counts, and **included** in the topic analysis.
- **2026-09-25 — Two citation counts per article:** total citations, and
  citations in the first 5 years after publication. Articles younger than
  5 years get a blank 5-year count, not a low one.
- **2026-09-27 — Include 5(2) "The Society for Neuroscience and the
  Undergraduate" (AE Stuart, E12–13).** It's in PubMed (PMID 23495312) but
  listed on funjournal.org without a link, so it's added by hand through
  `EXTRA_ITEMS` in `01_build_inventory.ipynb`.
- **2026-09-27 — Only proceedings issues count as FUN workshop items.**
  5(2) "IFEL TOUR: A Description of the Introduction to FUN Electrophysiology
  Labs Workshop at Bowdoin College…" describes a FUN workshop but is *not* a
  workshop paper. Other articles that describe FUN workshops outside the
  proceedings issues are treated the same way.
- **2026-10-02 — 20(3) is a regular issue, not a workshop issue.** The 2020
  FUN Summer Virtual Meeting proceedings are in 20(2). (Was question 1.)
- **2026-10-02 — Every item type counts in the per-volume counts**
  (articles, editorials, media reviews, case studies, and technical papers;
  interviews are filed as editorials), with the number of each type
  reported as a breakdown.
  Workshop items are still counted separately (see 2026-09-25). In
  `05_figures.ipynb`: `COUNT_ITEM_TYPES` lists all types. (Was question 3.)
- **2026-10-02 — Workshop articles can appear in the top-cited lists**,
  with no separate treatment. In `05_figures.ipynb`:
  `INCLUDE_WORKSHOP_IN_TOP_CITED = True`. (Was question 4.)
- **2026-10-02 — Workshop tagging stays as is:** every item in the six
  proceedings issues (133 items) counts as a workshop item, including
  proceedings introductions, award pieces, and perspectives. (Was question 6.)
- **2026-10-02 — "First 5 years" = the publication year plus the 4 years
  after** (e.g., 2010–2014 for a 2010 item). In `03_citations.ipynb`:
  `YEARS_AFTER_PUBLICATION = 4`. (Was question 7.)
- **2026-10-02 — Report OpenAlex citation counts.** NIH iCite stays in
  `data/june_citations.csv` as a behind-the-scenes cross-check only; the
  figures and tables use OpenAlex. (Was question 8.)
