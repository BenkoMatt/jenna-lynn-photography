# JLP V4.4-D — DESKTOP-GATED ZERO-MOVEMENT WORKFLOW (2.5-HOUR BUDGET, 4 AGENTS)

> **PART 2 OF 2.** This is the DESKTOP gate of the V4.4 split. Sibling doc:
> `WORKFLOW-PROMPT-V4.4-MOBILE.md` — execute that run FIRST; it ships the
> deterministic-masonry template + 6-element manifest and its output is THIS run's
> starting point. One responsive gallery — this run gates and perfects the ≥900px
> band; the mobile run already gated ≤899px.

You are Caddy executing a pre-authorized build workflow for Jenna Lynn Photography's
client photo-delivery system. This run is **V4.4-D**, second half of the V4.4 split.
After V4.4-M, the template's mobile band (≤899px) has deterministic no-movement
masonry; the desktop band (≥900px) still uses CSS-multicol, which REBALANCES at every
batch seam — rendered tiles jump columns and the wall shifts. Matt's bar (verbatim,
2026-09-25 morning):

> "I want 15 to load, then a loading screen (taking as much time as it needs), then
> the next 15 load and are already all in their dedicated spots in the gallery.
> Adding photos as it moves completely shifts the gallery around and makes it feel
> almost epileptic."

Mission: **at desktop widths, a tile once rendered never moves again, and every
appended tile lands in a pre-sized dedicated slot — while the showcase wall grammar
(5 columns, hairline gutters, offset rhythm) survives intact.**

Desktop context (why this band is its own run): the showcase wall Matt approved is a
DESKTOP composition — 5×~280px columns, 3px gutters, left-3 row-aligned / right-2
offset, 2:3/3:2 duo. The no-movement guarantee must not flatten it into a rigid grid;
this run's craft is keeping the rhythm while making placement deterministic.

Load these skills FIRST and follow them: `jlp-photo-delivery-ops`,
`programmatic-web-visual-qa`, `subagent-reliability`, `multi-agent-workflow-prompting`.
Visual QA gate at EVERY stage. Never claim a visual verdict the machine did not make.
Vision output is a hypothesis; pixel/geometry ground truth arbitrates.

---

## §1 MISSION (desktop band ≥900px)

Evolve the V4.4-M template so that scrolling a 100-photo gallery at desktop widths
produces **zero visible movement of already-rendered content**:

1. **Reserved slots.** Aspect-ratio boxes from manifest width/height (6-element
   entries) BEFORE images decode — no sliver growth, no late snap.
2. **Deterministic masonry at 5/3 columns.** Column assignment computed (the V4.4-M
   mechanism, generalized from 2-col to 5-col ≥1200 and 3-col ≥900); batch N+1
   appends never recomputes tiles 1..15N's x/y. Verify the showcase's offset rhythm
   survives — if deterministic placement changes the wall's feel vs
   `showcase-ref.png`, surface it to Matt rather than silently accepting.
3. **All V4.4-M behavior preserved**: exactly 15 at first paint; background prefetch
   while the fixed bottom-center ring plays; ONE mutation per batch; unit fade;
   favorites/PIN/lightbox/zip untouched; reduced-motion renders all.
4. **Cross-band guard:** the ≤899px band must still pass V4.4-M's probes after this
   run's changes (quick mobile regression gate — do not break the shipped mobile
   band while perfecting desktop).
