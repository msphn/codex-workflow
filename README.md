# Local ticket orchestrator

A local Codex workflow and engineering knowledge base for coordinating work
across existing repositories, from assessment to a locally committed owner handoff.

## Introduction

This is not a "one shot, slop it" harness. It's a helper to make drafting of a local change as good as possible. Currently the primary tech stack is based on symfony and php, but other technologies might be added as I desire.

So who is that for? Software engineers who want to have some structure, observability for their AI work in a best-effort environment. After you approve the plan, the coordinator can make local checkpoint commits on the ticket branch. It will not push or deploy. The entire setup is based on the expectation of the user being in charge and the actual engineer. This is not a vibe-coding setup.

Ideally you have a local folder with your applications, check this repository out next to it and configure the repositories.example.toml.

Run it -> answer questions -> review -> iterate. Eventually it might successfully one-shot you a solution.

## How it works

The main agent coordinates assessment, planning, owner approval, implementation, independent
review, acceptance testing, and handoff. Specialists handle the assigned stages.
[Project policy](AGENTS.md) defines boundaries and approval requirements;
[local-ticket](.agents/skills/local-ticket/SKILL.md) owns the stage procedure.

The [checkout preflight](.agents/skills/local-ticket/references/checkout-preflight.md)
prepares existing checkouts and ticket branches. Resume stops for an owner
decision when the remote base advances beyond ticket
HEAD, even with uncommitted work.

### Conditional specialists

[Stage guards](standards/stage-guards.md) define when an assessor, planner,
architecture reviewer, or security reviewer is required. Clear local work using
an existing pattern can have coordinator-led assessment and planning. Independent
code review checks architecture/security exemptions against the actual diff;
unknown applicability cannot justify omission. Plan approval, strict checkout
checks, delegated implementation, separate acceptance, and model settings remain
unchanged. Record each decision and evidence before approval and reassess after
changes. This reduces assignments, not the required stage outputs.

## Getting started

1. Open this directory as a local Codex project, trust it if prompted, and start
   a new local session. Configuration and skills live in `.codex` and `.agents`;
   there is no bootstrap directory or installer.
2. Copy [repositories.example.toml](repositories.example.toml) to
   `repositories.local.toml` if you have not configured it yet. Replace the
   example entries with your repository names and existing local checkout paths.
   The local registry is ignored by Git. Do not put credentials in it.
3. Verify the session's effective repository access and available agents before
   starting a ticket. Use an authorized Jira integration or paste the ticket.
   This project does not install integrations or credentials.

Project settings require trust and do not retroactively change an existing
session's permissions. Managed policy and session overrides still apply.

### Verify repository access

`writable_roots = ["../.."]` in `.codex/config.toml` resolves from the `.codex`
directory to this project's parent directory. The configured scope covers sibling
projects, including future ones. Registry paths instead resolve relative to
`repositories.local.toml`; registering a checkout does not grant permissions.
No per-ticket path arguments are needed once the registry is configured.

Start a new local session with:

```text
Verify this project's effective sandbox includes its parent directory, and that
the local-ticket and review skills and specialist roles are loaded. Do not start a ticket
or change application files. Report any session or managed-policy overrides.
```

Inspect effective permissions rather than relying on configuration text. For a
write probe, create a disposable sibling directory yourself and ask Codex to
create/delete a file only there. Do not use application files as probes.

## Daily use

Provide a ticket:

```text
Work on DEV-1234 using the local-ticket workflow.
```

Or invoke the skill explicitly:

```text
$local-ticket Work on DEV-1234.
```

You can also paste the ticket details. Assessment records applicable repository
guidance, selected engineering standards, checkout state, existing edits,
clarified requirements, acceptance criteria, questions, and complexity. Answer
material requirement questions; a ready assessment proceeds directly to planning.
The coordinator or required planner investigates the actual checkouts and proposes implementation,
contracts, failure handling, and validation. Approve that concrete plan to start
application-code changes. Overlaps with existing work require your decision.

To continue a ticket:

```text
Continue DEV-1234: <feedback>
```

The coordinator compares saved notes with actual checkouts and service versions,
marks affected evidence stale, and reruns relevant review/tests. Approval carries
forward for unchanged scope; material scope or contract changes require a new
decision. Every ticket has a mandatory `status.md` and supporting run notes under
`runs/<ticket-id>/`, ignored by Git. Notes identify the orchestrator revision and
any uncommitted instruction changes as well as the application snapshots.

