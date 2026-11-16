---
name: code-review
description: Review implementation correctness, cognitive complexity, Clean Code, SOLID, KISS, YAGNI, DRY, and test coverage. Use for a focused code review or the code domain of a coordinated review; report findings without editing code or delegating.
---

# Code review

Read [the shared review method](../../../standards/review-method.md) and apply its
scope, evidence, permissions, and findings format. This skill runs independently;
it does not require architecture or security review to produce its result.
When delegated, perform only this domain and return to the coordinator.

A human should be able to follow inputs, decisions, side effects, and results.
Assess readability independently of runtime correctness. Use Robert C. Martin's
Clean Code and SOLID principles as diagnostic tools, not a demand for more classes.

## Inspect the implementation

- **Correctness:** Trace success and failure paths against the requirements.
  For refactors, compare outputs, side effects, errors, and state transitions.
  Check validation boundaries, missing/optional values, and unintended changes.
- **Cognitive complexity:** Identify nesting, tangled conditions, hidden state,
  temporal dependencies, and helper chains that require unrelated context to
  understand. Explain the actual reading burden. Metrics may locate hotspots;
  do not invent a universal function length or complexity threshold.
- **Clean Code:** Check meaningful names, cohesive functions, clear control flow,
  visible side effects, and comments that explain reasons. Prefer explicit steps
  over clever compression when they make the behavior easier to verify.
- **SOLID:** Check that a component has a coherent responsibility, new behavior
  does not require scattered edits, replacements honor caller expectations,
  interfaces expose what consumers need, and dependencies are explicit. Recommend
  an interface or extraction only for a concrete benefit. Module-wide boundary
  changes belong to architecture review; report overlaps to the coordinator.
- **KISS / YAGNI / DRY:** Question speculative features, unnecessary indirection,
  and unused code after tracing consumers. Consolidate repeated business rules
  with common ownership; keep simple repetition when an abstraction would hide
  meaning or couple independently changing behavior.
- **State and lifecycle:** Check mutation order, cleanup, retries, concurrency,
  and partial failure where the flow depends on them. For UI code, trace effect
  setup/cleanup, timers, pending work, changing inputs, and state ownership using
  the installed framework's semantics. Do not apply backend patterns to UI code.
- **Errors:** Preserve causes and useful diagnostics. Check what callers observe
  and where failures are logged; avoid silent success or unexplained fallback.
- **Tests:** Read assertions, not just test names. Check meaningful decisions,
  failure paths, and regression coverage. Identify tests that mirror calls while
  missing observable behavior, persisted state, or lifecycle guarantees.

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
