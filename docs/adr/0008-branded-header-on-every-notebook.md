---
status: accepted
---

# Every notebook opens with the same branded header

A notebook here is delivered as a bare molab URL, usually pasted into an email. Whoever opens it arrives with no surrounding page, no navigation and no indication of who produced it or which product it belongs to — so the notebook has to say so itself. Every notebook therefore opens with an identical **branded header cell**: the CoreWeave mark, the product name, the product's own one-line description taken verbatim from its public page, and a link back to that page. Below it sits the notebook's own title and framing.

## The rules

- **The tagline is quoted from the product's public page, not written fresh.** If marketing's description and ours disagree, the customer notices, and theirs is the one they can check. Re-read the page when a notebook is revised.
- **The mark is inlined, never linked.** A CDN path can change or be blocked; a notebook that renders a broken image in front of a customer is worse than one with no logo at all.
- **The band is dark in both themes.** marimo and molab each have a light and a dark mode; a self-contained dark band means the white mark and every contrast ratio hold either way, with no theme-conditional styling to maintain.
- **Colours come from the established CoreWeave token set** — `#0A0E14` surface, `#0541E9` Lapis as the single accent (the bottom rule), `#FFFFFF`, `#B6BBC2` for secondary text, `#63A4FF` for the link on dark. Plus Jakarta Sans with a system fallback stack, and **no webfont is loaded**: an external stylesheet is one more thing to fail, and the fallback is perfectly respectable.
- **`app_title` is set on `marimo.App`** so the browser tab carries the product and the notebook's goal, not the filename.
- The header uses `mo.Html` rather than `mo.md`. Both render identically — the block is raw HTML containing no markdown, so `mo.Html` is simply the honest primitive.

## Consequences

- **The header is copied into each notebook, not imported.** [ADR-0002](0002-one-directory-per-demo.md) forbids shared code precisely so a notebook can be delivered alone, and that applies to the header too. Duplication is the intended cost; the canonical copy to paste from lives in the contributing guide.
- Because it is duplicated, a change to the header is a change to every notebook. Treat it as a rare, deliberate edit rather than something to tune.
- Only three constants differ per notebook: `PRODUCT`, `TAGLINE`, `PRODUCT_URL`. If a fourth thing needs to vary, that is a signal the header is growing into a template and should be reconsidered rather than parameterised in place.
