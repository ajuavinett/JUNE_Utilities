# Open questions and decisions

A running list for Ashley and Barbara to discuss. When a question is settled,
move it to **Decisions** with the date and the answer.

## Open questions

**Name the topic groups.** `04_topics.ipynb` found 15 groups of articles
   by their words; the computer doesn't name them. Read the top words and
   example titles in `data/topic_words.csv` and agree on a short name for
   each, then put them in `TOPIC_NAMES` in the notebook's Settings cell.
   Topic 10 ("science, interdisciplinary, curriculum…") looks like a
   catch-all; decide whether to report it as "general/curriculum".
10. **Are these the right eras?** Notebook 04 uses five-volume eras
    (1–5, 6–10, 11–15, 16–20, 21–24). Other options: by decade, or around
    events such as the move to Scholastica or the pandemic.
    - yes this is fine
11. **Check the topics in `topic_checks.csv`** (notebook 07, the
    hand-built topic list). One row per article (508), with the topics the
    word search suggests. Leave `topics` empty to accept the suggestion, or
    write the right topics (separated by "; ") or `none`, and write `yes` in
    `checked`. Also review the 18 topic definitions and word lists in
    `TOPICS` in the notebook's Settings. Broad topics to watch: Curriculum &
    program design (129 articles), Active learning (112), and Sensation &
    perception ("sensory" alone matches 39).
12. **Check the CUREs in `cure_themes.csv`.** Notebook 06 found 24 candidate
    articles; 17 count as CUREs for now (named in their title or keywords).
    For each row, fill in `is_cure` (yes/no), correct the suggested SfN
    `themes`, and mark `checked` = yes. Some named ones may not be CUREs
    themselves (e.g., 21(1) notes on the 2022 SfN teaching workshop, 22(2)
    microPublication Biology). Add rows for CUREs the search missed,
    especially course-based research described before the term "CURE"
    caught on (~2015).
13. **Which SfN theme list?** Notebook 06 uses SfN's current list (2025:
    11 themes, A–K). The list used through 2024 had 10 themes (A–J),
    without separate aging/degeneration and neuroimmunity/injury themes.
14. **Check the organisms in `organism_checks.csv`.** One row per article
    that names any organism (353 articles; 214 with suggested organisms).
    Correct the `organisms` column where the suggestion is wrong (delete or
    add names, separated by "; "), and write `yes` in `checked`. The
    suggestions for "Students as their own subjects" need the most care:
    they catch nearly every real self-experiment lab but include some that
    aren't (outreach programs, courses that only mention EEG); the
    `evidence` column shows the phrase behind each one. Short articles that
    name their organism only once or twice are missed (e.g., the 10(1)
    Golgi-Cox mouse lab, already corrected).
15. **Check the computational labs in `computational_checks.csv`.** One row
    per article the word search finds (101 articles; 71 featured, which are
    the ones in Figure 6 for now). Correct the `kinds` column (delete or add
    kinds, separated by "; "; empty = not a computational lab), and write
    `yes` in `checked`. Some first matches look doubtful, e.g. "Programming &
    coding" first in a 4(2) frog auditory electrophysiology lab, and "Open
    data & databases" first in a 5(1) fMRI exercise. Add rows for articles
    the search missed.

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
  FUN Summer Virtual Meeting proceedings are in 20(2). (Was question 1.)
- **2026-10-02 — Every item type counts in the per-volume counts**
  (articles, editorials, media reviews, case studies, and technical papers;
  interviews are filed as editorials), with the number of each type
  reported as a breakdown.
  Workshop items are included, each under its own type (see 2026-09-25). In
  `05_figures.ipynb`: `COUNT_ITEM_TYPES` lists all types. (Was question 3.)
- **2026-10-04 — Per-volume counts include FUN workshop items**, each
  counted under its own item type (article, editorial, review). This
  replaces "counted separately" (2026-09-25) for Figure 1 and Table 1;
  Table 1 also lists how many items per volume are workshop items, and
  workshop totals stay in Figure 2.
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
  Candidates are confirmed by hand in `organism_checks.csv`.
- **2026-10-04 — Topics: use a hand-built list** (`07_topic_list.ipynb`)
  rather than only the automatic groups from Step 4. 18 topics, each with
  a definition and word list; "general pedagogy" is split into active
  learning, curriculum & program design, and assessment. An article can
  have several topics, and a topic counts if its words are in the title,
  keywords, or abstract. (Was question 11.)
