---
description: In an empty folder, the first build request starts with the new-project flow, so memory exists from commit one.
tags: [adopt, memory, new-project, needs-bash]
max_turns: 60
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Edit, Write, Bash]
---

Start a new Python command-line project here called notes: `notes add "text"` saves a note and `notes list` prints them, stored in a JSON file. Private repo, just me, nothing live. Go ahead without asking.
