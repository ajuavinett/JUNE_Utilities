# Open questions and decisions

A running list for Ashley and Barbara to discuss. When a question is settled,
move it to **Decisions** with the date and the answer.

## Open questions

1. **Is 20(3) a workshop issue?** It doesn't look like one: its editorials are
   the 20th-anniversary editor-in-chief piece and opinion pieces, not a
   proceedings introduction. Leaning no.
3. **What counts as an "article" in the per-volume counts?** Research and
   teaching articles only, or also editorials, media reviews, interviews,
   and case studies? (We can report each type separately either way.)
   The Editorials section also holds items that aren't scholarship, such
   as award announcements, "Call for JUNE Editorial Board Members", and
   SfN meeting reports.
4. **Should workshop articles appear in the top-cited list?** Several 11(1)
   workshop papers (2012) are among the most-cited JUNE papers overall.
5. **Media reviews not indexed in PubMed:** most have no abstract. Include them
   in the topic analysis using the title only, or leave them out?
6. **Which items in the workshop issues count as workshop items?** Right now
   every item in those issues is tagged (128 items across 6 issues). That
   includes proceedings introductions, award pieces such as "The 2014 FUN
   Achievement Award" and "Jeanne Narum: A Lifetime of Achievement", and
   perspectives. Are any of these, or any regular articles in those issues,
   *not* workshop items? To review, filter `data/june_inventory.csv` on
   `is_fun_workshop`.
7. **How exactly should "first 5 years" be defined?** Notebook 03 currently
   counts citing papers published in the item's publication year or the 4
   years after (e.g., 2010–2014 for a 2010 item), and leaves the count blank
   for items published in 2022 or later. Alternatives: the 5 years *after*
   publication (2011–2015), or 60 months from the exact publication date.
   (The length of the window is `YEARS_AFTER_PUBLICATION` in the notebook's
   Settings cell; the other options need a small code change.)
8. **Which citation source do we report?** OpenAlex (counts citations from
   all kinds of scholarly works, including books, theses, and preprints) is
   the main count. NIH iCite (only papers in PubMed) is recorded as a
   cross-check; the two rank items very similarly (rank correlation 0.94).
   Report OpenAlex only, or both?
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
