# Architecture (as built)

> The map of what actually exists. Update it whenever modules, data, interfaces, commands or flows change.
> Only real paths and names: every one here must exist in the code.

## Runtime

<How the pieces run and talk to each other: processes, ports, services, scheduled jobs. A small text diagram
helps.>

## Code map

| Path | Responsibility |
|---|---|
| `<path>` | <what it owns> |

## Data

<Tables / models / files: name, key fields, who writes and who reads them. Migrations: where and how to run.>

## Interfaces

<Endpoints, CLI commands, events, public functions other code relies on.>

## How a request (or job) flows

1. <entry point> → 2. <next step, file:function> → …

## Configuration

<Settings and environment variables by NAME (never values): what each controls, where it's read.>

## Commands

```
<run>
<test>
<type check / lint / build>
```
