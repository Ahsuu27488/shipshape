---
name: shipshape-explain
description: Explains a change or a piece of code to the human in plain words - what it does, why, how it connects to the rest of the project, how it was verified and what could go wrong - using the project's memory docs and the real code. Use when the user asks "what did you change", "walk me through this", "explain this commit / PR / branch / file", or says they don't understand part of their own code.
license: MIT
metadata:
  author: Muhammad Ahsan
  version: "0.1.0"
---

# shipshape-explain: keep the human understanding their own code

1. **Find the subject:** the last change (`git log -1 -p`, or the current branch against the default branch),
   a named commit / PR (`gh pr diff <n>`) / branch, or a file or function.
2. **Read the context:** `docs/ARCHITECTURE.md` (where it sits), `docs/DECISIONS.md` (decisions that explain it),
   and the code around it, including its callers. Never explain from the diff alone.
3. **Explain** with the walkthrough format in `../shipshape/references/walkthrough.md`:
   what it does (behaviour, not files), why (decisions by number), how it connects (who calls it, what it calls,
   what data it touches), how it was verified, what could go wrong, and which lines to read first.
4. **Teaching level** (`.shipshape/local.json`, default working): in learning level, define each technical
   term briefly, use a small analogy if it helps, and end with one or two check questions; offer to go deeper.
5. If you find that the docs are wrong or missing something while explaining, say so and offer to fix them
   (`shipshape-memory`).

Plain words, short sentences. The goal is that the human could explain it to someone else afterwards.
