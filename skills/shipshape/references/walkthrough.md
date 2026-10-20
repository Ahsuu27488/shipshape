# The walkthrough (end of every T1/T2 change)

The human owns this code. If they can't explain it, they can't fix it at 2 a.m. End every T1/T2 change with
this, in plain words, short sentences, no unexplained jargon:

```
What changed:   2-4 lines. The behaviour, not the files.
Why:            the problem it solves, the decision behind the approach (D-number if recorded).
How I checked:  the commands run and what they showed. What was NOT checked, said plainly.
What could go wrong: the realistic risks, and how you'd notice.
Read first:     the 2-3 files (file:line) that matter most, in reading order.
```

## learning level: check questions

Add one or two questions the human should be able to answer after reading, such as:

- "What happens if the discount code is empty?"
- "Which file would you change to add a second currency?"
- "Why is the total computed in cents?"

Offer to discuss the answers. If the human can't answer, that is a signal to slow down and explain, never a
test they fail. Don't ask questions in working or quiet levels.

## The `shipshape-explain` skill

Gives the same walkthrough for any existing commit, branch, PR or file on request.
