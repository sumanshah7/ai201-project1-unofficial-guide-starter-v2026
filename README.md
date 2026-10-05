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

**4. (Unit 2)** I asked Claude to diagnose the criterion-5 miss and pick the
Milestone 4 improvement. It proposed hybrid search (BM25 + semantic fusion)
because the brief names that as the fix for exactly this failure mode
(semantic search ranking a related-but-wrong chunk above the right one). While
implementing it, Claude found and fixed a bug in its own first draft — fusing
two rankings can knock the single closest chunk out of the returned top-k,
which would have silently broken the relevance gate's 0.6 cutoff — before I'd
even asked about it. After measuring, the "fix" didn't help the question it
targeted and broke a previously-working one; I told Claude to report that
honestly and keep the change in the code rather than quietly reverting to a
version that looked better.

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

Produced by `run_eval.py::main`, 3 runs per question, caching off. Full file:
[`results/run_2026-10-04_2233_before.md`](results/run_2026-10-04_2233_before.md).
No `scorer.py` existed yet, so every verdict below is me reading the actual
answer text and judging hit/miss myself.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks don't split a section (sampled, static — not re-run per question) | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Cross-cutting answers cite both docs | 4 of 5 | 3/4* | 3/4* | 3/4* | MISSED |

\* Only 4 of my 5 test questions actually involve a fact duplicated between a
town guide and a cross-cutting guide (Q2, the Marchwood-station question,
turns out to be answerable from `guide_marchwood.md` alone — nothing in
`guide_eating.md` actually duplicates that specific fact). Of the 4 that do
qualify, 3 cited both documents in every run and 1 (the Brightwater→Kestrelford
question) cited only `guide_kestrelford.md` in all 3 runs.

Real output — criterion 1 and 5, question "How can someone get from
Brightwater to Kestrelford without a car?" (produced by `generate.py::answer_from_chunks`,
chunks from `store.py::search`):

```
To get from Brightwater to Kestrelford without a car, someone can take a bus, which runs roughly hourly on weekdays, every two hours on Saturdays, and does not run on Sundays.

Source: `guide_kestrelford.md`
```

This is a criterion-1 **hit** (the bus schedule is right there) and a
criterion-5 **miss** (the same schedule also appears in
`guide_regional_transport.md`'s "Buses" section, which never made it into the
top-5 retrieved chunks — see the diagnosis below).

Real output — criterion 3 (produced by `run_eval.py::check_out_of_scope`,
`gate.py::check`):

```
refused  (best distance 0.997)  Who won the 1994 World Cup?
-> gate refused 5 of 5
```

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | **MET** | Read all 5 questions' retrieved chunks myself against `python app.py ask --show-prompt`; all 5 contained the literal fact asked for, in all 3 runs. |
| 2 | Every answer names a source | **MET** | Every one of the 15 answers (5 questions × 3 runs) ended with a named `.md` file, either inline or in a `Sources:` line. |
| 3 | Gate stops out-of-corpus questions | **MET** | All 5 `OUT_OF_SCOPE` questions refused, distances 0.835–0.997, nowhere close to the 0.6 cutoff. |
| 4 | Chunks don't split a section | **MET** | Unchanged from Unit 1 — same chunker, same 5 sampled chunks, all 5 complete `##` sections with no sentence cut off. |
| 5 | Cross-cutting answers cite both docs | **MISSED** | Of the 4 test questions that genuinely involve a fact duplicated across a town guide and a cross-cutting guide, only 3 cited both — short of the "4 of 5" target no matter how you count the denominator. This is the closest call of the five, and I'm calling it a miss rather than rounding up, because the target says "4 of 5" and I can't produce a 4th hit by relabeling Q2 as a cross-cutting question when its answer never needed a second document. |

## Diagnoses

**Criterion 5 miss — retrieval stage.** For "How can someone get from
Brightwater to Kestrelford without a car?", the bus-schedule fact appears in
both `guide_kestrelford.md` ("Getting there") and `guide_regional_transport.md`
("Buses"). Retrieval's top-5 included the Kestrelford copy but not the
regional-transport copy — instead it pulled that file's "Walking and cycling"
section, which is closer to the question in *meaning* ("without a car" reads
semantically adjacent to "walking") even though "Buses" is the section that
actually duplicates the answer. I confirmed this directly: `python app.py ask
"..." --show-prompt` shows the five retrieved chunks, and
`guide_regional_transport.md#1` (Buses) simply isn't one of them. The model
answered correctly from what it had — this isn't a generation problem, the
citation is just incomplete because the right chunk never reached it.

No pattern across multiple questions here — this is the only miss, and it's a
single specific gap (one document's two relevant sections competing for one
retrieval slot) rather than something systemic. Worth noting on the "were my
targets set too easy" question from Milestone 3: criteria 1–4 held at a
stronger margin than I expected (5/5 against a 4/5 target, 3 times over) —
if I rewrote this unit's criteria today I'd tighten 1 and 3 to 5 of 5, since
nothing came close to failing them. Criterion 5 turned out to be the one with
real signal in it.

## The Improvement

