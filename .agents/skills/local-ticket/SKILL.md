---
name: local-ticket
description: Coordinate work on a pre-qualified Jira ticket or pasted ticket across existing local repositories, from assessment and owner approval through implementation, independent review, local acceptance testing, and uncommitted handoff. Use for ticket implementation requests in the orchestrator project.
---

# Orchestrate a ticket

The main session owns coordination and user communication. Read the root
`AGENTS.md` and `repositories.local.toml`. If the local registry is missing,
request setup using `repositories.example.toml`; do not guess checkout paths.
Paths below are relative to the orchestrator
root, not a target checkout. Use the installed roles in `.codex/agents/`.
Do not apply this workflow recursively inside delegated tasks.

Follow the project boundaries, approval policy, and model/context selection rules
in `AGENTS.md`. Apply those rules to every specialist assignment, including the
assessor and implementer. Record model selection and usage in `status.md`.

Create `runs/<ticket-key>/` and the five records in
[the run template](references/run-template.md) at intake, even if assessment is
blocked. For a pasted ticket without a key, use a short descriptive directory name.
The coordinator owns these records; specialists return results for it to record.
Mark future stages not started and keep credentials and personal test data out.
Record the orchestrator revision and any uncommitted instruction changes, using
file fingerprints for the instructions actually applied. Keep status current.

## Local environment recovery

Apply the root `AGENTS.md` recovery policy throughout assessment, implementation,
review, and acceptance testing. Check required tools and local services before
dependent work; do not wait until handoff to discover that validation cannot run.
The coordinator diagnoses reported failures and attempts documented,
non-destructive startup/recovery within session permissions, coordinating shared
services so another specialist's checks are not disrupted. Verify readiness and
that services use the intended checkout, then rerun affected checks.

If recovery cannot proceed or fails, ask the owner for specific help with the
observed error, attempted commands/results, and what is needed next. Record the
blocker and pending owner action in the run notes; pause dependent work while
independent assessment may continue. Do not repeatedly retry an unchanged
failure, silently bypass tooling, or treat reduced validation as completion.
Carry this policy in specialist assignments; read-only specialists return
recovery needs to the coordinator rather than changing services themselves.

## 1. Assess

- Read the supplied Jira ticket through an available authenticated integration,
  or use the pasted ticket. If neither is accessible, request its contents.
- Resolve repository names through `repositories.local.toml`; relative paths are
  relative to that file. Inspect only repositories relevant to the ticket. An
  unregistered sibling may be added after verifying its path and relevance.
- Before source inspection or delegation, complete the coordinator-owned
  [checkout preflight](references/checkout-preflight.md) for each checkout.
  Record its evidence and any owner decisions in `assessment.md`.
- Select and read applicable engineering standards using the routing rules in
  the orchestrator root `AGENTS.md`. Supply their absolute paths to the assessor;
  have it confirm applicability from the actual repository files and manifests.
  Record standards read, repository-specific exceptions, and material conflicts
  in `assessment.md`. Reassess applicability if affected technologies change.
- Delegate repository assessment to `assessor`, providing ticket details,
  relevant registry paths, verified checkout evidence, and the required outputs below. The coordinator
  retains responsibility for questions, proposal, and approval.
- Read target repository instructions, including applicable parent and nested
  `AGENTS.md` files. Inspect `git status --short`, staged and unstaged diffs, and
  relevant untracked files. Record the initial branch/HEAD and existing changes
  so later review can distinguish ticket changes from the owner's prior work.
  If proposed work overlaps existing edits, ask the owner how to proceed and
  wait before touching those edits. Preserve staged state and untracked files.
- Identify dependencies, API/event/schema contracts, acceptance criteria, local
  services, test data, and build/test commands. For affected application behavior,
  record the ownership and failure map from `standards/software-design.md`: rule
  owner, mutation paths, dependent contracts/representations, and consistency
  requirements on failure. Keep detail proportionate to the change.
  Check effective session access;
  configuration on disk does not prove that the current session loaded it.
- Ask about material ambiguities and continue independent read-only assessment.

## 2. Propose and await approval

Present the affected repositories, intended changes, contract decisions,
implementation order, and validation plan. Identify checks already blocked by
missing infrastructure or data. Ask for explicit approval and stop before
editing application files or starting implementation agents. A ticket request,
silence, or a status entry is not approval. Record the owner's actual response
and approved scope; carry that approval forward without asking again.

