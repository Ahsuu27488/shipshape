---
type: llm
weight: 3
---

PASS if the plan does all of these:
1. Follows the recorded rule for discount codes: a percentage applied to the subtotal BEFORE tax, with the discount rounded DOWN to the cent (decision D-003); tax computed on the discounted subtotal.
2. Names the concrete files involved (tinyshop/cart.py and/or a new module, and a test file).
3. Names how it will be verified (specific tests, for example a rounding-down case and a tax-after-discount case, run with python -m unittest).
4. Says the work will happen on a new branch rather than on main.
FAIL if it contradicts D-003 (discount after tax, rounding up or to nearest), invents a rule not in the docs while presenting it as the project's, or omits the verification.
