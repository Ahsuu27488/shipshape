---
type: tool_order
before: { tool: Bash, input_match: 'git (switch -c|checkout -b|switch --create)' }
after: { tool: Bash, input_match: 'git commit' }
---
