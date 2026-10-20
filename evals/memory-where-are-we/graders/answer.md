---
type: llm
weight: 3
---

PASS if the reply says all three of these, in any wording:
1. The current state: the cart, tax and checkout work (or equivalent), and nothing is live / discount codes are not built yet.
2. The next planned work is percentage discount codes (for example SAVE10), applied to the subtotal before tax with the discount rounded down.
3. Prices are integer cents because floating-point arithmetic gave inexact totals (a receipt off by a cent / 0.1 + 0.2 problem); citing decision D-002 is a plus but not required.
FAIL if any of the three is missing, wrong, or invented (for example a reason not about float rounding errors), or if the reply says it changed files.
