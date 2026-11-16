# Run notes

Create these five files under `runs/<ticket-id>/`. Replace prompts with evidence;
mark stages that have not run as **not started**. Keep credentials and personal
test data out of artifacts. Use paths, commands, and concise output excerpts.

Keep each fact in its owning record: assessment for requirements/baseline, plan
for approved decisions, review for findings, tests for acceptance evidence.
Other records may link to it's named section or a shared snapshot instead of
copying it. A reference must identify the exact evidence/version; it does not
replace checking current state. Keep `status.md` as the current stage, blockers,
and next-action index with links to detail. Preserve approval and decision history.
Update changed sections instead of rewriting the whole run after each tool call.
Store lengthy raw output in artifacts and summarize results, errors, and paths.

## status.md

- Ticket and summary
- Current stage
- Workflow version: orchestrator HEAD and relevant uncommitted instruction fingerprints; update on workflow changes
- Agent assignments: stage/role, agent identity, requested and exposed effective
  model/effort, fresh/inherited context, substitutions, and escalation reasons
- Usage and rework: available token/cost telemetry with source and accounting scope
  (including whether parent totals include children), elapsed time, repeated attempts,
  and reasons for rework; mark unavailable data unknown and avoid double-counting totals
- Approval: pending, or owner's decision and approved scope
- Checkout preflight: pass/blocked per repository, with evidence in assessment
- Blockers and questions
- Next action and owner
- Artifacts: [assessment](assessment.md), [plan](plan.md),
  [review](review.md), [tests](tests.md)
- Latest handoff: changes by repository and unresolved items

## assessment.md

- Original ticket and acceptance criteria, each with a stable identifier
- Orchestrator revision, applicable instruction paths/fingerprints, and workflow changes or owner exceptions on resume
- Repository paths and applicable instructions read
- Checkout preflight per repository: original branch/HEAD/status, selected
  remote/base, successful fetch time and commit, verified branch/HEAD,
  switch/fast-forward actions, blockers, and owner exceptions
- Applicable engineering standards: absolute paths read, applicability,
  repository-specific exceptions, and material conflicts or unreadable files
- Baseline: branch, HEAD, staged/unstaged changes, relevant untracked
  files, and content snapshots/fingerprints sufficient to identify later changes
- Existing-work overlaps and the owner's resolution
- Dependencies, shared contracts, assumptions, and missing information
- Ownership and failure map for affected application behavior (see
  `standards/software-design.md`): rule/state owner, mutation paths, dependent
  consumers/representations, and required consistency on failure; scale detail
  to the change and identify unresolved design decisions
- Available local services, test data, commands, and permission limitations
- Environment readiness and recovery: observed errors, attempted startup/recovery
  commands and results, readiness verification, and any help requested from the owner

## plan.md

- Proposed changes and file ownership by repository
- Ticket branch per repository, verified starting base commit, pre-implementation
  fetch/check evidence, and any owner decision about carrying existing edits
- Agreed API/event/schema contracts and dependency order
- Relevant ownership, transaction, message, and recovery decisions from assessment
- Implementation and acceptance test plan mapped to criteria
- Explicit approval record and any later scope decisions

## review.md

- Domain status table: code | architecture | security, each with reviewer,
  scope, not started/in progress/complete/blocked (or owner-requested omission),
  findings count, exact reviewed file/contract snapshot, checks, and limitations
- Ownership and failure map checked against actual callers, mutation paths, and
  side effects; record newly discovered paths or changed assumptions
- Reviewer context: fresh/inherited, selection mechanism or fallback, supplied inputs
- Consolidated numbered findings: impact severity, impact/trigger, file reference,
  evidence, consequence, recommendation, and originating review domain(s)
- Duplicate/conflicting findings reconciled with evidence; coordinator decisions
- Fix handoff and resolution per finding, affected domains, independent re-review
  results, and why any retained earlier domain results remain applicable
- Current versus stale results, missing/blocked domains, and unresolved findings;
  a skipped or blocked domain is not a completed review with no findings

## tests.md

- Tester identity, environment, running version, fixtures, context selection/fallback, and context seen
- Criterion | procedure/command | expected | observed | pass/fail/blocked
- Evidence and fingerprints of relevant code/contracts
- Data mutations and cleanup, if any
- Blocked checks and what would unblock them
- Environment recovery attempts, pending owner help, and checks rerun after recovery
- Fixes, affected re-runs, and stale results
