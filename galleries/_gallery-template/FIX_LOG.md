# V4 WINNER FIX LOG — D2 `jlp-editorial` convergence (fixer pass, 2026-09-24)

Source: `v4/drafts/jlp-editorial/gallery_template.html` → `v4/winner/gallery_template.html`.
Rulings: `v4/RULINGS.md` (binding). Each edit verified against current template code before apply.

## R1 — Mobile grid = 2 columns (capture fidelity, parent-spec error) — APPLIED
- `@media(max-width:519px){.grid{columns:1}}` → `columns:2` (line 113), extending the
  `columns:2` rule from the ≤899px breakpoint down to the 320px floor, per m-walk01 ground truth.
- Companion `sizes` attr `(max-width:519px) 98vw` → `48vw` (matches 2-col tile width).
- Evidence: smoke `R1_cols_390_320` = computed columnCount 2 at 390 **and** 320.

## R2 — Rendered-text floor stays 13px (≥11px carve-out withdrawn) — NO-OP (already compliant)
- D2 chrome is 13px minimum (`.cover-brand/.cover-meta/.cover-cta/.s/.count/pin-msg/hint/
  footer .brand/.ref` all `font-size:13px`); no 11–12px label exists to fix.
- Evidence: `verdict_jlp-editorial_full.json` → `font_size_floor` PASS both perspectives
  ("0 text nodes below 13px"); smoke re-run `console_errors: none`.

