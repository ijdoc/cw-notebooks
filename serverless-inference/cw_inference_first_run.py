# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "openai>=1.40",
#     "weave",
# ]
# ///
"""CoreWeave Serverless Inference: first run.

Open-weight models behind an OpenAI-compatible endpoint. Run it with:

    uvx marimo edit --sandbox cw_inference_first_run.py

Dependencies are declared inline (PEP 723), so --sandbox resolves them itself.
Credentials are entered in the notebook; nothing needs exporting.
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

        [Model catalog](https://wandb.ai/inference) &nbsp;&middot;&nbsp;
        [Pricing](https://wandb.ai/site/pricing/inference) &nbsp;&middot;&nbsp;
        [Read more &#8594;](https://coreweave.com/products/serverless-inference)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        Open-weight models behind an OpenAI-compatible endpoint, billed per token. The API is the OpenAI API with a different base URL and key.
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
                                "_Don't have a `WANDB_API_KEY`? "
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
                            mo.md("_Both team and project are required for tracing_"),
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
def _(UI_API_KEY, UI_BASE_URL, UI_ENTITY, UI_PROJECT, mo):
    import os

    import weave
    from openai import OpenAI

    mo.stop(not UI_API_KEY.value)

    # Inference has its own endpoint, separate from the W&B base URL above.
    INFERENCE_BASE_URL = "https://api.inference.wandb.ai/v1"

    _entity = UI_ENTITY.value.strip()
    _project = UI_PROJECT.value.strip()
    _target = f"{_entity}/{_project}" if (_entity and _project) else None

    # weave authenticates from the environment, not from an argument.
    os.environ["WANDB_API_KEY"] = UI_API_KEY.value
    if UI_BASE_URL.value.strip():
        os.environ["WANDB_BASE_URL"] = UI_BASE_URL.value.strip()

    # weave.init patches the OpenAI client, which is what produces traces.
    # The project= argument below is usage attribution and does not trace.
    tracing_on = False
    _tracing_error = None
    if _target:
        try:
            weave.init(_target)
            tracing_on = True
        except Exception as _e:
            _tracing_error = f"{type(_e).__name__}: {_e}"

    client = OpenAI(
        base_url=INFERENCE_BASE_URL,
        api_key=UI_API_KEY.value,
        project=_target,
    )

    if tracing_on:
        _status = f"Tracing to Weave under `{_target}`."
        _kind = "success"
    elif _tracing_error:
        _status = f"**Weave tracing failed:** `{_tracing_error}`"
        _kind = "danger"
    else:
        _status = "**Tracing is off.** Fill in both team and project above to turn it on."
        _kind = "warn"

    mo.md(f"Connected to `{INFERENCE_BASE_URL}`. {_status}").callout(kind=_kind)
    return INFERENCE_BASE_URL, OpenAI, client, os, tracing_on, weave


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

        ```python
        import os

        # the OpenAI SDK, pointed at CoreWeave instead of OpenAI
        from openai import OpenAI

        # your W&B API key, from wandb.ai/authorize
        WANDB_API_KEY = os.environ["WANDB_API_KEY"]

        client = OpenAI(
            # Inference has its own host, separate from the W&B API
            base_url="https://api.inference.wandb.ai/v1",
            # the same W&B key authenticates inference
            api_key=WANDB_API_KEY,
            # optional: attributes the spend to a team and project
            project="<team>/<project>",
        )

        # the catalog, as the API has it right now
        models = client.models.list()

        # each entry carries the model string you pass as model=
        for m in models.data:
            print(m.id)
        ```
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
        ## 2. Run an inference

        With the client from section 1, a request is the OpenAI chat completions call, unchanged:

        ```python
        resp = client.chat.completions.create(
            # any model string from the catalog above
            model="meta-llama/Llama-3.3-70B-Instruct",
            # the conversation so far, oldest first
            messages=[{"role": "user", "content": "Why is the sky blue?"}],
            # the ceiling on what the model may generate in reply
            max_tokens=600,
        )

        # the reply itself; usage and finish_reason come back alongside it
        print(resp.choices[0].message.content)
        ```

        Every model in the catalog takes that same request shape and returns the same response shape, so moving between them is a one-string change. Pick one below and send a prompt.

        /// admonition | Reasoning models need a larger max_tokens
            type: warn

        When using a reasoning model, allow enough tokens for the reasoning field *and* the reply. At least 600 is a reasonable floor, which is the default below.

        Reasoning models spend tokens thinking before answering, and that thinking is returned in a separate `reasoning` field rather than in `content`. If you set `max_tokens` too low, the budget is consumed by reasoning: `content` comes back empty with `finish_reason: "length"`.

        `openai/gpt-oss-120b` is a reasoning model. The dropdown is ordered non-reasoning-first.
        ///
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, models):
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

    mo.vstack(
        [
            mo.hstack([model_picker, max_tokens], justify="start", gap=2),
            prompt_box,
            send_button,
        ]
    )
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
        mo.md(_content if _content.strip() else "_(empty, see the note above)_"),
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
        ---
        ## 3. Compare cost and latency

        This sends the same prompt to each selected model and times it. Every column in the table comes from the response you saw in section 2:

        - `seconds`: wall-clock time measured around the call, not something the API returns.
        - `prompt tokens`: `usage.prompt_tokens`, what your prompt cost to send.
        - `completion tokens`: `usage.completion_tokens`, what the model generated in reply.
        - `tokens/sec`: `usage.completion_tokens` divided by `seconds`.
        - `finish`: `choices[0].finish_reason`. `stop` is a complete answer, `length` is one cut off at `max_tokens`.

        Both token counts are what you are billed on. Per-token prices are on the [pricing page](https://wandb.ai/site/pricing/inference).
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
        ## 4. Move to dedicated capacity

        Dedicated Inference serves your own weights on dedicated GPU nodes, through the same OpenAI-compatible API. Take the client from section 1 and point it at your own endpoint:

        ```python
        # your own dedicated endpoint, same call sites
        client = OpenAI(
            base_url="https://<your-endpoint>.inference.coreweave.com/v1",
            api_key=WANDB_API_KEY,
            project="<team>/<project>",
        )
        ```

        That base URL is the only line that changes. The requests, the response handling and the model strings stay exactly as they are above.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        ## 5. Trace calls to Weave

        Two separate things are involved here, and only the first produces traces. `weave.init` patches the OpenAI client, so every call made afterwards is logged with its inputs, outputs, token counts, latency and cost. The `project` argument on the client is usage attribution: it tags spend, and on its own it traces nothing.

        ```python
        import os
        import weave
        from openai import OpenAI

        # weave authenticates from the environment, not from an argument
        os.environ["WANDB_API_KEY"] = WANDB_API_KEY

        # 1. Tracing. Patches the OpenAI client, so calls below are logged.
        weave.init("<team>/<project>")

        client = OpenAI(
            base_url="https://api.inference.wandb.ai/v1",
            api_key=WANDB_API_KEY,
            # 2. Usage attribution.
            project="<team>/<project>",
        )
        ```

        `weave` is declared in this notebook's inline dependencies, so it is already installed. In your own project run:

        ```sh
        pip install weave
        ```

        ### Put the reasoning in its own column

        A reasoning model returns its thinking in `choices[0].message.reasoning`, buried three levels into the response. Wrap the call in a `weave.op` and return that field at the top level, and it becomes a column of its own:

        ```python
        # @weave.op logs whatever the function returns as the call's output
        @weave.op
        def ask(prompt: str, model: str) -> dict:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
            )
            message = resp.choices[0].message
            # both at the top level, so Weave shows them as output.content
            # and output.reasoning rather than nested inside the response
            return {
                "content": message.content,
                "reasoning": getattr(message, "reasoning", None),
            }
        ```

        In the traces table, add `output.reasoning` through the column manager. Filtering it on "is not empty" finds the calls that spent their budget thinking. Column paths take dots for keys and square brackets for list indices, so on the untouched OpenAI call the same field is `output.choices[0].message.reasoning`.
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
        f"Every call above is logged under `{_entity}/{_project}`.\n\n"
        f"[Open in Weave &#8594;]({_app}/{_entity}/{_project}/weave)"
        if tracing_on
        else "Enter a team and a project in the form at the top to log calls to Weave."
    ).callout(kind="success" if tracing_on else "warn")
    return


if __name__ == "__main__":
    app.run()
