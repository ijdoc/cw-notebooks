# cw-notebooks

Runnable notebook demos for the CoreWeave portfolio — open-weight inference, evaluation, and the developer surface. Each one opens in your browser and runs against your own API key.

| Demo | What it shows | |
|---|---|---|
| [Serverless Inference — getting started](serverless-inference/) | Live model catalog, one-string model swaps, schema-enforced extraction (including a failure worth seeing), measured cost and latency, and the one-line move to dedicated capacity | [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/ijdoc/cw-notebooks/blob/main/serverless-inference/cw_inference_first_run.py) |

## Running a notebook

Notebooks are [marimo](https://marimo.io) notebooks — plain Python files with their dependencies declared inline, so nothing needs installing first:

```sh
export WANDB_API_KEY="<your key from wandb.ai/authorize>"
uvx marimo edit --sandbox serverless-inference/cw_inference_first_run.py
```

Requires [uv](https://docs.astral.sh/uv/). Or click the molab badge and run it in your browser with no local setup at all.

## What this repo is, and is not

**It is public, and it contains no customer information of any kind** — no company or personal names, no data, no credentials, nothing sourced from an internal system. Every example input is synthetic, written for the demo, and each notebook says so. This is an absolute rule rather than a default, and the reasoning is in [ADR-0001](docs/adr/0001-no-customer-or-private-information-ever.md).

**Nothing here collects anything from you.** No analytics, no telemetry, no phone-home, no writing your inputs or outputs to any store the author can read. You run these against your own data under your own credentials, and nothing about that run leaves your machine unless you send it somewhere yourself.

**Notebooks are small on purpose.** They aim to start fast, finish in a minute or two, and need nothing but a key — no GPU, no large downloads, no training ([ADR-0006](docs/adr/0006-portability-budget-for-notebooks.md)). A demo that needs more than that is not a notebook you can open from a link, and belongs elsewhere.

## Layout

One directory per demo, each self-contained with its own `README.md` and no shared code — a notebook is delivered on its own, so it has to make sense on its own ([ADR-0002](docs/adr/0002-one-directory-per-demo.md)). The vocabulary is in [`CONTEXT.md`](CONTEXT.md), the decisions are in [`docs/adr/`](docs/adr/README.md), and [`docs/contributing/`](docs/contributing/README.md) has the header template and the checklist for adding one.

## Licence

MIT. See [LICENSE](LICENSE).
