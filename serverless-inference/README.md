# Serverless Inference — getting started

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/ijdoc/cw-notebooks/blob/main/serverless-inference/cw_inference_first_run.py)

Open-weight models behind an OpenAI-compatible endpoint, billed per token. Five sections, roughly two minutes each.

```sh
export WANDB_API_KEY="<your key from wandb.ai/authorize>"
uvx marimo edit --sandbox cw_inference_first_run.py
```

## What it covers

1. **The model catalog is an API call, not a slide.** Any list emailed to you is stale on arrival, so the notebook asks the endpoint.
2. **Switching models is a one-string change.** Same request shape, same response shape, different weights.
3. **A document becomes a row.** Schema-enforced extraction, where the shape is guaranteed during generation rather than hoped for in the prompt.
4. **Cost and latency you can measure.** Run your own prompt across several models and read the numbers off your own workload.
5. **The same code moves to dedicated capacity.** Two arguments change; every call site stays.

## The interesting part is section 3

The extraction demo is built around a **failure**, deliberately. The obvious instruction — "extract exactly as written" — misreads a *rejected* disposition on a nonconformance report and returns the rejected value, while producing perfectly valid JSON. Nothing downstream would flag it; a dashboard would show a clean row.

A negation-aware instruction fixes it. Both outcomes are deterministic at `temperature=0`.

The point is not that the model is bad. It is that **a schema guarantees the shape and not the truth**, and the difference between those two prompts is not something you reason your way to at a whiteboard — you find it by evaluating against documents whose answers you already know. For a regulated workload that is the whole ballgame.

## Two things worth knowing before you hit them

**Reasoning models can return empty content.** Some models in the catalog spend tokens thinking before answering, and return that separately from `content`. Set `max_tokens` too low and the budget goes to reasoning, leaving `content` empty with `finish_reason: "length"` — not an error, just nothing. Give them room, or pick a non-reasoning model when you want a direct answer.

**Serverless Inference is text-to-text today.** No image or multimodal support. If part of your workload is scanned documents or images, that part does not run here yet.

## About the example document

The nonconformance report in section 3 is **synthetic** — written for this demo, referencing real public standards but describing nothing and nobody real. Paste your own text over it; that is a better demo than anything prepared in advance.
