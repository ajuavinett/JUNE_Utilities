# Open questions and decisions

A running list for Ashley and Barbara to discuss. When a question is settled,
move it to **Decisions** with the date and the answer.

## Open questions

1. **Is 20(3) a workshop issue?** It doesn't look like one: its editorials are
   the 20th-anniversary editor-in-chief piece and opinion pieces, not a
   proceedings introduction. Leaning no.
2. **Do other FUN workshop writeups count?** A few articles describe FUN workshops
   but aren't in a proceedings issue, e.g. 5(2) "IFEL TOUR: … Introduction to FUN
   Electrophysiology Labs Workshop at Bowdoin College". Count them as workshop
   articles, or only the proceedings issues?
3. **What counts as an "article" in the per-volume counts?** Research and
   teaching articles only, or also editorials, media reviews, interviews,
   and case studies? (We can report each type separately either way.)
   The Editorials section also holds items that aren't scholarship, such
   as award announcements, "Call for JUNE Editorial Board Members", and
   SfN meeting reports.
6. **Which items in the workshop issues count as workshop items?** Right now
   every item in those issues is tagged (128 items across 6 issues). That
   includes proceedings introductions, award pieces such as "The 2014 FUN
   Achievement Award" and "Jeanne Narum: A Lifetime of Achievement", and
   perspectives. Are any of these, or any regular articles in those issues,
   *not* workshop items? To review, filter `data/june_inventory.csv` on
   `is_fun_workshop`.

## Notes for the journal (not decisions for us)

- **funjournal.org link error in 20(2):** "Convening the Undergraduate
  Neuroscience Education Community in a Period of Rapid Change" links to the
  E21 introduction's page and PDF instead of its own (E25–E28, per PubMed).
4. **Should workshop articles appear in the top-cited list?** Several 11(1)
   workshop papers (2012) are among the most-cited JUNE papers overall.
5. **Media reviews not indexed in PubMed:** most have no abstract. Include them
   in the topic analysis using the title only, or leave them out?

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
