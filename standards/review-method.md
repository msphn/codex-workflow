# Review evidence and reporting

Shared method for the code, architecture, and security review skills. Each skill
owns its review questions; this file keeps evidence and reporting consistent.
Read the actual code and verify claims before proposing changes. Review does not
authorize fixes, broader refactoring, or external actions.

## Scope and evidence

- For application ticket work, require coordinator preflight evidence and verify
  branch/HEAD and expected working-tree state before source inspection. Return
  missing evidence or mismatches to the coordinator. Do not fetch, switch branches,
  or update shared checkouts. Standalone reviews use their explicit scope/baseline.
- Read applicable repository instructions and supplied standards. Use original
  requirements, approved scope, existing-change baseline, and ownership/failure
  map where relevant; inspect actual code and callers rather than accepting an
  implementation summary. Report missing required inputs.

- Establish the requested scope, applicable instructions/standards, acceptance
  criteria, and baseline. Inspect the full in-scope diff and relevant untracked
  files, then trace affected callers and consumers. Separate introduced issues
  from existing problems that materially affect the work.
- Record the exact reviewed state: branch/HEAD and content fingerprints or an
  equivalent snapshot of relevant files/contracts. HEAD alone misses local edits.
  Return state mismatches to the coordinator; do not switch shared checkouts.
- Use actual requirements; label assumptions and missing context. Check nearby
  implementations and counterevidence before treating a pattern as defective.
  Verify uncertain external contracts against authoritative documentation.
- For an application-wide review, map main workflows and sample ordinary modules
  as well as hotspots. State coverage and omissions; do not imply exhaustive review.
- Explain concrete correctness, security, reading, or change consequences.
  Maintainability findings do not require a runtime bug. Design labels, arbitrary
  size limits, pattern preferences, and lint success are not evidence by themselves.

## Verification and permissions

- Use available test evidence and inspect its assertions. Run relevant checks
  only within the assignment's permissions and environment; coordinate shared
  fixtures and services. A read-only reviewer returns checks requiring writes or
  service-data changes to the coordinator rather than performing them itself.
- Reproductions must reflect real framework semantics. Distinguish source
  inspection, mocks, isolated fixtures, and real integration tests. Investigate
  failures enough to separate defects from environment or baseline limitations.
- Do not claim a mocked call or passing unit test establishes end-to-end behavior.
  Report exact checks, results, substitutions, and blocked checks. A review does
  not replace the separate black-box acceptance stage.
- Preserve unrelated work. Do not edit files, stage, commit, push, open PRs, deploy,
  change remote systems, or probe production as part of a review assignment.
  Specialists do not delegate; the coordinator owns delegation and fixes.
  Read-only behavior is an instruction, not a separate sandbox; permissions are
  inherited from the session.

## Findings

Number findings locally using this format; the coordinator renumbers merged results:

```text
{number}: {severity} - {title}
Domain: {code | architecture | security; list multiple after reconciliation}

{file:line, evidence, trigger or maintenance burden, affected caller, consequence}

{smallest proportionate recommendation}
```

Use impact severity in every review domain:

- **critical:** Severe impact on core behavior, data integrity, confidentiality,
  or availability; a release blocker.
- **important:** A material correctness, reliability, security, or maintainability
  problem that should be fixed before shipping; explain why it blocks.
- **improvement:** An optional change with a concrete benefit; does not block shipping.

Code, architecture, and security reviewers each assign severity to their own
findings using this scale. `security` identifies a domain, not a severity. For a
security finding, additionally state attacker prerequisites, reachable path,
impact, and whether it should block shipping. The coordinator preserves domain
attribution and reconciles severity by practical impact, not by reviewer identity.
Order findings by urgency. Keep each independently actionable, distinguish
confirmed issues from uncertain concerns, and retract claims contradicted by evidence.
Do not downgrade a material reading/change burden solely because behavior works.
If nothing actionable remains, say so without inventing findings.

## Review result

Return the review domain, context mode/limitations, scope, reviewed state, findings, counterevidence or
uncertainty, checks/results, coverage gaps, and any owner decisions needed.
Distinguish a completed review with no findings from a blocked review. If asked
for an overall assessment, explain its criteria, strengths, and limitations;
do not infer authorship or intent from the code. Only the coordinator merges
domains, resolves overlaps, and reports completion of the full review stage.
