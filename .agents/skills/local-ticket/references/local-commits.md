# Local checkpoint commits

Only the coordinator stages and commits ticket work. Read this procedure before
each checkpoint. Plan approval covers local commits within unchanged scope;
do not seek per-commit approval. This does not
authorize pushes, PRs, deployment, automatic amend/squash/rebase, or commits of
orchestrator setup changes. A commit is a checkpoint, not acceptance.

## Before staging

1. Require the owner's actual plan approval, assigned scope, verified feature
   branch, immutable starting base SHA, and existing-change baseline. Verify
   current branch/HEAD and changes against the last handoff. No commits during
   assessment/planning or on master/develop. Preserve explicit owner branch
   naming exceptions; never infer that an arbitrary branch is authorized.
2. Stop writers and coordinate shared services while checking and committing.
   Commit a coherent implementation step only after its required checks pass
   on the exact proposed contents. Failed or unavailable required checks leave
   that step uncommitted and blocked. Independent review and acceptance happen
   later and remain separate gates. Do not split changes to evade a failed check.
3. Inspect the existing index before staging. Owner-staged or unexplained staged
   changes block committing until the owner resolves their disposition. Do not
   unstage, stash, overwrite, or include them automatically. A failed previous
   coordinator commit may leave staged work: verify its recorded provenance
   and contents before retrying.
4. Compare changes with the owner baseline. Permission to carry or edit owner
   changes does not authorize committing them. Require explicit authorization to
   include them. If ticket and owner
   hunks cannot be separated reliably, pause committing and ask the owner.

## Stage, verify, commit

- Stage only explicitly selected ticket paths/hunks. Never use `git add .`,
  `git add -A`, `git commit -a`, or a commit command with path arguments that
  bypasses the inspected index. Inspect the complete staged diff and path list;
  each hunk must belong to approved ticket work or explicitly authorized owner work.
- Ensure staged contents match the validated implementation. Partial staging
  can produce a different program from the tested worktree; validate the exact
  staged version or leave the commit blocked. Do not create a shadow checkout
  to work around this project's checkout policy.
- Use the ticket key followed by a colon, a space, and a short description
  as the commit subject, e.g. `DEV-123: foobar`.
  Commit only the inspected index with normal hooks enabled. Never bypass hooks,
  disable signing requirements, or change unrelated Git configuration to proceed.
- After success or failure, inspect HEAD, index, worktree, and untracked files.
  Hooks can modify files or stage additional changes. Compare the actual commit
  and remaining changes with the validated snapshot. If hooks changed code,
  mark affected evidence stale and rerun checks before review/acceptance credit.
  If unexpected or owner changes entered a commit, stop and ask for recovery;
  do not rewrite history or silently continue. A failed hook is not a commit.
- Record before/after SHA, purpose, selected changes, exact checks and results,
  hook outcomes, and any authorized owner changes in `plan.md`. Refresh checkout
  evidence for the next specialist. Store concise links in `status.md`.

## Review, fixes, and handoff

Review all changes since the recorded starting base, including every checkpoint
and any remaining local edits. Never use `HEAD~1` as the full-ticket baseline.
Review and acceptance fixes follow this same commit procedure; use follow-up
commits, then affected re-review/retest. Do not amend earlier checkpoints.

Record repositories separately. Cross-repository commits are not atomic;
a checkpoint in one repository does not establish ticket readiness. Handoff
includes base/HEAD, commit purposes, remaining changes, full-ticket diff commands,
current review results, acceptance outcomes, and blockers. The owner retains
final acceptance and decides whether to publish or rewrite history.