## 3. Implement

After approval, repeat the checkout preflight and create the ticket branch from
the verified base as described in its reference. Reassess if the base changed.
On a resume, verify the recorded ticket branch instead of creating another one.
Provide the verified branch/HEAD, fetched base commit/time, and existing-change
baseline to the implementer; require local verification before source access.

Delegate to `implementer` after approval. Provide the ticket, acceptance criteria,
approved scope, repository paths and instructions, existing-change baseline,
contracts, the assessed ownership and failure map, file ownership, validation
plan, and the absolute paths of applicable
engineering standards with any recorded exceptions. Require the implementer to
read those standards before implementation. Use existing checkouts. Keep
writers sequential when files or contracts overlap. Only the coordinator may
create the approved ticket branch through the preflight procedure; specialists
must not switch shared checkouts. Do not create worktrees.

Preserve unrelated work, including changes inside files being edited. Bring
material scope or contract changes back to the owner for approval; routine
implementation choices and fixes within scope do not require renewed approval.
Wait for implementation and relevant checks before review.

## 4. White-box review

Follow the project-local [review coordinator](../review/SKILL.md) for delegation,
context selection, assignments, stable snapshots, reconciliation, and re-review.
Provide the current preflight evidence and the approved ticket assessment/plan.
Record its per-domain results, fixes, retained evidence, and blockers in `review.md`.
Route approved fixes to the implementer before acceptance testing.

## 5. Black-box testing

Start `black_box_tester` without inherited conversation history: use
`fork_turns="none"` where supported. Supply a self-contained assignment with the
orchestrator root, role instructions, applicable repository instructions, original
acceptance criteria, approved contracts, local endpoints/startup instructions,
permitted test data/mutations, and run directory. Do not pass implementation
reasoning or reviewer conclusions as expected behavior. If the client cannot
select fresh context, disclose inherited context in `tests.md`; do not claim
context isolation. On retest, supply the affected criteria and current runtime
evidence without redefining expected results from the fix.
Supply current checkout evidence and require local branch/HEAD verification
before local inspection or testing. Keep expected outcomes independent of
implementation summaries. Confirm services
use the current changed checkouts before crediting results.

Run observable acceptance checks against available local services. Record each
criterion as pass, fail, or blocked with evidence. A unit-test run or mocked
dependency does not prove the corresponding real integration. Fix failures
within scope, review relevant fixes, and rerun affected acceptance checks.
For environment blockers, follow the local environment recovery procedure above;
if recovery fails, request owner help and keep the affected criteria blocked.

## 6. Handoff

Wait for all delegated work. Inspect final working-tree state and distinguish
ticket changes from the baseline. Summarize changes by repository, review
findings and resolutions, exact tests run, per-criterion outcomes, blocked
checks, and open questions. Leave changes uncommitted for owner iteration.

## Resume and iterate

On feedback or a resumed ticket, read the run notes and compare the recorded
orchestrator revision/instruction fingerprints with the current workflow. Record
material workflow changes and any required revalidation; do not silently count
historical stages as satisfying newly introduced requirements. Existing owner
approval still carries forward for unchanged application scope.
Repeat the checkout preflight before inspecting source or editing. Do not switch
a dirty ticket checkout to the base to refresh it. Compare the run notes with actual
branch, HEAD, staged/unstaged diffs, relevant untracked files, and running service
versions. Record a content fingerprint or equivalent precise snapshot for the
files/contracts behind each review and test result; branch and HEAD alone miss
uncommitted edits. Mark affected review/test results stale after later changes.
Keep still-relevant evidence, but rerun invalidated checks before reporting them
as current. Resolve new overlaps with the owner. Reuse approval for unchanged
scope and seek approval for material scope or contract changes. Continue the
same run, recording the latest next action and handoff.

Markdown notes do not enforce a durable pipeline or permission separation.
Separate tester context reduces bias but cannot guarantee source-blind testing.

Use agent activity for progress visibility. If named roles are unavailable but
delegation exists, read the corresponding TOML instructions and pass them to
separate subagents, including configured model choices only when supported.
Disclose the fallback; do not claim per-role settings or isolation were applied.
If delegation itself is unavailable, report the required independent stage
blocked. Do not start another Codex process to evade session restrictions.

