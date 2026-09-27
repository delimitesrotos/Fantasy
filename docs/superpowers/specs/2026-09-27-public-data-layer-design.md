# Public Data Layer Design

## Purpose

The repository must become a reliable, read-only decision aid for a user of
LALIGA Fantasy Oficial who interacts through a normal LLM chat on Android.
Dynamic facts must be acquired and validated before the existing decision
skills reason about them. The system must prefer `UNKNOWN` over an exact value
whose platform or freshness cannot be proved.

The repository remains a GitHub repository plus GitHub Actions. It will not
connect to a LALIGA account, store credentials, call private LALIGA APIs, or
execute any action in the game.

## Audited source

The canonical public page is:

`https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado`

The audit on 2026-09-27 established that:

- the page is public server-rendered HTML and requires no authenticated API;
- its canonical URL, heading, and copy explicitly identify LALIGA Fantasy
  Oficial;
- each player row exposes a FútbolFantasy player ID, normalized source name,
  position, team ID, current value, previous values, and daily differences;
- the rendered row contains the display name and team name;
- the next-opponent cell contains the target matchday and, when available, the
  starter probability;
- the page contains an explicit market update timestamp;
- 661 rows were available during the audit;
- `robots.txt` does not disallow crawling;
- the response advertises a rate limit of 30 requests per 10 seconds;
- no public JSON endpoint was needed or selected;
- the site's legal notice reserves rights over its content, so the integration
  must fetch infrequently, attribute the provider, store only the factual
  fields needed by this project, and never copy editorial text or source code.

The extractor will identify itself with a repository-specific user agent. It
will not bypass blocks, cookies, CAPTCHAs, or other protections. A future block
or material policy change disables acquisition rather than triggering an
evasion attempt.

## Source policy

### Market value and daily change

The primary source is the audited FútbolFantasy LALIGA Fantasy Oficial market
page. A value is accepted only when all platform markers match, the source
timestamp parses, the row has an unambiguous player identity, and the complete
dataset passes validation.

The source update timestamp on the page is authoritative for the market cycle.
A market snapshot is `fresh` through the end of the next expected daily update
window, with a maximum age of 30 hours. It becomes `stale` after that threshold
and `unknown` when no valid observation exists.

No other fantasy platform, generic search result, search snippet, or cached
result can replace a missing current market value. A value explicitly read by
the user from the official app has conversation-local precedence.

### Starter probability

The primary source is the probability embedded in the same audited player row.
The target matchday must be present and parseable. Because the page does not
publish a separate per-probability update time, the record stores
`source_updated_at: null`, the observed `retrieved_at`, and its target
matchday. A successful observation is `fresh` for 8 hours, then `stale`.

Rows without a published probability produce no numeric estimate. They are
represented as unavailable, never as zero.

### Injuries, suspensions, and fixtures

These fields remain contextual. FútbolFantasy, official club sources, LALIGA,
and reliable sports reporting may be consulted. A general web search can help
locate context, but it cannot manufacture or override an exact market value.

## Repository architecture

The existing decision architecture remains in place. The new components are:

```text
data/
  public/
    latest/
      players.json
      market-values.json
      starter-probabilities.json
      metadata.json
    historical/
      .gitkeep
    examples/
      *.json
scripts/
  public_data/
    __init__.py
    fetch.py
    parse.py
    freshness.py
    validate.py
    serialize.py
  update_public_data.py
tests/
  fixtures/
  test_parse.py
  test_freshness.py
  test_validation.py
  test_update_pipeline.py
.github/workflows/update-public-data.yml
source/data-policy.md
docs/data-architecture.md
```

Python standard-library modules are sufficient: `urllib.request` for the one
public HTTP request, `html.parser` for extraction, `zoneinfo` and `datetime`
for timestamps, and `json` for deterministic output. No browser automation or
runtime package installation is required.

## Data contracts

All timestamps use ISO 8601 with timezone offsets. JSON is UTF-8, pretty
printed, key-sorted, and ends with a newline.

