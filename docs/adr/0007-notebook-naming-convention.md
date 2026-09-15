---
status: accepted
---

# Notebooks are named `cw_<feature>_<goal>.py`

A notebook's filename is the visible tail of every molab URL it is delivered through, and it is also what the file is called once someone downloads it — at which point it has left this repo and carries no surrounding context. So the name has to describe the notebook standing alone. The convention is **`cw_<feature>_<goal>.py`**, where `<feature>` is a **one-word product handle** from a fixed vocabulary (`inference`, `weave`, `models`, `agentlens`, `sandboxes`, `aria`, `registry`, `rl`) and `<goal>` is **verb-first, one or two words**, naming what the reader will have *done* by the end rather than what the notebook contains.

## Considered Options

- **Spelling out the product** (`cw_serverless_inference_evaluate.py`) — rejected: inside `cw-notebooks/serverless-inference/` it says "CoreWeave" twice and "serverless inference" twice, and the URL becomes unreadable. The one-word handle is the rule that actually controls length.
- **Dropping the `cw_` prefix**, since the repo is already entirely CoreWeave work — rejected. The prefix is not there to disambiguate within the repo; it is there because **the file leaves the repo**. In a stranger's Downloads folder, `evaluate_open_weight_models.py` is anonymous and `cw_inference_first_run.py` is not. Same reasoning as the `cw-` skill prefix, different mechanism.
- **Naming by content rather than outcome** (`..._structured_extraction.py`) — rejected: a notebook usually has several sections and the one you would name it after is rarely the one the reader came for.

## Consequences

- **Budget: three tokens after `cw_`, roughly thirty characters.** A name needing four tokens is a signal the notebook is doing two jobs and should be split — which also keeps each piece inside the portability budget ([ADR-0006](0006-portability-budget-for-notebooks.md)).
- **Renaming a notebook breaks its molab URL**, which by then may be sitting in sent email and customer bookmarks. Names are therefore chosen once, deliberately, at creation. There is no redirect.
- **`<goal>` avoids the word "evaluate"** where plain assessment is meant, because in this domain it reads as *running evals*. Prefer `first_run`, `benchmark`, `migrate`, `trace`, `monitor`, `finetune`.
- The directory name still carries the product, so the handle and the directory are deliberately redundant by one word — accepted, because the filename must survive being separated from the directory.
