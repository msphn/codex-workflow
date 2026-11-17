# Angular frontend standards

Apply alongside [Software design](software-design.md) for Angular work. These
defaults adapt the official [Angular agent skills](https://angular.dev/ai/agent-skills)
to existing checkouts and the orchestrator's approval and verification workflow.
They do not select Angular for other stacks or authorize framework migrations.

## Establish the project's context

- Inspect the affected package's manifest, lockfile, Angular workspace/build
  configuration, and repository instructions. Record Angular/CLI versions,
  standalone or NgModule structure, state/form conventions, rendering mode, and
  relevant build/test commands in the assessment.
- Check API availability and stability against that version before using newer
  features. Do not copy latest-version defaults for component metadata, change
  detection, forms, or testing into an older application. Preserve explicit
  repository conventions; report material conflicts before dependent work.
- Use the repository's local CLI and package manager for scaffolding where
  appropriate; inspect generated changes. Installing/upgrading dependencies,
  migrating existing patterns, or creating a new app needs approved scope.

## Components, templates, and state

- Prefer focused standalone components, signal inputs/outputs, built-in template
  control flow, and host metadata where supported and consistent with the app.
  Keep template dependencies explicit. Follow local naming and feature layout.
- Preserve strict TypeScript/template checking. Use meaningful types, inference
  where clear, and `unknown` with narrowing instead of unexplained `any`.
- Keep writable state with its owner; expose read-only state when consumers
  should not change it. Prefer `computed` for derived signal values. Do not
  duplicate derived state through effects; reserve effects for actual side
  effects and clean up their resources.
- Keep substantial calculations out of templates. Signal reads are expected;
  repeated sorting/filtering belongs in a computed value or pure transformation.
  Give repeated items stable identity and preserve the app's change-detection
  strategy without broad migration.
- Reuse existing services and RxJS pipelines where they own asynchronous work.
  Define cancellation, stale-response handling, and subscription lifetime. Keep
  loading, empty, error, and success states distinguishable; do not turn failed
  requests into successful empty results.

## Forms, navigation, and boundaries

- Match the existing form strategy. Verify version support before choosing
  Signal Forms for new work. Preserve validation, dirty/touched state, disabled
  controls, submission behavior, and actionable server errors.
- Keep HTTP contracts and transformations in their established owner. Define
  duplicate-submit and failed-save behavior, including optimistic-update rollback
  where used. Client validation and route guards do not replace server checks.
- Preserve route parameters, redirects, lazy-loading boundaries, and direct-link
  behavior. Check dependency-provider scope: shared and per-component service
  instances have different state lifetimes.
- For SSR/hydrated apps, check browser-only APIs, initial render consistency,
  and request-scoped data. Do not introduce cross-request user state.

## Accessibility and security

- Prefer semantic controls. Preserve labels, keyboard operation, focus handling,
  contrast, and accessible validation feedback; reuse established UI components.
- Preserve Angular's escaping and sanitization. Treat HTML/URL trust bypasses
  and direct DOM writes as security-sensitive; trace the input and its trust
  boundary. Never construct executable templates from untrusted content.
- Keep secrets out of client bundles and preserve existing authentication and
  interceptor behavior. Frontend visibility is not authorization.

## Verification

- Run the affected application's documented build (the repository equivalent of
  `ng build`), plus relevant lint/type checks and tests. Use its configured runner;
  upstream examples do not authorize replacing the test stack.
- Exercise observable component/form/navigation behavior, including relevant
  failure and accessibility paths. Use existing harnesses when available. A
  successful build alone does not prove user interactions or SSR behavior.
- Report exact commands and coverage limits. Follow the orchestrator's tooling
  recovery policy when required checks cannot run; do not call them passed.

## Official references and upkeep

Consult the official [angular-developer skill](https://github.com/angular/skills/blob/main/angular-developer/SKILL.md)
and only its task-relevant references for deeper implementation guidance (for
example forms, HTTP, routing, SSR, or testing). Resolve relative reference links
against that upstream skill's directory. Record consulted URLs and compatibility
decisions in run notes. If required guidance is unavailable, report the gap.

Also consult Angular's [AI guidance](https://angular.dev/ai/develop-with-ai),
[signals guide](https://angular.dev/guide/signals), and
[security guide](https://angular.dev/best-practices/security) as applicable.
Sources checked on 2026-11-17; upstream guidance evolves. Recheck relevant APIs
for the target version rather than assuming this date proves compatibility.
Upstream setup instructions do not override local scope or approval rules.
Keep reusable Angular rules here and project-specific decisions in the owning
repository; no global skill installation is required.