### Player identity

`players.json` is an object with schema metadata and a `players` array. Each
player has:

```json
{
  "id": "futbolfantasy:13036",
  "source_id": "13036",
  "name": "Yoel Lago",
  "normalized_name": "yoel_lago",
  "team": "Celta",
  "team_source_id": "5",
  "position": "DEF"
}
```

The stable repository ID is namespaced with the provider ID. Normalized names
are lookup aliases, not primary keys. Normalization applies Unicode NFKD,
removes combining marks, lowercases, replaces non-alphanumeric runs with one
underscore, and trims underscores. Source IDs may contain letters because the
page includes non-player entities; records with position `Entrenador` are
excluded from player snapshots.

Source ID is the primary identity. Duplicate IDs are fatal. Duplicate
`normalized_name` values are allowed only when team or position distinguishes
them; consumers must then use the ID or a composite lookup.

### Market values

Each entry in `market-values.json` contains:

```json
{
  "player_id": "futbolfantasy:13036",
  "market_value": {
    "value": 10825329,
    "currency": "EUR",
    "daily_change": 522098,
    "platform": "laliga_fantasy_oficial",
    "source": "futbolfantasy",
    "source_url": "https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado",
    "retrieved_at": "2026-09-27T12:00:00+02:00",
    "source_updated_at": "2026-09-27T03:00:00+02:00",
    "freshness": "fresh"
  }
}
```

### Starter probabilities

Each published estimate in `starter-probabilities.json` contains:

```json
{
  "player_id": "futbolfantasy:13036",
  "starter_probability": {
    "value": 95,
    "target_matchday": 8,
    "source": "futbolfantasy",
    "source_url": "https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado",
    "retrieved_at": "2026-09-27T12:00:00+02:00",
    "source_updated_at": null,
    "freshness": "fresh"
  }
}
```

### Metadata

`metadata.json` is the trust entry point for an LLM. It contains schema
version, generation time, pipeline status, the canonical platform, row counts,
and a source entry for each dataset with provider, URL, status, retrieval time,
source update time, freshness threshold, last success, and any error.

Consumers must inspect metadata before opening individual datasets. A dataset
cannot be treated as current when its metadata status is `stale` or `unknown`,
even if its file still contains a last-known numeric value.

## Acquisition and parsing

`fetch.py` performs one HTTPS GET with a descriptive user agent, a 30-second
timeout, response-size ceiling, and content-type check. HTTP errors, timeouts,
redirect loops, oversized responses, and non-HTML responses are explicit
failures.

`parse.py` uses a purpose-built `HTMLParser` subclass. It first proves the
platform with independent page markers. It then reads player-row attributes
and scoped text. It does not infer a platform by column position. The parser
also extracts the page update timestamp in `Europe/Madrid`, the matchday, and
the optional starter percentage.

The parser fails loudly when required page markers, timestamp, columns, or row
attributes disappear. It does not use regex as the primary HTML parser.

## Validation and atomic publication

Validation occurs before any file in `data/public/latest/` changes. Checks
include:

- platform equals `laliga_fantasy_oficial`;
- source URL and provider are canonical;
- source and retrieval timestamps parse and are not implausibly future-dated;
- at least 400 non-coach players exist;
- at least 15 teams and all four player positions exist;
- every player ID is unique and every reference resolves;
- values are positive integers and daily changes are integers;
- starter probabilities are integers from 0 through 100;
- target matchdays are positive integers;
- an excessive missing-probability rate is recorded but is not fatal because
  the provider legitimately omits some estimates;
- no single player's value changes by more than 50% from the prior valid
  snapshot without an explicit `--allow-large-change` maintenance override;
- player count cannot fall by more than 20% from the previous snapshot;
- current output cannot silently switch platform.

Serialization happens in a temporary directory. Only after every dataset and
cross-file check passes are all four files atomically replaced. Identical
semantic data does not create unnecessary historical copies.

