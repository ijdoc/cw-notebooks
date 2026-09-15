# Contributing to cw-notebooks

This repo is public and read by customers. Before anything else, read [ADR-0001](../adr/0001-no-customer-or-private-information-ever.md): **no customer or private information enters this repository**, and **nothing here collects anything from whoever runs it**. Those are absolute. The vocabulary is in [`CONTEXT.md`](../../CONTEXT.md); the decisions are in [`docs/adr/`](../adr/README.md).

## Adding a notebook

1. **Pick the name first**, using `cw_<feature>_<goal>.py` ([ADR-0007](../adr/0007-notebook-naming-convention.md)). `<feature>` is a one-word handle — `inference`, `weave`, `models`, `agentlens`, `sandboxes`, `aria`, `registry`, `rl` — and `<goal>` is verb-first, one or two words, naming what the reader will have *done*. Budget three tokens after `cw_`, roughly thirty characters. **The name is chosen once**: it is the tail of a molab URL that will end up in sent mail, and there is no redirect.
2. **Create a directory per demo** ([ADR-0002](../adr/0002-one-directory-per-demo.md)) holding the notebook, its own `README.md`, and any synthetic fixtures. No shared code, no imports between demos.
3. **Declare dependencies inline** (PEP 723) so `uvx marimo edit --sandbox <file>` works with nothing installed.
4. **Paste the header cell below verbatim**, changing only the three constants.
5. **Keep it inside the portability budget** ([ADR-0006](../adr/0006-portability-budget-for-notebooks.md)) — no GPU, no large downloads, no training, done in a minute or two.
6. **Generate and commit a session snapshot** ([ADR-0005](../adr/0005-commit-session-snapshots-for-molab-previews.md)): `uvx marimo export session --sandbox <file>`. Review what the snapshot *rendered*, not just the source — anything displayed is published.
7. **Add it to the table in the root `README.md`** with its molab badge.

## The header cell

Every notebook opens with this, unchanged except for `PRODUCT`, `TAGLINE` and `PRODUCT_URL` ([ADR-0008](../adr/0008-branded-header-on-every-notebook.md)). It is **copied, not imported** — a notebook has to survive being delivered on its own.

Set the app title on the same line as the width:

```python
app = marimo.App(width="medium", app_title="CoreWeave <Product> — <goal>")
```

Then, as the first cell after the `import marimo as mo` cell:

