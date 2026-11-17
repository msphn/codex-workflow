# Workflow evidence and regression checks

Requires Python 3.9+ and Git. No third-party packages or provider credentials.

## Read-only evidence helper

After successful checkout preflight, freeze writers and capture the concrete
files/contracts behind the handoff. Use the immutable starting SHA, not HEAD~1:

```sh
python3 scripts/workflow_evidence.py snapshot --repo /absolute/application \
  --base <starting-sha> --remote-base origin/develop \
  --paths src/example.php tests/example.php > /absolute/run/evidence.json
python3 scripts/workflow_evidence.py check /absolute/run/evidence.json
```

Store output outside the application checkout so evidence does not change its
own status. `snapshot` writes JSON to stdout; it never stages, commits, fetches,
or modifies files. The caller owns saving it. `check` returns 0 for unchanged,
1 for changed, 2 for errors. Missing/deleted files, executable bits and symlink
targets are represented. Directories/submodules and symlinked parent paths are
rejected; enumerate concrete files and capture submodule checkouts separately.

Evidence includes all commits and committed paths from the starting base to HEAD,
whole-checkout status/index, and hashes of explicitly selected files only. A
change elsewhere can alter status without a content hash; an already-dirty file
outside the supplied scope can change without detection. Include all files and
contracts relevant to the result, and use the full diff for review. This is not
a complete repository backup, an ownership classifier, or an atomic lock.
Two matching reads detect ordinary concurrent edits but do not replace freezing
writers. Do not capture large unrelated files or secrets unnecessarily.

The remote-base fields describe a local ref, not proof of a successful recent
fetch. Record fetch time/result separately. False ancestry, mismatched branch,
owner changes and changed evidence go back to the coordinator under preflight.
An unchanged snapshot does not prove approval, passing tests, a current runtime,
or completed reviews. No helper output authorizes a commit.

## Deterministic tests

```sh
python3 -m unittest discover -s tests/workflow -p 'test_*.py' -v
```

Tests create disposable Git repositories with synthetic data under the system
temporary directory, make local fixture commits, and remove the fixtures. They
never use application repositories, networks or model APIs. They verify complete
commit-range evidence, preservation/visibility of owner-staged work, snapshot
invalidation, hook mutation detection, and remote-base ancestry reporting.
These are tests of evidence mechanics, not tests that an agent follows policy.

## Live agent behavior evaluations

Run only when the owner explicitly requests live evaluations. The deterministic
suite does not launch agents. Use the scenarios in [scenarios.md](scenarios.md),
with fresh sessions and designated disposable fixtures; do not execute them
against the owner's working checkouts. Provisioning fixture repositories for an
evaluation requires explicit evaluation authorization, not a ticket workaround.

Record workflow revision/fingerprints, harness and effective model settings,
scenario input, tool transcript, observed file/index/commit changes, stage result,
violations, rework, elapsed time and available token usage. Judge actions and
artifacts against the scenario criteria, not an agent's recitation of the policy.
Compare before/after behavior with the same scenario and settings; repeat where
needed to account for variability. Mark unrun or inconclusive scenarios honestly.