On acquisition, parsing, or validation failure, the pipeline leaves the last
valid data files untouched, rewrites only `metadata.json` to record the failure
and calculate `stale`/`unknown`, emits a clear error, and exits non-zero. The
workflow therefore becomes visibly red without replacing known-good data.

`--check` parses and validates without publishing. `--input` accepts a local
fixture for deterministic tests. `--now` is available only for tests and
reproducible validation.

## Freshness gate

Freshness is computed, never trusted from input JSON:

- market values: source age at most 30 hours;
- starter probabilities: retrieval age at most 8 hours and target matchday
  still known;
- future timestamps beyond five minutes: invalid;
- no observation: `unknown`;
- valid observation older than its threshold: `stale`.

The scheduled workflow recalculates metadata on every run. If the provider
returns an old cycle, the workflow must not label it fresh merely because it
was retrieved recently.

## Scheduling

One workflow runs on standard `ubuntu-latest`, supports manual dispatch, uses
least-privilege `contents: write`, and has a concurrency group to avoid
overlapping updates.

It runs four times daily at widely separated UTC hours. This is enough to keep
the eight-hour probability window useful while remaining negligible compared
with the advertised rate limit. The same response contains the market data,
so no additional requests are made. The market source timestamp prevents a
later retrieval from masquerading as a new market cycle.

After a successful update, the workflow commits only when generated files
changed. It never uses larger runners, paid APIs, AI services, browser
automation, or credentials beyond the repository-scoped GitHub token.

## Decision-layer changes

`SKILL.md` will define this resolution order:

1. explicit value from the user's official app for the current conversation;
2. repository snapshot after passing the freshness gate;
3. canonical source opened and verified directly;
4. secondary sources for context only;
5. general search for context only;
6. `UNKNOWN`.

It will include the explicit search-result policy: a snippet is never evidence
for an exact dynamic LALIGA Fantasy value.

The four existing workflow skills will be amended narrowly:

- market analysis reads metadata and bulk snapshots before contextual search;
- buy decisions enforce the value precedence above;
- daily manager enriches the user's one daily private market list from the
  bulk public snapshot;
- lineup reads starter probabilities first and searches only for contextual
  developments such as injuries, press conferences, suspensions, or rotation.

Responses distinguish `HECHO`, `ESTIMACIÓN`, and `ANÁLISIS` when dynamic facts
affect a recommendation.

`data/user_state.md` remains a template containing no real user data. Skills
will treat statements such as `Compré a X por 8M` as incremental private-state
events and will not request a complete new screenshot after every operation.

## Tests and acceptance

Unit tests use compact, original HTML fixtures rather than copied production
pages. They cover:

- a fresh valid snapshot;
- a prior-day snapshot after the next cycle becomes stale;
- explicit selection of LALIGA Fantasy Oficial from multi-platform markup;
- rejection when platform identity is missing;
- ignoring a contradictory search snippet;
- conversation-local precedence of a value reported from the official app;
- normalization of accents and punctuation;
- duplicate IDs and broken references;
- missing, malformed, negative, or out-of-range values;
- structural changes and row-count collapse;
- atomic preservation of the previous snapshot on failure.

The critical live acceptance check runs the pipeline against FútbolFantasy and
confirms that Yoel Lago, David Soria, and Kylian Mbappé resolve through the
snapshot with source, platform, and freshness. Their numeric values are not
hardcoded into permanent tests.

## Out of scope

- LALIGA authentication or private APIs;
- automated bids, sales, lineups, or clauses;
- extraction of the user's private league market;
- a server, database, hosted application, PWA, or paid service;
- search-engine snippets as structured data;
- copying code from reference repositories.

## Success criteria

The work is complete when a normal LLM can answer from a fresh repository
snapshot without open search, every dynamic value carries source/platform/time
provenance, stale values cannot present as current, platform ambiguity fails
closed, the last valid data survives provider failures, GitHub Actions refreshes
the public layer automatically, and the user's only operational interaction is
still a normal chat plus minimal private league input.
