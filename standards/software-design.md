# Software design standards

Technology-neutral defaults for assessment, planning, implementation, and review. Apply
proportionately to the task and existing architecture. Follow explicit repository
conventions, report material conflicts, and stay within the approved scope.
Language, framework, and architectural patterns belong in scoped standards.

## Ownership and failure map

During planning, answer these questions for the affected behavior using actual
callers and state changes. A small change may need only a few sentences.

1. Who owns the rule and the state it protects?
2. Which interactions, entry points, or background operations can change it?
3. Which consumers, contracts, or derived representations depend on the result?
4. What must remain consistent if part of the operation fails?

Record unresolved decisions and use this map in implementation and review.
Update it when new callers or failure paths emerge; it does not require a new
architectural layer.

## Cohesion and readability

- Keep related decisions and state with their owner. Split responsibilities when
  they have different reasons to change, not to meet file or method size limits.
- Separate substantial calculations from acquiring inputs and applying effects
  when that makes the decision independently understandable and testable.
- Make the path from input to result easy to trace. Use names that explain intent
  and make side effects visible. Document non-obvious reasons, not obvious syntax.
- Preserve useful existing boundaries. Justify additions by a concrete change
  they simplify or a failure they contain; avoid layers that merely forward calls.

## Dependencies and contracts

- Keep reusable behavior independent of its caller's presentation or transport.
  Express meaningful differences as explicit inputs rather than hidden context
  or caller-specific flags.
- Give shared contracts a clear owner. Keep consumers independent of internal
  representations that they do not need. Check actual callers and dependencies;
  folder structure alone does not establish separation.
- Make dependencies explicit using the project's conventions. Avoid hidden
  service lookups and mutable global state where explicit inputs suffice.
- Identify affected producers and consumers before changing a public contract.
  Make compatibility and representation changes intentional and verifiable.

## Abstractions

- Introduce an abstraction for an actual shared responsibility, substitution, or
  extension need. Do not create one for every component or hypothetical future.
- Share rules with common ownership. Similar-looking code with different reasons
  to change may be clearer kept separate.
- Define selection, ordering, and unsupported cases for extensible behavior.
  A small closed choice may be clearer as an explicit branch.
- Introduce separate models when their contracts or lifecycles differ, rather
  than to fill nominal layers. Prefer concrete decision criteria over pattern names.

## State and failures

- Enforce each invariant where all relevant changes can be covered. Identify
  bypass paths; validation at one entry point does not protect every other caller.
- Give derived state an authoritative source and an update/invalidation owner.
  Account for changes to relationships as well as values.
- When effects can partially succeed, specify what has happened, what remains,
  and whether retry is safe. Distinguish the primary result from auxiliary failures.
- Preserve diagnostic context. Do not hide unexpected failures behind success,
  empty results, or unexplained defaults. Explain what validation and limits protect.

## Verification and review

- Keep permanent regression tests focused on expected application behavior,
  domain rules, and supported contracts. A changed implementation detail alone
  does not justify a permanent test.
- Distinguish regression coverage from one-time validation. For one-time data
  migrations, conversions, or repair scripts, normally use temporary checks and
  record their results in the run notes. Keep such checks in the permanent suite
  only when they protect an explicit ongoing requirement, such as supported
  upgrade compatibility.
- Test decisions and observable outcomes through the mechanism providing the
  guarantee. Include relevant denied paths, corrections, repeated operations,
  and partial failures. Mocked calls alone do not establish real integration.
- Make time-dependent behavior controllable and test exact boundaries. Preserve
  the feature's intended semantics rather than imposing one global interval rule.
- State substitutions, coverage limits, and unverified behavior. Tie findings to
  concrete correctness, reading, or maintenance consequences; separate defects
  from preferences and recommend proportionate fixes.

## Extending these standards

Keep this file independent of a language, framework, or service hierarchy. Add
technology-specific rules and short examples to the appropriate scoped standard,
with explicit applicability. Keep repository-specific conventions in that
repository. Each rule should have one primary home; reference rather than repeat it.
