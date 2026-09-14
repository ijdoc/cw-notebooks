# cw-notebooks

Public, runnable notebook demos for the CoreWeave portfolio. This glossary defines the terms used in this repository. The one thing to understand before anything else: **this repo is public and holds no customer or private information of any kind** ([ADR-0001](docs/adr/0001-no-customer-or-private-information-ever.md)).

## Language

**Demo**:
One self-contained thing a customer can be shown and then run themselves, living in its own top-level directory with its notebook, its `README.md`, and its **synthetic fixtures**. Demos never import from each other ([ADR-0002](docs/adr/0002-one-directory-per-demo.md)).
_Avoid_: example, tutorial, sample (all imply documentation rather than a delivered artifact), project.

**Notebook**:
A [marimo](https://marimo.io) notebook — a plain `.py` file that diffs, reviews and runs as a script, with dependencies declared inline (PEP 723) so it runs via `uvx marimo edit --sandbox` with nothing installed first. The unit of delivery.
_Avoid_: ipynb, Jupyter, Colab, script (it is reactive, not sequential).

**molab**:
marimo's hosted notebook service, and the **delivery surface** here. It has **no publish step** — no upload, no API, no account: it fetches a notebook from a public GitHub URL, `https://molab.marimo.io/github/{owner}/{repo}/blob/{branch}/{path}`. That property is why this repository is public ([ADR-0003](docs/adr/0003-marimo-and-molab-as-the-delivery-surface.md)).
_Avoid_: marimo cloud, marimo.app (the older client-side runner), hosting, deploying or publishing *to* molab — nothing is pushed anywhere.

**Session snapshot**:
A pre-rendered execution of a notebook, produced by `uvx marimo export session --sandbox <notebook>` and **committed**, so a molab visitor sees output immediately instead of an empty notebook. It captures whatever the notebook *displayed*, which makes it the sharpest edge of the no-private-information rule ([ADR-0005](docs/adr/0005-commit-session-snapshots-for-molab-previews.md)).
_Avoid_: cache, output, export (ambiguous — `marimo export` has eight subcommands), snapshot (bare).

**Synthetic fixture**:
Input data written specifically for a demo and derived from nothing real — the only kind of input a notebook here may carry. A notebook always says, in the notebook, that its data is synthetic, so nobody mistakes it for a customer's.
_Avoid_: sample data, test data, mock (implies a stand-in for something real that exists here — it does not), anonymised or redacted data (both mean real data with the identifiers removed, which is forbidden, not encouraged).

**De-identification**:
The work of turning a demo built for one account into something publishable: removing names, the account, the internal framing and the reasoning about the buyer, and replacing any real input with a **synthetic fixture**. A prerequisite of delivery, not a courtesy, because the delivery mechanism is a public URL. A demo that cannot survive it stays private ([ADR-0004](docs/adr/0004-internal-framing-stays-in-the-private-repo.md)).
_Avoid_: anonymisation, scrubbing, sanitising (too weak — it implies cleaning something that may still be here), redaction.

**WASM export**:
`marimo export html-wasm` — a static, self-contained HTML file that runs the notebook client-side. The fallback delivery route for a demo that cannot be published, since it can be handed over directly rather than served from a public URL. Its Python runtime loads from a CDN, so it is fragile in restricted hosting.
_Avoid_: static export, HTML export (`marimo export html` is a different, non-interactive thing), offline notebook.

**Private gig repo**:
A separate, private repository holding the internal half of every demo: the account, the call history, the commercial position, the run sheet. It links *to* this repo; nothing here links back, and nothing here acknowledges that any specific account exists ([ADR-0004](docs/adr/0004-internal-framing-stays-in-the-private-repo.md)).
_Avoid_: the work repo, the private repo (ambiguous). Referred to by role, never by name or address — see ADR-0004.

## Flagged ambiguities

**"Publish"** — in molab's case nothing is published *to* anywhere. A notebook becomes available by being committed to this public repo; molab reads it live from GitHub. Say "commit it and link it", not "publish it to molab", or the next reader will go looking for an upload command that does not exist.

**"Notebook"** — in this repo it means one marimo `.py` file in one demo directory. marimo is a CoreWeave product, so "notebook" also names a thing CoreWeave ships; when that distinction matters, say "a notebook in this repo".

## Example dialogue

> **Colleague:** Can you send me the notebook you demoed? And is there one for the account I'm working?
>
> **jdoc:** The notebook, yes — it's a molab link, it'll open in your browser and run against your own key. But there's no per-account notebook and there won't be. The demo is generic by construction: this repo is **public**, so it holds no customer information at all, and the input it works on is a **synthetic fixture** I wrote.
>
> **Colleague:** So where's the part about *why* it landed — what the buyer cared about?
>
> **jdoc:** Private gig repo. That's the split: the runnable thing is public, the argument is not. If you want the framing for your account, write it there; don't put it next to the notebook.
>
> **Colleague:** Can I add a cell that logs runs to your W&B project so you can see how it goes?
>
> **jdoc:** No — and that's a rule, not a preference. Nothing here collects anything from whoever runs it. If you want tracing, point it at *your* project.
