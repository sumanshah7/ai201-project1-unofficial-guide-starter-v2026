# The Unofficial Guide

Suman Kumar Sah — corpus: city_guides

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

The Unofficial Guide answers travel questions about `city_guides` — fourteen
documents covering nine fictional towns and five topics that cut across all of
them (eating, walking, regional transport, seasons, accessibility). It answers
concrete, logistics-shaped questions a visitor would actually ask: how to get
somewhere without a car, when a town is worth visiting, how late a kitchen
stays open, when a parking lot fills up. Every answer names the document(s) it
came from, and a question the corpus doesn't cover (world capitals, car
maintenance, medication dosages) gets an honest refusal instead of a guess.

## Chunking Strategy

**Chunk size:** section-based, not a fixed count — see below. 900 characters
is the ceiling before an oversized section gets sub-split, and the shortest
chunk a section may stand as on its own is 180 characters.
**Overlap:** 150 characters, only used on the rare section that needs
sub-splitting (the longest single section in the corpus is 711 characters, so
this almost never fires).

Every `city_guides` document is organized into labelled `## ` sections —
Getting there, Eat and drink, When to go, and so on — and in Milestone 1 the
starter's fixed 800-character window sliced straight through those headings:
14 documents came out as 51 chunks with no regard for where a section started
or ended. Reading the documents made the fix obvious — split on the heading
structure the documents already have, not on a character count.

`split_documents()` in `chunker.py` now splits each document at its `##`
headings. Two adjustments on top of that:

- A few documents (`guide_eating.md`, `guide_regional_transport.md`) open with
  only a title line and little or no intro paragraph before the first heading.
  That intro gets folded into the first section instead of becoming its own
  near-empty chunk.
- Any section under 180 characters after that gets merged into its neighbor,
  so no chunk is a heading with barely a sentence under it.
- Every chunk is prefixed with the document title and its section heading, so
  a chunk read completely on its own still says which town and which topic
  it's about.

I changed my mind once partway through: my first version chunked on headings
but didn't prefix the document title, and a chunk like "## When to go / Late
spring and early autumn..." was ambiguous about which town it belonged to
outside the context of the full prompt. Adding the title line fixed that.

Result: 81 chunks, averaging 369 characters (shortest 209, longest 885),
produced by `chunker.py::split_documents`.

## Sample Chunks

<!-- python app.py chunks -n 5 -->

**Chunk 1** — source: `guide_accessibility.md` — produced by: `chunker.py::split_documents`

```
# Getting around the region with limited mobility
## Straightforward
An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

**Thornby Wells** is the easiest town in the region. It is flat, compact, and
everything is within three minutes of everything else. Parking is free for two
hours anywhere in town and the station is central. The pump room and gardens
are level throughout.

**Marchwood** has a modern tram network with level boarding on all four lines,
running every 8 minutes on weekdays. The city museum and covered market are both
step-free. The distances between districts are the main consideration.

**Brightwater** is level along the river and through the centre. The mill museum
is step-free. The station is a 15-minute walk from campus on flat ground, or the
shuttle meets the four busiest arrivals.
```

**Chunk 2** — source: `guide_corry_vale.md` — produced by: `chunker.py::split_documents`

```
# Corry Vale
## When to go
May to September. Outside those months the pub in the third village closes, the farm shop reduces its hours, and several footpaths become genuinely boggy rather than merely wet. The road is not gritted above the second village and is impassable in snow.
```

**Chunk 3** — source: `guide_givens_mill.md` — produced by: `chunker.py::split_documents`

```
# Givens Mill
## Eat and drink
A tearoom attached to the mill, open 10 to 4 daily except Tuesdays, which sells bread made from the flour ground twenty metres away and is the reason most people come. One pub, food served lunchtimes and Thursday to Saturday evenings.
```

**Chunk 4** — source: `guide_kestrelford.md` — produced by: `chunker.py::split_documents`

```
# Kestrelford
## When to go
Late spring and early autumn. The Saturday market runs year-round but is much reduced from November to February. August is busy with walkers. The single-track approach road is genuinely difficult in snow and the town can be cut off for a day or two most winters.
```

