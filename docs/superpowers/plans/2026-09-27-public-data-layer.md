# Public Data Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a validated, provenance-rich public snapshot of LALIGA Fantasy Oficial market values and starter probabilities that existing decision skills consume before web search.

**Architecture:** A dependency-free Python package fetches one canonical server-rendered FútbolFantasy page, parses it into typed records, validates the complete batch, computes freshness, and atomically publishes deterministic JSON. A scheduled GitHub Action runs the pipeline on a standard public runner; documentation and existing skills define fail-closed consumption rules.

**Tech Stack:** Python 3.11 standard library, `unittest`, JSON, GitHub Actions YAML.

**Spec:** `docs/superpowers/specs/2026-09-27-public-data-layer-design.md`

## Global Constraints

- Never authenticate with LALIGA or use private/undocumented LALIGA APIs.
- Use only public data plus human-provided private state; never commit real private league data.
- Use only `ubuntu-latest`; no larger runners, paid APIs, AI services, browser automation, servers, or databases.
- Treat exact dynamic values as `UNKNOWN` unless platform and freshness are validated.
- Keep the existing decision architecture and modify it narrowly.
- Use only the Python standard library at runtime and in tests.

## Review Focus

- Truncated HTML after valid-looking rows must fail instead of publishing a partial snapshot.
- A deceptive page mentioning LALIGA Fantasy in content but using another platform canonical URL must fail.
- Duplicate source IDs must fail even when names and teams differ.
- A future source timestamp beyond five minutes must fail.
- Publication failure must preserve every prior data file except failure metadata.

---

### Task 1: Parser, identity, and freshness

**Files:**
- Create: `scripts/public_data/__init__.py`
- Create: `scripts/public_data/models.py`
- Create: `scripts/public_data/parse.py`
- Create: `scripts/public_data/freshness.py`
- Create: `tests/fixtures/valid_market.html`
- Create: `tests/fixtures/ambiguous_platform.html`
- Create: `tests/test_parse.py`
- Create: `tests/test_freshness.py`

**Interfaces:**
- Produces: `parse_market_html(html: str, retrieved_at: datetime) -> ParsedSnapshot`, `normalize_name(name: str) -> str`, and `classify_freshness(observed_at, now, max_age) -> str`.
- `ParsedSnapshot` exposes `source_updated_at`, `players`, `market_values`, and `starter_probabilities`.

- [ ] **Step 1: Add failing parser and freshness tests**

```python
snapshot = parse_market_html(VALID_HTML, datetime.fromisoformat("2026-09-27T12:00:00+02:00"))
self.assertEqual(snapshot.players[0].id, "futbolfantasy:13036")
self.assertEqual(snapshot.market_values[0].value, 10825329)
self.assertEqual(snapshot.starter_probabilities[0].value, 95)
self.assertEqual(normalize_name("Kylian Mbappé"), "kylian_mbappe")
self.assertEqual(classify_freshness(observed, now, timedelta(hours=30)), "fresh")
```

Also assert that missing canonical platform markers, malformed rows, a truncated table, out-of-range percentages, and timestamps more than five minutes in the future raise typed errors.

- [ ] **Step 2: Run tests and observe the missing-module failure**

Run: `python3 -m unittest tests.test_parse tests.test_freshness -v`

Expected: FAIL because `scripts.public_data` does not exist.

- [ ] **Step 3: Implement minimal dataclasses, parser, normalization, and freshness**

```python
@dataclass(frozen=True)
class Player:
    id: str
    source_id: str
    name: str
    normalized_name: str
    team: str
    team_source_id: str
    position: str

def normalize_name(name: str) -> str:
    decomposed = unicodedata.normalize("NFKD", name)
    ascii_name = "".join(c for c in decomposed if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "_", ascii_name.lower()).strip("_")
```

Use `HTMLParser` state scoped to `tr.elemento_jugador`, require the canonical URL and H1 platform marker, and require a closed market table.

- [ ] **Step 4: Run parser and freshness tests**

Run: `python3 -m unittest tests.test_parse tests.test_freshness -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/public_data tests/fixtures tests/test_parse.py tests/test_freshness.py
git commit -m "feat: parse canonical fantasy market data"
```

### Task 2: Batch validation and deterministic serialization

**Files:**
- Create: `scripts/public_data/validate.py`
- Create: `scripts/public_data/serialize.py`
- Create: `tests/test_validation.py`
- Create: `tests/test_serialize.py`

