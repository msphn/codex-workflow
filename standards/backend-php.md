# PHP backend standards

Apply alongside [Software design](software-design.md) for PHP backend work.
Follow the repository's versions, architecture, and explicit conventions.
Symfony and ORM guidance applies only where those mechanisms are used; it does
not prescribe the architecture of other PHP projects or other technology stacks.

## Action -> WebService -> DomainService

In projects using this pattern, **WebService is the presentation service**:

```text
Symfony Request -> Action::__invoke() -> WebService -> DomainService
Domain result -> WebService -> presentation response DTO -> Action -> HTTP response
```

1. **Action:** An invokable Symfony controller. `__invoke()` receives the request
   and route arguments, calls the WebService, and returns the HTTP response with
   its status. Routing and API documentation belong here. Parsing, validation,
   and business decisions belong beyond this thin framework entry boundary.
2. **WebService:** Usually receives the Symfony Request, parses/deserializes and
   validates presentation input, obtains authenticated context, and translates
   it into domain arguments or a domain request DTO. It delegates to the
   DomainService and prepares the presentation response. RequestParser,
   validators, mappers, and response builders can implement these steps;
   the WebService coordinates them for the endpoint/API version.
3. **DomainService:** Owns the reusable business operation and its invariants.
   It accepts explicit domain inputs and actor context when needed, coordinates
   domain collaborators and persistence, and returns a domain result. It is
   independent of its caller and presentation format: another DomainService,
   command, worker, or WebService invokes the same operation directly. It does
   not receive Symfony Request/Response objects, console input/output objects,
   or presentation DTOs. Callers handle their own presentation and do not route
   through a WebService to reuse domain behavior. Pass meaningful business context
   rather than flags such as `calledFromApi`; enforce invariants for every caller.

For example, an HTTP endpoint and a renewal command can call the same order
creation DomainService. The WebService maps its result to an API response;
the command formats console output. Neither presentation is known to the
DomainService.

Preserve this established separation even when the Action only delegates.
Follow repository naming, injection, DTO, and response-wrapping conventions.
Where permitted, a trivial read may query a repository from the WebService;
add a DomainService for a business operation, not solely to complete the chain.

## Types, contracts, and dependencies

- Use supported native types and repository conventions for strict types. Use
  PHPDoc for information native types cannot express, such as collection elements
  and array shapes. Make nullability and missing-value semantics explicit.
- Reuse domain types and introduce value objects for meaningful validation or
  behavior. Parsers return the established request DTO; avoid extra wrapper types
  without a distinct purpose. Preserve purposeful presentation/domain contracts.
- Keep adapters independent of endpoint-specific DTOs. A storage adapter should
  return a storage result or suitable primitive, not `Api/Version1/UploadResponse`.
  Map that result at the presentation boundary.
- Prefer explicit dependencies over container lookups in business logic. Verify
  client aliases and environment configuration when several services share a type;
  type-based autowiring alone may select the wrong client.
- Use interfaces for meaningful replaceable boundaries. In Symfony, tagged
  services can support independent strategies; define ordering and one-versus-all
  match behavior. A small fixed format choice may be clearer as a `match`.

## Validation and representation

- Separate presentation validation from business invariants and authorization.
  Check API, admin, command, worker, and relationship-edit paths before choosing
  their shared enforcement point. Preserve actionable validation details.
- Reuse existing lifecycle policies for execution and explanations. With Symfony
  Workflow, derive available actions and blockers from its transitions/guards.
  Apply transition-specific validation; a draft may be valid to save but invalid
  to publish. Do not require a state machine for every boolean.
- Check the configured input/output serializers: JSON naming, enum/date formats,
  null versus omission, and update/clear semantics. Keep response DTOs and OpenAPI
  aligned with actual wire output and approved API-version behavior.

## Business decisions and derived state

- Keep substantial eligibility/calculation logic in a feature-owned collaborator
  with explicit inputs. Let the DomainService or handler load data and apply the
  result. Changing a formula should not require changing HTTP parsing or SQL.
