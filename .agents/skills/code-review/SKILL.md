---
name: code-review
description: Review implementation correctness, cognitive complexity, Clean Code, SOLID, KISS, YAGNI, DRY, and test coverage. Use for a focused code review or the code domain of a coordinated review; report findings without editing code or delegating.
---

# Code review

## Description

Read [the shared review method](../../../standards/review-method.md) and apply its
scope, evidence, permissions, and findings format. This skill can run independently.
When delegated, review only this domain and return to the coordinator.

A human should be able to follow inputs, decisions, side effects, and results.
Assess readability independently of runtime correctness. Use Robert C. Martin's
Clean Code and SOLID principles as diagnostic tools, not a demand for more classes.

## Model selection

Use the model and reasoning effort configured for [code_reviewer](../../../.codex/agents/code_reviewer.toml). Follow the [coordinator’s model selection and escalation rules](../../../AGENTS.md#model-selection-and-context).

## What to check

| Review point | What to inspect |
| --- | --- |
| Correctness | Trace success and failure paths, validation, optional inputs, and caller-visible outputs, side effects, errors, and state transitions. For refactors compare against the baseline. |
| Cognitive complexity | Trace decisions through conditions, nesting, hidden state, helper chains, and required call order. Identify the specific reading burden. |
| Clean Code | Check names, function cohesion, control flow, visible side effects, and whether comments explain why. |
| SOLID | Check responsibility and reasons to change, scattered edits, substitutability, consumer needs, and dependency direction. Tie proposed interfaces or extractions to a concrete benefit. |
| KISS / YAGNI / DRY | Trace consumers. Check whether existing code already serves the requirement, whether each new mechanism earns its cost, and whether repeated rules have one owner. Preserve independently changing behavior. |
| State and lifecycle | Trace mutation order, cleanup, retries, concurrency, and partial failure. For UI changes also follow effects, timers, pending work, and changing inputs using the installed framework’s semantics. |
| Errors | Trace what callers observe, where failures are logged, and whether causes and diagnostics survive. Check fallbacks and silent success. |
| Tests | Read assertions for meaningful decisions, failures, persisted state, and observable lifecycle behavior. Identify guarantees that interaction mocks leave unverified. |

Inspect every item in **What to check**. Skip an item only when you can explain
why it does not apply. If evidence needed for an applicable check is unavailable,
report it as blocked and name the missing evidence.

In every review result, including a specialist handoff, return a Markdown table
with columns **Review point | Result | Evidence or reason**. Copy every review
point above verbatim, once, in the same order, including skipped and blocked
items. Use **Checked**, **Found problems**, **Skipped**, or **Blocked** as
defined in the [handoff checklist](../../../standards/specialist-handoff.md#review-checklist).

## Local decision pass

Start with changed local decisions before expanding into broad failure risks.
For a guard or fallback, trace the value from its construction and
actual callers: what states do the types permit, and which can reach this branch?
Check whether every condition justifies the resulting exception, response, or
default. A combined condition can conceal different failure meanings. Question
defensive checks when the established contract already guarantees the invariant;
do not remove protection merely because the happy path makes it look redundant.

For changed input contracts, compare what each caller must supply with what each
execution path uses. Explain any avoidable reading or change burden even when all
current calls work. Report concrete small improvements alongside larger defects;
do not invent a finding for every decision or require extra abstractions.

Include a compact decision-evidence table after the domain checklist for changed
rejection and fallback paths: **Location | Assumption and provenance | Outcome**.
Identify the actual constructor, caller, or lifecycle evidence, and whether the
branch and its outcome fit that evidence. Group equivalent paths; if none changed,
say so. A checklist label or a general statement that validation was checked does
not replace this trace. Use the table to support findings, not inflate their count.

## Ticket guard screening

For local-ticket reviews, read [stage guards](../../../standards/stage-guards.md)
and check the recorded R-A/R-S decisions against the full ticket diff and relevant
callers, contracts, and input/data paths. Return each exemption as confirmed or
challenged with evidence. Unknown applicability is challenged, not confirmed.
Report new triggers to the coordinator for a distinct specialist; do not delegate
or claim this screening completes architecture/security review. Standalone focused
code reviews retain their requested scope.

## Severity within this domain

Use the shared impact scale. A broken core workflow or data-corrupting result can
be critical; a material edge-case regression or demonstrated maintenance burden
can be important. Optional simplification is an improvement. Explain the actual
trigger and impact rather than assigning severity from a style label.

## Return

Use the shared format and identify this as the `code` review. State what was
actually checked and what remains unverified. For a maintenance finding, explain
which reading or change task becomes unnecessarily difficult and propose the
smallest improvement. Do not dismiss it solely because tests pass.

If a security or architectural concern is encountered, flag its evidence and
suggest the appropriate domain; do not silently discard it or start another agent.
A clean code-review result does not establish completion of the other domains.
