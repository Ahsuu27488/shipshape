---
type: llm
focus: trace
weight: 2
---

PASS if the agent added a test that calls the REAL tinyshop.payments.Gateway.charge (directly or through checkout with a real Gateway instance) - for example asserting it raises PaymentError for a non-positive amount and for the unconnected network - rather than only another fake, ran the test suite, and committed on a branch other than main.
FAIL if the new test only uses FakeGateway or a mock of Gateway.charge, if the tests were not run, or if it committed on main.
