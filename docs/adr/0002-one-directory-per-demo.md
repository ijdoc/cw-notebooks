---
status: accepted
---

# One directory per demo, and the notebook is the unit of delivery

Each demo gets its own top-level directory holding its notebook, its own `README.md`, and any synthetic fixtures it needs. There is no shared package, no `src/`, and no cross-demo imports: a notebook is delivered to a customer **on its own**, often as a single molab URL, so it must make sense with nothing else present.

## Considered Options

- **A conventional Python package with demos importing shared helpers** — less duplication, and the shape the deprecated `autoresearch-loop` repo reached for. Rejected because a shared helper breaks the delivery model: the moment a notebook imports `from cw_notebooks.util import …`, it can no longer be opened from a URL or pasted into a customer's environment, which is the entire point.
- **A flat directory of notebook files** — simpler, and fine at three notebooks. Rejected because fixtures and per-demo READMEs have nowhere to live, and demos accumulate.

## Consequences

- **Duplication across notebooks is accepted and expected.** Two notebooks that both build an OpenAI client will both contain those three lines. That is cheaper than coupling them.
- Each notebook declares its own dependencies inline (PEP 723), so there is no repo-level `pyproject.toml` and no lockfile. Demos cannot drift into a shared dependency set.
- A demo is retired by deleting its directory.