## R3 — Pill must never occlude footer text at max scroll; keep 110px-class clearance — VERIFIED, NO CSS CHANGE
- Read current code first: `.gallery-main` bottom padding is 24px (D2 uses tighter main
  padding than v3's 110px), footer bottom padding `calc(120px + safe-area)` — v3's
  110px main-bottom clearance intent is carried by the footer 120px + pill hidden-at-footer
  scroll-reveal, unchanged by R1/R4/R5 (no spacing edits touched main/footer).
- Evidence: gates `pill_footer_clearance` PASS (parent run, "max-scroll: clear"); fixer
  smoke re-verified after all edits: `R3_pill_footer_390` = clear, `R3_pill_footer_1440` = clear.

## R4 — Soften the hard-edged translucent band across the mid-hero — APPLIED
- Base scrim: added smooth fade stops `…50% 42%, rgba(26,13,17,.30) 78%, 0 100%` — the
  old 42%→0 fall created the visible hard band edge at its top boundary; now tapers to zero.
- Top scrim (contributed the band's other hard edge): `.48 → .24 @60% → 0` instead of
  a hard `.48 → 0` single-fall.
- Re-ran scrim check on rendered pixels: `R4_scrim_contrast_h1` p2=38 p50=91 p98=255
  → 6.79:1 ≥ 4.5 AA (parent re-run of the full pixel check still required per contract).

## R5 — Lightbox back arrow: bare thin gray arrow, no ring — APPLIED
- Split the shared hover rule: `.lb-back` no longer receives the cream circular
  hover/focus wash that read as a focus-ring leak; it keeps 44×44px hit area, gray
  `#757575` arrow, color-only hover. `.lb-ic` cluster unchanged.
- Evidence: smoke `R5_back_bare_arrow` = computed bg `rgba(0,0,0,0)` (no ring), 44×44px.

## R6 — Port D3 heart chips (CONDITIONAL) — CONDITION FALSE, NOT PORTED (rejected with rationale)
- Verified in code: heart visibility rule `.ph .heart{opacity:0}` lives **inside**
  `@media (hover:hover) and (pointer:fine)` — a control that never matches on touch
  devices, so hearts render `opacity:1` (always visible) at 390/320 by construction.
  D2 already satisfies "reachable-without-hover"; porting D3's chips would duplicate
  controls. Rejected: condition not met.
- Evidence: smoke `R6_heart_visible_390` and `R6_heart_visible_320` = opacity 1, 44×44px;
  gates `favorites_persist_reload` PASS both perspectives (parent run).

## Smoke (fixer-owned, playwright): overflow PASS at 1440/768/390/320 · 2-col at 390/320 ·
## pill clearance clear at 390/1440 · scrim 6.79:1 · bare back arrow 44px · hearts visible
## 44px at 390/320 · zero console errors. Token set preserved: 15/15 (== v3 set).

---

# FIXER PASS 2 (2026-09-24, R7–R11 — convergence cap; smoke-verified before report)

Each edit verified against current template code before apply. Smoke harness:
parent's `render_draft_harness.py` fixture (ava-liam, PIN 2026, 10 photos) +
playwright chromium; fixer-owned checks only — full QA batteries remain
parent-owned per the RULINGS.md verification contract.

## R7 (BLOCKER) — PIN input accepts 4-8 digits — APPLIED
- Markup: `maxlength="4"` → `maxlength="8"`; aria-label "4-digit download PIN"
  → "Download PIN (4 to 8 digits)".
- Handler: digit-only filter kept; `.slice(0,4)` → `.slice(0,8)`; autosubmit
  `length===4` → `length===PIN.length` (Enter still submits via #pinSubmit).
- Evidence: rendered `maxlength=8`; value probe "12345678" fully retained
  (slice(0,8) capacity); typed digits auto-submit at PIN.length — 4 wrong
  digits → err message, modal stays open, field clears; correct 2026 →
  "Unlocked!" ok path, modal closes, pending action drains.

## R8 (MAJOR) — favorites filter: empty state + freshness — APPLIED
- New `#favEmpty` inline message ("No favorites yet — tap the heart on any
  photo.") after `#theGrid`; `.fav-empty` style 14px (≥13px floor), taupe,
  centered. Filter logic extracted to `applyFilter()`; message hidden flag =
  filterFavs && visible==0. Heart-toggle handler calls `applyFilter()` while
  filtered — visible set re-evaluates immediately, no stale empty grid.
- Evidence: filter ON, 0 favs → 0 tiles + message shown; heart ON while
  filtered → 1 tile instantly, message hides; heart OFF → empty state returns.

## R9 (MAJOR) — lightbox focus trap + scroll lock + restore — APPLIED
- `openLb` sets `body.style.overflow='hidden'`; `closeLb` restores it (lastFocus
  restore already existed, kept). Tab/Shift+Tab now cycle focus inside
  #lightbox. Trap selector initially `button, [href], input, …` — smoke caught
  `[href]` matching SVG `<use>` children inside buttons, letting focus escape
  6× in 30 Tabs; fixed to `button:not([disabled]), a[href],
  input:not([type="hidden"]), select, textarea, [tabindex]:not([tabindex="-1"])`.
- Evidence (after fix): 30×Tab + 30×Shift+Tab → 0 escapes outside #lightbox;
  body scroll locked while open, unlocked after close; focus restored to the
  originating tile img (data-idx 2); initial focus #lbClose.

## R10 (MINOR batch) — ALL FOUR APPLIED
- (a) 320px chevrons: `#lbPrev/#lbNext` inset 8px → 10px (photo edge starts at
  the 10px stage padding); ≤560px adds a white rail — rgba(255,255,255,.92)
  bg + matching 4px ring shadow, taupe glyph. Evidence @320: rail bg white .92,
  glyph fully on rail, control 48×48 (≥44).
- (b) `.cover h1` gains `overflow-wrap:anywhere;max-width:100%` — single-word
  long names wrap inside the frame. Evidence @320: synthetic 34-char name
  renders 4 lines, no horizontal bleed, no doc overflow, inside the 10px
  frame guard.
- (c) Lightbox navigation (Prev/Next buttons, ArrowLeft/Right, touch half-tap)
  now walks `visiblePhotos()` — the filtered set — not all PHOTOS; hidden
  photos are skipped, zero visible → no-op. Evidence: filter with only photo 0
  favorited, open photo 0, Next and Prev → caption unchanged.
- (d) `#favFilter` aria-label tracks state: "Showing favorites" when pressed,
  "Show only favorites" when not — agrees with the visible span. Evidence:
  rendered attribute matches in both states.

## R11 (NIT) — dead data-intent / fireDownload name param — APPLIED (remove-branch)
- `pinModal.setAttribute('data-intent',…)` removed (`afterMsg` param voided;
  its single call site passes 'Download' so the signature stays honest).
- `fireDownload(href,name)` → `fireDownload(href)` (name unused — a.download
  always derived from href); `gated(fn,label)` → `gated(fn)`; 'zip'/'photo'
  literals dropped from both call sites.

## Smoke (fixer-owned, playwright, pass 2): SMOKE PASS —
## overflow 0 at 1440/768/390/320 · 2-col at 390/320 · R7 8-digit capacity +
## autosubmit-at-PIN.length + wrong→err + correct→unlock · R8 empty state +
## instant re-eval · R9 0/60 Tab escapes + scroll lock + restore · R10c skip
## filtered · R10d labels · R10a rail + R10b wrap @320 · zero console errors ·
## token set 15/15. Parent full verification pending per contract.

---

# V4.1 GRID REVISION — "showcase look" (2026-09-24, Matt's client-directed feedback)

Source: `v4/SPEC-v4.1.md` (showcase recipe, pixel-verified). Scope: GRID ONLY —
cover, lightbox, PIN, favorites, pill, BACK TO TOP untouched. Each edit verified
against current template code before apply. Smoke harness: parent's
`render_draft_harness.py` (ava-liam, PIN 2026, 10 photos) + playwright chromium.

## G1 — Desktop columns 4 → 5 at ≥1200px — APPLIED
- `.grid{columns:4}` → `columns:5` (base rule); `@media(max-width:1199px)` stays
  `columns:3`, ≤899px stays `columns:2`, ≤519px stays `columns:2` (R1 mobile floor).
- `sizes` attr updated to match: `24vw` → `(max-width:1199px) 32vw, 20vw`
  (desktop tile ≈20vw at 5 cols; no srcset over-downloading at 3-col).
- NO spanning tiles added — variety stays orientation mixing only, per spec step 4.
- Evidence: smoke computed columnCount 5 @1440 (tile 278×417 — the showcase's
  pixel-measured 278-280px column width exactly), 3 @1024, 2 @768/390/320;
  native ratios preserved (7-8 tiles ≈1.4-1.6 h/w, 2 tiles 0.67/0.78).

## G2 — Gutters 8px → 4px hairline, both axes — APPLIED
- `--gutter:8px` → `4px` (drives `column-gap` AND `.ph` margin-bottom — one knob,
  both axes). ≤899px override `--gutter:5px` → `4px` (was the only off-hairline value).
- Outer page padding: `.gallery-main` 18px → 16px (desktop), ≤899px 5px → 4px —
  edges read as a frame, matching the ~1% hairline proportion.
- Evidence: computed columnGap 4px at 1440/1024/768/390/320; measured ROW
  gutters (consecutive tile bottoms, same column) = 4px at 1440/390/320.

## G3 — MOBILE CLAUSE (Matt addition, binding): same idea on mobile — APPLIED
- 2 columns kept at 390 AND 320 (Pixieset capture ground truth, R1 ruling
  unchanged); gutters switched to the same 4px hairline both axes + 4px outer
  margins so the mobile floor reads as one contiguous photo wall.
- Native 2:3/3:2 mix, NO spans (`.grid` has no span mechanism — CSS columns).
- Hearts untouched: `.heart` stays 44×44px, always visible on touch (R6 ruling).
- Evidence: computed columnCount=2 AND columnGap=4px at BOTH 390 and 320;
  heart boxes 44×44 at 390/320; doc scrollWidth == innerWidth (no overflow) at
  390 AND 320; favorites empty-state still works at 390 (filter ON, 0 favs →
  0 tiles + #favEmpty shown).

## v4.1 Smoke (fixer-owned, playwright): SMOKE PASS —
## 5-col @1440 (tile 278px ≈ showcase 278-280) · 3-col @1024 · 2-col @768/390/320 ·
## columnGap 4px all widths · row-gutters 4px @1440/390/320 · overflow 0 at
## 1440/768/390/320 · hearts 44px @390/320 · fav-empty-state works · data-loaded
## 10/10 every viewport · zero console errors · token set 15/15 (== v3 set).
## Cover/lightbox/PIN/favorites/pill/BACK TO TOP code paths untouched.
## Parent: qa_battery_v4.py `v4_grid_gutters` must be RE-TUNED before re-run
## (gap >= 3 && <= 10; span >= 0.95vw) per SPEC-v4.1 verification contract.

## V4.0.1 — PREVIEW SHARPNESS FIX (2026-09-24 11:05, parent-applied)
**Symptom:** grid previews fuzzy on Matt's iPhone (3x DPR).
**Root cause chain (all three links had to be present):**
1. The ava-liam FIXTURE predates the 9/21 sharpness fix: its thumbs were
   400px-max-edge (267px wide) — generate_gallery.py's THUMB_EDGE=800 law
   (9/21) was never back-ported to the fixture bytes.
2. The harness emitted SRCSET={} (fixture index.html had no SRCSET map), so
   the template's srcset logic fell back to NOTHING — tiles rendered the
   267px thumb stretched to 280px CSS / 840 device px at 3x DPR = 32% of
   required resolution.
3. (Contributing) v4.1's hairline-gutter showcase grid makes tiles LARGER on
   screen, raising the resolution bar further.
**Fix (both layers):**
- Regenerated all 10 fixture thumbs to THUMB_EDGE=800 (now 533x800) using the
  generator's own make_preview; generated the missing photos-md/ tier (1650px).
- render_draft_harness.py now BUILDS the 3-tier srcset map (thumbs 800w,
  photos-md 1650w, photos <native>w) when the fixture lacks one — matching
  generate_gallery.py lines 242-250 — so the browser density-picks correctly.
**Verified:** SRCSET map renders with 10 entries; browser fetches across all
three tiers at mobile 3x DPR; vision sharpness on the mobile grid = 7.5/10
with lace/petals/brickwork/ring detail resolvable (soft flags = backlit
photos, not upscaling). Public /v4-demos route serves the new 533x800 thumbs.
**Standing law:** NEVER regenerate a gallery from pre-9/21 fixture bytes —
thumbs ship at 800px max edge, 3-tier srcset always present.


## V4.1.1 — GUTTER HAIRLINE MATCH (2026-09-24 11:20, parent-applied)
Vision compare vs the showcase said NEEDS-FIXES; geometry ground-truth showed
the claimed "2-3x wider gutters" was an over-read (ours 4px vs showcase 3px,
pixel-measured both). Real deltas were content-volume (10-photo fixture vs a
full session) + the standing download pill (R3 feature, by design). Applied
the free 1px match: --gutter 4px -> 3px. Re-verified: 39/39 + 6/6 + 6/6.
NOTE for Matt: the "ragged bottom" and pill-overlap in the mid-grid screenshot
are (a) end-of-10-photos and (b) the download pill standing feature - both
disappear as artifacts once real sessions (100+ photos) fill the wall.


## V4.2 — PROGRESSIVE LOADING (Pixieset-style) (2026-09-24 ~14:30, parent-applied)
Matt directive: "Pixieset will limit to only 15 or so photos before adding a
loading animation at the bottom of the screen as you load. This makes it feel
much smoother." (Approved: "You are approved for however much time you need...
focus on mobile users.")
**Implementation (gallery_template.html, in place + ported):**
- Windowed render: BATCH=15 first paint; IntersectionObserver sentinel
  (rootMargin 250%) appends the next batch ~2.5 viewports early; batches of
  15 until the manifest is exhausted.
- Loading indicator: thin 2px rose "breathing line" (scaleX pulse, 1.4s),
  FIXED at the bottom screen edge (bottom: 88px + safe-area, above the
  dl-bar) - the Pixieset position; never a spinner; pointer-events:none.
  First draft had it at the DOM seam (4+ viewports below fold on mobile) -
  moved to fixed after vision flagged invisibility.
- prefers-reduced-motion: render-all immediately, no pulse, no appends.
- No IntersectionObserver (ancient): render-all fallback (correctness first).
- Favorites filter suppresses appends while active; restores on unfilter
  (verified: filtered->hidden, unfiltered->visible again when batches remain).
- Lightbox + hearts unaffected: they operate on the full PHOTOS manifest
  (verified: ArrowRight x25 walks tiles far beyond rendered range).
**Stress test:** 120-photo gallery generated through the REAL pipeline
(synthesized from the 10 ava-liam photos; stress-120 scratch slug). Mobile
390x844@3x: 30 tiles at load (2 batches - sentinel within reach at load, by
design: pre-fetch), 30->60->90->120 across the scroll, all landed by scrollY
9800 of 16825; desktop identical. Zero JS errors both perspectives.
**Verification:** 39/39 functional + 7/7 + 7/7 look (incl. new v4_progressive
check) on BOTH the 10-photo demo AND stress-120; vision seam PASS (uniform
gutters, no layout jump) + indicator PASS (subtle, above dl-bar).
**Note:** initial render = 30 tiles on small galleries because the sentinel
starts within the 250% reach - intended pre-fetch, matches Pixieset feel.


## V4.2.1 — FULL-SCALE PUBLIC DEMO (2026-09-24 ~15:10, parent-applied)
Matt: "Make the demo like 100 photos please. You can use some of Jossalyn's
grad session if you need to."
- Built demo-100: 100 photos (10 ava-liam wedding + 90 jossalyn-grad,
  interleaved 1:9 so the grid opens with variety), generated through the REAL
  pipeline (thumbs 800-law, 3-tier srcset, zip 71.4MB, PIN 2026).
- Public /v4-demos now serves demo-100 via static http.server on 127.0.0.1:8474
  (funnel config untouched - the route still targets :8474; only what :8474
  serves changed). The 10-photo harness demo is retired from the route.
- Verified: public manifest=100, windowed loading live (mobile probe 30 ->
  100/100, indicator hides at end, zero JS errors); 39/39 + 7/7 + 7/7;
  vision grid flags adjudicated non-defects (pill overlap = R3 by-design
  scroll-reveal; "white sliver" = the 4px margin law, pixel-measured 100%
  clean edge).
- Superseded: stress-120 scratch gallery (was tailnet-only :8479) - server
  stopped; demo-100 is the canonical showpiece.


## V4.2.2 — PINNED-AT-BOTTOM DEAD-END FIX (2026-09-24 ~15:40, parent-applied)
Matt (on his phone): "there are only 30 photos in the gallery."
**Reproduced:** fast flicks to the absolute bottom with throttled network
stalled the wall at 75/100 (Matt saw 30 on a harder case). Root cause:
IntersectionObserver only fires on re-entry TRANSITIONS; each append pushes
the sentinel beyond the 250% reach, and a user pinned at the page bottom
cannot scroll further, so the sentinel never re-enters and no batch ever
fires again - the wall dead-ends.
**Fix (two parts, both in template + demo-100 output):**
1. Top-up chain in appendBatch(topUp): after each scroll-triggered append,
   if the user is pinned at the absolute bottom (pinnedAtBottom()), keep
   appending (300ms spacing). Only on scroll-triggered calls - the initial
   fill never chains (an earlier reach-based top-up cascaded all 100 at
   load; caught in test and replaced by the pinned test).
2. Debounced scroll-listener backstop (120ms): IO cannot fire when the user
   is ALREADY at the bottom (no re-entry transition at all), so a passive
   scroll hook starts the top-up chain. Insertion-order bug (backstop landed
   inside the if/else, orphaning the else) caught by node --check and fixed.
**Verified (throttled 0.4s/img, mobile 390x844@3x):** initial 30 (windowing
intact, NOT cascaded); fast-flick-to-bottom now reaches 100/100 (was 75);
pinned-at-bottom fills to 100; indicator hides at end; normal scroll cadence
30->45->75->90->100; desktop flick test 100/100; zero JS errors everywhere;
39/39 + 7/7 + 7/7 batteries green. Public /v4-demos serves the fix now.


## V4.3 — PROGRESSIVE LOADING v2 (circle ring + background prefetch) (2026-09-24 evening)
Matt directive: "I want 15 loaded at a time. When you try loading the other ones,
I want it loaded in the background while a loading animation plays. I want it to
be a visually appealing circle loading animation. Use vision." (8h budget, up to
20 agents, adversarial convergence approved.)
**Workflow:** 3 stance drafts (D1 pixieset-ring / D2 ring-and-shimmer / D3
mobile-first) -> parent probes+batteries+vision on each -> D2 winner ->
fresh-eyes refuter -> (pending) fixer -> swap.
**Contract changes vs v4.2:**
- Initial render EXACTLY 15 (was 30 double-batch)
- Background pre-fetch: after each append, next batch's THUMB-tier images
  (PHOTOS[i][2]) pre-fetched via new Image() - never full-res (metered-safe)
- Circle ring loader replaces breathing line: rose #c4758a arc on cream track
- Staggered 60ms tile fade when a batch lands
**Evidence (parent-verified):** probes P1-P7 7/7 via MutationObserver append
counting (polling jumps were ambiguous); 39/39; 14/14; ring vision PASS
(elegance 8, brand 9, size 8); layout-shift vision PASS mobile+desktop;
dry-run swap render token-clean + all gates green before production swap.
**Refuter (fresh eyes, read-only): FIX-FIRST — 1 BLOCKER + 5 MAJOR + 3 MINOR.**
Parent behaviorally confirmed the BLOCKER (persisted favorites render outline on
appended tiles; first tap silently deletes) — AND traced it into production v4.2.2
(appendBatch never re-synced hearts). Also confirmed: IO reach 250% > per-batch
growth (desktop appends only via pinned backstop), prefetch on wrong tier for 3x
phones (thumb vs rendered md), filter-bypass in IO/backstop.
**Fixer pass (deleg_9c137c2b) applied 7 fixes + 1 choke-point extension
(showRing no-ops when filterFavs):** heart state seeded from favs in tileHTML +
drawHearts() after append; REACH 250%->120%; prefetch md tier p[3]; filterFavs
guards on IO + backstop; sr-only live-region text; .ph-error broken-thumb
treatment; escaped alt/aria interpolation.
**Parent re-verification (all independent):** token 15/15 + node --check;
BLOCKER regression probe PASS (persisted heart renders FILLED, toggles
correctly); probes 7/7 (appends [15,15,15,15,15,10]); 39/39; 14/14; ring
visuals untouched (vision PASS pre-fix, CSS byte-identical); production swap
token-clean; PUBLIC route end-to-end: initial=15, heart20=true, flick 100/100,
appends [15,15,15,15,15,10], zero JS errors; 39/39 + 14/14 on final origin.
**Deferred (need Matt/generator change):** aspect-ratio placeholders (manifest
has no w/h — generator contract change), CSS-multicol tile shuffle on append
(v4.1 architecture; visible only as tiles jumping columns at seams).


## V4.3.1 — BATCH-UNIT LOADING (Matt's epileptic-gallery fix) (2026-09-25 ~09:30)
Matt: "as you scroll down, random images will begin to load and will add into
the gallery... I want 15 to load, then a loading screen (taking as much time as
it needs), then the next 15 load and are already all in their dedicated spots...
Adding photos as it moves completely shifts the gallery around and makes it feel
almost epileptic."
**Root cause:** appendBatch inserted tiles into the DOM immediately; each img
then decoded lazily at its own pace (random pop-ins) while CSS-multicol
rebalanced columns — plus the 60ms per-tile stagger read as sequential pop-ins.
**Fix (batch-unit loading):**
- appendBatch now builds all 15 tiles OFF-DOM and background-fetches every
  image via srcset-matched probe Images; only when ALL 15 are loaded/errored
  does a SINGLE mutation append the batch — tiles appear complete, in their
  final spots, in one paint, then fade in as a unit (rAF x2, no stagger).
- Ring plays for as long as the fetch takes (watchdog 8s: never wedges).
- prefetchNext (md tier) fires from settle() after the batch lands.
- BUGS CAUGHT IN SELF-TEST: (a) leftover decode-gated if(first) block crashed
  ('first is not defined') — removed, prefetchNext moved into settle; (b) settle()
  could run synchronously from cache-complete probes BEFORE `var done=` executed
  ('done is not a function') — done converted to a hoisted function declaration.
- Ring placement: inline-at-seam was invisible during real scrolling (caught
  twice now); ring is FIXED at bottom-center (v4.2.2 position, above the
  download pill) while a batch fetches — the visible 'loading screen'.
**Verified:** progression 15->30->45->60->75->90->100 in strict 15-batch
mutations; ring caught in-viewport mid-scroll; vision loading-screen PASS
(rose spinner visible, elegant, above the download pill); 39/39 + 7/7 + 7/7;
zero JS errors; applied to production template + winner copy + demo-100 output.


## V4.4-M — DETERMINISTIC MASONRY, ZERO MOVEMENT (2026-09-25 ~13:05)
Matt's bar: "tiles never move once rendered; every appended tile lands in its
dedicated slot." Mobile-first run (V4.4-M) of the V4.4 split.
**Root cause of the epileptic wall:** CSS-multicol rebalances on every append
(measured: 158 tile moves per 100-photo walk at 390px).
**Fix (winner: deterministic-masonry, 2-draft adversarial + breaker + fixer):**
- place() assigns each tile shortest-column-first from manifest w/h (6-element
  entries) and freezes inline left/top/width inside position:relative #theGrid;
  appends place NEW figs only — tiles 1..15N structurally unrevisable.
- P8 probe (no-movement) + P9 (reserved slots) added to v4/v44m_probes.py;
  probes discriminate (baseline P8 FAILS with 158 moves).
- Generator: __PHOTOS_JSON__ now 6 elements [full, alt, thumb, medium, w, h]
  (backward compatible; template probes 4-element entries).
- Ruling fixes: R1 place() consults manifestDims before 2/3 fallback (watchdog
  phantom slot); R2 #lbFav wired (spec violation since v4.1, breaker-caught);
  R3 no appended tile can stay a permanent invisible hole; R4 ph-error clamped
  to slot; R5 lightbox-defers-appends documented.
- Battery probe fix: v4_grid_gutters measures rendered gaps (architecture-
  agnostic contract check), not CSS column-gap.
**Verified (parent, public route):** P8=0/P9=0 at 390+320 (baseline 158);
appends [15x6,10]; flick 100; 39/39; 7/7+7/7; mobile customer journey green
(PIN->15->ring->unit landing->favorites->reload FILLED->filter->pill);
B1 repro: 12s stall -> landscape tile lands at real 126.33px slot (was 284px
phantom); M1 repro: lbFav toggles + persists + dynamic label; public 200 via
relay + r.jina.ai. Backups: v4/backups/v44m-run1/.
## V4.4-M.2 — AVIF/WebP previews (2026-09-25, Matt: "push that file size fixes")
- Generator: 4-worker AVIF+WebP pass for thumbs+md tiers (ffmpeg libaom-av1 qp 68 /
  Pillow WEBP q80/82); idempotent skip when variants exist. Zip untouched (full-res
  EXIF-stripped JPEG — download path identical).
- Manifest: 10-element entries ([full,alt,thumb,md,w,h, thumb_avif,thumb_webp,md_avif,md_webp]);
  6-element and 4-element still valid (template guards p.length>=6 / >=10).
- Template: tileHTML builds <picture> AVIF>WebP>JPEG (sizes preserved); new tokens
  __SRCSET_AVIF_JSON__/__SRCSET_WEBP_JSON__ (17-token contract for new regens).
- Probe+prefetch AVIF-aware: probe/prefetch warm p[8] (md AVIF) on 10-element
  manifests — measured over the wire: 31/31 AVIF, 0 JPEG fetched.
- Measured: thumbs -66%, md -69%, 31-tile walk 10,660 KB JPEG -> 3,129 KB AVIF (-71%).
- Gates: v44m probes ALL PASS 390+320 (P8=0, appends exact), battery 7/7+7/7,
  zero JS errors. Demo-100 rebuilt; public route serving new build.
- Gotchas hit: index patch anchored on 'var SRCSET=' prefix clobbered the srcset
  var (caught live: 0 pictures rendered); template var-block edit lost mid-sequence
  (execute_code string surgery) — rule: multi-edit template work goes through patch().
## V4.4-M.3 — mobile ring at gallery bottom (2026-09-25, Matt: "I want it added at
## the bottom of the gallery as its loading instead")
- Mobile band (<=899px): .load-more is IN-FLOW right after #theGrid (bottom of the
  gallery content); desktop keeps the fixed bottom-center band.
- Proximity gate: showRing() on mobile requires seamNear() (sentinel within 1.05
  viewports); scroll listener reveals it when a batch is in flight as the user
  approaches; 500ms poll hides it if an append pushes the seam off-screen again.
- Behavior truth (measured): with prefetch + 8s watchdog the wall normally outruns
  the scroll, so the ring correctly stays hidden until the user is actually AT a
  loading seam — exactly when it's wanted. Jump-to-bottom + stalled batch: ring
  shows in-flow at the seam. Desktop untouched (fixed, verified).
- Gates: v44m probes ALL PASS 390+320 (P8=0, appends exact, 0 JS errors).
## V4.4-M.4 — unified in-flow ring at ALL widths (2026-09-25, Matt: "same issue on
## desktop... I want it to be the same as the mobile version")
- .load-more base rule: position:relative (in-flow after #theGrid) at ALL widths;
  the fixed bottom-screen band is GONE. Margin 4px 0 12px at the seam.
- JS gates unified: showRing proximity gate, armRingPoll, and scroll-reveal no
  longer key off innerWidth — one behavior everywhere.
- Desktop verified: pos=relative, bottom=auto at 1440; mobile probes ALL PASS
  390+320 (P8=0, 0 JS errors); battery 7/7 desktop + 7/7 mobile.
- Note: production template had LOST the M.3 CSS override during M.2→M.3 sync
  (winner-copy cross-stream); M.4 unifies base CSS so there is no per-band
  divergence left to lose.
