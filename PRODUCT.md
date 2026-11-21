# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
One person: the owner of the factory, a developer who files GitHub issues and lets agents carry them to merged pull requests. They use the dashboard about equally in two ways: left open on a side screen as an ambient monitor (what's running, is anything stuck), and opened on purpose a few times a day to unblock stopped tasks and file new ones.

## Product Purpose
A personal software factory: GitHub issues labelled `factory` in onboarded repos move through six agent stages (triage, spec, build, preflight, review, approve) to a merged PR, several tasks at once. A person is asked only when a check isn't confident. The dashboard shows that conveyor at a glance and lets the person act on it. Success: the person knows within a second whether anything needs them, and can see where every task is without reading.

## Operating Context
- Served by `_tools/dashboard.py` on localhost only (`/factory dashboard`); polls `/api/state` every 10s while visible.
- Data: the runner's state (alive, mode, last pull), each task's stage verdicts (`pass`, `fail: retry NN`, `fail: human`, `reject`), the agents running now and what each is doing, the repos onboarded.
- Actions on the page: open a task's stage files and history, create a new task (GitHub issue). Unblocking happens via the `/unblock` skill or `factory.py feedback`, not on the page.
- Stage names and verdict words are the factory's own vocabulary (see `CONTEXT.md`); the page uses them as-is.

## Capabilities and Constraints
- One self-contained HTML file (`_tools/dashboard.html`): no build step, no web fonts, no CDN scripts. Works offline. System fonts only.
- Always dark (see Brand Commitments).
- Tasks: queued, running, needs you, merged, rejected. Agents: up to `FACTORY_AGENTS` (default 4) at once.

## Evidence on Hand
Real state only; no sample data is shipped. Empty states (no tasks, runner stopped, no agents) are normal and must read well.

## Product Principles
1. "Needs you" outranks everything; nothing else should compete with it.
2. Readable from across a desk: state is carried by position and colour, not by reading text.
3. The factory's own words, not dashboard jargon.
4. Zero setup: it opens and works.

## Brand Commitments
- The dashboard follows the category standard, not a themed world: the owner wants it to look like a modern dashboard on the level of Linear and Vercel (user's choice, 2026-11-21, after rejecting two themed directions).
- Always dark, whatever the OS setting (user's choice).
