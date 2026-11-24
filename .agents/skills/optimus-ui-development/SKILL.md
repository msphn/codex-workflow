---
name: optimus-ui-development
description: Develop, debug, and review Angular UIs using @openng/optimus-ui, using upstream Agent Skill docs, the component manifest, and MCP lookups. Apply to Optimus components, forms, templates, and theming; confirm the package because p-prefixed selectors alone also occur in PrimeNG.
---

# Develop with Optimus UI

Use alongside [Angular standards](../../../standards/frontend-angular.md).
This skill adapts upstream documentation to existing applications; it does not
authorize dependency upgrades, a PrimeNG migration, or replacement of app-wide
providers, themes, or form conventions.

## Establish compatibility

Inspect the affected package manifest, lockfile, installed package when available,
and existing imports. Record the resolved Optimus UI and Angular versions, theme
packages, and local wrapper components. A `p-*` selector alone does not identify
Optimus UI. Use this skill when the affected UI uses `@openng/optimus-ui`, or when
Optimus adoption/migration is explicitly in scope.

Match documentation to the resolved version, not just a dependency range. Check
the [compatibility table](https://optimus.openng.org/installation#compatibility)
and installed peer dependencies when compatibility matters. Do not infer that
an application supports a new API because it appears in the latest docs.

## Retrieve only the relevant documentation

Choose an available source below; do not load all sources or the full library
manual for each task. Record its version, URL or local path, and relevant
component/guide sections in the run notes. Check actual content: an HTTP success
can contain an HTML error page, and a current download can contain older docs.

### Official Agent Skill files

If the upstream `optimus-ui` skill is installed, read its `SKILL.md` version and
index, then only the relevant `references/components/<slug>.md` and
`references/guides/<slug>.md`. Resolve those paths against the upstream skill's
directory, not this adapter. Use `rg -n '^##'` to locate sections before reading
large component files; use the index to map selectors to documentation slugs.

For online access use the [LLM index](https://optimus.openng.org/llms/llms.txt),
then `https://optimus.openng.org/llms/components/<slug>.md` or
`https://optimus.openng.org/llms/pages/<slug>.md`. Avoid `llms-full.txt` unless a
broad investigation actually needs the whole manual.

Upstream publishes an [installable archive](https://optimus.openng.org/llms/optimus-ui-skill.zip)
and [discovery index with a digest](https://optimus.openng.org/.well-known/agent-skills/index.json).
When installation/update is in scope, its documented commands are
`npx skills add https://optimus.openng.org` and `npx skills update optimus-ui`.
Inspect destination and version; do not overwrite this adapter or install globally
as a side effect of UI work. Reading the targeted web docs needs no installation.

### MCP, when available

Discover the session's Optimus tools before claiming they are configured. The
[official MCP package](https://github.com/openng-org/optimus-ui/blob/2.1.0/packages/optimus-ui-mcp/README.md)
is `@openng/optimus-ui-mcp`; its bundled manifest describes its own release.
For an explicitly requested setup, pin it to the application's release (for
example `npx -y @openng/optimus-ui-mcp@2.1.0`), verify package availability, and use
the host's supported MCP configuration. Do not silently register a server.

- `search`: find the relevant component, API, type, example, or guide.
- `get_component`: retrieve imports, selectors, inputs, outputs, templates,
  methods, and examples for the selected component.
- `get_example` and `get_type`: resolve a specific example or event/model type.
- `get_guide`: retrieve the relevant configuration, styling, or other guide.
- `list_components`: use when component discovery is the task.

Use returned lookup arguments and the exposed tool schema rather than guessing
identifiers. These tools are read-only. If unavailable, use the file/web sources;
MCP is not a prerequisite for ordinary implementation.

### Machine-readable API

The [manifest](https://optimus.openng.org/llms/manifest.json) provides `entryPoints`
for imports and declarations, `components` for examples and tokens, and `guides`.
Validate JSON, schema/version metadata, and compatibility before using it. Filter
to the relevant entry point/component instead of dumping the manifest into context.
Use it for exact selectors, allowed input values, defaults, output payloads,
template contexts, forms support, and pass-through keys.

If docs are stale, unavailable, or conflict, verify the specific API against the
installed package's typings/metadata or the matching
[release-tagged source](https://github.com/openng-org/optimus-ui/tree/2.1.0)
(replace the tag with the target version). Report unresolved gaps rather than
inventing bindings or treating PrimeNG memory as authoritative.

## Apply and verify

- Reuse the application's wrappers and established patterns. Verify exact imports,
  bindings, event payloads, and template contexts before implementing or reviewing
  them; adapt examples to the app's form and module/standalone conventions.
- For styling, consult the relevant theme, token, or pass-through documentation
  and existing theme configuration before targeting internal DOM/CSS. Preserve
  overlays, focus, keyboard navigation, labels, and disabled/validation behavior.
- Run the application's documented build and affected checks, and exercise the
  changed interactions under the Angular standards. Documentation lookup is not
  runtime validation.
- Supply this skill's absolute path plus the version and relevant documentation
  references to assigned assessors, planners, implementers, and reviewers. Keep
  concrete app decisions in the owning repository or ticket notes.

## Source baseline and upkeep

Based on the [2.1.0 release](https://github.com/openng-org/optimus-ui/releases/tag/2.1.0)
and its [documentation generator](https://github.com/openng-org/optimus-ui/blob/2.1.0/apps/docs/scripts/build-llm-skill.mjs),
checked 2026-11-24. At that check the published archive identified itself as
2.0.2 and the public manifest URL returned HTML titled “Page Not Found”. These
are observations, not permanent restrictions: recheck publication and versions
when using them. This adapter bundles no upstream docs and configures no MCP
server; keep upstream API details in the versioned sources rather than copying
an entire generated manual here.