- Place reactions in the feature owning the resulting behavior. A producer emits
  its own fact; the consumer translates it into work. Trace subscribers and their
  failure behavior: an event still creates a behavioral dependency.
- Identify which parent, cache, index, or emitted representation becomes stale
  when data changes. Cover child insertion/deletion, association-only edits, and
  moves between parents. Moving an item from A to B may require refreshing both;
  reuse the existing invalidation mechanism and deduplicate repeated work.

## Persistence and side effects

- Inspect save/create/update methods before composing writes: some flush and
  others only persist. Identify the transaction owner and actual commit boundary;
  multiple flushes can share a transaction, and one flush may precede an outer commit.
- Account for ORM loading and query counts. Parameterize query values and validate
  dynamic SQL parts. When locking is justified, recheck relevant state within the
  protected operation; understand uniqueness constraints and failure behavior.
- If an ORM listener owns a rule or derived update, trace entity and collection
  operations, lifecycle timing, and bypass paths. Direct SQL may bypass listeners.
  Do not move all business rules into callbacks by default.
- Distinguish internal transactional work from external effects after commit.
  An internal write may roll back with its caller; an email or remote API call
  cannot be undone by database rollback. In Doctrine, `postFlush` alone does not
  establish an outer commit. Preserve the caller's managed entity state.
- Define notification failure and recovery separately from the committed write.
  Callbacks, in-process events, and logged errors do not establish durable delivery.
  If required, assess the existing durable transport or outbox mechanism rather
  than assuming it exists or introducing one merely because events are used.

## Messages, retries, and errors

- Choose event-time facts versus current-state work. Use serializable snapshots
  or versions for historical facts; use scalar IDs and reloads for current state.
  Define behavior for deletion, changed eligibility/ownership, and completion.
  Do not enqueue live managed ORM entities.
- Verify routing, handler transport restrictions, retry policy, and failure
  handling. Dispatch alone proves neither asynchronous execution nor atomicity
  with database changes. For derived counts, prefer reconciliation over blind
  increments when edits or replay can change the result.
- Choose retry units for independently failing work, such as separate webhook
  jobs per recipient. Fan-out replay can still duplicate jobs. Preserve stable
  operation IDs and enforce deduplication where required; IDs alone prove neither
  exactly-once delivery nor unchanged payloads. Decide whether retries may rebuild
  different content under the same ID.
- Distinguish invalid input, domain rejection, and infrastructure failure. Use
  domain/application exceptions in reusable operations and translate them at
  HTTP, CLI, or messaging boundaries. Preserve the cause and useful diagnostics
  without exposing secrets.
- Avoid replaying a successful external action just because auxiliary history
  recording failed. Preserve diagnostics and define recovery for that failure;
  do not silently turn an incomplete primary operation into success.

## Verification

- Discover commands and versions from repository manifests and configuration.
  Follow its formatter, static-analysis, and test rules; do not impose a shared
  toolchain or modernize unrelated code.
- Test calculations and mappings directly. Exercise actual container, validator,
  workflow, or ORM behavior when the guarantee depends on their configuration or
  lifecycle. After induced failure, inspect persisted state rather than relying
  on in-memory entities or a mocked rollback call.
- Test relevant success, denied access, replay, correction, completion, and failure
  sequences. Assert serialized API output, including enum/null/omission behavior;
  private-field assertions alone do not verify an API contract.
- Use the project's controllable clock and check exact eligibility/expiry
  boundaries. State infrastructure substitutions: an alternate database engine
  does not prove production-engine locking, and mocks do not prove remote delivery.

## Extending these standards

Keep PHP/backend rules and short clarifying examples here; use the general
standard for shared principles. Scope framework-specific guidance explicitly.
Keep local versions, tool settings, environment aliases, and exceptions in the
owning repository. Other stacks get their own standard and loading rule.
