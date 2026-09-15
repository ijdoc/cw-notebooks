---
status: accepted
---

# The notebook header is plain markdown: a wordmark, a title, a link

[ADR-0008](0008-branded-header-on-every-notebook.md) specified a styled header — a dark band with an inlined mark, brand tokens, an explicit font stack and inline CSS. It rendered correctly, and it was still the wrong thing: it looked like a web component dropped into a notebook, and marimo notebooks are also viewed in **app mode and slide mode**, where a heavy custom band reads as an intrusion rather than a title. The header is now three lines of ordinary markdown — a hosted CoreWeave wordmark, an `#` title, and one line carrying the product's own description and a link to its page.

```markdown
<img src="…/69de8e8600c3f18e49d4bf47_logo.svg" width="360" alt="CoreWeave" />

# <Product> — <goal>

<the product's own one-line description from its public page>
[coreweave.com/products/<product>](https://coreweave.com/products/<product>)
```

This mirrors a pattern that worked well for years on the W&B notebooks: a logo, a heading, nothing else. A notebook title should look like a notebook title.

## What carries over from ADR-0008, and what does not

**Carried over:** the tagline is still **quoted from the product's public page** rather than written fresh, because the customer can check it; `app_title` is still set on `marimo.App` so the browser tab names the product and the goal; and the header is still **copied into each notebook, never imported**, since [ADR-0002](0002-one-directory-per-demo.md) requires a notebook to survive delivery on its own.

**Reversed:** the mark is now **linked, not inlined**. ADR-0008 argued that a CDN can fail and a broken image in front of a customer is worse than no logo. That is still true, and it is accepted anyway — the cost of being wrong is one missing image with intact `alt` text, and the benefit is a header a person can read, copy and edit without touching a wall of base64 or inline CSS. Simplicity won a judgement call, not an argument.

**Dropped:** the dark band, the brand tokens, the font stack, the inline styling, and the per-notebook `PRODUCT` / `TAGLINE` / `PRODUCT_URL` constants. The values now sit in the markdown where they are read.

## Consequences

- **The wordmark is not theme-adaptive.** Its glyph is brand blue but its lettering is `currentColor`, which resolves to black inside an `<img>` — so on a dark background the text half is faint while the glyph still reads. Accepted, rather than fixed with a `<picture>` element, because theme-conditional markup is exactly the complexity this ADR exists to remove. Revisit only if a dark-mode screenshot is ever needed for something that matters.
- **The header depends on a Webflow CDN path** that CoreWeave controls and may change without notice. If it breaks, every notebook shows alt text until the URL is updated in each one — a visible, cheap failure.
- Because the header is markdown rather than HTML, it renders identically in the editor, in app mode, in slide mode, and in a molab preview, with no styling to verify per surface.
