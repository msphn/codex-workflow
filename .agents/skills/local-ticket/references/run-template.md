# Run notes

Create these records under `runs/<ticket-id>/`. Replace prompts with evidence;
mark stages that have not run as **not started**. Keep credentials and personal
test data out of artifacts. Use paths, commands, and concise output excerpts.

Keep facts in their owning record: assessment for requirements/baseline; plan for
investigation, decisions, and approval; review for findings; tests for acceptance.
Link to named sections or shared snapshots instead of copying evidence. A
reference must identify the exact evidence/version; it does not
replace checking current state. Keep `status.md` as the current stage, blockers,
and next-action index with links to detail. Preserve approval and decision history.
Update changed sections instead of rewriting the whole run after each tool call.
Store lengthy raw output in artifacts and summarize results, errors, and paths.

## status.md

- Ticket and summary
- Current stage: assessment, planning, awaiting plan approval, implementation, review, acceptance, or handoff; distinguish blocked from not started
- Workflow version: orchestrator HEAD and relevant uncommitted instruction fingerprints; update on workflow changes
- Agent assignments: stage/role, agent identity, requested and exposed effective
  model/effort, fresh/inherited context, substitutions, and escalation reasons
- Usage and rework: available token/cost telemetry with source and accounting scope
  (including whether parent totals include children), elapsed time, repeated attempts,
  and reasons for rework; mark unavailable data unknown and avoid double-counting totals
- Approval: pending, or owner's decision and approved scope
- Specialist outcome headers from standards/specialist-handoff.md, with links
  to their owning records; completion of a stage is not ticket acceptance
- Per-repository starting base, current HEAD, checkpoint count, and remaining
  local changes; link commit/check evidence in plan.md
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
- Clarified scope and criteria, owner questions/options and actual answers
- Guard A decision, concrete evidence, and assessment owner (coordinator or assessor)
- Assessment outcome: ready for planning or waiting for specific answers
- Likely dependencies, confirmed existing behavior versus assumptions, complexity,
  and uncertainty for planning; distinguish requirement blockers from technical risks

## plan.md

- Specialist guards: P, R-A, R-S; required/not required/unresolved, evidence and stage owner; reclassifications with reasons (standards/stage-guards.md)
- Planning inputs: exact assessment/criteria version, owner answers, repository
  instructions, verified checkout/baseline evidence, and applicable standards read
- Updated standards applicability, exceptions, or conflicts discovered during planning
- Detailed source evidence, dependencies, shared contracts, and closest existing implementation
- Ownership and failure map for affected application behavior (see
  `standards/software-design.md`): rule/state owner, mutation paths, dependent
  consumers/representations, and required consistency on failure; scale detail
  to the change and identify unresolved design decisions
- Available local services, test data, commands, and permission limitations
- Environment readiness and recovery: observed errors, attempted startup/recovery
  commands and results, readiness verification, and any help requested from the owner

- Proposed changes and file ownership by repository
- Ticket branch per repository, verified starting base commit, pre-implementation
  fetch/check evidence, and any owner decision about carrying existing edits
- Immutable starting base SHA kept separately from later fetched bases and HEADs
- Checkpoint ledger per repository: before/after SHA, purpose, selected changes,
  exact checks/results, hook outcomes, authorized inclusion of owner changes,
  and remaining edits. No cross-repository atomicity implied
- Agreed API/event/schema contracts and dependency order
- Relevant ownership, transaction, message, and recovery decisions
- Implementation and acceptance test plan mapped to criteria
- Explicit approval record and any later scope decisions
- Planning outcome: ready for owner approval or blocked, with specific questions/checks

## review.md

- Domain status table: code | architecture | security, each with reviewer,
  scope, not started/in progress/complete/blocked/not required (with guard evidence),
  findings count, exact reviewed file/contract snapshot, checks, and limitations
- Independent code reviewer's R-A/R-S exemption screening: confirmed/challenged, evidence, newly required assignments and resolutions
- Ownership and failure map checked against actual callers, mutation paths, and
  side effects; record newly discovered paths or changed assumptions
- Reviewer context: fresh/inherited, selection mechanism or fallback, supplied inputs
- Consolidated numbered findings: impact severity, impact/trigger, file reference,
  evidence, consequence, recommendation, and originating review domain(s)
- Duplicate/conflicting findings reconciled with evidence; coordinator decisions
- Fix handoff and resolution per finding, affected domains, independent re-review
  results, and why any retained earlier domain results remain applicable
- Fix attempts per finding; after two unresolved attempts, fresh diagnosis or
  escalation and the changed approach before another attempt
- Full-ticket commit range and local edits inspected; exact reviewed HEAD and
  relevant content fingerprints, including any hook-induced changes
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
