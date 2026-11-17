# Conditional specialist assignments

Applies to local-ticket work. Assessment and planning still happen; these guards
choose who performs them. Standalone general reviews retain all three domains;
explicitly focused reviews retain their requested scope.

## Always required

Keep checkout preflight, applicable standards, existing-work protection, a concrete
plan and explicit owner approval before application edits, delegated implementation,
independent code review, and separate black-box acceptance. Model/effort settings,
commit rules, required runtime checks, and blocked-stage handling are unchanged.

## Guards

A specialist is required when any trigger in its row applies. Owner requests for
a specialist take precedence. A small diff or low file count never proves low risk.

| ID / specialist | Required when | Coordinator may handle / omit only when |
| --- | --- | --- |
| A / assessor | Requirements or acceptance criteria have material gaps or contradictions; repository/behavior ownership is uncertain; multiple repositories are affected; identifying affected behavior requires open-ended discovery. | A single repository and behavior owner are established, requirements and criteria are clear, and focused inspection identifies the affected behavior and closest existing pattern. Coordinator performs and records assessment. |
| P / planner | Multiple repositories; API/event/schema compatibility changes; changed ownership or shared contracts; transactions, async timing, retries or concurrency change; multiple mutation paths must preserve an invariant; new dependency/pattern or unresolved design/failure-handling choices. | One repository, an established applicable pattern, no listed trigger, and a concrete change/validation plan can be grounded in focused inspection. Coordinator produces the plan, including the scaled ownership/failure map. |
| R-A / architecture reviewer | Changed rule/state ownership, shared interfaces/contracts, dependency direction, persistence schema, transaction boundaries, events/retries/concurrency, or cross-component consistency/failure guarantees; a concrete architectural concern is discovered. | Evidence shows a local change following an existing pattern without any listed effect. Independent code reviewer verifies this classification against the full ticket diff and relevant callers. |
| R-S / security reviewer | Changed authentication/authorization/tenant isolation; sensitive data access/exposure; untrusted-input validation, parsing, escaping or flow into a sensitive sink; uploads/executable content; secrets/cryptography; security-relevant configuration/dependencies; abuse protections or a concrete reachable security concern. | Evidence shows no changed security behavior or trust boundary. Existing use of HTTP or user data alone is not a trigger; changes to their protection or handling are. Independent code reviewer verifies this classification against the full ticket diff and relevant paths. |

## Decisions and reclassification

After successful checkout preflight, the coordinator records A in assessment and
P, R-A, R-S in a `Specialist guards` table in plan.md before seeking approval:
`Guard | required / not required / unresolved | concrete evidence | stage owner`.
Use exact paths/sections and snapshot references, not just “simple” or “low risk”.
An unresolved guard is never an exemption: investigate it before dependent work;
if focused inspection cannot establish the exemption, assign the specialist.
Missing capability for a required assignment means blocked, not not-required.
No separate owner permission is needed to invoke a triggered specialist within
approved scope. Material application scope/contract changes still need approval.

Supply guard decisions with implementation/review handoffs. Implementers report
new triggers; the coordinator reassesses on changed scope, contracts, code or
resume evidence. Newly triggered assessment/planning must finish before dependent
implementation continues. Preserve useful existing evidence instead of restarting
unaffected stages. Do not use a late exemption to erase a blocking finding.

The independent code reviewer must report R-A and R-S as confirmed or challenged,
with evidence, even when both specialists were initially classified not required.
A challenged or unresolved exemption requires the relevant specialist before
review completion. This screening is not a completed architecture/security review.
For required domains use distinct independent reviewers and existing re-review
rules. Reassess guards after fixes; retain unaffected results only with reasons.

In review.md record an omitted domain as `not required — <guard/evidence>`, never
passed or completed. Final readiness requires current code review, all triggered
domain reviews, resolved blocking findings, and the existing acceptance checks.
Report omitted domains explicitly in handoff. Preserve prior review results;
workflow changes alone do not require repeating valid completed work.
