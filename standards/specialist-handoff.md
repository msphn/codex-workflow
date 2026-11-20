# Specialist assignments and results

Applies to specialists. The coordinator supplies this file’s absolute path with
each assignment.
Use it alongside role-specific evidence, standards, findings, and test tables.

## Assignment

Supply only stage-relevant inputs, with absolute paths and named sections:

- Task, assigned role, scope/files, constraints, and expected stage result.
- Original requirements and approved contracts relevant to this stage; actual
  owner approval for implementation, and unresolved decisions where applicable.
- Checkout path, branch/HEAD, immutable starting base, current preflight evidence,
  existing-owner-change baseline, and exact snapshot being handed off.
- Required role/skill/repository instructions, applicable standards and exceptions.
- Evidence locations, available tools/services, and permitted tests/mutations.

Require explicit reads and local state verification. Missing or stale essential
inputs block dependent work. Keep implementation reasoning out of independent
review and acceptance assignments. No accumulated session transcript by default.

When the owner names an implementation to follow, treat matching it as an
acceptance criterion. The coordinator includes the exact reference paths in the
implementation and review assignments. The implementer starts from the reference
and adapts it only where the ticket or existing target behavior requires a
difference. Record the reason for material differences in the ticket plan.
Before checkpointing, the coordinator compares the changed files directly with
the reference and has the implementer remove unsupported additions. During
review, the reviewer independently makes the same comparison.

## Result

Start results with this header, followed by role-specific evidence:

```text
Status: COMPLETE | COMPLETE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
Scope and snapshot: assigned scope; branch/HEAD and relevant file fingerprints
Result: stage outcome, including findings or failed acceptance criteria
Evidence / checks: commands, outcomes, and exact evidence references
Concerns or missing inputs: specific unresolved issues, or none
Next action: concrete action and responsible actor
```

- `COMPLETE`: assigned work finished, with no unresolved concern. It never means
  the entire ticket passed all stages.
- `COMPLETE_WITH_CONCERNS`: assigned investigation/review/testing finished but
  findings, failures, uncertainty, or owner decisions remain. Include their impact.
- `NEEDS_CONTEXT`: required information is missing; name it and who can supply it.
- `BLOCKED`: the stage cannot finish, for example because a required service,
  permission, model, or check is unavailable. State what would unblock it.

Completed reviews or test executions may still have blocking findings or
failures. Missing runtime checks are blocked, never passed. Assessor
results still distinguish ready for planning from waiting for specific answers.

### Review checklist

For each assigned review domain, place a Markdown results table after the status
header. Copy the first column of the skill’s **What to check** table verbatim,
in order, with one row per item. Use the same format for standalone reviews.

| Review point | Result | Evidence or reason |
| --- | --- | --- |
| <exact review point> | <one outcome below> | <brief evidence, finding reference, or reason> |

- **Checked** — inspected the applicable scope and found no actionable issue.
  Name what was examined and the conclusion.
- **Found problems** — reference the numbered finding or findings for this item.
- **Skipped** — explain specifically why the item does not apply to this change.
- **Blocked** — identify the missing evidence or unavailable check and its impact.

When an item has both a finding and a verification gap, use **Found problems**
and record the gap in the same row. A blocked required check still affects the
overall status under the shared review method.

The coordinator records results in the existing run records; no extra report
per agent is required. Link large
raw artifacts where useful; the header must expose blockers without another read.
