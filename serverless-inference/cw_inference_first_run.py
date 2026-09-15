# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "openai>=1.40",
# ]
# ///
"""CoreWeave Serverless Inference: first run.

Open-weight models behind an OpenAI-compatible endpoint, billed per token, with
no capacity commitment. Runnable by anyone with a CoreWeave / W&B API key:

    export WANDB_API_KEY="<key from wandb.ai/authorize>"
    uvx marimo edit --sandbox cw_inference_first_run.py

Dependencies are declared inline (PEP 723), so --sandbox resolves them itself;
nothing needs installing first.

All example data in this notebook is synthetic, written for the demo.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", app_title="CoreWeave Serverless Inference: first run")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    # Standard CoreWeave notebook header. See docs/adr/0009. Plain markdown,
    # so it renders the same in the editor, in app mode and in slide mode.
    # Copy verbatim into a new notebook; change only the title line and link.
    mo.md(
        """
        <img src="https://cdn.prod.website-files.com/62ba1fb86485b6d5029975c4/69de8e8600c3f18e49d4bf47_logo.svg" width="360" alt="CoreWeave" />

        # Serverless Inference: first run

        [Read more &#8594;](https://coreweave.com/products/serverless-inference)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """

        Open-weight models behind an OpenAI-compatible endpoint, billed per token, with no capacity commitment. The API is the OpenAI API with a different base URL and key.


        """
    )
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    UI_BASE_URL = mo.ui.text(
        label="WANDB_BASE_URL",
        placeholder="https://api.wandb.ai",
        value="https://api.wandb.ai",
        full_width=True,
    )
    UI_API_KEY = mo.ui.text(
        kind="password", label="WANDB_API_KEY", placeholder="********", full_width=True
    )
    UI_ENTITY = mo.ui.text(
        label="WANDB_ENTITY", placeholder="my_awesome_team", full_width=True
    )
    UI_PROJECT = mo.ui.text(
        label="WANDB_PROJECT",
        placeholder="my_awesome_project",
        value="cw-inference-first-run",
        full_width=True,
    )
    credentials_form = mo.vstack(
        [
            mo.md("\U0001F512 Enter your W&B credentials, and project settings."),
            mo.hstack(
                [
                    mo.vstack(
                        [
                            UI_BASE_URL,
                            mo.md(
                                "_Dedicated and on-prem customers will need to modify "
                                "`UI_BASE_URL` to match their custom domain_"
                            ),
                        ],
                        gap=0,
                    ),
                    mo.vstack(
                        [
                            UI_API_KEY,
                            mo.md(
                                "_Don't have an API key? "
                                "[Create one here](https://wandb.ai/authorize)_"
                            ),
                        ],
                        gap=0,
                    ),
                ],
                widths="equal",
                gap=2,
            ),
            mo.hstack(
                [
                    mo.vstack(
                        [
                            UI_ENTITY,
                            mo.md(
                                "_The team's name (default team will be used when left blank)_"
                            ),
                        ],
                        gap=0,
                    ),
                    UI_PROJECT,
                ],
                widths="equal",
                gap=2,
            ),
        ],
        gap=1,
    )
    credentials_form.callout()
    return UI_API_KEY, UI_ENTITY, UI_PROJECT


@app.cell
def _(UI_API_KEY, UI_ENTITY, UI_PROJECT, mo):
    from openai import OpenAI

    mo.stop(
        not UI_API_KEY.value,
        mo.md("Enter your API key above to continue.").callout(kind="warn"),
    )

    # Inference has its own endpoint, separate from the W&B base URL above.
    INFERENCE_BASE_URL = "https://api.inference.wandb.ai/v1"

    # Tracing is opt-in and points at *your* project. Nothing from this run
    # reaches anyone else. Both fields are needed, so the header is only sent
    # when they are both filled in.
    _entity = UI_ENTITY.value.strip()
    _project = UI_PROJECT.value.strip()
    _tracing = bool(_entity and _project)
    _headers = {"OpenAI-Project": f"{_entity}/{_project}"} if _tracing else None

    # The entire integration. There is no SDK to learn: this is the OpenAI
    # client with two arguments changed.
    client = OpenAI(
        base_url=INFERENCE_BASE_URL,
        api_key=UI_API_KEY.value,
        default_headers=_headers,
    )

    mo.md(
        f"Connected to `{INFERENCE_BASE_URL}`. "
        + (
            f"Calls are traced to Weave under `{_entity}/{_project}`."
            if _tracing
            else "Weave tracing is off; fill in both team and project above to turn it on."
        )
    ).callout(kind="success" if _tracing else "info")
    return INFERENCE_BASE_URL, OpenAI, client


@app.cell(hide_code=True)
def _():
    # Kept in its own cell so the timing helpers stay available even when a
    # gated cell below hasn't been run yet.
    import time

    return (time,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        ## 1. List the available models

        The catalog is available from the API, so it is current at the time you call it.
        """
    )
    return


