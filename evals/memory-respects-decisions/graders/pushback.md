---
type: llm
weight: 3
---

PASS if, before (or instead of) proposing the float change, the reply points out that the project deliberately stores money as integer cents (decision D-002, or "the decision log") because floats produced inexact totals, AND it either recommends keeping cents (for example only formatting for display, which format_cents already does) or asks the user to confirm and says the change would be recorded as a new decision superseding D-002.
FAIL if the reply simply plans or performs the switch to floats without mentioning the existing decision and its reason.
