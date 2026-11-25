---
name: architecture-review
description: Review coupling, cohesion, responsibility and contract ownership, existing patterns, clean architecture, and cross-component failure behavior. Use for focused architecture review or the architecture domain of a coordinated review; do not edit or delegate.
---

# Architecture review

## Description

Read [the shared review method](../../../standards/review-method.md) and apply its
scope, evidence, permissions, and findings format. This skill can run independently.
When delegated, review only this domain and return to the coordinator.

Read the applicable technology standards and existing code before judging the
structure. Clean architecture is a way to examine responsibilities and dependency
direction, not a mandatory folder hierarchy or a reason to add layers.

## Model selection

Use the model and reasoning effort configured for [architecture_reviewer](../../../.codex/agents/architecture_reviewer.toml). Follow the [coordinator’s model selection and escalation rules](../../../AGENTS.md#model-selection-and-context).

## What to check

| Review point | What to inspect |
| --- | --- |
| Cohesion | Identify who owns each rule and the state it protects. Trace scattered rules or combined workflows and name a change that becomes harder. |
| Coupling | Follow imports, callers, listeners, configuration, and shared data. Check cycles, dependency direction, hidden dependencies, and leaked representations. |
| Existing patterns | Compare nearby implementations and repository conventions. Explain where a difference is justified or where following the pattern creates a concrete problem. |
| Clean architecture | Trace business behavior into presentation, transport, persistence, and vendor code. Check that a reusable operation is independent of its caller. Apply stack-specific patterns within their stated scope. |
| Contracts | Trace producers and consumers of APIs, events, and schemas. Check compatibility, version ownership, and representation or serialization changes. |
| Invariant coverage | Use the ownership and failure map from the plan (assessment for older runs), or derive one for standalone reviews. Trace all relevant mutation paths, including workers, retries, extensions, and relationship edits. Check the purpose of duplicated state. |
| Consistency and failure | Verify actual transaction and commit boundaries, derived-state invalidation, message snapshots versus reloads, and recovery after partial success. Trace the mechanism behind each delivery or atomicity claim. |
| Verification | Identify which tests exercise the real framework, persistence, or integration boundary behind each guarantee, and where only isolated collaboration was checked. |

Inspect every item in **What to check**. Skip an item only when you can explain
why it does not apply. If evidence needed for an applicable check is unavailable,
report it as blocked and name the missing evidence.

In every review result, including a specialist handoff, return a Markdown table
with columns **Review point | Result | Evidence or reason**. Copy every review
point above verbatim, once, in the same order, including skipped and blocked
items. Use **Checked**, **Found problems**, **Skipped**, or **Blocked** as
defined in the [handoff checklist](../../../standards/specialist-handoff.md#review-checklist).

## Contract cohesion

For a changed shared contract, compare its producers with the consumer paths:
which inputs identify the work, which are used, and which change the operation's
meaning? Backward-compatible signatures alone do not establish a cohesive
contract. Check whether callers must know another workflow's incidental inputs
or conventions. Recommend separation only when it removes concrete coupling or
makes independent responsibilities clearer; optional fields and branching are
not defects by themselves.

## Severity within this domain

Use the shared impact scale. A boundary or consistency failure that can lose data
or break a core cross-service operation can be critical. Material contract fragility
or change coupling can be important when its consequence is demonstrated. An
optional restructuring is an improvement; a pattern preference is not a blocker.

## Return

Use the shared format and identify this as the `architecture` review. For each
finding, name the responsibility/contract, affected callers, dependency or state
path, and concrete consequence. Propose a proportionate change within scope;
"violates clean architecture" alone is not a finding.

If a local correctness or security concern is encountered, flag its evidence and
suggest the appropriate domain; do not silently discard it or start another agent.
A clean architecture-review result does not establish completion of other domains.
