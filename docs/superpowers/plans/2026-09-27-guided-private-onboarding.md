# Guided Private Onboarding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a persistent private-state onboarding flow and deliberative decision briefs for a non-technical Fantasy user.

**Architecture:** The repository defines and tests onboarding, a mandatory private-state turn controller, a versioned `.xlsx` template and the recommendation contract. A normal chat creates a private Google Sheet in the player's connected Drive, persists detected changes before analysis and resumes from Drive in a new chat.

**Tech Stack:** Python 3 standard library, Markdown skills, Excel template and Google Drive/Sheets actions in the player's chat.

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
- [ ] Add exact trigger, prompt and automatic Sheet-update behavior to the skills.
- [ ] Replace imperative response formats with contextualized alternatives and user confirmation.
- [ ] Run the full test suite and `git diff --check`.

### Task 4: Versioned private-state workbook

**Files:**
- Create: `templates/Fantasy-Estado-Privado.xlsx`
- Create: `templates/README.md`
- Create: `data/private_drive_state.md`

**Interfaces:**
- Consumes: workbook schema in the design spec.
- Produces: a blank public template imported only to the friend's connected Drive.

- [ ] Create and visually verify the `.xlsx` workbook and evidence index.
- [ ] Document import, confirmation, automatic writeback and new-chat recovery.
- [ ] Verify the repository contains no real private data.

### Task 5: Integration

**Files:** all files above.

**Interfaces:**
- Consumes: verified repository change and private sheet.
- Produces: merged `main` via an auditable pull request.

- [ ] Run the complete unit suite, data pipeline check and whitespace validation.
- [ ] Commit, push, create and attach the pull request.
- [ ] Merge the pull request to `main` and verify the merge commit and Actions configuration.
