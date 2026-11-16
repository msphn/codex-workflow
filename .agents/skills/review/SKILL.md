---
name: review
description: Coordinate a review with separate code, architecture, and security specialists by default, then reconcile evidence-backed findings. Use for a general code/change-set/application review; focused review skills can also be invoked independently.
---

# Coordinate a review

The main session coordinates; it does not replace the independent reviewers.
Read [the shared review method](../../../standards/review-method.md) for evidence,
verification, and the merged findings format. Use project-local skills and roles.

## Default review split

For a general review, delegate all three domains, including small changes. Scale
scope and depth to the change rather than silently omitting a domain. A specialist
may report no applicable issue after inspecting its surface; a skipped or blocked
review is not a completed review with no findings.

| Domain | Role | Skill | Primary responsibility |
| --- | --- | --- | --- |
| Code | `code_reviewer` | [code-review](../code-review/SKILL.md) | Correctness, cognitive complexity, Clean Code, SOLID, KISS, YAGNI, DRY, tests |
| Architecture | `architecture_reviewer` | [architecture-review](../architecture-review/SKILL.md) | Coupling, cohesion, ownership, patterns, clean architecture, cross-boundary behavior |
| Security | `security_reviewer` | [security-review](../security-review/SKILL.md) | Applicable OWASP checks and concrete attack paths |

An explicitly focused request may use just the corresponding skill; label that
scope and do not claim a full review. If an existing workflow has already assigned
a domain, run only that domain; never restart coordination or delegate recursively.
The coordinator owns the cross-domain result and all specialist assignments.

## Assign

1. Establish the scope, acceptance criteria, baseline, changed files, and exact
   current content snapshot. Read applicable repository guidance and standards.
   In ticket work, retain the checkout preflight and approved scope; a review
   request does not grant permission to change branches or application code.
2. Start a distinct reviewer for each domain, none of whom implemented the change.
   Start initial reviews without inherited conversation history, using
   `fork_turns="none"` where supported. If unavailable, disclose inherited context
   in the results rather than claiming context isolation. Run reviewers in
   parallel when capacity permits, otherwise in waves; do not collapse domains
   into one agent to fit a concurrency limit.
3. Give each reviewer the same code snapshot, original requirements, existing-work
   baseline, relevant interfaces, ownership/failure map, test evidence, applicable
   instructions/standards, orchestrator root, role instructions, and its skill's
   absolute path. Include current checkout preflight evidence for ticket work.
   Make assignments self-contained and require explicit reads. Provide raw evidence
   without implementation reasoning or conclusions that favor a particular finding.
   Record the context mode and supplied inputs. Re-review may reuse that domain's
   reviewer with its prior findings and the new snapshot.
4. Keep the reviewed files stable while reviews run. Specialists inspect code and
   return evidence; they do not edit, delegate, change service data, or switch the
   shared checkout. Coordinate checks that might interfere with shared services.

If new named roles are unavailable in the session but delegation exists, read
`.codex/agents/<role>.toml` and supply its instructions to separate generic agents.
Disclose this fallback; do not claim the named roles were loaded. If delegation
is unavailable, report the missing independent reviews as blocked. Self-review
is not a substitute; do not start another process to evade session restrictions.

## Reconcile and follow through

- Wait for all assigned domains and record each result, reviewer, scope, snapshot,
  findings, verification, and blockers. Partial results remain partial.
- Inspect decisive evidence, deduplicate overlapping findings by underlying issue,
  and retain which domains raised them. Assign merged finding IDs and order by
  impact. Resolve conflicting recommendations against actual contracts and
  counterevidence; agreement between agents alone is not verification.
- Record any issue discovered outside a specialist's primary domain and route it
  to the relevant reviewer. Do not let scope boundaries hide a demonstrated defect.
- A review alone does not authorize fixes. In an approved implementation workflow,
  send scoped findings to the implementer; otherwise present recommendations.
  Bring material scope changes back to the owner.
- After edits, mark affected review results stale and have the relevant reviewers
  re-review the new state. Assess impact across all three domains; retain an older
  result only with an explicit reason its reviewed assumptions remain valid.
- Report the combined findings using the shared format, with per-domain coverage,
  verification limits, and unresolved decisions. The full stage is complete only
  when all required domains have current completed results; unresolved findings
  remain visible even after the review work itself is complete.
