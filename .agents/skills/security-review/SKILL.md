---
name: security-review
description: Review applicable OWASP security basics by tracing attacker-controlled input, identity, authorization, sensitive data, configuration, and failure paths. Use for a focused security review or the security domain of a coordinated review; no code edits, production probes, or delegation.
---

# Security review

## Description

Read [the shared review method](../../../standards/review-method.md) and apply its
scope, evidence, permissions, and findings format. This skill can run independently.
When delegated, review only this domain and return to the coordinator.

Establish the affected attack surface: what an untrusted caller controls, which
identity/privileges they have, what boundary they cross, and which data or action
must be protected. Trace the path through actual code, middleware, configuration,
and infrastructure. A safeguard absent from a diff may exist elsewhere.

## Model selection

Use the model and reasoning effort configured for [security_reviewer](../../../.codex/agents/security_reviewer.toml). Follow the [coordinator’s model selection and escalation rules](../../../AGENTS.md#model-selection-and-context).

## What to check

Use the [OWASP Top 10](https://top10.owasp.org/2025/) as an awareness guide and the
[OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) for specific
controls. This is a scoped code review, not an OWASP compliance certification.
Do not force every topic onto every change; record inspected surfaces and gaps.

| Review point | What to inspect |
| --- | --- |
| Identity and access | Trace authentication, ownership, tenant isolation, object/action permissions, and server-side enforcement. Where relevant check token trust, expiry, issuer, audience, and session invalidation. |
| Input and injection | Trace controlled values to queries, commands, templates, HTML, paths, and parsers. Check parameterization, contextual encoding, safe paths, and allowed fields. |
| Sensitive data and cryptography | Inspect secrets, responses, logs, errors, caches, credentials, and transport protection. Verify established password, key, and cryptographic practices. |
| Configuration and supply chain | Check changed permissions, debug exposure, defaults, dependencies, builds, and artifact integrity. Verify advisory claims against installed versions and authoritative sources. |
| Workflow abuse | Trace reachable step bypass, replay, and resource exhaustion. Identify the business condition or limit that matters for this operation. |
| Failures and detection | Trace failed controls, leaked diagnostics, and security logging or alerting. Check whether useful evidence survives without exposing private data. |
| Feature-specific controls | Check relevant outbound destinations, browser credentials and CSRF, file storage and serving, deserialization, XML parsing, redirects, and origin protections. Consult the applicable official cheat sheet where needed. |
| Verification | Inspect denied-access and malicious-input tests alongside success paths. Verify mitigations and framework defaults against the reachable path. |

Inspect every item in **What to check**. Skip an item only when you can explain
why it does not apply. If evidence needed for an applicable check is unavailable,
report it as blocked and name the missing evidence.

In every review result, including a specialist handoff, return a Markdown table
with columns **Review point | Result | Evidence or reason**. Copy every review
point above verbatim, once, in the same order, including skipped and blocked
items. Use **Checked**, **Found problems**, **Skipped**, or **Blocked** as
defined in the [handoff checklist](../../../standards/specialist-handoff.md#review-checklist).

## Severity within this domain

Use the shared impact scale with exploitability, attacker prerequisites, and
exposure. Reachable account takeover or broad sensitive-data access can be critical;
a demonstrated weakness with material but more limited impact can be important.
Optional hardening without a demonstrated material weakness is an improvement.
Record `security` as the domain and justify severity from the actual attack path.

## Verify and return

Use only authorized local environments for reproductions; return checks needing
writes/service mutations to the coordinator. Do not probe live production or
invoke external actions to demonstrate a vulnerability.

Use the shared format and identify this as the `security` review. Each concrete
weakness must state attacker prerequisites, reachable source-to-effect path,
impact, evidence, and a proportionate fix. Distinguish a demonstrated weakness,
unverified concern, and optional hardening. Report blockers and coverage gaps;
no findings is not a guarantee that the application is secure.
