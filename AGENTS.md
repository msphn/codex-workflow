# Repository Guidelines

## Communication preferences

- Use generic masculinum.
- Use a laid-back but focused tone.
- Be concise and direct. Lead with the answer or outcome.
- Explain technical decisions in plain language.
- Distinguish confirmed facts from assumptions.
- Challenge my assumptions when you have concrete evidence.
- Avoid flattery, canned phrases, and unnecessary summaries.

## Purpose & Boundaries

This project coordinates pre-qualified Jira tickets across existing application repositories for the owner's review. Leave all changes uncommitted. Never stage, commit, push, create pull requests, or deploy. Read Jira through the available integration, or use a pasted ticket; change Jira only when explicitly requested. Production access and external mutations require explicit direction. Work in existing application checkouts; do not clone, create shadow copies, or create worktrees.

## Project Structure & Configuration

Keep application source code, tests, and assets in their existing checkouts. This directory contains the orchestration workflow, specialist instructions, repository registry, and reusable engineering standards; it has no application build or test suite.

As the setup develops, keep a repository-name-to-local-path registry, a workflow skill, and specialist role instructions here. Configure selected repository write access once through supported project-scoped Codex settings; do not require paths in every ticket command. Registry entries do not grant filesystem permissions. Verify effective access before implementation.

## Workflow and Approval Policy

For ticket work, follow `.agents/skills/local-ticket/SKILL.md`, which owns the assessment, proposal, implementation, review, acceptance testing, and handoff procedure. The main session coordinates; specialists perform only their assigned stage.

Wait for explicit owner approval of the concrete plan before editing application files. Carry approval forward for unchanged scope. Ask about material ambiguities, overlapping owner edits, and material scope or contract changes before dependent work. Preserve unrelated staged, unstaged, and untracked changes.

For white-box review, follow `.agents/skills/review/SKILL.md`, which owns the three-domain delegation, reconciliation, and re-review procedure. Black-box acceptance uses a separate specialist and the ticket's approved criteria. Missing reviews or unavailable acceptance checks remain blocked and must be reported.

## Checkout and Branch Policy

Our standard is `master`/`develop`. New tickets use freshly verified `develop` unless the owner specifies another base. Name ticket branches `feature/<Jira-ticket-key>[-<short-description>]`, preserving the key and using a lowercase, hyphen-separated description. Other names require explicit owner direction.

For ticket work, the coordinator follows `.agents/skills/local-ticket/references/checkout-preflight.md` before application source inspection, before implementation, on resume, and when adding a repository. That reference owns the Git procedure, evidence, and specialist verification requirements. Specialists never switch or update shared checkouts. Standalone reviews use their explicitly supplied scope and baseline without changing the checkout.

Strict resume checks are intentional: if the remote base advances beyond ticket HEAD, stop for the owner's decision even when ticket changes are uncommitted or appear unrelated. Do not decide independently that the new base can be ignored. Never discard or automatically stash existing work. Orchestrator setup changes do not require switching this repository to `develop`.

## Engineering Standards

For tasks involving application code, read `standards/software-design.md` during assessment. For tasks involving PHP backend code, also read `standards/backend-php.md`. Resolve these paths from the orchestrator root. Determine applicability from affected files, manifests, and repository instructions, not only from ticket wording; reassess when affected technologies change. Load each technology-specific standard only for its stated scope. When adding a standard, define its applicability and loading rule here.

Include the absolute paths of applicable standards in assignments to assessors, implementers, and reviewers. Require each specialist to read them before starting its assigned stage. Record the selected standards and material conflicts in the assessment. If a required file cannot be read, report the gap rather than claiming it was applied.

Treat shared standards as defaults. Follow explicit target-repository conventions where they differ, and report material conflicts during assessment. Standards do not authorize refactoring outside the approved scope. Black-box expected behavior continues to come from the ticket and approved acceptance criteria.

For affected application behavior, record the ownership and failure map described in `standards/software-design.md` during assessment and use it in implementation handoffs and review. Keep shared standards self-contained and portable: use generic examples, not dependencies on named repositories, private code, or machine-specific source paths. Store concrete project conventions in the target repository and task-specific evidence in run notes.

## Development & Testing Conventions

Discover build, run, lint, and test commands from each target repository's documentation and manifests. Follow its indentation, naming, formatting, test framework, and coverage requirements. Do not invent shared commands or coverage thresholds. Distinguish focused checks from full suites and report exactly what ran.

When required local tooling or services are unavailable, diagnose the failure and try the documented, non-destructive local startup or recovery steps within session permissions (for example, start the installed Docker runtime and the application's local services). The coordinator owns recovery of shared services; specialists report failures to it. If recovery fails or requires owner action, ask the owner for specific help and pause dependent work. Do not bypass required tooling, weaken checks, or substitute mocks or source inspection for required runtime tests. Keep affected checks blocked until recovery is verified and those checks run successfully. Starting local services does not authorize destructive resets, unrelated configuration changes, or production access.

## Agent Roles & Visibility

Define implementation, review, and testing responsibilities in separate role instructions. Roles inherit session permissions; role instructions alone cannot guarantee read-only access or isolation.

### Model selection and context

Use the coordinator defaults in `.codex/config.toml` and specialist defaults in
`.codex/agents/<role>.toml`. Set both model and reasoning effort explicitly when
configuring a role. Before delegation, check the effective tool/role settings;
record unavailable models or overrides rather than claiming disk settings applied.

Start initial specialist assignments with fresh context (`fork_turns="none"`
where supported). Supply a focused, self-contained handoff with the required
instructions, paths, checkout evidence, scope, contracts, and stage inputs. Required
inputs may use absolute file paths and named sections instead of copied text;
require the recipient to read them and report missing or stale evidence. Keep the
assignment's task, boundaries, and expected result explicit. Do not send unrelated
run history or implementation reasoning to independent reviewers/testers.
Reuse a specialist for related follow-ups when its model and context remain
appropriate; send changed inputs and affected scope, retaining required state
verification and review/test independence.

Escalate the affected assignment to `gpt-6-astra` with `medium` reasoning for
difficult concurrency, authorization, billing, or data-loss reasoning, or unresolved
review disagreements. Use `high` when the remaining problem needs deeper reasoning.
The coordinator may make this escalation within the approved scope and must record
the reason. A role file's model/effort takes precedence over spawn overrides. If
it prevents escalation, use a fresh generic agent with explicit model/effort and
the original role's full instructions, required skills, and assignment boundaries;
disclose this substitution. Stop an existing writer before assigning its files to
a replacement. If the requested model cannot be selected, report the limitation.

Keep Luna out of the six specialist defaults. It may handle bounded support work
such as file discovery, documentation lookup, or execution of a fully specified
check; it does not replace a required review or independent acceptance stage.

Record requested and, when exposed, effective model/effort, context mode,
escalations, usage, and rework in run notes. Mark unavailable telemetry unknown;
do not estimate savings from model names. Compare total ticket usage and repeated
attempts across representative tickets before reducing these defaults further.

Use Codex's agent activity view. Every ticket must have `runs/<ticket-id>/status.md` and the supporting records defined by the local-ticket run template, including blocked tickets. Keep status current at stage changes and handoff. These records are mandatory but do not enforce authorization, isolation, or a durable state machine.
