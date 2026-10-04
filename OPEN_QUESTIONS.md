# Open questions and decisions

A running list for Ashley and Barbara to discuss. When a question is settled,
move it to **Decisions** with the date and the answer.

## Open questions

- **Check `hand_checks.csv`** — one file, one row per article (508), for
  every hand check in notebooks 06 and 07. For each question there's a
  `(suggested)` column from the word search and an answer column: leave the
  answer empty to accept the suggestion, or write what's right (separated
  by "; ") or `none`. Write `yes` in `checked` once you've checked the
  whole row. What to watch for:
  - **Organisms** (`organisms`): the "Students as their own subjects"
    suggestions need the most care: they catch nearly every real
    self-experiment lab but include some that aren't (outreach programs,
    courses that only mention EEG); `organisms: self-experiment evidence`
    shows the phrase behind each. Short articles that name their organism
    only once or twice are missed (e.g., the 10(1) Golgi-Cox mouse lab,
    already corrected).
  - **Computational labs** (`computational`): 71 articles suggested. Some
    first matches look doubtful, e.g. "Programming & coding" first in a
    4(2) frog auditory electrophysiology lab, and "Open data & databases"
    first in a 5(1) fMRI exercise. `computational: in abstract only`
    lists kinds that count only if you add them.
  - **CUREs** (`CURE`, `CURE themes`): 24 candidates; 15 count for now
    (named in their title or keywords, `yes`), abstract-only ones don't
    (`maybe`), and two named ones are marked `no` (see Decisions). Write
    `yes`/`no` to decide, and correct the SfN theme letters. Write `yes`
    for CUREs the search missed, especially course-based research
    described before the term caught on (~2015).
  - **Topics** (`topics`): also review the 18 topic definitions and word
    lists in `TOPICS` in notebook 07's Settings. Broad topics to watch:
    Curriculum & program design (129 articles), Active learning (112), and
    Sensation & perception ("sensory" alone matches 39).

## Notes for the journal (not decisions for us)
- **Media reviews not indexed in PubMed:** most have no abstract. Include them
   in the topic analysis using the title only, or leave them out?
   - *Waiting on:* Ashley to ask Elaine, Erik, and Bill why media reviews
     aren't indexed in PubMed.
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
- **2026-09-25, revised 2026-10-04 — Workshop items are counted separately
  only to show how many workshop issues and items JUNE has published**
  (Figure 2, table 2). Otherwise they're **included in every count**:
  items per volume (Figure 1), citations, top-cited lists, topics,
  organisms, computational labs, and CUREs.
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
  FUN Summer Virtual Meeting proceedings are in 20(2).
- **2026-10-02 — Every item type counts in the per-volume counts**
  (articles, editorials, media reviews, case studies, and technical papers;
  interviews are filed as editorials), with the number of each type
  reported as a breakdown.
  Workshop items are included, each under its own type (see 2026-09-25). In
  `05_figures.ipynb`: `COUNT_ITEM_TYPES` lists all types.
- **2026-10-04 — Per-volume counts include FUN workshop items**, each
  counted under its own item type (article, editorial, review). This
  replaces "counted separately" (2026-09-25) for Figure 1 and Table 1;
  Table 1 also lists how many items per volume are workshop items, and
  workshop totals stay in Figure 2.
- **2026-10-02 — Workshop articles can appear in the top-cited lists**,
  with no separate treatment. In `05_figures.ipynb`:
  `INCLUDE_WORKSHOP_IN_TOP_CITED = True`.
- **2026-10-02 — Workshop tagging stays as is:** every item in the six
  proceedings issues (133 items) counts as a workshop item, including
  proceedings introductions, award pieces, and perspectives.
- **2026-10-02 — "First 5 years" = the publication year plus the 4 years
  after** (e.g., 2010–2014 for a 2010 item). In `03_citations.ipynb`:
  `YEARS_AFTER_PUBLICATION = 4`.
- **2026-10-02 — Report OpenAlex citation counts.** NIH iCite stays in
  `data/june_citations.csv` as a behind-the-scenes cross-check only; the
  figures and tables use OpenAlex.
- **2026-10-03 — Model organisms: one yes/no per organism per article —
  does the article include an activity with it?** Anything counts: live
  animals or behavior, dissections and tissue, data or images from the
  organism, humans as participants, and plants and algae. Organisms are
  searched in each article's full text (PDF, reference list removed), not
  just the abstract. PDFs are saved in `pdfs/` on Ashley's computer, not on
  GitHub.
- **2026-10-04 — Humans count only as "Students as their own subjects":**
  lab activities where students experiment on themselves or on each other
  (lab partners, classmates). Not counted: analyzing existing human data
  (e.g., fMRI or PET datasets), courses that only mention a technique, and
  students testing other people (e.g., middle schoolers in outreach).
  Candidates are confirmed by hand in `hand_checks.csv`.
- **2026-10-04 — Topics: use a hand-built list** (`07_topic_list.ipynb`)
  rather than only the automatic groups from Step 4. 18 topics, each with
  a definition and word list; "general pedagogy" is split into active
  learning, curriculum & program design, and assessment. An article can
  have several topics, and a topic counts if its words are in the title,
  keywords, or abstract.
- **2026-10-04 — The automatic topic groups (Step 4) are exploratory only.**
  We won't name them; the manuscript will most likely use our own topic
  list (Step 7).
- **2026-10-04 — Keep the five-volume eras** (1–5, 6–10, 11–15, 16–20,
  21–24) for all by-era results.
- **2026-10-04 — Use SfN's current theme list** (2025: 11 themes, A–K)
  for CURE themes.
- **2026-10-04 — Two articles that name CUREs aren't CUREs:** 21(1)
  "Teaching Neuroscience: Reviving Neuroanatomy, Notes on the 2022 SfN
  Professional Development Workshop on Teaching" and 22(2) "microPublication
  Biology: An Introduction to Publishing and Teaching…". Marked `no` in the
  `CURE` column of `hand_checks.csv`.