**What I changed:** Added hybrid search — `store.py::search` now runs a BM25
keyword pass (`rank-bm25`, via a new `_bm25_index` function) alongside the
existing semantic search and combines the two rankings with reciprocal rank
fusion, gated by `config.HYBRID_SEARCH`. While building it I found and fixed a
real bug it would have introduced: fusing rankings can push the single closest
chunk (by cosine distance) out of the returned top-k, which would silently
break the relevance gate's 0.6 cutoff, since the gate only ever sees the
distances of whatever `search()` hands back. `search()` now guarantees the
globally-nearest chunk always stays in the returned set regardless of how
fusion re-ranks the rest.

**Why I picked it:** The diagnosis pointed specifically at semantic search
ranking a wrong-but-related chunk (walking/cycling) above the right one
(buses) for a "without a car" query — exactly the failure mode the brief's own
Milestone 4 menu says hybrid search is for: "when your questions contain
names, numbers, or exact terms that semantic search glides past."

### Run Log — After

Produced by `run_eval.py::main`, same 5 questions, 3 runs each, `HYBRID_SEARCH
= True`. Full file: [`results/run_2026-10-04_2241_after.md`](results/run_2026-10-04_2241_after.md).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks don't split a section (unchanged — chunking wasn't touched) | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Cross-cutting answers cite both docs | 4 of 5 | 1/4 | 1/4 | 1/4 | MISSED (worse) |

Real output — the question hybrid search was supposed to fix, after the change
(produced by `generate.py::answer_from_chunks`):

```
To get from Brightwater to Kestrelford without a car, you can take a bus, which runs roughly hourly on weekdays and every two hours on Saturdays (there is no bus service on Sundays). Alternatively, you can walk along the Kestrelford trackbed, which is a six-mile walking route following the old railway line.

Source: `guide_kestrelford.md` and `guide_walking.md`
```

`guide_regional_transport.md` still never appears — it checked the BM25
scores directly: the Buses section's actual text never uses the word "bus" at
all (it says "service"), and shares only place names with the query, so it
wasn't a strong keyword match either. Hybrid search couldn't fix a chunk that
has neither the right embedding neighborhood nor the right vocabulary.

Real output — the regression, same question structure, different question
(produced by `generate.py::answer_from_chunks`):

```
Question: What's the best time of year to visit Brightwater, and why?

Based on the provided documents, late May is arguably the best week of the year to visit Brightwater because days are long, everything is running, and the students have left (*guide_seasons.md*).

Additionally, September is noted as the other "sweet spot" because it is warm, quiet, and everything is still open (*guide_seasons.md*).
```

Before the change, this question's answer cited both `guide_brightwater.md`
and `guide_seasons.md` in all 3 runs. After, `python app.py ask "..."
--show-prompt` shows why: the `guide_brightwater.md` chunk retrieved is now
its "Getting there" section (train times, no airport) instead of its "When to
go" section (the actual May/June recommendation) — the BM25 pass pulled in a
different, irrelevant chunk from that same file and displaced the one that
mattered.

**Did it help?** No. It didn't fix the question it was chosen for — the
target chunk's wording ("service," not "bus") meant BM25 had nothing to grab
onto — and it broke a previously-working citation on a different question by
letting an irrelevant chunk from the same file outrank the relevant one.
Criterion 5 went from 3 of 4 eligible hits to 1 of 4. Everything else
(criteria 1–4) held steady. I'm keeping the change in the shipped code rather
than quietly reverting it, because "one change, measured" is supposed to
include the case where the measurement says no.

## What's Still Broken

**Criterion 5 (still missed, now worse).** Two separate problems, both at the
retrieval stage: (1) `guide_regional_transport.md`'s "Buses" section has never
once been retrieved for the Kestrelford-transport question, under either
semantic or hybrid search, because it doesn't share enough meaning *or*
vocabulary with "without a car" — fixing this would need either a much larger
top-k, or a chunk that includes a synonym bridge ("bus service" rather than
just "service"). (2) Hybrid search's BM25 pass has no way to tell "relevant to
this file's topic" from "relevant to this query," so it can promote any
chunk from a file that scored well on place-name overlap, not just the chunk
that actually answers the question. If I kept working on this, I'd revert
`HYBRID_SEARCH` to `False` by default and only enable it per-query when a
question contains a proper noun with no close semantic match in the top
results — a narrower trigger than "always on."

I ran out of time to try that narrower version, which is a real stopping
point, not a cosmetic one — building a reliable "when does BM25 actually
help" heuristic is its own small project.

## What I'd Do Differently

Criteria 1 and 3 I'd tighten to 5 of 5 — across 2 full test runs (6 total
passes) neither one came within a full question of missing, so "4 of 5" turned
out not to be where this system's real risk lives. Criterion 5, on the other
hand, I'd keep at 4 of 5 but rewrite the question set behind it: right now only
4 of my 5 general test questions happen to be genuine cross-cutting cases, and
one criterion built on an accidental subset of another criterion's question
list is more fragile than it looks. Next time I'd write 5 questions
specifically designed to duplicate a fact across a town guide and a
cross-cutting guide, rather than discovering after the fact that only 4 of my
general-purpose questions qualified.