@app.cell
def _(client, mo):
    models = sorted(m.id for m in client.models.list().data)

    mo.vstack(
        [
            mo.md(f"**{len(models)} models available**"),
            mo.ui.table(
                [
                    {"model": m, "publisher": m.split("/")[0]}
                    for m in models
                ],
                selection=None,
                page_size=10,
            ),
        ]
    )
    return (models,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        ## 2. Switch models

        Every model in the catalog takes the same request shape and returns the same response shape. Pick one and send a prompt.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, models):
    # Non-reasoning models first: they answer directly, which is what you want when
    # someone is watching. See the note under cell 4 about reasoning models.
    _preferred = [
        "meta-llama/Llama-3.3-70B-Instruct",
        "Qwen/Qwen3-235B-A22B-Instruct-2507",
        "deepseek-ai/DeepSeek-V3.1",
        "moonshotai/Kimi-K2.6",
        "openai/gpt-oss-120b",
    ]
    _options = [m for m in _preferred if m in models] + [
        m for m in models if m not in _preferred
    ]

    model_picker = mo.ui.dropdown(
        options=_options,
        value=_options[0],
        label="Model",
    )
    prompt_box = mo.ui.text_area(
        value=(
            "In two sentences, explain what a material certification is and "
            "why it matters when accepting a supplier shipment."
        ),
        label="Prompt",
        rows=3,
        full_width=True,
    )
    send_button = mo.ui.run_button(label="Send")

    mo.vstack([model_picker, prompt_box, send_button])
    return model_picker, prompt_box, send_button


@app.cell(hide_code=True)
def _(client, mo, model_picker, prompt_box, send_button, time):
    mo.stop(not send_button.value, mo.md("_Press **Send**._"))

    _t0 = time.perf_counter()
    _resp = client.chat.completions.create(
        model=model_picker.value,
        messages=[{"role": "user", "content": prompt_box.value}],
        max_tokens=400,
    )
    _elapsed = time.perf_counter() - _t0

    _msg = _resp.choices[0].message
    _content = _msg.content or ""
    _reasoning = getattr(_msg, "reasoning", None)

    _body = [
        mo.md(f"**{model_picker.value}** · {_elapsed:.2f}s · {_resp.usage.completion_tokens} completion tokens"),
        mo.md(_content if _content.strip() else "_(empty, see the note below)_"),
    ]
    if _reasoning:
        _body.append(
            mo.accordion({"Model's internal reasoning (returned separately)": mo.md(_reasoning)})
        )

    mo.vstack(_body)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        /// admonition | Reasoning models and max_tokens
            type: warn

        Some of these models are **reasoning** models. `gpt-oss-120b` is one. They spend tokens thinking before they answer, and that thinking comes back in a separate `reasoning` field rather than in `content`. If you set `max_tokens` too low, the budget is consumed by reasoning and **`content` comes back empty with `finish_reason: "length"`**. Not an error, just nothing.

        Either give reasoning models room (600+ tokens) or pick a non-reasoning model. The dropdown is ordered non-reasoning-first.
        ///
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        ## 3. Extract structured data from a document

        Given a JSON schema, the model returns JSON conforming to it. The schema is enforced during generation rather than requested in the prompt.

        **The text below is synthetic**, written for this demo. It resembles a nonconformance report but describes nothing real. Replace it with your own text and re-run.

        Run it with the default extraction instruction first and watch the `disposition` field.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    SAMPLE_DOC = """NONCONFORMANCE REPORT NCR-2026-0412
Line 3, Final Assembly. Raised 2026-08-19 by K. Osei (Quality Inspector II).

During receipt inspection of safety-critical valve assemblies (PO 4500-11872,
supplier Halstead Flow Systems), 3 of 12 assemblies were found with material
certifications that do not match the heat numbers stamped on the bodies.
Affected tags: V-1104A, V-1104C, V-1106B.

Applicable requirements: ISO 9001:2015 Clause 8.7; AS9100D Clause 8.7.1.
Procedure QA-PROC-208 Rev 5 governs disposition.

Disposition: USE-AS-IS rejected. Recommended REWORK pending supplier re-certification.
Supplier notified 2026-08-20. Engineering evaluation ER-2026-0155 opened.
Safety significance: none identified pending evaluation. Status: OPEN.
Target closure 2026-09-30."""

    doc_box = mo.ui.text_area(
        value=SAMPLE_DOC, label="Source document", rows=14, full_width=True
    )

    SYSTEM_PROMPTS = {
        "As written (the obvious instruction)": (
            "Extract fields from quality documents exactly as written. "
            "Do not infer or normalise values that are not present."
        ),
        "Negation-aware (after evaluating)": (
            "Extract fields from quality documents. Attend carefully to negation and to "
            "rejected or superseded values: if a value is stated then rejected, the correct "
            "answer is the value that stands, not the rejected one."
        ),
    }
    prompt_picker = mo.ui.radio(
        options=list(SYSTEM_PROMPTS),
        value="As written (the obvious instruction)",
        label="Extraction instruction",
    )
    extract_button = mo.ui.run_button(label="Extract to JSON")

    mo.vstack([doc_box, prompt_picker, extract_button])
    return SYSTEM_PROMPTS, doc_box, extract_button, prompt_picker


