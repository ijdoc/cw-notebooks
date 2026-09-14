---
status: accepted
---

# This repository is public, and no customer or private information ever enters it

This repo exists to be **read by strangers**. Its notebooks are served to customers through [molab](https://molab.marimo.io), which can only fetch from a public GitHub repository — so being public is not a convenience, it is the product requirement ([ADR-0003](0003-marimo-and-molab-as-the-delivery-surface.md)). Everything here is therefore written on the assumption that a customer, a competitor, a journalist and a search engine will all read it. **No customer information and no private information ever enters this repository** — not in a notebook, not in a commit message, not in a branch name, not in a committed session snapshot, and not in an issue.

This is an absolute rule, not a default to be weighed against convenience. There is no "internal" directory here and there never will be: internal framing lives in the private gig repo ([ADR-0004](0004-internal-framing-stays-in-the-private-repo.md)).

## What must never appear

- **Customer and prospect identity** — company names, people's names, job titles tied to a company, email addresses, phone numbers, logos. No exceptions for "they're a public reference" — customer-logo use needs marketing approval that this repo cannot carry.
- **Anything sourced from an internal system** — Salesforce records or links, Gong calls or transcripts or links, Granola notes, internal Confluence or Drive links, Slack quotes or channel names, `go/` links. A link alone leaks the account's existence and is as disqualifying as the content.
- **Customer data of any kind** — documents, prompts, datasets, outputs, logs, even a single row. Where a notebook needs input, it uses **synthetic data written for the purpose** and says so in the notebook.
- **Credentials and identifiers** — API keys, tokens, org or entity names, project slugs, endpoint hostnames that are not publicly documented, account ids. Notebooks read credentials from the environment and **never display them**, not even truncated: a committed session snapshot would preserve whatever was on screen.
- **Unreleased or internal-only product information** — roadmap, launch dates before announcement, internal reasoning about why a product exists, internal competitive analysis, pricing not on the public pricing page.
- **jdoc's own private information** — personal identifiers, host names, filesystem paths under `$HOME`, anything from the personal vault.

## Nothing is collected, either

The rule runs in both directions: these notebooks must not **gather** anything from whoever runs them. No analytics, no telemetry, no phone-home, no error reporting to a service jdoc controls, no writing a runner's inputs or outputs to a W&B project or any other store jdoc can read. A customer runs one of these against their own data, under their own credentials, and nothing about that run reaches jdoc unless they choose to tell him. A notebook that needs a destination for traces uses the runner's own project, named by the runner.

## Consequences

- **A demo that cannot be de-identified does not belong here.** It stays in the private repo and is delivered by screen share. That is a legitimate outcome, not a failure.
- **Synthetic data has to be good.** The honest cost of this rule is that writing convincing synthetic examples is real work, and a weak example makes a weak demo. Budget for it rather than reaching for something real.
- **Session snapshots are committed** for molab previews ([ADR-0005](0005-commit-session-snapshots-for-molab-previews.md)), and a snapshot captures rendered output. Anything the notebook *displays* is therefore published, which is why the credential rule above forbids even truncated display.
- **Git history is forever.** A leak fixed in a later commit is still public. The remedy for a real leak is to treat the material as compromised — rotate the credential, notify whoever is affected — not merely to push a correction.
- This repo's history is expected to survive jdoc's employment. Write accordingly.
