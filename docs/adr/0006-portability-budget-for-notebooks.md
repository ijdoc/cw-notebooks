---
status: accepted
---

# A portability budget for notebooks — a soft guideline, not a gate

molab runs notebooks on modest shared resources, and a notebook opened from a link is competing with a customer's patience. So demos here are written to a **portability budget**: small enough to start fast, finish in a minute or two, and need nothing but a key. Concretely, aim for no GPU, no multi-gigabyte download, no model training, no long-running job, and a cold start measured in seconds.

This is a **guideline, deliberately soft**. It shapes what gets built for this repo; it does not forbid an ambitious demo from existing. A demo that cannot fit the budget is not a molab notebook, and its home is either a WASM export handed over directly or a screen-shared session from the private repo — which is a routing decision, not a rejection.

## Consequences

- **The budget shapes demo design up front, which is the point.** "What can I show in ninety seconds against a live endpoint with no setup?" produces better demos than trimming an ambitious one afterwards.
- **Inference-shaped demos fit naturally; training-shaped demos do not.** Anything whose cost is a forward pass against a hosted endpoint is comfortably inside the budget. Anything that trains, fine-tunes, or downloads weights is outside it, and should be reframed to *read the results* of a run performed elsewhere rather than perform the run.
- A demo that outgrows the budget is not deleted — it moves to a delivery route that suits it, and the notebook here may remain as the lightweight entry point to it.
- Because the budget is soft, it needs a judgement call rather than a check. No CI enforces it.
