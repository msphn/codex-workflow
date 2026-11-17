---
name: security-review
description: Review applicable OWASP security basics by tracing attacker-controlled input, identity, authorization, sensitive data, configuration, and failure paths. Use for a focused security review or the security domain of a coordinated review; no code edits, production probes, or delegation.
---

# Security review

Read [the shared review method](../../../standards/review-method.md) and apply its
scope, evidence, permissions, and findings format. This skill can run independently.
When delegated, review only this domain and return to the coordinator.

Establish the affected attack surface: what an untrusted caller controls, which
identity/privileges they have, what boundary they cross, and which data or action
must be protected. Trace the path through actual code, middleware, configuration,
and infrastructure. A safeguard absent from a diff may exist elsewhere.

## Apply relevant OWASP checks

Use the [OWASP Top 10](https://top10.owasp.org/2025/) as an awareness guide and the
[OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) for specific
controls. This is a scoped code review, not an OWASP compliance certification.
Do not force every topic onto every change; record inspected surfaces and gaps.

- **Identity and access:** Separate authentication from authorization. Check
  ownership, tenant isolation, object/action permissions, and server-side access
  checks. Verify token signature/trust, expiry, issuer/audience as applicable,
  and session invalidation. Missing identity or failed checks must not grant access.
- **Input and injection:** Trace controlled values into SQL/NoSQL, commands,
  templates, HTML, paths, and parsers. Check parameterization, contextual output
  encoding, safe path handling, and allowlisted fields where mass assignment applies.
- **Sensitive data and cryptography:** Inspect secrets, responses, logs, errors,
  caches, credential handling, and transport protection. Verify established
  password/key/cryptography practices rather than recommending custom schemes.
- **Configuration and supply chain:** Inspect changed permissions, exposed debug
  features, unsafe defaults, dependency/build changes, and relevant data/artifact
  integrity checks. Verify vulnerability claims against current authoritative
  advisories and actual versions; do not speculate from a package name.
- **Workflow abuse:** Check step bypass, replay, resource exhaustion, and relevant
  limits against reachable operations. Identify business conditions an attacker
  can violate rather than inventing unprovided requirements or arbitrary limits.
- **Failures and detection:** Check fail-open paths, leaked diagnostics, and whether
  meaningful security failures reach the intended logging/alerting mechanism.
  Preserve useful evidence without exposing credentials or personal data.
- **Feature-specific controls:** Where applicable, check SSRF for controlled
  outbound destinations; CSRF for automatically attached browser credentials;
  file-upload storage/serving restrictions; unsafe deserialization or XML parsing;
  redirect handling; and relevant browser-origin protections. Consult the specific
  official cheat sheet when semantics or mitigations are uncertain.

## Severity within this domain

Use the shared impact scale with exploitability, attacker prerequisites, and
exposure. Reachable account takeover or broad sensitive-data access can be critical;
a demonstrated weakness with material but more limited impact can be important.
Optional hardening without a demonstrated material weakness is an improvement.
Record `security` as the domain and justify severity from the actual attack path.

## Verify and return

Check denied access and malicious-input tests alongside success paths. Trace
mitigations and counterevidence, including framework defaults, before reporting.
Use only authorized local environments for reproductions; return checks needing
writes/service mutations to the coordinator. Do not probe live production or
invoke external actions to demonstrate a vulnerability.

Use the shared format and identify this as the `security` review. Each concrete
weakness must state attacker prerequisites, reachable source-to-effect path,
impact, evidence, and a proportionate fix. Distinguish a demonstrated weakness,
unverified concern, and optional hardening. Report blockers and coverage gaps;
no findings is not a guarantee that the application is secure.