```python
@app.cell(hide_code=True)
def _(mo):
    # ---------------------------------------------------------------------
    # CoreWeave notebook header — standard across every notebook in this
    # repo (docs/adr/0008). Copy this cell verbatim into a new notebook and
    # change only the three constants. The mark is the official CoreWeave
    # glyph, inlined rather than linked so the header never depends on a CDN
    # staying up, and the band is dark in both themes so the white mark and
    # the contrast ratios hold either way.
    # ---------------------------------------------------------------------
    PRODUCT = "Serverless Inference"
    TAGLINE = "Run leading open-source models or your own LoRA weights with one API call."
    PRODUCT_URL = "https://coreweave.com/products/serverless-inference"

    _MARK = (
        '<svg width="22" height="22" viewBox="0 0 25 25" fill="none" '
        'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<path fill-rule="evenodd" clip-rule="evenodd" d="M9.56108 15.7745H6.07265C5.8599 '
        "15.7745 5.64716 15.6426 5.51883 15.4238L3.90295 12.4458C3.81852 12.227 3.81852 "
        "12.0082 3.90295 11.8328L5.51883 8.85484C5.64716 8.63605 5.8599 8.5041 6.07265 "
        "8.5041H8.07183C8.28458 8.5041 8.49733 8.37215 8.62565 8.15335L10.0727 "
        "5.48102C10.201 5.26222 10.0305 5 9.81773 5H4.45677C3.98906 5 3.60577 5.26222 "
        "3.35081 5.65639L0.159562 11.5255C-0.0531874 11.9197 -0.0531874 12.4007 0.159562 "
        "12.7949L3.35081 18.6206C3.56356 19.0147 3.98906 19.2769 4.45677 "
        "19.2769H11.307C11.5619 19.2769 11.6903 19.0147 11.5619 18.7959L10.0727 "
        '16.0802C10.0305 15.8614 9.81773 15.7729 9.56276 15.7729L9.56108 15.7745Z" fill="white"/>'
        '<path d="M17.0899 5.22038C17.2182 5.00165 17.5152 5.00176 17.6436 5.22038L19.0049 '
        "7.58562C19.2176 7.97976 19.2177 8.46104 19.0049 8.85515L13.3887 19.1032C13.2604 "
        "19.322 12.9633 19.322 12.835 19.1032L11.3458 16.3444C11.2613 16.169 11.2614 "
        "15.9499 11.3458 15.7311L17.0899 5.22038ZM22.1114 5.22038C22.2397 5.00166 22.5367 "
        "5.00179 22.6651 5.22038L24.0264 7.58562C24.2813 7.97976 24.2811 8.46102 24.0684 "
        "8.85515L18.4522 19.1032C18.3238 19.3218 18.0268 19.3219 17.8985 19.1032L16.3672 "
        "16.3444C16.2828 16.1691 16.2828 15.9499 16.3672 15.7311L22.1114 5.22038ZM11.2618 "
        "5.17546C11.3901 4.95677 11.6872 4.9567 11.8155 5.17546L13.7725 8.6364C13.8568 "
        "8.85511 13.8569 9.11739 13.7725 9.29265L12.0704 12.402V12.401C11.9841 12.6196 "
        "11.6449 12.6192 11.5167 12.3571L9.60162 8.81023C9.51722 8.6349 9.51726 8.37232 "
        '9.60162 8.19695L11.2618 5.17546Z" fill="white"/></svg>'
    )
    _FACE = (
        "'Plus Jakarta Sans',ui-sans-serif,system-ui,-apple-system,"
        "'Segoe UI',Roboto,sans-serif"
    )

    # mo.Html rather than mo.md: the block is raw HTML with no markdown in it.
    # (mo.md renders it identically — this is a semantic choice, not a workaround.)
    mo.Html(
        f'<div style="background:#0A0E14;border-radius:10px;padding:22px 24px 20px;'
        f'border-bottom:3px solid #0541E9;font-family:{_FACE};">'
        f'<div style="display:flex;align-items:center;gap:9px;margin-bottom:14px;">{_MARK}'
        f'<span style="color:#FFFFFF;font-size:12px;font-weight:600;letter-spacing:0.16em;'
        f'text-transform:uppercase;">CoreWeave</span></div>'
        f'<div style="color:#FFFFFF;font-size:26px;font-weight:700;line-height:1.15;'
        f'margin-bottom:8px;">{PRODUCT}</div>'
        f'<div style="color:#B6BBC2;font-size:15px;line-height:1.5;max-width:60ch;'
        f'margin-bottom:16px;">{TAGLINE}</div>'
        f'<a href="{PRODUCT_URL}" target="_blank" rel="noopener" '
        f'style="color:#63A4FF;font-size:13px;font-weight:600;text-decoration:none;">'
        f"Product overview &#8594;</a></div>"
    )
    return
```

**`TAGLINE` is quoted from the product's public page**, not written fresh — if our description and marketing's disagree, the customer can check, and theirs wins. Re-read the page when revising a notebook.

## Writing style inside a notebook

Show the failure, not only the happy path. The most valuable thing in the first notebook is a prompt that returns valid JSON with the wrong answer, and the one-line change that fixes it — a demo where everything works teaches nothing and reads as a sales pitch. Say when example data is synthetic, in the notebook, every time.

Prefer non-reasoning models in any dropdown default: reasoning models spend the token budget thinking and can return empty `content` with `finish_reason: "length"`, which is a poor thing to discover live.

## Commits

Conventional Commits, explicit staging, imperative subject. Scopes: `demos` (a notebook and its directory), `docs` (ADRs, this guide), `readme`.