**Chunk 5** — source: `guide_regional_transport.md` — produced by: `chunker.py::split_documents`

```
# Getting around the region
## The railway
The line runs along the river valley, connecting Brightwater to the regional
hub in 50 minutes. Eleven services a day on weekdays, six on Sundays. The line
north of Brightwater closed in 1963 and everything beyond it is bus or car.

Tickets are cheaper booked the day before than on the day, and considerably
cheaper than that booked a week ahead. There is no ticket office at
Brightwater station outside weekday mornings; the machine on the platform takes
cards only.
```

## Sample Answer

**Question:** how do I get to Kestrelford and what's the best time of year to visit?

**Answer:**

```
To get to Kestrelford, you can drive (taking 55 minutes from Brightwater, with
the last eight miles on a single-track road) or take a bus from Brightwater,
which runs roughly hourly on weekdays, every two hours on Saturdays, and not
at all on Sundays (there is no railway station) [guide_kestrelford.md].

The best times to visit are late spring and early autumn [guide_kestrelford.md].

Sources retrieved: guide_kestrelford.md, guide_walking.md
```

**My relevance cutoff:** 0.6 (the starter's default). I ran the 5 questions in
`questions.py` and the 5 in `OUT_OF_SCOPE` through `python app.py retrieve` and
recorded the best distance for each. The two groups came out wide apart with a
clean gap between them — 0.306–0.359 for in-corpus questions, 0.835–0.997 for
out-of-scope ones — so 0.6 already sits comfortably in the middle rather than
needing to move.

| Question | In corpus? | Best distance |
|---|---|---|
| How late do kitchens stay open in Marchwood compared to the rest of the region? | yes | 0.359 |
| Why should visitors avoid eating right around the Marchwood train station? | yes | 0.351 |
| What time do the Halden Bay parking lots fill up on a summer weekend? | yes | 0.345 |
| What's the best time of year to visit Brightwater, and why? | yes | 0.340 |
| How can someone get from Brightwater to Kestrelford without a car? | yes | 0.306 |
| What is the capital of Mongolia? | no | 0.838 |
| How do I change the oil in a diesel engine? | no | 0.908 |
| Who won the 1994 World Cup? | no | 0.997 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.835 |
| How do I write a for loop in Rust? | no | 0.836 |

## How I Used AI

**1.** I asked Claude to design and implement `split_documents()` in
`chunker.py` for a chunking strategy that fit `city_guides` specifically,
after I'd read through several documents and noticed they were all organized
into labelled `##` sections that the starter's fixed-width chunker ignored.
The first version it wrote split on headings but didn't carry the document
title into each chunk, so a chunk like the "When to go" section for Kestrelford
read identically to the "When to go" section for Corry Vale once it was
outside the context of the full document — I asked it to prefix every chunk
with the title line, which fixed the ambiguity.

**2.** For Milestone 4, I had Claude run all 5 `questions.py` entries and all 5
`OUT_OF_SCOPE` entries through `python app.py retrieve` and report the best
distance for each rather than eyeballing a couple by hand — that's what
produced the ten-row table above. Because the gap between the two groups came
out unusually wide (0.359 vs. 0.835), we didn't need to move the threshold off
its 0.6 default; I changed the comment in `config.py` to record the
measurement instead of changing the number.

**3.** Claude drafted my first pass at `questions.py` and `criteria.md`, and I
pushed back on that — I didn't just accept criteria written for me without
checking them. We went through each one the way the Milestone 2 breakout
activity describes: for criterion 1, Claude ran each of my 5 questions through
`python app.py ask --show-prompt`, and I read the actual retrieved chunks
myself and judged hit-or-miss for each (all 5 turned out to contain the
answer, better than the 4-of-5 target). I did the same for criterion 2
(checked that every answer we'd run so far ended with a `Sources retrieved:`
line) and criterion 3 (re-ran a second out-of-scope question myself and
confirmed the refusal). For criteria 4 and 5 — the two I was supposed to write
myself — I reviewed Claude's proposed wording against evidence from my own
test runs (the sample chunks for 4, the multi-document source lists for 5) and
chose to keep both once I could point to why each one held.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