5. **Zero client-data risk.** Real galleries NEVER touched. Regen targets:
   demo-100 refresh + scratch `v44-regen` only (if the template changed since
   V4.4-M's regen; otherwise reuse).

**Band gate:** acceptance viewports **1440×900 (primary), 1280×800 and
1024×768 (3-col band), plus 1920×1080 wide sanity**. Mobile (≤899px) is a REGRESSION
check only (quick probes at 390 — must still pass P1–P8).

**Success criteria (machine-verified before you report done):**
1. **P8 (no-movement) at 1440 AND 1024:** every tile present before append k has the
   SAME column index and x/y after every later append (±1px) across the 100-photo
   walk. A single moved tile fails the run.
2. **P9 (reserved slots) at 1440:** appended tiles have final layout height on FIRST
   paint after append (growth ≤2px).
3. **Showcase-grammar fidelity (vision + pixel):** at 1440, the wall still matches
   the Pixieset showcase grammar — 5 columns, ~3px hairline gutters, 2:3/3:2 duo,
   offset rhythm (compare against `showcase-ref.png`; gutters within 1px). The
   rhythm is a design law — deterministic placement must not read as a rigid grid.
4. V4.3 probes P1–P7 all PASS at 1440 (initial 15; appends exactly 15 per mutation;
   ring visible/hidden; prefetch before scroll; flick 100/100; zero JS errors;
   reduced-motion).
5. `gates/qa_battery.py` **39/39** at BOTH 1440 and 390 AND `v4/qa_battery_v4.py`
   **7/7 + 7/7**.
6. **Desktop customer journey (hard ship-blocker):** at 1440×900: open link → PIN →
   grid loads 15 → scroll → ring plays → next 15 lands as a unit with zero movement
   → favorite → heart persists after reload → hover states render AND revert
   (cards/hearts/download) → keyboard walk (grid focus → lightbox ←→ Esc → focus
   visible) → download pill/zip fires.
7. Resize integrity: 1440→390→1440 mid-session — no stuck columns, no JS errors,
   no tile overlap (a resize re-layout may move tiles ONCE, deterministically; list
   it as a documented behavior, never mid-scroll).
8. Production swap + public route proven (relay-forced curl + r.jina.ai). Nothing
   pushed to any git remote.

**Vision gates:** (a) ring visible + elegant + on-brand at 1440 mid-scroll;
(b) batch landing NO perceptible jump (before/after frames); (c) wall rhythm vs
showcase-ref.png — vision PASS required, pixel-arbitrated on disagreement.

## §2 CANONICAL SCOPE + BOUNDING DECISIONS (override only by editing this prompt)

- **Design law:** desktop = 5 cols ≥1200 (tile ~278px), 3 cols ≥900, 3px gutters,
  native 2:3/3:2 mix, offset rhythm, no hero spans, 44px targets, AA contrast, JLP
  rose/cream tokens, `prefers-reduced-motion` render-all.
- **The ring:** V4.3 D2 visual unchanged (40px SVG, 270° rose arc, glow halo, fixed
  bottom-center, `role="status"`). Inline-at-seam was PROVEN invisible twice.
- **Batch contract unchanged:** BATCH=15, first paint exactly 15, background probe
  fetch (md tier / srcset-matched), ONE mutation per batch, unit fade, 8s watchdog,
  hoisted `done()` (cache-complete-probe race is REAL — §6).
- **Manifest contract:** 6-element entries `[full, alt, thumb, medium, w, h]` already
  shipped by V4.4-M; this run CONSUMES them (do not re-litigate; if V4.4-M did not
  run or the manifest is still 4-element, STOP and run V4.4-M first).
- **Column-count boundary:** 5→3 col transition at 1200/899 must be deterministic in
  BOTH bands — a tile crossing the breakpoint on resize may re-layout ONCE
  (documented), never during appends.
- **Out of scope:** real-client regeneration, pushing to any remote, favorites sync /
  accounts / selling, CSP/header work, homepage/nav changes, re-touching the mobile
  band's design (regression-guard it only).

## §3 VERIFIED ENVIRONMENT (re-verify git/servers at start — do not re-derive)

- **Project root:** `/root/projects/sites/jlp-photo-delivery/` (no git repo;
  scope-guarded edits + backups under `v4/backups/`).
- **Production template:** `gallery_template.html` — post-V4.4-M (deterministic
  mobile masonry + 6-element manifest support). Token contract 15 tokens incl.
  `__PHOTOS_JSON__`, `__SRCSET_JSON__`, `__COVER__`, `__COVER_POS__`, `__PIN__`,
  `__ZIP__`, `__COUNT__` — NEVER break token substitution.
- **Canonical winner copy:** `v4/winner/gallery_template.html` (sync at every swap).
- **Generator:** `generate_gallery.py` — V4.4-M already emits 6-element
  `__PHOTOS_JSON__` (w/h at [4]/[5]). ⚠️ WIPES the entire output dir before the zip
  branch — full regen (with zip) is the ONLY safe invocation; `--no-zip` DELETES the
  existing zip. 100-photo regen ≈ 8–10 min → background `terminal` +
  `process_manage wait`, read the log's EXIT line; NEVER kill the wrapper PID;
  `ps aux | grep generate_galler[y]` before rebuilding (bracket the grep).
- **Deliveries:** `/root/projects/sites/jlp-deliveries/<slug>/` — `demo-100` (PIN
  2026) regen target; `ava-liam`, `ava-liam-v4-regen`, `jossalyn-grad` OFF-LIMITS.
- **Serving:** demo-100 static origin = `http.server 127.0.0.1:8474` → public funnel
  path `/v4-demos`. Draft harnesses: `v4/render_draft_harness.py` (env
  `V43_FIXTURE=<deliveries dir>`) on loopback 8486–8493. ⚠️ Kernel-reaped servers —
  Popen `start_new_session=True`; verify served bytes = your draft (marker comment)
  before trusting probe verdicts (stale-serve trap).
- **Gates:** `/usr/local/lib/hermes-agent/venv/bin/python3 gates/qa_battery.py
  --kind gallery --url http://127.0.0.1:8474/ --out <json> --label <x> --pin 2026
  --couple-token "Ava & Liam" --date "September 12, 2026" --count 100`.
  `v4/qa_battery_v4.py` (7/7 per perspective). Real expected values EVERY run.
- **Probes:** `v4/v43_probes.py` extended by V4.4-M with **P8 no-movement / P9
  reserved-slot** (verify they exist and carry a `--viewport` / width parameter —
  if hardcoded mobile, extend for 1440/1024; do not rewrite). MutationObserver-
  level append counting is contract truth (polling lies).
- **Showcase reference:** `/root/.hermes/cache/scratch/showcase-ref.png` + the
  measured grammar: 5×~280px cols, 3px gutters, left-3 row-aligned / right-2 offset,
  2:3/3:2 duo, no spans. If the scratch file was pruned (24h scratch cleanup),
  measure from the live demo screenshots under `v4/screenshots/` instead.
- **Vision:** glm-5.3-flash direct to `https://ollama.com/v1/chat/completions`,
  `OLLAMA_API_KEY` from `/root/.hermes/.env`. FLAKY: retry once, longer timeout.
  ONE image, downscaled ≤700px, short prompt, max_tokens ≥1200. Playwright only in
  the Hermes venv python.
- **Funnel law (9/20 hazard class):** `/v4-demos` is an ADD-ONLY funnel path on 443.
  NEVER run broad `tailscale serve ... off` / `--set-path=/ off` — they silently
  kill ALL routes; local curls can't detect it (VPS hairpins its own ts.net name).
  Public proofs ONLY via (a) `curl --resolve <host>:443:<relay-IP>
  https://<host>/v4-demos/` (relay IP from `dig +short <host> @8.8.8.8`), (b)
  r.jina.ai. Funnel changes this run: NONE.
- **Model pin (Matt):** every agent runs `glm-5.3-flash` via ollama-cloud. Ollama-
  only. `delegation.max_concurrent_children` ≤ 6.
- **Git:** author `Caddy <caddyaibot@gmail.com>` per-commit `-c` overrides. **No
  push to any remote without Matt's explicit approval.**
- **Run ledger:** read `v4/v44-STATE.md` first — it carries V4.4-M's results, the
  winning mechanism, and open issues. This run builds on them; do not re-litigate
  mobile decisions.

## §4 SOURCE ARTIFACTS (all paths verified on disk 2026-09-25)

| Artifact | Path | State / role |
|---|---|---|
| Production template | `/root/projects/sites/jlp-photo-delivery/gallery_template.html` | post-V4.4-M; base every draft copies |
| Winner copy | `v4/winner/gallery_template.html` | canonical; sync target |
| V4.4-M report | `v4/v44m-REPORT.md` | winning mobile mechanism + handoff |
| Run ledger | `v4/v44-STATE.md` | V4.4-M results + open issues; append this run |
| Generator | `generate_gallery.py` | 6-element manifest already shipped by V4.4-M |
| Live demo output | `/root/projects/sites/jlp-deliveries/demo-100/index.html` | regen target (via real generator) |
| Probes | `v4/v43_probes.py` | P1–P9 truth; extend for desktop viewports |
| Batteries | `gates/qa_battery.py`, `v4/qa_battery_v4.py` | 39 + 7/7×2 regression floor |
| Specs | `v4/SPEC-v4.3.md`, `v4/SPEC-v4.4M.md` | binding ring/batch/masonry law |
| Workflow history | `v4/winner/FIX_LOG.md` | V4.0.1→V4.4-M gotcha ledger |
| Harness | `v4/render_draft_harness.py` | `V43_FIXTURE` env; draft renders on loopback |
| Swap tool | `v4/v44m_swap.py` (or `v43_swap.py`) | validated pattern; adapt → `v44d_swap.py` |

## §5 THE 4-AGENT ROSTER (2.5h: 2 drafters + 1 breaker + 1 fixer; parent probes do
refutation duty. If gates finish early, the parent MAY dispatch one optional
fresh-eyes refuter — never at the cost of the close. Every child: goal+context
self-contained, JSON-safe; outputs are FILES; incremental-write discipline; final
chat response <60 lines. Subagent self-reports are NEVER trusted — parent verifies
every claim on disk/behavior.)

