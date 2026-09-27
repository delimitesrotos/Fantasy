# Guided Private Onboarding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a persistent private-state onboarding flow and deliberative decision briefs for a non-technical Fantasy user.

**Architecture:** The repository defines and tests the state machine, a portable `ESTADO_FANTASY` capsule and the recommendation contract. A normal chat asks for one missing input, records only confirmed changes in the visible capsule and can resume from that capsule in a new chat.

**Tech Stack:** Python 3 standard library, Markdown skills and a YAML-shaped portable state capsule.

**Spec:** `docs/superpowers/specs/2026-09-27-guided-private-onboarding-design.md`

## Global Constraints

- Never place real private league data or credentials in the public repository.
- Ask exactly one onboarding question at a time.
- Require at least two contextualized options for consequential recommendations.
- Persist only explicitly confirmed events.
- Use standard GitHub-hosted runners only; add no paid infrastructure.

## Review Focus

- Partially completed onboarding must resume at the first missing stage.
- A daily trigger with incomplete state must route to onboarding rather than advice.
- Empty or single-option briefs must be rejected.
- Missing exact prices must remain `UNKNOWN`, not inferred from another platform.
- Unconfirmed choices must not become events.

---

### Task 1: Onboarding state machine

**Files:**
- Create: `tests/test_private_state.py`
- Create: `scripts/private_state/onboarding.py`
- Create: `scripts/private_state/__init__.py`

**Interfaces:**
- Consumes: private state mappings parsed from the canonical capsule.
- Produces: `next_onboarding_step(state, trigger)` returning a stable stage, prompt and destination flow.

- [ ] Write failing tests for stage order, one-question responses and ready routing.
- [ ] Run `python3 -m unittest tests.test_private_state -v` and verify missing-module failure.
- [ ] Implement the minimal pure state machine.
- [ ] Run the test and full suite; verify all pass.

### Task 2: Deliberative decision contract

**Files:**
- Create: `tests/test_decision_brief.py`
- Create: `scripts/private_state/decision_brief.py`

**Interfaces:**
- Consumes: a recommendation mapping produced by a chat or adapter.
- Produces: `validate_decision_brief(brief)` and `event_from_confirmed_choice(...)`.

- [ ] Write failing tests that reject bare advice and unconfirmed mutation.
- [ ] Run the focused test and verify the expected failure.
- [ ] Implement structural validation and confirmed-event creation.
- [ ] Run focused and full suites; verify all pass.

### Task 3: Human and agent protocols

**Files:**
- Create: `docs/private-state-workflow.md`
- Create: `docs/onboarding-conversation.md`
- Create: `EMPEZAR_AQUI.md`
- Create: `skills/onboarding.md`
- Create: `skills/decision-brief.md`
- Modify: `SKILL.md`
- Modify: `skills/daily-manager.md`
- Modify: `skills/buy-decision.md`
- Modify: `data/user_state.md`
- Modify: `README.md`
- Modify: `protocolo_grill.md`

**Interfaces:**
- Consumes: state machine and brief contract from Tasks 1–2.
- Produces: exact non-technical onboarding dialogue and agent operating procedure.

- [ ] Document the canonical sheet lifecycle and freshness policy.
- [ ] Add exact trigger, prompt and capsule-update behavior to the skills.
- [ ] Replace imperative response formats with contextualized alternatives and user confirmation.
- [ ] Run the full test suite and `git diff --check`.

### Task 4: Portable private-state capsule

**Files:**
- Create: `work/build_private_state_template.mjs` (untracked intermediate)
- Export: `work/Mi Liga Fantasy.xlsx` (untracked intermediate)
- Create: `data/private_state_capsule.md`

**Interfaces:**
- Consumes: capsule schema in the design spec.
- Produces: a blank public template that the chat completes only inside the friend's conversation.

- [ ] Define the complete portable capsule with `UNKNOWN` defaults.
- [ ] Document confirmation, regeneration and new-chat recovery behavior.
- [ ] Verify no external account or real private data is required.

### Task 5: Integration

**Files:** all files above.

**Interfaces:**
- Consumes: verified repository change and private sheet.
- Produces: merged `main` via an auditable pull request.

- [ ] Run the complete unit suite, data pipeline check and whitespace validation.
- [ ] Commit, push, create and attach the pull request.
- [ ] Merge the pull request to `main` and verify the merge commit and Actions configuration.
