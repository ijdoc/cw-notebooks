---
status: accepted
---

# Notebooks are marimo, and molab is the delivery surface — which is why this repo is public

Notebooks here are [marimo](https://marimo.io) notebooks: plain Python files that diff, review and run as scripts, with dependencies declared inline (PEP 723) so `uvx marimo edit --sandbox <file>` works with nothing installed first. The hosted surface is **molab**, for customers who need to run a notebook without installing anything at all.

The decisive constraint, discovered rather than designed: **molab has no publish step.** There is no upload, no API, no account to authenticate against. It is a viewer that fetches a notebook from a public GitHub URL of the form `https://molab.marimo.io/github/{owner}/{repo}/blob/{branch}/{path}`. Wanting molab delivery therefore *means* wanting a public repository — which is the whole reason this repo exists separately from the private gig repo, and why [ADR-0001](0001-no-customer-or-private-information-ever.md) is absolute rather than a preference.

## Considered Options

- **Keeping notebooks in the private gig repo and exporting WASM HTML** (`marimo export html-wasm`) — preserves privacy completely and needs no second repo. Rejected as the default because the export pulls its Python runtime from a CDN at load time, which makes it fragile in restricted hosting, and because a static export loses the "clone it and change it" affordance that makes a notebook better than a deck. Still the right answer for a demo that cannot be de-identified.
- **Jupyter or Colab** — universal familiarity. Rejected: JSON notebooks cannot be meaningfully reviewed, hidden execution state has misfired in live demos, and Colab makes Google the delivery mechanism.

## Consequences

- Every notebook must be safe to publish before it can be delivered. De-identification is a prerequisite of the delivery mechanism, not a courtesy.
- `/wasm` may be appended to a molab URL to run a notebook client-side, but only for notebooks whose dependencies are pyodide-compatible. Anything needing a GPU, a large download, or long wall-clock time is not a molab notebook at all and should not pretend to be.
- marimo is a CoreWeave product, so authoring demos as marimo notebooks is also dogfooding.
