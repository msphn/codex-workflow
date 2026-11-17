---
name: architecture-review
description: Review coupling, cohesion, responsibility and contract ownership, existing patterns, clean architecture, and cross-component failure behavior. Use for focused architecture review or the architecture domain of a coordinated review; do not edit or delegate.
---

# Architecture review

Read [the shared review method](../../../standards/review-method.md) and apply its
scope, evidence, permissions, and findings format. This skill can run independently.
When delegated, review only this domain and return to the coordinator.

Read the applicable technology standards and existing code before judging the
structure. Clean architecture is a way to examine responsibilities and dependency
direction, not a mandatory folder hierarchy or a reason to add layers.

## Trace responsibilities and change impact

- **Cohesion:** Identify who owns each rule and the state it protects. Look for
  independent workflows combined in one component or one rule scattered across
  components. Explain a concrete change that becomes harder; size alone is not a
  finding, and extraction must clarify ownership rather than relocate complexity.
- **Coupling:** Follow imports, callers, listeners, configuration, and shared data.
  Check dependency direction, cycles, leaked representations, hidden dependencies,
  and contracts owned by the wrong layer. Events do not eliminate coupling.
- **Existing patterns:** Compare nearby implementations and repository guidance.
  Preserve useful conventions and recognize justified differences. A recurring
  poor pattern is not a requirement to copy it; recommend a scoped correction.
- **Clean architecture:** Check whether business behavior depends unnecessarily
  on presentation, transport, persistence, or vendor details. Verify reusable
  operations are independent of their caller. Apply technology-specific patterns
  only in their stated scope, not as universal architectural requirements.
- **Contracts:** Trace producers and consumers before proposing model/interface
  changes. Check API, event, and schema compatibility, version ownership, and the
  impact of serialization or representation changes across boundaries.
- **Invariant coverage:** Check the plan's ownership and failure map (or the assessment for older runs), or
  derive a compact one for standalone review. Follow all relevant mutation paths,
  including secondary entry points, workers, extensions, retries, and relationship
  edits. Question duplicated state while recognizing legitimate caches and drafts.
- **Consistency and failure:** Trace transaction ownership, actual commit timing,
  derived-state invalidation, message snapshots versus reloads, and recovery after
  partial success. Verify claimed atomicity/delivery through the actual mechanism;
  callback names or stable message IDs are not sufficient evidence.
- **Verification:** Check that tests exercise the boundaries supplying the claimed
  guarantees. Distinguish isolated collaboration tests from real framework,
  persistence, and integration behavior. Identify missing cross-boundary coverage.

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