### Local commits and checkpoints

The coordinator commits coherent implementation steps after their required
checks pass, then obtains independent code review, triggered architecture/security
reviews, and separate acceptance
testing. Fixes use follow-up commits and affected re-review/retest. A commit is
progress evidence, not acceptance. Owner-staged work blocks committing until
resolved; owner changes are never included without explicit authorization.
See [the commit procedure](.agents/skills/local-ticket/references/local-commits.md).

Each repository keeps its immutable starting base, checkpoint list, exact review
and test snapshots, and remaining local changes. The handoff includes the whole
ticket diff, not just the latest commit. No automatic amend, squash, rebase, push,
PR creation, or deployment. You retain scope decisions and final acceptance.

Specialists use [one result contract](standards/specialist-handoff.md). After two
unsuccessful fixes of the same review finding, the coordinator requires a fresh
diagnosis or escalation before another attempt. Blocking findings remain blocking.

## Models and usage

The starting defaults are:

| Role | Model | Reasoning effort |
| --- | --- | --- |
| Coordinator | `gpt-6-astra` | `medium` |
| Assessor | `gpt-6.1-sol` | `medium` |
| Planner | `gpt-6-astra` | `medium` |
| Implementer | `gpt-6.1-sol` | `medium` |
| Code, architecture, and security reviewers | `gpt-6.1-sol` | `high` |
| Black-box tester | `gpt-6.1-sol` | `medium` |

Defaults live in `.codex/config.toml` and specialist role files. The coordinator
owns questions, presentation, and the approval record. A required planner owns
technical planning; otherwise the coordinator performs it.
Verify effective settings when starting work: session or managed-policy overrides
may differ from the files, and editing files does not prove a running agent changed.