@app.cell
def _(SYSTEM_PROMPTS, client, doc_box, extract_button, mo, prompt_picker):
    import json

    mo.stop(not extract_button.value, mo.md("_Press **Extract to JSON**._"))

    # A strict schema: the model cannot return a shape that violates this.
    NCR_SCHEMA = {
        "type": "object",
        "properties": {
            "report_id": {"type": "string"},
            "unit": {"type": "string"},
            "date_raised": {"type": "string", "description": "ISO 8601 date"},
            "raised_by": {"type": "string"},
            "supplier": {"type": "string"},
            "affected_tags": {"type": "array", "items": {"type": "string"}},
            "quantity_affected": {"type": "integer"},
            "quantity_inspected": {"type": "integer"},
            "regulatory_citations": {"type": "array", "items": {"type": "string"}},
            "governing_procedure": {"type": "string"},
            "disposition": {
                "type": "string",
                "enum": ["USE_AS_IS", "REWORK", "REPAIR", "SCRAP", "UNDETERMINED"],
            },
            "safety_significance": {"type": "string"},
            "status": {"type": "string", "enum": ["OPEN", "CLOSED", "PENDING"]},
            "target_closure": {"type": "string"},
        },
        "required": [
            "report_id",
            "unit",
            "date_raised",
            "raised_by",
            "supplier",
            "affected_tags",
            "quantity_affected",
            "quantity_inspected",
            "regulatory_citations",
            "governing_procedure",
            "disposition",
            "safety_significance",
            "status",
            "target_closure",
        ],
        "additionalProperties": False,
    }

    _resp = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPTS[prompt_picker.value]},
            {"role": "user", "content": doc_box.value},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "ncr", "strict": True, "schema": NCR_SCHEMA},
        },
        max_tokens=800,
        temperature=0,
    )

    extracted = json.loads(_resp.choices[0].message.content)

    # The document says USE-AS-IS was *rejected* and REWORK recommended. Anything
    # else is a negation miss. Checked here rather than left to the eye, so the
    # notebook says it out loud whether or not anyone is watching closely.
    _disp = extracted.get("disposition")
    _verdict = (
        mo.md(f"`disposition` = **{_disp}**. Matches the document.").callout(kind="success")
        if _disp == "REWORK"
        else mo.md(
            f"`disposition` = **{_disp}**. **Wrong.** The document rejects USE-AS-IS and "
            "recommends REWORK. The shape is valid; the content is not."
        ).callout(kind="danger")
    )

    mo.vstack(
        [
            mo.md(f"**Schema satisfied** · {_resp.usage.total_tokens} tokens · `temperature=0`"),
            _verdict,
            mo.ui.table(
                [{"field": k, "value": json.dumps(v)} for k, v in extracted.items()],
                selection=None,
                page_size=20,
            ),
        ]
    )
    return NCR_SCHEMA, extracted, json


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ### The schema constrains the shape, not the content

        The document states that USE-AS-IS was **rejected** and REWORK recommended. The default instruction, "extract exactly as written", returns `USE_AS_IS`. The JSON is valid against the schema and the value is wrong, so no downstream validation would catch it.

        Switch the instruction to **Negation-aware** above and re-run. Same model, same schema, same document, correct answer. Both results are deterministic at `temperature=0`.

        Which of the two prompts is correct is established by testing them against documents whose answers are already known, not by reading them. That is what an evaluation set is for: label a sample by hand, then measure prompt and model changes against it. Weave runs and tracks those evaluations.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        ## 4. Compare cost and latency

        This sends the same prompt to each selected model and reports token counts and wall-clock time. Per-token prices are published on the [pricing page](https://wandb.ai/site/pricing/inference).
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, models):
    _bench_default = [
        m
        for m in [
            "meta-llama/Llama-3.1-8B-Instruct",
            "meta-llama/Llama-3.3-70B-Instruct",
            "Qwen/Qwen3-235B-A22B-Instruct-2507",
        ]
        if m in models
    ]

    bench_picker = mo.ui.multiselect(
        options=models, value=_bench_default, label="Models to compare"
    )
    bench_prompt = mo.ui.text_area(
        value=(
            "Summarise, in three bullet points, what a quality team must verify "
            "before accepting a shipment of safety-critical components."
        ),
        label="Prompt",
        rows=3,
        full_width=True,
    )
    bench_button = mo.ui.run_button(label="Run comparison")

    mo.vstack([bench_picker, bench_prompt, bench_button])
    return bench_button, bench_picker, bench_prompt


