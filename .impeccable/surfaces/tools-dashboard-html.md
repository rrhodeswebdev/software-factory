---
version: 1
slug: "tools-dashboard-html"
primary_target: "_tools/dashboard.html"
related_targets: []
---

# Dashboard surface brief

Scope: `_tools/dashboard.html`, the factory dashboard. Mode: Operate. Used as an ambient side-screen monitor and for focused check-ins (unblock, file tasks). At a glance: something needs me, the factory is alive, where each task is, throughput. Must not feel too sparse. Constraints from PRODUCT.md: one self-contained file, system fonts, follows OS light/dark.

Decision history: the user first got the assigned Drawing Check Set, then switched to the dealt challenger Packed Module Grid (japanese-high-density-web) in their own words: "Do the second design option, I don't like this one". After seeing it built they said "It still looks old and not like a modern dashboard" and took the category standard: Linear and Vercel as the bar, always dark.

## Direction contract

THESIS: A modern product dashboard at the level of Linear and Vercel, dense rather than roomy. It refuses themed costume and the old cramped eight-column board: tasks are one full-width grouped list.

OWN-WORLD: Always dark. Near-black ground (#0a0a0b), panels #111113 with 1px #232328 borders and 12px radii, white primary button. Text #ededef / #b4b4bb / #8a8a93. One accent, violet #8b7cf6, means merged; blue = running, green = passed stage, amber = sent back, red = needs you. Drawn status icons in Linear's grammar. System sans, tabular numerals, large tight stat numbers.

STORY: The person sees the red Needs-you panel first if anything is stopped (or the runner is down), the stat strip and runner pill next, then the stage-count strip and the grouped task list; agents and merged-by-day sit on the right.

FIRST VIEWPORT: Top bar: logo mark and name, runner pill, New task. Four stat tiles. Needs-you panel. Left: Tasks panel with a six-stage count strip, then In progress / Queued / Finished groups with sticky headers, scrolling inside the panel so the page is one window tall. Right: Agents seats and a 7-day merged bar chart.

FORM: Category standard (canon) at full craft, chosen in the user's words over the roll. seed:1f90186bb667c4ba. Signature move: each task row carries a six-segment stage track with its current stage named above it.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
