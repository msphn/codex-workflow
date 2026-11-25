# Refactor completeness

Apply when the change moves, replaces, or consolidates responsibilities. Do not
invent a refactor where none occurred or expand into unrelated restructuring.

Identify equivalent operations before and after the change. Map their preparation,
decisions, derived values, effects, and outputs, including supporting helpers. Mark
each as moved, retained, duplicated, intentionally changed, or removed, with source
references. Explain retained work from the value it produces and its consumers,
not merely its enclosing layer's name.

Trace an ordinary direct invocation of the new reusable boundary using its declared
inputs. What work must callers still perform to obtain the original operation's
result? Distinguish interpreting a transport/form representation from determining
persisted or externally consumed values. Check whether required preparation is
explicit in the boundary's contract or implicitly depends on its original caller.

Assess missing or duplicated responsibility using concrete caller obligations and
maintenance tasks. The absence of a second caller limits runtime-bug claims but does
not establish that an extraction is complete. Preserve justified presentation work
and independently changing representations; do not move all code or demand layers.

Include a compact before/after map and direct-call trace in the review's ownership
analysis. Report the smallest useful improvement or contract clarification with
counterevidence. A deliberately narrower operation can be appropriate; explain its
contract rather than requiring a finding or a broader implementation.
