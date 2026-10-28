# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four sentences. -->

This community is a subreddit for people visiting New York City. For this
project, I read posts from the subreddit where visitors ask questions and locals share
recommendations about planning a trip or tips getting around, such as events, attractions, food, and
activities in NYC.

<!-- Candidate distinctions after reading most of the posts:
     1. Numbers vs. vague amounts: some posts give and calculate concrete
        numbers (prices, times, distances), while others stay vague ("long,"
        "too much," "pricey").
     2. Location detail: some posts give exact locations and describe the
        surrounding area, while others refer to places only vaguely.
     3. Quick take vs. deep analysis: some posts are short and to the point,
        like a quick reaction or a single fact, while others explain in detail
        the what, why, and how. -->

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `informative`

**Definition:** Advice backed by concrete, checkable details, such as numbers
(prices, travel times, distances, years) or descriptions of what a place/area is like

**Example 1:**
> For some local pubs and bars you can just hang in, I'd suggest the Old Town Tavern on 18th St (operating since 1892, backdrop for a bunch of movies), Pete's Tavern in the Grammercy Park area (operating since 1864, O'Henry wrote stories here, and can be busy), The Whitehorse tavern on Hudson St is a good place to chill (2nd oldest bar since 1880, a favorite with the Beat poets of the 1950s).
If you go south from Washington Square on Macdougal St, there are a bunch of little trattorias and coffee bars that are a good stop. Eataly on the southwest side of Madison Park at 23rd st is an italian food and restaurant market with plenty of choices and places to sit. Good coffees and gelatos.
A bit more upscale with a Parisian cafe flair, consider Steak Frites on 9th ave. Or for an adventure for some good dim sum, try the Nom Wah tea parlor on Doyers St. Its a small very local place that's been around since 1920. You will think you've teleported to a back ally in Hong Kong.
For something a little different, consider a visit to Olifactory on Mott St, where you can design your own perfume.


**Example 2:**
> Might get downvoted but, Roosevelt island is a great spot not too far from JFK and 20 min uber (~$30-$40) to LGA. It has awesome views over Manhattan skyline, waterfront and nice park on the south point with the views both of Manhattan and Long Island City (& Pepsi cola sign). if it's a weekend, F train (Airtrain+E+F) goes directly to the island in like ~45-50 mins from JFK if all schedules align perfectly. If you end up having a bit more time to spare after getting to RI and walk around - you can take a tram to Manhattan and walk a little bit to see townhouses on the Upper East side on 61 and 62nd street decorated for Halloween, and walk 10 mins to Park Avenue for iconic Metlife building view (it all will take like 40-50 mins with 5 min rides on the tram each way).

### `quick_take`

**Definition:** A short, to-the-point reaction or recommendation that may name
a place but gives no numbers and no detail description of the place 

**Example 1:**
>stomach the cost vs stomach the commute. You can always do half and half. Plan hotels on the party nights and reserve

**Example 2:**
>If she likes old buildings I would highly recommend the tenement museum which is near little Italy and Chinatown

### The hardest boundary

**Which two labels:** `informative` vs. `quick_take`, when a short post names a
specific place.

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->
If the post gives at least one concrete, checkable detail about a place, it is
`informative`, even if it is short or opinionated. A detail counts if it is
either a number (price, travel time, distance, year) or a description specific
enough that a reader could picture the place or find their way there (what it
looks like, what it's known for, how to get there). If the post only names a
place, or gives an opinion without saying why, it is a `quick_take`.

Test: remove the place name. If nothing checkable or picturable is left, it's
a `quick_take`.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** https://www.reddit.com/r/visitingnyc/

**How I labelled them:** Pre-labelled with AI and going through all of them to correct as needed. <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. --> 

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| quick_take |  142|57.26%  |
| informative |  106|42.74%  |
| **Total** |  248| 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:*
> I wouldn’t. LIRR trains don’t run as frequently as the trains in the city and you’d have to schedule it out, it sounds like a lot to do every day. I’d do a couple nights in the city and maybe a couple nights with them on the days you want to do Queens and Brooklyn (which you should do, don’t only see Manhattan).
> *Could have been:*
> informative
> *I chose "quick_take", because:* although it names a few places (the LIRR, Queens, Brooklyn, Manhattan), it stays vague — it gives no train frequencies or travel times and no details about what to do in Queens or Brooklyn. It reads as a personal recommendation ("I wouldn't") rather than information the reader can act on.

**2.**
> *The post:*
> I just came back from a 1 week trip to nyc and was staying in Long Island the whole time. Commute is long but doable I just woke up early everyday and headed into the city for a whole day to maximize my time. If you really want to experience the super late night life maybe get a hotel for one or two days, but I think its not such a huge deal to stay in Long Island. I was able to do everything I wanted to do
> *Could have been:*
> quick_take
> *I chose "informative", because:* although it has no useful specifics (the only number is "1 week"), it explains *why* the long commute is doable — waking up early and spending full days in the city — and suggests a concrete alternative (a hotel for a night or two for late-night plans). That firsthand reasoning gives the reader actionable guidance, which tips it from a quick take into informative.

**3.**
> *The post:*
> Long island is not a home base for a New York City vacation. Loads of people in the tri-state area love to delude themselves, and others, that they’re in close proximity to “the city” but they’re simply not. They’re in suburbia and it’s a significant distance away from Manhattan.
> *Could have been:*
> quick_take
> *I chose "informative", because:* it reads like local insight — it corrects a common misconception that Long Island is close to "the city," explaining that it is suburbia and a significant distance from Manhattan. For a visitor deciding where to stay, that context about how far they would be from the center is genuinely useful, even without exact travel times. This kind of insider description is the detail a reader needs to picture how far Long Island really is from the city.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** distilbert-base-uncased

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, seed 42 (three-seed run: 42, 7, 2024)

**Anything I changed from the defaults, and why:** I didn't change anything

**Split sizes:** train 172 / val 38 / test 38. Test split per label: quick_take 22, informative 16.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* "Here are my label definitions and one post that sits between two of them. Make the strongest case for each of the two labels. Don't tell me which one is right and don't rewrite my definitions." with my label definitions and post
- *What came back:* 

Case for informative

The post gives actionable advice with a reason attached. It tells the reader not to use Long Island as a base for a NYC trip, and it explains why: the area is suburban, and it sits a significant distance from Manhattan. That is a description of what the place is like (suburbia, not urban core) and a stated rationale, which your quick take definition says is absent from quick takes. A reader can act on it immediately (book elsewhere) without asking “why not?” The post also corrects a specific misconception, that people in the tri-state area are “close” to the city, so it carries real content beyond a bare verdict. It names no numbers, but the definition says “numbers... or descriptions of what a place is like,” and “suburbia” plus “significant distance” is a description of the place’s character and its relationship to Manhattan. The reasoning is also checkable: anyone can look up Long Island’s distance and transit times to confirm it.

Case for quick take

The post is a short, opinionated reaction. It is one recommendation (don’t stay on Long Island) delivered with attitude (“love to delude themselves”), which is the register of a reaction rather than a guide. It names a place but gives no numbers: no miles, no train times, no prices, no years. “Significant distance” and “suburbia” are vague and generic, not concrete, checkable details, and they don’t describe the place in any way that would let a reader picture it (no mention of the LIRR, towns, or what the commute is like). The reader would still need a follow-up: how far, how long, how do I get in? The “reasoning” is a single assertion restated (“not close because it’s far”), which is closer to emphatic opinion than to supporting explanation. And the post is two sentences long, built around a punchy verdict, which fits “short, to-the-point reaction or recommendation.”

- *What I changed:* I didn't use this to change anything beside to see how my label works. Since it works like I want, so I keep the definition as it is. 

**Moment 2**

- *What I asked for:* A script to collect about 200 comments from r/VisitingNYC and put them into `labels.csv`, skipping deleted/removed comments and AutoModerator posts.
- *What came back:* `collect_comments.py`. Reddit blocks logged-out scripts, so it doesn't pull from Reddit directly. Instead I save each thread's `.json` page from my browser into the `threads/` folder, and the script walks every comment (replies included) and adds each one to `labels.csv` as a row with the `text` filled in and the `label` left blank. Re-running it keeps the rows I've already labelled and only adds new comments.
- *What I changed:* I used the script only to fill in the `text` column. I picked which threads to save and which to delete. 

**Pre-labelling disclosure:** I used AI to pre-label the comments, then reviewed every label myself. Where I disagreed with the AI's label, I changed it and marked the row with "cold" in the `note` column of `labels.csv`.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.526 | 0.816 | +0.289 |
| Macro F1 | 0.525 | 0.813 | +0.288 |
| F1 — `informative` | 0.550 | 0.788 | +0.238 |
| F1 — `quick_take` | 0.500 | 0.837 | +0.337 |

**What I predicted before I looked:** The trained model will have higher number than the baseline model on every measure. 
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:** The baseline is close to a coin flip (0.526 accuracy), and the trained model reaches 0.816, so fine-tuning really learned the difference between the labels. `quick_take` improved the most (+0.337 F1). `informative` is still the weaker label.
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