**STANDING RULE — VISUAL GATE ON EVERY UPDATE (desktop band):** any template
mutation is NOT done until probes + batteries re-run green on that exact state at
**1440×900** AND fresh desktop screenshots land under
`v4/screenshots/v44d/<subject>/`. Mobile 390 is a quick regression probe only
(P1–P8 must stay green — the V4.4-M guarantee must not regress). A desktop FAIL
fails the mutation outright; a mobile REGRESSION also fails it.

Parent-owned pre-work (NOT counted in the 4; ~25 min):
- **P-A. Pre-flight:** read `v4/v44m-REPORT.md` + run ledger; confirm production
  template carries the V4.4-M mechanism (marker comment); 8474 healthy; funnel
  `/v4-demos` 200 via relay-forced curl; stage backups (`v4/backups/v44m-<ts>/`).
- **P-B. Desktop probes:** extend P8/P9 with 1440/1024 viewport support; **validate
  discrimination**: run against the post-V4.4-M template at 1440 — if the V4.4-M
  mechanism already generalized cleanly, P8 may PASS; record which tiles/regions
  still move (that region list is this run's work order). Write
  `v4/SPEC-v4.4D.md` (desktop band contract + rhythm-fidelity gate).

**Wave 1 — build (agents 1–2, parallel, ~35 min).** Each drafter copies the
production template into `v4/v44d/draft-<stance>/gallery_template.html` and builds a
COMPLETE desktop-band candidate, designed and self-checked at 1440×900 FIRST, briefed
with §2, §4, `SPEC-v4.4D.md`, its stance, and the showcase grammar measurements:
- **Agent 1 — "generalized-masonry" stance (RECOMMENDED bet):** take V4.4-M's
  deterministic column-assignment mechanism and generalize it to 5 cols ≥1200 / 3
  cols ≥900 — shortest-column-first using known w/h; verify the offset rhythm
  (left-3 row-aligned / right-2 offset feel) survives; if the computed wall reads
  rigid vs the showcase, implement the measured offset pattern deterministically
  (e.g. orientation-aware column bias) rather than accepting a flatter wall.
- **Agent 2 — "hybrid-band" stance (contrast bet):** desktop keeps a rigid CSS grid
  with row-span math from w/h (rigid = trivially no-movement), trading some offset
  randomness for determinism — but must still pass the §1.3 grammar gate; if the
  rigid wall loses the showcase feel, restore rhythm via computed placement of the
  3:2 landscapes.
Drafter contract: demo-100 fixture data; 15-token contract intact; batch/ring/ARIA/
reduced-motion byte-preserved where untouched; mobile band untouched except where
the mechanism is shared (regression-guard only); `draft-README.md` with the
movement-guarantee mechanism + rhythm-preservation approach in ≤8 lines; run
NOTHING (gates parent-owned). No git ops, no regens, no funnel changes.

**Parent adjudication (~15 min):** gates + P8/P9 at 1440 + 1024 on both drafts;
showcase-grammar vision compare on the winner-candidates; verify-before-apply;
rulings R1..Rn; select winner (whole-draft win — port ONE named element from the
loser with rationale). If demo-100 needs a regen for any template-level token
change, kick it (backgrounded) now — it overlaps later phases; otherwise skip
(the V4.4-M regen already emitted 6-element manifests).

**Wave 2 — desktop breaker (agent 3, ~25 min).** Read-only adversarial pass at
1440×900 (primary) + 1024 + 1920: mixed portrait/landscape batches, fast flicks,
pinned-bottom chains, favorites filter on/off mid-scroll, reload mid-wall
(heart-sync), hover-storm during landing (rapid hover over appended tiles), keyboard
walk during landing, lightbox open during landing, resize 1440→1024→1440 mid-session,
8s-watchdog abuse. Plus mobile regression spot-checks at 390 (P1–P8). Findings
severity-tagged to `v4/critiques/v44d-breaker.md`. Any tile movement at 1440/1024
during appends = BLOCKER; any mobile regression = BLOCKER.

**Wave 3 — fixer (agent 4, ~30 min).** Applies parent rulings + breaker findings in
place; `node --check` on extracted JS after EVERY edit; logs applied/rejected + IDs
in an HTML comment; runs P1–P9 smoke at 1440 + 390 regression on its harness port;
writes the verdict JSON. One bounded second pass if parent refutation finds
survivors.

**Parent close (~25 min):** adapt `v44d_swap.py` (token-set diff pre-swap, backups);
swap production + winner copy; regen demo-100 only if template tokens changed
(otherwise verify current output matches); relay-forced curl + r.jina.ai public
proofs; **run the §1.6 desktop customer journey + a mobile spot-check on the PUBLIC
route** before reporting; update `FIX_LOG.md` (V4.4-D entry) + run ledger; report.

## §6 GOTCHA LEDGER (confirmed in prior rounds — handle, don't rediscover)

1. **Hoisting race:** callbacks (settle/done) defined AFTER an async-trigger loop
   must be hoisted `function` declarations — cache-complete probes fire
   synchronously and run `settle()` before `var done=` assigns (shipped-bug class,
   2026-09-25).
2. **Leftover blocks after rewrites:** removing a line its consumer still references
   (`if(first)`) crashes on first scroll. After every surgical edit, grep the
   function for orphaned identifiers.
3. **MutationObserver truth:** tile-count polling misreads chained top-ups; only
   DOM-mutation logging is contract truth.
4. **Stale harness trap:** verify served bytes = your draft (marker comment) before
   trusting any probe verdict on a reused port.
5. **Vision flake protocol:** retry with longer timeout; single downscaled image;
   pixels win when vision and pixels disagree (gutter 1px delta, ring invisibility —
   both past vision misreads).
6. **execute_code kernel:** no playwright/PIL in the sandbox interpreter — spawn the
   venv python via subprocess; long jobs backgrounded; servers `start_new_session=True`.
7. **Battery hygiene:** real `--pin/--couple-token/--date/--count` every run; check
   the verdict's URL field is the serve you intended.
8. **Regen wipe law:** full regen only; backgrounded; EXIT line read; orphan check;
   half-built dirs deleted before retry.
9. **Multicol muscle memory:** the 5-col band has been CSS-multicol since v4.1 — a
   computed mechanism changes WHICH column a tile lands in. Pixel-compare the
   winning wall against showcase-ref.png before accepting (the offset rhythm is the
   aesthetic Matt approved; determinism must not flatten it).

## §7 BUDGET — 2.5 HOURS WALL CLOCK (start at session start; hard stop at 2:30)

| Clock | Phase | Exit artifact |
|---|---|---|
| 0:00–0:25 | P-A pre-flight + P-B desktop probes + discrimination check | region list of remaining desktop movement; SPEC-v4.4D written |
| 0:25–1:00 | Wave 1 (agents 1–2, parallel) | 2 desktop drafts |
| 1:00–1:15 | Parent adjudication | R1..Rn + winner |
| 1:15–1:40 | Wave 2 (agent 3, desktop breaker + mobile spot-check) | findings file |
| 1:40–2:10 | Wave 3 (agent 4, fixer + bounded second pass) | fixed winner + smoke verdict |
| 2:10–2:30 | Parent close: swap + public proofs + journey on public bytes | shipped, FIX_LOG V4.4-D, report |

Checkpoint discipline: append every phase to `v4/v44-STATE.md` (run V4.4-D) so an
interruption resumes from disk. If budget forces a choice between polish and
verification, verification wins. Hard stop at 2:30: ship the best verified state +
explicit gaps list.

## §7b BOUNDARIES (non-negotiable)

1. Nothing pushes to any git remote; author Caddy per-commit.
2. Real client galleries never regenerated or touched. Regen target: demo-100 only,
   and only if template tokens change.
3. Funnel/serve config: NO route changes. No broad `off` commands, ever.
4. No AI-generated photos; EXIF-strip enforced by generator, re-verified by gates.
5. No client PII anywhere public; demo stays fictional (Ava & Liam, PIN 2026).
6. No unrelated refactors, no dead-CSS pruning, no Phase-4 scope.
7. Do NOT redesign the ≤899px band — V4.4-M shipped it; regression-guard only.

## §8 FINAL REPORT (`v4/v44d-REPORT.md` + chat summary)

Must contain: winning stance and why; P8/P9 results at 1440 AND 1024 (ZERO moved
tiles — quote the numbers); showcase-grammar vision compare verdict (rhythm
preserved?); the desktop customer-journey verdict (every step, public route); mobile
regression spot-check status; rulings applied/rejected; probe/battery/vision verdict
JSONs; before/after seam screenshots at 1440; demo-100 regen evidence (if run);
public-route relay-forced curl + external-fetcher proof; swap backup paths; remaining
gaps (resize re-layout behavior, honest list); handoff: **"Both bands shipped —
V4.4 complete: mobile (V4.4-M) + desktop (V4.4-D). Demo live at /v4-demos, PIN 2026."**