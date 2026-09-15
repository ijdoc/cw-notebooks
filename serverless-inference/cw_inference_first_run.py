# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "openai>=1.40",
# ]
# ///
"""CoreWeave Serverless Inference: first run.

Open-weight models behind an OpenAI-compatible endpoint. Run it with:

    uvx marimo edit --sandbox cw_inference_first_run.py

Dependencies are declared inline (PEP 723), so --sandbox resolves them itself.
Credentials are entered in the notebook; nothing needs exporting.

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
    # Copy verbatim into a new notebook; change only the title line and links.
    mo.md(
        """
        <img src="https://cdn.prod.website-files.com/62ba1fb86485b6d5029975c4/69de8e8600c3f18e49d4bf47_logo.svg" width="360" alt="CoreWeave" />

        # Serverless Inference: first run

        [Read more &#8594;](https://coreweave.com/products/serverless-inference) &nbsp;&middot;&nbsp;
        [Model catalog](https://wandb.ai/inference) &nbsp;&middot;&nbsp;
        [Pricing](https://wandb.ai/site/pricing/inference)
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
    return


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
            mo.md("\U0001f512 Enter your W&B credentials, and project settings."),
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
    return UI_API_KEY, UI_BASE_URL, UI_ENTITY, UI_PROJECT


@app.cell
def _(UI_API_KEY, UI_ENTITY, UI_PROJECT, mo):
    from openai import OpenAI

    mo.stop(not UI_API_KEY.value)

    # Inference has its own endpoint, separate from the W&B base URL above.
    INFERENCE_BASE_URL = "https://api.inference.wandb.ai/v1"

    # Tracing points at your own project. The header is only sent when both
    # the team and the project are filled in.
    _entity = UI_ENTITY.value.strip()
    _project = UI_PROJECT.value.strip()
    tracing_on = bool(_entity and _project)
    _headers = {"OpenAI-Project": f"{_entity}/{_project}"} if tracing_on else None

    client = OpenAI(
        base_url=INFERENCE_BASE_URL,
        api_key=UI_API_KEY.value,
        default_headers=_headers,
    )

    mo.md(f"Connected to `{INFERENCE_BASE_URL}`").callout(kind="success")
    return INFERENCE_BASE_URL, OpenAI, client, tracing_on


@app.cell(hide_code=True)
def _():
    # Kept in its own cell so the timing helpers stay available even when a
    # gated cell below has not been run yet.
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

    mo.md(f"**{len(models)} models**\n\n" + "\n".join(f"- `{m}`" for m in models))
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
    # Non-reasoning models first: they answer directly. See the note below the
    # response about reasoning models and max_tokens.
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

    model_picker = mo.ui.dropdown(options=_options, value=_options[0], label="Model")
    max_tokens = mo.ui.number(
        start=1, stop=8000, step=50, value=600, label="max_tokens"
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

    mo.vstack([mo.hstack([model_picker, max_tokens], justify="start", gap=2),
               prompt_box, send_button])
    return max_tokens, model_picker, prompt_box, send_button


@app.cell(hide_code=True)
def _(client, max_tokens, mo, model_picker, prompt_box, send_button, time):
    mo.stop(not send_button.value)

    _t0 = time.perf_counter()
    _resp = client.chat.completions.create(
        model=model_picker.value,
        messages=[{"role": "user", "content": prompt_box.value}],
        max_tokens=int(max_tokens.value),
    )
    _elapsed = time.perf_counter() - _t0

    _msg = _resp.choices[0].message
    _content = _msg.content or ""
    _reasoning = getattr(_msg, "reasoning", None)

    _body = [
        mo.md(
            f"**{model_picker.value}** &middot; {_elapsed:.2f}s &middot; "
            f"{_resp.usage.completion_tokens} completion tokens &middot; "
            f"finish_reason `{_resp.choices[0].finish_reason}`"
        ),
        mo.md(_content if _content.strip() else "_(empty, see the note below)_"),
    ]
    if _reasoning:
        _body.append(
            mo.accordion({"Reasoning returned by the model": mo.md(_reasoning)})
        )

    mo.vstack(_body)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        /// admonition | Reasoning models need a larger max_tokens
            type: warn

        When using a reasoning model, allow enough tokens for the reasoning field *and* the reply. At least 600 is a reasonable floor, which is the default above.

        Reasoning models spend tokens thinking before answering, and that thinking is returned in a separate `reasoning` field rather than in `content`. Set `max_tokens` too low and the budget is consumed by reasoning: `content` comes back empty with `finish_reason: "length"`. It is not an error, so nothing will flag it.

        `openai/gpt-oss-120b` is a reasoning model. The dropdown is ordered non-reasoning-first.
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

        Below: a short report, and five fields to pull out of it. The text is synthetic, written for this demo. Replace it with your own and re-run.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    SAMPLE_DOC = """NONCONFORMANCE REPORT NCR-2026-0412
Raised 2026-08-19 by K. Osei.

3 of 12 valve assemblies from supplier Halstead Flow Systems arrived with material
certifications that do not match the heat numbers stamped on the bodies.

Disposition: USE-AS-IS rejected. REWORK recommended, pending supplier re-certification.
Status: OPEN."""

    SYSTEM_PROMPTS = {
        "As written": (
            "Extract fields from quality documents exactly as written. "
            "Do not infer or normalise values that are not present."
        ),
        "Negation-aware": (
            "Extract fields from quality documents. Attend carefully to negation and to "
            "rejected or superseded values: if a value is stated then rejected, the correct "
            "answer is the value that stands, not the rejected one."
        ),
    }
    doc_box = mo.ui.text_area(
        value=SAMPLE_DOC, label="Source document", rows=9, full_width=True
    )
    prompt_picker = mo.ui.radio(
        options=list(SYSTEM_PROMPTS),
        value="As written",
        label="Extraction instruction",
    )
    extract_button = mo.ui.run_button(label="Extract to JSON")

    mo.vstack([doc_box, prompt_picker, extract_button])
    return SYSTEM_PROMPTS, doc_box, extract_button, prompt_picker


@app.cell
def _(SYSTEM_PROMPTS, client, doc_box, extract_button, mo, prompt_picker):
    import json

    mo.stop(not extract_button.value)

    NCR_SCHEMA = {
        "type": "object",
        "properties": {
            "report_id": {"type": "string"},
            "supplier": {"type": "string"},
            "quantity_affected": {"type": "integer"},
            "disposition": {
                "type": "string",
                "enum": ["USE_AS_IS", "REWORK", "REPAIR", "SCRAP"],
            },
            "status": {"type": "string", "enum": ["OPEN", "CLOSED"]},
        },
        "required": [
            "report_id",
            "supplier",
            "quantity_affected",
            "disposition",
            "status",
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
        max_tokens=600,
        temperature=0,
    )

    extracted = json.loads(_resp.choices[0].message.content)

    # The document rejects USE-AS-IS and recommends REWORK. Checked here rather
    # than left to the eye, so the notebook says it either way.
    _disp = extracted.get("disposition")
    _verdict = (
        mo.md(f"`disposition` is **{_disp}**, which matches the document.").callout(
            kind="success"
        )
        if _disp == "REWORK"
        else mo.md(
            f"`disposition` is **{_disp}**. The document rejects USE-AS-IS and "
            "recommends REWORK, so this value is wrong. The JSON is still valid "
            "against the schema."
        ).callout(kind="danger")
    )

    mo.vstack(
        [
            mo.md(
                f"Schema satisfied &middot; {_resp.usage.total_tokens} tokens "
                "&middot; `temperature=0`"
            ),
            mo.json(extracted),
            _verdict,
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

        This sends the same prompt to each selected model and reports token counts and wall-clock time. Per-token prices are on the [pricing page](https://wandb.ai/site/pricing/inference).
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
    mo.stop(not bench_button.value)
    mo.stop(not bench_picker.value, mo.md("Select at least one model."))

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
            _comp = _r.usage.completion_tokens
            _rows.append(
                {
                    "model": _m,
                    "seconds": round(_dt, 2),
                    "prompt tokens": _r.usage.prompt_tokens,
                    "completion tokens": _comp,
                    "tokens/sec": round(_comp / _dt, 1) if _dt > 0 else None,
                    "finish": _r.choices[0].finish_reason,
                }
            )
        except Exception as _e:  # a model can be busy; keep the rest going
            _rows.append(
                {"model": _m, "seconds": None, "finish": f"error: {type(_e).__name__}"}
            )

    mo.vstack(
        [
            mo.ui.table(_rows, selection=None),
            mo.md(
                "_Latency includes your network path to the endpoint. Run it from "
                "where your workload runs for a number you can plan against._"
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
        """
    )
    return


@app.cell(hide_code=True)
def _(UI_BASE_URL, UI_ENTITY, UI_PROJECT, mo, tracing_on):
    _entity = UI_ENTITY.value.strip()
    _project = UI_PROJECT.value.strip()
    # The app lives on the same host as the API, without the api. prefix.
    _app = (UI_BASE_URL.value.strip().rstrip("/") or "https://api.wandb.ai").replace(
        "//api.", "//", 1
    )

    mo.md(
        "### Tracing\n\n"
        + (
            f"Calls from this notebook are logged to Weave under `{_entity}/{_project}`, "
            f"with traces, token counts and costs.\n\n"
            f"[See traces &#8594;]({_app}/{_entity}/{_project}/weave/traces)\n\n"
            "Traces go to your project only. Nothing from this notebook is reported "
            "anywhere else."
            if tracing_on
            else "Enter a team and a project in the form at the top to log calls to Weave."
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        **Limit:** Serverless Inference is text-to-text only. Images, scanned documents and PDFs-as-images are not supported.
        """
    )
    return


if __name__ == "__main__":
    app.run()
