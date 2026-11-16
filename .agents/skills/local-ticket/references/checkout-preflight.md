# Checkout and branch preflight

The coordinator owns this check for every affected application checkout.
Run it before source inspection, before implementation starts, on resume, and
when adding a repository. Specialists verify the handed-off state locally;
they do not switch branches or update the checkout themselves. This procedure
covers application repositories, not edits to the orchestrator setup itself.

## Defaults and permitted initial inspection

- The standard branch model is `master`/`develop`. Use `develop` as the base for
  new ticket branches unless the owner explicitly specifies another base.
  Do not implement on `master` or directly on `develop`.
- Use `origin` unless the owner or repository instructions identify another
  remote. If remote/base selection is missing or conflicting, ask; do not
  silently substitute the current branch, remote HEAD, `main`, or `master`.
- Before the check passes, read only repository instructions and Git metadata
  needed for it: checkout identity, branch/HEAD, status (including untracked
  files), remotes, refs, and in-progress Git operations. Defer source searches,
  diffs, manifests, dependency inspection, and tests until the check passes.
- Record the original branch, HEAD, and status before changing checkout state.
  Block on an unfinished merge, rebase, cherry-pick, or other Git operation.

## Fresh remote state

Fetch the selected base explicitly, for example:

```sh
git fetch origin refs/heads/develop:refs/remotes/origin/develop
```

Use the actual selected remote/base when different. Require a successful fetch
and a resolvable remote-tracking ref; record its commit ID and fetch time. A
cached ref or failed fetch does not establish freshness. If the ref was rewritten
and the fetch fails, report it rather than forcing the update. Handle permission
or network failures through the session's normal approval/error mechanisms.

## New ticket: assessment and planning on the base

- Require the selected local base branch to exist. If it is absent, report the
  gap rather than creating a replacement or using another branch.
- If the checkout is on another branch and is clean, switch to the existing
  base with `git switch develop` (substitute an explicitly selected base).
  Never force a switch or carry dirty work across branches automatically.
- Compare local base HEAD with the freshly fetched base. If equal, continue.
  If strictly behind and clean, update with `git merge --ff-only origin/develop`.
  If ahead, diverged, detached, or dirty and requiring a switch/update, stop for
  the owner's decision. Never reset, clean, stash, rebase, or create merge commits
  to make the check pass. Recheck branch, HEAD, and status after any operation.
- Pass only when checked out on the selected base and HEAD equals the fetched
  base commit. Existing local edits may remain only when no switch/update was
  needed; record them in assessment and resolve overlaps before implementation.
- An existing feature branch is not evidence of an authorized resume. Preserve
  it; do not reuse it for a new ticket even if its name looks related.

## Assessment to planning

Planning stays on the verified base for a new ticket; do not create a ticket
branch yet. Supply the assessment's preflight evidence and current expected
changes. The planner verifies branch/HEAD and working-tree state before source
inspection. A mismatch returns to the coordinator for fresh preflight; resume
and added repositories also require it. Record changed evidence and invalidate
affected conclusions before dependent planning.

## After approval: create the ticket branch

Repeat the fetch and base checks before implementation. If the base changed since
assessment, reassess affected conclusions and update the plan/baseline; seek
renewed approval only for material scope or contract changes.

Require a clean checkout before creating a ticket branch, or an explicit owner
decision about carrying existing edits into that branch. Use the branch naming
convention in the orchestrator root `AGENTS.md` unless the owner explicitly
specifies another name. For a pasted ticket without a Jira key, obtain the key
or an explicit branch name before creating the branch; assessment may continue.
Create it from the verified checked-out base using
`git switch -c <ticket-branch>`. Never use `-C` or overwrite an existing name; a
collision requires an owner decision or another unused name. Record branch name,
base commit, HEAD, and pre-existing changes. Confirm the new branch HEAD equals
the fetched base before handing off implementation. Do not commit or push.

## Resume and stage handoffs

- A resumed ticket may stay on its recorded ticket branch. Fetch the base again,
  then verify checkout path, ticket branch, HEAD, recorded base commit, and
  working-tree state against the run notes before source inspection or edits.
  Never treat missing records as proof that an arbitrary feature branch is valid.
- Require the recorded base to be an ancestor of ticket HEAD and the fresh remote
  base to be an ancestor of ticket HEAD. If either check fails, stop for the
  owner's decision; do not automatically switch away, rebase, merge, or move
  uncommitted ticket work. Remote-base advancement beyond ticket HEAD deliberately
  requires owner intervention, even if ticket files are unchanged. Report the
  recorded and fetched commits and await an explicit owner decision to update
  the checkout or continue on the recorded base. Record any exception and its
  scope; do not infer permission from an earlier implementation approval.
- Before each delegated stage, supply preflight evidence: path, remote/base,
  fetched base commit/time, expected branch/HEAD, existing changes, and owner
  exceptions. Specialists verify branch/HEAD and expected local changes before
  opening source or editing. A mismatch returns to the coordinator for a fresh
  check. Coordinate stage handoffs so no other agent switches the shared checkout.
- Dirty ticket changes are expected during implementation, review, and testing;
  compare them with the run baseline rather than demanding a clean checkout.
  Recheck after interruptions or signs of external changes. Invalidate affected
  assessment, planning, review, and test evidence after branch/base/code changes.

Record pass or blocked with evidence and the owner's actual exception/resolution.
A note saying “checked” is not proof of current checkout state. This is an
instruction-driven check, not an enforced Git hook or filesystem lock.