**Interfaces:**
- Consumes: `ParsedSnapshot` from Task 1.
- Produces: `validate_snapshot(snapshot, previous=None, minimum_players=400) -> None`, `build_documents(snapshot, now) -> dict[str, dict]`, and `publish_documents(documents, output_dir) -> None`.

- [ ] **Step 1: Add failing validation and publication tests**

```python
with self.assertRaises(ValidationError):
    validate_snapshot(snapshot_with_duplicate_ids, minimum_players=1)

publish_documents(documents, output_dir)
self.assertEqual(json.loads((output_dir / "metadata.json").read_text()), documents["metadata.json"])
```

Cover positive values, integer daily changes, four positions, minimum teams and players, resolved references, duplicate IDs, row-count collapse, >50% prior-value changes, deterministic ordering, and preservation when a staged document is invalid.

- [ ] **Step 2: Run tests and observe missing functions**

Run: `python3 -m unittest tests.test_validation tests.test_serialize -v`

Expected: FAIL because validation and serialization modules do not exist.

- [ ] **Step 3: Implement validation and atomic publication**

```python
def publish_documents(documents: Mapping[str, Mapping[str, object]], output_dir: Path) -> None:
    with tempfile.TemporaryDirectory(dir=output_dir.parent) as raw_tmp:
        tmp = Path(raw_tmp)
        for name, document in documents.items():
            (tmp / name).write_text(json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        for name in documents:
            os.replace(tmp / name, output_dir / name)
```

Validate the full document set before the first `os.replace` and sort records by namespaced player ID.

- [ ] **Step 4: Run validation and serialization tests**

Run: `python3 -m unittest tests.test_validation tests.test_serialize -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/public_data tests/test_validation.py tests/test_serialize.py
git commit -m "feat: validate and publish public snapshots"
```

### Task 3: Fetcher and update command

**Files:**
- Create: `scripts/public_data/fetch.py`
- Create: `scripts/update_public_data.py`
- Create: `tests/test_fetch.py`
- Create: `tests/test_update_pipeline.py`

**Interfaces:**
- Consumes: parser, validation, and serialization APIs from Tasks 1-2.
- Produces: `fetch_html(url=CANONICAL_URL, timeout=30, max_bytes=8_000_000) -> str` and CLI exit status 0 only after a valid check or publication.

- [ ] **Step 1: Add failing boundary and pipeline tests**

```python
response = FakeResponse(b"<html></html>", "text/html; charset=UTF-8")
self.assertEqual(fetch_html(opener=FakeOpener(response)), "<html></html>")
self.assertNotEqual(run(["--input", "tests/fixtures/ambiguous_platform.html", "--check"]), 0)
```

Cover content-type rejection, byte ceiling, explicit user agent, local fixture mode, check mode, successful publication, and preservation plus stale failure metadata after invalid input.

- [ ] **Step 2: Run tests and observe missing modules**

Run: `python3 -m unittest tests.test_fetch tests.test_update_pipeline -v`

Expected: FAIL because fetcher and CLI do not exist.

- [ ] **Step 3: Implement fetch and CLI orchestration**

```python
parser.add_argument("--input", type=Path)
parser.add_argument("--output", type=Path, default=Path("data/public/latest"))
parser.add_argument("--check", action="store_true")
parser.add_argument("--allow-large-change", action="store_true")
```

The live path makes exactly one request. The failure path writes only metadata when prior output exists and returns non-zero.

- [ ] **Step 4: Run focused and complete tests**

Run: `python3 -m unittest tests.test_fetch tests.test_update_pipeline -v && python3 -m unittest discover -s tests -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/update_public_data.py scripts/public_data tests/test_fetch.py tests/test_update_pipeline.py
git commit -m "feat: add fail-closed public data pipeline"
```

### Task 4: Public snapshots and scheduled workflow

**Files:**
- Create: `data/public/latest/players.json`
- Create: `data/public/latest/market-values.json`
- Create: `data/public/latest/starter-probabilities.json`
- Create: `data/public/latest/metadata.json`
- Create: `data/public/historical/.gitkeep`
- Create: `data/public/examples/README.md`
- Create: `.github/workflows/update-public-data.yml`

