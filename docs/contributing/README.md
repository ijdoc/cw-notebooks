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

Every notebook opens with the same header ([ADR-0009](../adr/0009-header-is-plain-markdown.md)): a CoreWeave wordmark, the title, and links to the model catalog, pricing and the product page. **Plain markdown, deliberately.** It renders identically in the editor, in app mode, in slide mode and in a molab preview, with nothing to verify per surface.

Set the app title alongside the width:

```python
app = marimo.App(width="medium", app_title="CoreWeave <Product>: <goal>")
```

Then, as the first cell after the `import marimo as mo` cell:

```python
@app.cell(hide_code=True)
def _(mo):
    # Standard CoreWeave notebook header. See docs/adr/0009. Plain markdown,
    # so it renders the same in the editor, in app mode and in slide mode.
    # Copy verbatim into a new notebook; change only the title line and links.
    mo.md(
        """
        <img src="https://cdn.prod.website-files.com/62ba1fb86485b6d5029975c4/69de8e8600c3f18e49d4bf47_logo.svg" width="360" alt="CoreWeave" />

        # Serverless Inference: first run

        [Model catalog](https://wandb.ai/inference) &nbsp;&middot;&nbsp;
        [Pricing](https://wandb.ai/site/pricing/inference) &nbsp;&middot;&nbsp;
        [Read more &#8594;](https://coreweave.com/products/serverless-inference)
        """
    )
    return
```

Change the title line and the link. Leave the rest alone.

The header is **copied, not imported** ([ADR-0002](../adr/0002-one-directory-per-demo.md)): a notebook has to survive being delivered on its own. Duplication is the intended cost.

## Credentials

**Never ask the reader to export an environment variable.** Credentials are collected in the notebook, through the standard form: `WANDB_BASE_URL`, `WANDB_API_KEY` (as `kind="password"`), `WANDB_ENTITY` and `WANDB_PROJECT`, laid out with `mo.vstack` and `mo.hstack` and rendered with `.callout()`. Copy it from `serverless-inference/cw_inference_first_run.py`.

Gate everything downstream on the key with `mo.stop`, so a reader who has not filled the form sees a prompt rather than a stack trace.

Where a notebook traces to Weave, pass `project="<team>/<project>"` to the `OpenAI` client, built from the entity and project in the form. Both parts are required, so report the tracking status in the connection callout at the top rather than leaving the reader to discover at the bottom that nothing was logged. **Traces land in the reader's own project and nowhere else** ([ADR-0001](../adr/0001-no-customer-or-private-information-ever.md)). Say so in the notebook.

Two things follow from collecting credentials in the UI. The key is never written to the file and never appears in a committed session snapshot, which is the point. But a headless `marimo export session` has no key either, so a gated notebook produces a thin preview showing only the form. That is the accepted trade against [ADR-0005](../adr/0005-commit-session-snapshots-for-molab-previews.md).

## Prose style

**No em dashes.** Use a colon, a full stop, a comma or parentheses. This applies to notebook prose, READMEs and this guide. ADR narratives already written are frozen and keep theirs.

## Writing style inside a notebook

Show the failure, not only the happy path. The most valuable thing in the first notebook is a prompt that returns valid JSON with the wrong answer, and the one-line change that fixes it — a demo where everything works teaches nothing and reads as a sales pitch. Say when example data is synthetic, in the notebook, every time.

Prefer non-reasoning models in any dropdown default: reasoning models spend the token budget thinking and can return empty `content` with `finish_reason: "length"`, which is a poor thing to discover live.

## Commits

Conventional Commits, explicit staging, imperative subject. Scopes: `demos` (a notebook and its directory), `docs` (ADRs, this guide), `readme`.
