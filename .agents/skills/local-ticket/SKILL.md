---
name: local-ticket
description: Coordinate work on a pre-qualified Jira ticket or pasted ticket across existing local repositories, from assessment and planning through owner approval, implementation, independent review, local acceptance testing, and uncommitted handoff. Use for ticket implementation requests in the orchestrator project.
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
assessor, planner, and implementer. Record model selection and usage in `status.md`.

Create `runs/<ticket-key>/` and the five records in
[the run template](references/run-template.md) at intake, even if assessment is
blocked. For a pasted ticket without a key, use a short descriptive directory name.
The coordinator owns these records; specialists return results for it to record.
Mark future stages not started and keep credentials and personal test data out.
Record the orchestrator revision and any uncommitted instruction changes, using
file fingerprints for the instructions actually applied. Keep status current.

## Local environment recovery

Apply the root `AGENTS.md` recovery policy throughout assessment, planning, implementation,
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
  relevant registry paths, verified checkout evidence, and the required outputs
  below. The assessor owns focused requirements investigation; the coordinator owns preflight,
  effective access checks, questions, proposal, approval, and recording results.
  Inspect decisive evidence or gaps rather than routinely repeating the assessor's
  searches and source reads. This does not replace independent review.
- Require the assessor to read applicable parent and nested repository
  instructions, inspect `git status --short`, staged/unstaged diffs and relevant
  untracked files, and return the initial branch/HEAD and existing-change baseline
  so later review can distinguish ticket changes from the owner's prior work.
  The assessor reports overlaps; the coordinator asks the owner how to proceed
  and waits before dependent edits. Preserve staged state and untracked files.
- Require clarified scope and acceptance criteria, affected repositories and likely
  dependencies, confirmed behavior versus assumptions, meaningful product choices,
  and complexity or uncertainty for planning. Use focused source inspection to
  ground these conclusions; detailed design, file changes, failure-path tracing,
  and implementation/test order belong to planning.
- Ask about material ambiguities and record the owner's answers. Continue
  independent read-only assessment while waiting. End with **ready for planning**
  or **waiting for specific answers**. Unanswered requirements that materially
  change the solution block dependent planning; complexity alone does not.
- The coordinator checks effective session access; configuration on disk does
  not prove that the current session loaded it.

## 2. Plan

When assessment is ready, proceed without a separate assessment approval gate.
Delegate to `planner` with fresh context under the root AGENTS.md rules. Supply
the original ticket, clarified scope and acceptance criteria, assessment and owner
answers, registry paths, baseline, current checkout evidence, and absolute paths
of applicable engineering standards. Require local branch/HEAD and expected-change
verification before source inspection. On resume or when adding repositories,
repeat coordinator preflight first; mismatches return to the coordinator.

The planner reads repository instructions and standards, traces existing behavior
and contracts, and identifies the closest existing implementation. It owns the
detailed ownership and failure map from `standards/software-design.md`, proposed
changes and file ownership by repository, dependency order, compatibility and
migration needs, and concrete implementation and acceptance validation mapped to
criteria. It verifies documented tooling, service, and test-data readiness and
reports recovery needs to the coordinator. Record technical evidence, applicable
standards updates, decisions, and blocked checks in `plan.md`.

Use assessment evidence without routinely repeating discovery. The coordinator
checks decisive evidence and gaps, then presents the plan. If planning uncovers a
material product question, return it to the owner, record the answer in assessment,
and update dependent planning. Routine technical choices remain the planner's
responsibility. Neither specialist edits application files or approves implementation.

## 3. Propose and await approval

Present the affected repositories, intended changes, contract decisions,
implementation order, and validation plan. Identify checks already blocked by
missing infrastructure or data.

Identify the closest existing implementation and explain whether the proposal
follows it. Explicitly distinguish ticket requirements from optional policy
changes. For proposed deviations—such as a new dependency, lifecycle listener,
custom frontend asset, or content restriction—explain why the existing approach
is insufficient. Present optional additions separately from the minimum
implementation.

Ask for explicit approval and stop before
editing application files or starting implementation agents. A ticket request,
silence, or a status entry is not approval. Record the owner's actual response
and approved scope; carry that approval forward without asking again.

## 4. Implement

After approval, repeat the checkout preflight and create the ticket branch from
the verified base as described in its reference. Reassess if the base changed.
On a resume, verify the recorded ticket branch instead of creating another one.
Provide the verified branch/HEAD, fetched base commit/time, and existing-change
baseline to the implementer; require local verification before source access.

Delegate to `implementer` after approval. Provide the ticket, acceptance criteria,
approved scope, repository paths and instructions, existing-change baseline,
contracts, the planned ownership and failure map, file ownership, validation
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

## 5. White-box review

Follow the project-local [review coordinator](../review/SKILL.md) for delegation,
context selection, assignments, stable snapshots, reconciliation, and re-review.
Provide the current preflight evidence and the approved ticket assessment/plan.
Record its per-domain results, fixes, retained evidence, and blockers in `review.md`.
Route approved fixes to the implementer before acceptance testing.

## 6. Black-box testing

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

## 7. Handoff

Wait for all delegated work. Inspect final working-tree state and distinguish
ticket changes from the baseline. Summarize changes by repository, review
findings and resolutions, exact tests run, per-criterion outcomes, blocked
checks, and open questions. Leave changes uncommitted for owner iteration.

## Resume and iterate

On feedback or a resumed ticket, start with `status.md`, then read the linked
scope, approval, evidence, and outstanding decisions needed for the next stage.
Read earlier history when it affects those decisions; do not reload every artifact
by default. Compare recorded orchestrator revision/instruction fingerprints with
the current workflow. Record material workflow changes and any required
revalidation; do not silently count
historical stages as satisfying newly introduced requirements. Existing owner
approval still carries forward for unchanged application scope. Older runs may
retain technical evidence in assessment; link to that evidence instead of moving
or recreating it solely for the stage split. Require missing planning inputs for
the next dependent stage without rerunning completed assessment solely for format.
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