**Interfaces:**
- Consumes: `python3 scripts/update_public_data.py` from Task 3.
- Produces: repository-readable current data and a scheduled/manual workflow.

- [ ] **Step 1: Run the live pipeline in check mode**

Run: `python3 scripts/update_public_data.py --check`

Expected: PASS with one canonical request and a validation summary above 400 players.

- [ ] **Step 2: Publish a live snapshot locally**

Run: `python3 scripts/update_public_data.py`

Expected: PASS and four valid JSON files under `data/public/latest/`.

- [ ] **Step 3: Add the standard-runner workflow**

```yaml
on:
  schedule:
    - cron: "17 2,8,14,20 * * *"
  workflow_dispatch:
jobs:
  update:
    runs-on: ubuntu-latest
```

Grant only `contents: write`, use concurrency, run tests before update, and commit generated files only when changed.

- [ ] **Step 4: Validate workflow constraints and full suite**

Run: `python3 -m unittest discover -s tests -v && python3 -m json.tool data/public/latest/metadata.json >/dev/null && ! rg "larger|self-hosted|macos-|windows-" .github/workflows`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .github data/public
git commit -m "ci: refresh public fantasy data automatically"
```

### Task 5: Source policy, skills, and user documentation

**Files:**
- Create: `source/data-policy.md`
- Create: `docs/data-architecture.md`
- Modify: `README.md`
- Modify: `SKILL.md`
- Modify: `skills/market-analysis.md`
- Modify: `skills/buy-decision.md`
- Modify: `skills/daily-manager.md`
- Modify: `skills/lineup.md`
- Modify: `data/user_state.md`

**Interfaces:**
- Consumes: metadata and dataset contracts from Tasks 1-4.
- Produces: instructions that make a normal LLM resolve current facts safely.

- [ ] **Step 1: Document the acquisition, validation, and decision boundaries**

Document the canonical URL, provenance fields, 30-hour and 8-hour freshness gates, fail-closed behavior, legal/robots audit, and explicit `UNKNOWN` fallback.

- [ ] **Step 2: Update the core and workflow skills**

Add the resolution order, search-snippet prohibition, app-value precedence, bulk snapshot enrichment, `HECHO`/`ESTIMACIÓN`/`ANÁLISIS` output convention, and incremental private-state events.

- [ ] **Step 3: Update README and private-state template**

Explain the intelligence and public-data layers, Android/chat-only workflow, automatic refresh, and strict prohibition on committing real private data.

- [ ] **Step 4: Run full verification and inspect the acceptance players**

Run: `python3 -m unittest discover -s tests -v && python3 scripts/update_public_data.py --check && python3 -m json.tool data/public/latest/players.json >/dev/null && git diff --check`

Expected: PASS. Inspect the generated records for Yoel Lago, David Soria, and Kylian Mbappé and confirm platform, provider, timestamps, and freshness are present.

- [ ] **Step 5: Commit**

```bash
git add README.md SKILL.md skills data/user_state.md source docs/data-architecture.md
git commit -m "docs: consume validated public fantasy data"
```

### Task 6: Final audit, PR, and merge

**Files:**
- Modify only files required by findings from the final audit.

**Interfaces:**
- Consumes: the complete branch.
- Produces: a green pull request merged into `main`.

- [ ] **Step 1: Verify repository visibility and workflow cost constraints**

Run: `gh repo view delimitesrotos/Fantasy --json visibility,nameWithOwner && rg -n "runs-on:" .github/workflows`

Expected: visibility `PUBLIC`; every job uses `ubuntu-latest`.

- [ ] **Step 2: Run final verification**

Run: `python3 -m unittest discover -s tests -v && python3 scripts/update_public_data.py --check && git diff --check && git status --short`

Expected: tests and live check pass; no whitespace errors; only intended files are present.

- [ ] **Step 3: Push and create the PR**

```bash
git push -u origin feature/public-data-layer
gh pr create --base main --head feature/public-data-layer --title "feat: add validated public fantasy data layer" --body-file .superpowers/sdd/2026-09-27-public-data-layer/pr-body.md
```

- [ ] **Step 4: Merge only after required checks pass**

```bash
gh pr checks <number> --watch
gh pr merge <number> --merge --delete-branch
```

- [ ] **Step 5: Verify merged state**

Run: `gh pr view <number> --json state,mergedAt,mergeCommit,url`

Expected: state `MERGED` with a merge commit and URL.
