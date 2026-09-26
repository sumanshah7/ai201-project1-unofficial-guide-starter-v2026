# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** My five questions each point at a single sentence or two
inside one town's `##` section (e.g. Marchwood's closing hours, Halden Bay's
parking times), and `city_guides` gives each fact exactly one home — there's no
redundancy to fall back on the way there might be in a corpus where several
documents mention the same thing. I expect one question to be the hard case:
"how to get from Brightwater to Kestrelford without a car" pulls from both a
town guide and the cross-cutting `guide_regional_transport.md`, so the answer
depends on retrieval grabbing the right chunk from either document, not both.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** This is closer to a code guarantee than a probabilistic
one — `generate.py`'s grounding instruction requires a citation on every
non-refused answer, and the prompt only ever contains chunks that already carry
their `source` filename. There's no path through the code where an answer gets
generated without retrieved chunks attached to it, so I'm not hedging to 4 of 5
the way I do for the retrieval and gate criteria.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:** `city_guides` is about travel logistics for a specific
fictional region, and the `OUT_OF_SCOPE` questions (world capitals, diesel
engines, ibuprofen dosage, Rust syntax) share no vocabulary with it at all, so I
expect these to sit far past whatever cutoff I pick — this should be the
easiest criterion to hit, not the hardest. I'm leaving it at 4 of 5 rather than
5 of 5 because I haven't measured the actual distances yet (that's Milestone 4)
and I'd rather leave room for one surprising overlap than claim a perfect score
I haven't seen.

---

## 4. Chunks don't split a section across two pieces

At least 4 of 5 chunks I sample with `python app.py chunks -n 5` contain one
complete `##` section — heading plus its full paragraph — with no sentence cut
in half at the start or the end.

**Why this target:** Every document in `city_guides` is organized into labelled
sections (Getting there, Eat and drink, When to go, ...), and in Milestone 1 I
watched the starter's fixed 800-character chunker slice straight through those
headings — 14 documents became 51 chunks with no respect for where a section
started or ended. A chunk that stops mid-section is exactly the "too big"/"cut
in the wrong place" failure the brief warns about, so measuring against section
boundaries is the most direct way to check whether my Milestone 3 chunker
actually fixed that.

---

## 5. Cross-cutting answers cite both documents involved

For questions whose answer draws on both a town-specific guide and one of the
five cross-cutting guides (`eating`, `walking`, `seasons`, `regional_transport`,
`accessibility`), the answer names both source documents in at least 4 of 5
such questions.

**Why this target:** `city_guides` is unusual among the three corpora in that
the same fact is sometimes split across a town guide and a cross-cutting guide
on purpose — Kestrelford's bus schedule appears in both
`guide_kestrelford.md` and `guide_regional_transport.md`, worded slightly
differently. A source line that names only one of the two isn't wrong exactly,
but it's incomplete in a way that's specific to this corpus's structure, and
it's the kind of error "every answer names a source" (criterion 2) would let
through silently. I'm not requiring 5 of 5 because retrieval only returns the
single best chunk per document region, so one of the two relevant chunks
missing the cutoff is a real possibility, not just a tuning failure.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
