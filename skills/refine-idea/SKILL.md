---
name: refine-idea
description: Software factory stage 01. Turns a raw software idea into a decided brief by asking one question at a time, each with a recommended answer.
---
# refine-idea - from a raw idea to a decided brief

Goal: a brief someone could spec without asking a question that changes what gets built.

## Method
1. Restate the idea in one sentence and name the person it serves. If you cannot, that is the first question.
2. Ground it in the repo: read the target repo's `README` and `AGENTS.md` / `CLAUDE.md`, and look for anything that already does part of this. Say what you found.
3. Find the gaps that change what gets built, in this order, skipping what is already answered:
   - who has the problem, and how they cope today
   - what is observably different for them when this ships
   - the smallest version worth shipping
   - what is explicitly not included
   - constraints: deadline, platform, data, money, compliance
   - how we will know it worked
4. Ask one question per message, each with a recommended answer and a one-line reason, so "yes" is a complete reply.
5. When the idea bundles several outcomes, propose the smallest one and offer the rest as separate runs.
6. If the person is not in the conversation, answer each question with your recommendation and record it under Assumptions.
7. Stop when no remaining question would change behavior. Those go under Open questions.

## Brief shape (under ~400 words)
```
# {idea} - brief
## Problem
## Who it is for
## Outcome
## Scope
## Non-goals
## Assumptions
## Open questions
```
