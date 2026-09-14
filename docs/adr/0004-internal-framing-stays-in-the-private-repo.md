---
status: accepted
---

# Internal framing stays in the private gig repo; this repo carries only what a customer may read

Every demo has two halves: the artifact a customer runs, and the internal reasoning around it — which account it is for, what they said on the last call, the commercial crux, what not to volunteer, the run sheet. Those halves live in **different repositories**. The runnable artifact lives here, public and de-identified. The framing lives in a separate private repository, which indexes this repo by link rather than copying anything from it. That repository is referred to here by role only: naming it would itself be a small leak, and this repo has no reason to know its address.

This is not a new idea being introduced; it is an existing practice being made explicit. The deprecated `autoresearch-loop` repo was already described as "deliberately kept separate … so the repo stays shareable with the prospect," with the framing held in a private note.

## Consequences

- **The account brief points here; nothing here points back.** A reader of this repo learns nothing about who a demo was built for, because there is no link to follow and no acknowledgement that an account exists.
- A notebook's own `README.md` describes what the notebook demonstrates, never who asked for it or why they were interested.
- When the two disagree — the private brief says "lead with the negation failure because they are a safety-critical buyer," the public notebook just demonstrates the negation failure — that is correct, not drift.
- The split has a cost: a demo's full story requires both repos, and only jdoc can see one of them. Accepted; the alternative is a public repo that leaks an account list.
