# Guided Private Onboarding — Design

## Goal

Make a non-technical LALIGA Fantasy user productive from three natural prompts—
`Empezar Fantasy`, `¿Qué hago hoy?` and `Prepara mi jornada`—without relying on
chat memory and without turning recommendations into unexplained orders.

## Architecture

The public repository remains the source for decision rules, onboarding and
validated public data. A compact `ESTADO_FANTASY` capsule inside the normal chat
is the explicit state for the user's league, roster, rivals, private market and
confirmed events. The chat asks for one missing item at a time and rewrites the
capsule only with confirmed facts.

No real league data, credentials or account access may enter this public
repository. The repository contains only the blank capsule template. No Drive,
external database, code execution or setup by the repository owner is required.

## Onboarding state machine

The assistant resolves these stages in order and asks exactly one concrete
question per turn:

1. `league_rules`: scoring, squad/position limits, clauses, bonuses and market
   cadence.
2. `own_team`: roster, cash, team value and protected players.
3. `standings`: current table and the rivals that matter most.
4. `rival_rosters`: known rival squads, captured progressively rather than as a
   blocking bulk import.
5. `ready`: daily use is enabled.

If the user arrives with `¿Qué hago hoy?` before onboarding is complete, the
assistant does not issue a recommendation from partial private context. It
explains the single missing input and asks for the smallest screenshot or value
that advances the next stage.

## Canonical private capsule

`data/private_state_capsule.md` defines the portable YAML block. The chat shows
the complete updated capsule after every confirmed state change. If the friend
opens a new chat, the onboarding asks for the last capsule; if it is unavailable,
it reconstructs the state progressively from current screenshots. Thus the
system does not depend on hidden cross-chat memory.

## Freshness

- League rules: valid until the user reports a rule change.
- Own roster/cash: reconcile after every confirmed event; otherwise warn after
  48 hours.
- Private market: valid only for the capture date.
- Standings: valid for the current matchday; warn after seven days.
- Rival rosters: may be partial; show the last known date and never imply
  completeness.

Stale or missing inputs are visible in the answer. They lower confidence and
may block an exact bid ceiling, but do not erase useful strategic context.

## Deliberative recommendation contract

Every consequential recommendation is a decision brief, not an imperative. It
must include:

1. Decision and deadline.
2. Verified context with source and freshness.
3. Unknowns and uncertainty.
4. At least two viable options, including `no actuar` when meaningful.
5. For every option: upside, downside, cash/roster/rival impact, conditions,
   reversibility and confidence.
6. The assistant's reasoned preference and the threshold at which it changes.
7. A direct question asking the user to choose.

The user's selection remains pending until explicitly confirmed. Only then may
the assistant append an event and emit an updated capsule.

## Success criteria

- A non-technical user can start with any of the three trigger phrases.
- The assistant asks one input at a time and resumes at the first missing stage.
- A complete state enters the appropriate daily, matchday or general flow.
- Bare recommendations such as `compra X` fail validation.
- A valid brief exposes evidence, alternatives and implications.
- No event mutates private state without explicit confirmation.