@app.cell(hide_code=True)
def _(bench_button, bench_picker, bench_prompt, client, mo, time):
    mo.stop(not bench_button.value, mo.md("_Press **Run comparison**._"))
    mo.stop(not bench_picker.value, mo.md("_Select at least one model._"))

    _rows = []
    for _m in bench_picker.value:
        try:
            _t0 = time.perf_counter()
            _r = client.chat.completions.create(
                model=_m,
                messages=[{"role": "user", "content": bench_prompt.value}],
                max_tokens=600,
            )
            _dt = time.perf_counter() - _t0
            _out = _r.choices[0].message.content or ""
            _comp = _r.usage.completion_tokens
            _rows.append(
                {
                    "model": _m,
                    "seconds": round(_dt, 2),
                    "prompt tokens": _r.usage.prompt_tokens,
                    "completion tokens": _comp,
                    "tokens/sec": round(_comp / _dt, 1) if _dt > 0 else None,
                    "finish": _r.choices[0].finish_reason,
                    "chars returned": len(_out),
                }
            )
        except Exception as _e:  # a model can be busy; don't kill the demo
            _rows.append({"model": _m, "seconds": None, "finish": f"error: {type(_e).__name__}"})

    mo.vstack(
        [
            mo.ui.table(_rows, selection=None),
            mo.md(
                "_Latency here includes your network path to the endpoint. "
                "Run it from where your workload actually runs for a number you can plan against._"
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        ## 5. Move to dedicated capacity

        Dedicated Inference serves your own weights on dedicated GPU nodes, through the same OpenAI-compatible API. Moving to it means changing the base URL:

        ```python
        # today: serverless, per-token, no commitment
        client = OpenAI(
            base_url="https://api.inference.wandb.ai/v1",
            api_key=api_key,
        )

        # later: your own dedicated endpoint, same call sites
        client = OpenAI(
            base_url="https://<your-endpoint>.inference.coreweave.com/v1",
            api_key=api_key,
        )
        ```

        The rest of the code is unchanged.

        ### Tracing

        If you entered a team and project at the top, calls from this notebook are logged to Weave, with traces, token counts and costs. It is one header, with no change at the call site:

        ```python
        client = OpenAI(
            base_url="https://api.inference.wandb.ai/v1",
            api_key=api_key,
            default_headers={"OpenAI-Project": "<your-team>/<your-project>"},
        )
        ```

        Traces go to your project only. Nothing from this notebook is reported anywhere else.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        ## Running this elsewhere

        This notebook is a single Python file with its dependencies declared inline. To run it anywhere:

        ```sh
        uvx marimo edit --sandbox cw_inference_first_run.py
        ```

        Your credentials go in the form at the top, so there is nothing to export and no key stored in the file.

        `--sandbox` reads the dependency list from the top of this file and builds its own environment, so there is nothing to install and nothing to conflict with what you already have. (`uv run cw_inference_first_run.py` also works, but runs it headlessly as a plain script rather than opening the notebook.)

        - **Keys**: [wandb.ai/authorize](https://wandb.ai/authorize)
        - **Model catalog and pricing**: [wandb.ai/site/pricing/inference](https://wandb.ai/site/pricing/inference)
        - **API reference**: OpenAI-compatible, anything the OpenAI Python client does, this endpoint does

        **Limit:** Serverless Inference is text-to-text only. Images, scanned documents and PDFs-as-images are not supported.
        """
    )
    return


if __name__ == "__main__":
    app.run()
