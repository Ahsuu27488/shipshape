# When it isn't clear what to build

Use this when the request is a direction rather than a description: a new app, a fuzzy feature, "I have an
idea", "make it better". A clear request skips it: do it, or ask one precise question (Step 1).

The risk here is not bad code but good code for the wrong thing. Every gap you fill with a guess is a decision
the human never got to make. Good questions help them as well: many people only find out what they want while
they answer.

## The conversation

1. **Open with one question.** Your first message has two parts: one line saying they can skip the questions
   and let you choose (if they do, name your main choices in one line each; that list, or for a project the
   design file, is what they approve), and one open question that invites a concrete story: "What happened
   the last time you needed this?"
2. **One question per message,** in their words, without a list of sample answers. Open questions first; offer
   two or three options only when they are stuck; when they say "you choose", make a concrete proposal.
   Sometimes a guess works better than a question: say what you think the reason is, and let them correct you.
3. **Know what you need to learn** (a checklist for you, not questions to recite): what it is and who it's for;
   why it matters now, and how they will know it worked; what it must not do, and what would count as failure
   even if it runs; what exists already; which technical choices (platform, language, libraries) they want to
   make and which they leave to you. In an existing project, use what the project already has.
4. **Look before you ask.** The code, STATUS and DECISIONS answer many questions; don't ask what they already
   say. Offer to look further (their files and data, other products, the web) when it would help; they decide.
5. **Play it back in parts.** Once you understand one part (what it's for, or how one part works), describe it
   back in a short paragraph, say which parts are your guesses, and ask what you got wrong or left out. Then the
   next part. If it's something visual (a screen, a page, a chart), show a rough mockup: it says more than prose.

## Size it, then write it down

Say the size in one line; the human can overrule it.

| Size | The description lives in | Then |
|---|---|---|
| Quick, and already clear | the request | just do it |
| A small change | a few lines in chat | the normal steps, from Step 2 |
| A project | `docs/plans/<yyyy-mm-dd>-<slug>-design.md` | a plan built from the design (Step 4) |

Size is how much to write down; the tier (Step 2) is how careful to be. A small change to payments is still T2.
A request that hides several independent projects gets split: name them, agree which comes first, and do them
one by one.

**The design file** lets someone who wasn't in the conversation plan the work: why it exists and what it's for;
what it must and must not do; the limits (time, money, platforms); every choice the human made, in their words;
and the choices still open, with the ones you settled yourself marked as yours. Before you hand it over, have it
read by someone who wasn't in the conversation (a separate agent, session or person), or read it that way
yourself; whatever only the human can answer goes to them in one message.

## Build nothing until they approve

They approve what they have read: for a small change, the few lines in chat; for a project, the design file.
Agreeing with an idea is not approving a description they haven't seen. Until then, read and explore all you
like, but don't write code, set up a project or install anything. Exception: a quick throwaway experiment they
asked for. Label it throwaway; turning it into the real thing needs its own approval.

**Unattended:** nobody can answer. If one reading is clearly the most conservative, take it and write every
assumption in the plan. If what to build is a choice only the human can make, write your questions in the plan,
then stop and report (`shipshape-unattended`).

Adapted from the `brainstorming` skill of superpowers (github.com/obra/superpowers, MIT, © Jesse Vincent).