[Project policy](AGENTS.md#model-selection-and-context) defines focused fresh
handoffs and escalation to Astra for difficult or unresolved assignments. Role
settings take precedence over spawn overrides, so escalation may use a generic
agent carrying the original role's complete instructions. Luna is reserved for
bounded support tasks, not a required review or acceptance stage.

Run notes track models, usage, and rework. Compare total usage and attempts across
representative tickets before lowering defaults; mark unavailable telemetry unknown.

## Engineering knowledge base

The shared standards are reusable guidance, with generic examples and no
dependency on a particular application repository:

- [Software design](standards/software-design.md): ownership, cohesion,
  dependency direction, invariants, consistency, and failure behavior.
- [PHP backend](standards/backend-php.md): presentation/domain boundaries,
  validation, serialization, persistence, messaging, and testing. It explains
  `Action -> WebService -> DomainService`, with WebService as the presentation
  service and DomainService independent of its caller and presentation format.

The coordinator selects applicable standards during assessment and supplies them
to assessors, planners, implementers, and reviewers. Shared standards are defaults;
explicit target-repository conventions take precedence. Record concrete project
exceptions in that repository and task-specific evidence in run notes.

Keep examples beside their rules. New technology standards need an applicability
rule in `AGENTS.md`; other stacks do not inherit the PHP architecture.

## Where to customize

| File | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Project boundaries, approval/branch policy, communication, and standards routing |
| [standards/software-design.md](standards/software-design.md) | Shared design and review principles |
| [standards/backend-php.md](standards/backend-php.md) | PHP backend guidance |
| [standards/review-method.md](standards/review-method.md) | Common reviewer procedure, evidence, impact severity, and findings format |
| [.codex/config.toml](.codex/config.toml) | Coordinator model/effort, ticket routing, and parent sandbox settings |
| [.codex/agents/assessor.toml](.codex/agents/assessor.toml) | Requirements assessment, repository identification, and blocking questions |
| [.codex/agents/planner.toml](.codex/agents/planner.toml) | Repository implementation and validation planning |
| [.codex/agents/implementer.toml](.codex/agents/implementer.toml) | Implementation after approval |
| [.codex/agents/code_reviewer.toml](.codex/agents/code_reviewer.toml) | Independent correctness and code-quality review |
| [.codex/agents/architecture_reviewer.toml](.codex/agents/architecture_reviewer.toml) | Independent responsibility, coupling, and cohesion review |
| [.codex/agents/security_reviewer.toml](.codex/agents/security_reviewer.toml) | Independent security review |
| [.codex/agents/black_box_tester.toml](.codex/agents/black_box_tester.toml) | Observable local acceptance testing |
| [.agents/skills/local-ticket/SKILL.md](.agents/skills/local-ticket/SKILL.md) | Ticket stages, handoffs, and resumption |
| [.agents/skills/local-ticket/references/checkout-preflight.md](.agents/skills/local-ticket/references/checkout-preflight.md) | Git preparation, checks, evidence, and stop conditions |
| [.agents/skills/review/SKILL.md](.agents/skills/review/SKILL.md) | Review coordination, delegation, and reconciliation |
| [.agents/skills/code-review/SKILL.md](.agents/skills/code-review/SKILL.md) | Correctness, cognitive complexity, Clean Code, SOLID, KISS, YAGNI, DRY |
| [.agents/skills/architecture-review/SKILL.md](.agents/skills/architecture-review/SKILL.md) | Coupling, cohesion, existing patterns, and clean architecture |
| [.agents/skills/security-review/SKILL.md](.agents/skills/security-review/SKILL.md) | Applicable OWASP checks and attack-path evidence |
| `repositories.local.toml` | Ignored repository-name-to-local-path registry |
| [repositories.example.toml](repositories.example.toml) | Registry template for another machine |
| `runs/<ticket-id>/` | Ignored status, assessment, plan, review, and test notes |

Add skills at `.agents/skills/<name>/SKILL.md` with YAML `name` and `description`.
Add roles as `.codex/agents/<name>.toml` with `name`, `description`, and
`developer_instructions`. This project sets both `model` and
`model_reasoning_effort` in every specialist role file to avoid implicit inheritance.

Use `$review` for a coordinated review; standalone general reviews cover all three
domains. Ticket reviews use the explicit specialist guards.
Initial specialists receive fresh context when supported,
with explicit assignments and disclosed fallbacks. Review domain and impact
severity are recorded separately.

Use `$code-review`, `$architecture-review`, or `$security-review` for an explicitly
focused review. Each can run independently and reports only its own coverage.
Extend domain-specific checks in the corresponding skill; keep common evidence
and reporting rules in `standards/review-method.md`.

Roles cover assessment, planning, implementation, domain review, and acceptance.
Verify their availability in a new session after changing role files. The workflow
skills define fallback behavior when named roles or delegation are unavailable.
Keep shared reviewer procedure in `standards/review-method.md`; role files select
the domain skill and retain essential boundaries. Avoid copying stage procedures
into role files or this overview.

## Boundaries and validation

Work stays in existing checkouts: no clones, shadow copies, or worktrees. Only
the coordinator may stage/commit approved application work on the ticket branch.
Orchestrator setup changes remain uncommitted unless separately authorized.
Do not push, open PRs, or deploy. Jira reads are allowed for
intake. Jira changes, production access, and external mutations require explicit
direction. Shell network access and connector access are separate permissions.

This workflow uses native agents, skills, and Markdown run notes. It has no SDK
daemon, scheduler, or dashboard. Instructions and notes do not enforce a durable
pipeline or approval barrier. Roles inherit session permissions; no-edit
instructions do not create a separate sandbox. A separate tester cannot
guarantee source blindness. Missing infrastructure or data means blocked checks,
not successful validation.

Record validation evidence and limitations in the relevant local run notes.
Verify effective permissions in the session where work will run; configuration
and past results are not proof.

### Workflow checks

Run the deterministic evidence-helper tests with:

```sh
python3 -m unittest discover -s tests/workflow -p 'test_*.py' -v
```

These use disposable local Git fixtures, not application checkouts or providers.
[Workflow testing](tests/workflow/README.md) documents the read-only snapshot
helper and separate live agent scenarios. Deterministic tests validate evidence
mechanics; they do not prove agent compliance. Live evaluations require an
explicit request and are never started by the helper or test suite.

## Official references

- [Project configuration and trust](https://learn.chatgpt.com/docs/config-file/config-basic)
- [Relative configuration paths](https://learn.chatgpt.com/docs/config-file/config-advanced)
- [Custom agents and inherited permissions](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Local skill discovery](https://learn.chatgpt.com/docs/build-skills)
