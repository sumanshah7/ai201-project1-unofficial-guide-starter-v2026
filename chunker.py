"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


_HEADING_RE = re.compile(r"\n(?=## )")


def _split_section_if_long(
    title_line: str, heading: str, body: str, source: str, index: int
) -> list[Chunk]:
    """
    One section, as its own chunk if it fits under CHUNK_SIZE, or sliced into
    overlapping windows if it doesn't (rare — see the note in config.py).
    Every piece keeps the document title and section heading as a prefix, so a
    chunk read in isolation still says which town and which topic it's about.
    """
    prefix = f"{title_line}\n{heading}\n" if heading else f"{title_line}\n"
    full = f"{prefix}{body}".strip()

    if len(full) <= config.CHUNK_SIZE:
        return [
            Chunk(
                text=full,
                source=source,
                index=index,
                produced_by="chunker.py::split_documents",
            )
        ]

    # Oversized section: window over the body, re-attaching the prefix to
    # every window so each piece still stands on its own.
    window = config.CHUNK_SIZE - len(prefix)
    overlap = config.CHUNK_OVERLAP
    pieces: list[Chunk] = []
    start = 0
    while start < len(body):
        piece_body = body[start : start + window].strip()
        if piece_body:
            pieces.append(
                Chunk(
                    text=f"{prefix}{piece_body}".strip(),
                    source=source,
                    index=index + len(pieces),
                    produced_by="chunker.py::split_documents",
                )
            )
        start += window - overlap
    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents on their `##` section headings instead of on a raw
    character count.

    city_guides documents are organised by heading (Getting there, Eat and
    drink, When to go, ...), and a fixed-size window cuts straight through
    those — the starter's fallback turns 14 documents into 51 chunks with no
    regard for where a section starts or ends. Splitting on the headings the
    documents already have keeps each section's sentences together instead.

    A few documents open with only a one-line title and little or no intro
    paragraph before the first heading (e.g. `guide_eating.md`), so that intro
    is folded into the first section rather than becoming a near-empty chunk
    of its own. The same merge-forward rule applies to any section that comes
    out under `config.MIN_CHUNK_CHARS` after that.
    """
    chunks: list[Chunk] = []
    for doc in documents:
        parts = _HEADING_RE.split(doc.text)
        title_line = parts[0].splitlines()[0].strip()
        intro = "\n".join(parts[0].splitlines()[1:]).strip()

        # Each remaining part starts with its "## Heading" line.
        raw_sections: list[tuple[str, str]] = []
        for part in parts[1:]:
            lines = part.strip().splitlines()
            heading, body = lines[0], "\n".join(lines[1:]).strip()
            raw_sections.append((heading, body))

        if not raw_sections:
            # No headings at all — the whole document is one chunk.
            chunks.append(
                Chunk(
                    text=doc.text,
                    source=doc.source,
                    index=0,
                    produced_by="chunker.py::split_documents",
                )
            )
            continue

        # Fold the title/intro into the first section rather than giving it
        # its own chunk.
        first_heading, first_body = raw_sections[0]
        raw_sections[0] = (
            first_heading,
            f"{intro}\n\n{first_body}".strip() if intro else first_body,
        )

        # Merge any section under MIN_CHUNK_CHARS forward into its neighbour
        # (backward if it's the last one) so no chunk is a heading with
        # barely any content under it.
        merged: list[tuple[str, str]] = []
        for heading, body in raw_sections:
            if merged and len(body) < config.MIN_CHUNK_CHARS:
                prev_heading, prev_body = merged[-1]
                merged[-1] = (prev_heading, f"{prev_body}\n\n{heading}\n{body}")
            else:
                merged.append((heading, body))
        if len(merged) > 1 and len(merged[-1][1]) < config.MIN_CHUNK_CHARS:
            last_heading, last_body = merged.pop()
            prev_heading, prev_body = merged[-1]
            merged[-1] = (prev_heading, f"{prev_body}\n\n{last_heading}\n{last_body}")

        index = 0
        for heading, body in merged:
            pieces = _split_section_if_long(title_line, heading, body, doc.source, index)
            chunks.extend(pieces)
            index += len(pieces)

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
