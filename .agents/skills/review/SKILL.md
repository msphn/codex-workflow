---
name: review
description: Coordinate independent code review and required architecture/security specialists, then reconcile evidence-backed findings. Use for a general code/change-set/application review; focused review skills can also be invoked independently.
---

# Coordinate a review

The main session coordinates independent reviewers.
Read the orchestrator root `AGENTS.md` and apply its model/context selection and
escalation rules. Record requested/effective model and effort, context mode, and
any substitution with each domain's results; mark unavailable telemetry unknown.
Read [the shared review method](../../../standards/review-method.md) for evidence,
verification, and the merged findings format. Use project-local skills and roles.
Use [the specialist handoff contract](../../../standards/specialist-handoff.md)
in assignments and require its status header in each result.

## Default review split

Standalone general reviews require all three domains; scale depth to the change.
For local-ticket work, read [stage guards](../../../standards/stage-guards.md): code
review is mandatory; R-A/R-S determine architecture/security assignments. Supply
recorded decisions to the code reviewer for independent verification against the
full ticket diff and affected paths. Unresolved/challenged exemptions require the
relevant specialist. Owner-requested domains always run.

Record valid exemptions as `not required` with guard evidence, not completed
reviews. A missing required domain is blocked. Screening does not claim specialist
coverage. A specialist may report no actionable issue after inspecting its surface.

| Domain | Role | Skill | Primary responsibility |
| --- | --- | --- | --- |
| Code | `code_reviewer` | [code-review](../code-review/SKILL.md) | Correctness, cognitive complexity, Clean Code, SOLID, KISS, YAGNI, DRY, tests |
| Architecture | `architecture_reviewer` | [architecture-review](../architecture-review/SKILL.md) | Coupling, cohesion, ownership, patterns, clean architecture, cross-boundary behavior |
| Security | `security_reviewer` | [security-review](../security-review/SKILL.md) | Applicable OWASP checks and concrete attack paths |

Focused requests may use one domain skill; label the scope, not a full review.
If an existing workflow has already assigned
a domain, run only that domain; never restart coordination or delegate recursively.
The coordinator owns the cross-domain result and all specialist assignments.

## Assign

1. Establish the scope, acceptance criteria, baseline, changed files, and exact
   current content snapshot. Read applicable repository guidance and standards.
   In ticket work, retain the checkout preflight and approved scope; a review
   request does not grant permission to change branches or application code.
   For ticket work, include every commit since the immutable starting base and
   remaining local edits/untracked files, distinguished from owner baseline work.
   The latest commit alone is not a full-ticket review.
2. Assign each required domain a distinct reviewer who did not implement the change.
   Start initial reviews without inherited conversation history, using
   `fork_turns="none"` where supported. If unavailable, disclose inherited context
   in the results rather than claiming context isolation. Run reviewers in
   parallel when capacity permits, otherwise in waves; do not collapse domains
   into one agent to fit a concurrency limit.
3. Give each reviewer the same code snapshot, original requirements, existing-work
   baseline, relevant interfaces, ownership/failure map, test evidence, applicable
   instructions/standards, orchestrator root, role instructions, and its skill's
   absolute path. Include current checkout preflight evidence for ticket work.
   Use absolute paths and named sections for shared inputs, require explicit reads,
   and keep the domain task and boundaries in each assignment. Provide raw evidence
   without implementation reasoning or conclusions that favor a particular finding.
   Include ticket guard decisions and require code-review screening of exemptions.
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
- Compare the review-point column in each specialist’s results table with the
  assigned skill’s **What to check** table. Require identical names and order,
  exactly one result per item, and a concrete reason for each skipped or blocked
  check. Return incomplete tables or unsupported conclusions to the reviewer.
- Check that maintenance conclusions use maintenance evidence. Current correctness,
  passing tests, or absence of a blocker alone do not settle the maintenance impact
  of a structural dependency or choice identified in a report. Apply this check even
  when the reviewer has not labeled that dependency a problem. If its reading or
  change cost remains unanswered, request one bounded
  follow-up on the concrete task and affected consumers, without prescribing a fix.
  Accept an evidence-backed no-finding answer; do not reopen resolved questions or
  turn this check into a finding quota or another full review.
- Lead the owner-facing review with the requested focus and its actionable
  findings, including non-blocking improvements. Include each assigned domain’s
  complete results table and update finding references to the merged IDs.
- Inspect decisive evidence, deduplicate overlapping findings by underlying issue,
  and retain which domains raised them. Assign merged finding IDs and order by
  impact. Resolve conflicting recommendations against actual contracts and
  counterevidence; agreement between agents alone is not verification.
- Record any issue discovered outside a specialist's primary domain and route it
  to the relevant reviewer. Do not let scope boundaries hide a demonstrated defect.
- A review alone does not authorize fixes. In an approved implementation workflow,
  send scoped findings to the implementer; otherwise present recommendations.
  Bring material scope changes back to the owner.
- Reconcile the code reviewer's guard screening before declaring the review complete;
  assign newly required domains and record evidenced exemptions in the domain table.
- After edits, reassess ticket guards and mark affected review results stale and have the relevant reviewers
  re-review the new state. Supply the changed snapshot, delta, affected findings,
  and any revised contracts; expand inspection to callers and assumptions affected
  by the delta. Do not routinely restart unchanged domain investigations.
  Assess impact across all three domains; retain an older result only with an
  explicit reason its reviewed assumptions remain valid.
- Report the combined findings using the shared format, with per-domain coverage,
  verification limits, and unresolved decisions. The full stage is complete only
  when all required domains have current completed results; unresolved findings
  remain visible even after the review work itself is complete.

## Non-progress checkpoint

Track fix attempts by consolidated finding ID in `review.md`. An attempt is
a fix followed by independent re-review. After
two attempts fail to resolve the same finding, require a fresh diagnosis or
model escalation under AGENTS.md before a third attempt. Record the evidence,
what changes in the approach, and who owns the next action. Do not restart the
counter by renaming or rediscovering the same underlying issue.

Keep the original implementer for ordinary follow-ups; stop its writing before
assigning replacement ownership. Material scope/contract changes return to the
owner. If no supported new approach is available, report the blocker and ask for
the specific decision needed. Never discard/downgrade a blocking finding or
declare completion merely because attempts were exhausted. Evaluate the two-attempt
threshold against run evidence.
