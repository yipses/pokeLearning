# Progress Log — Poké Learning

How the project got from a basic spelling/math quiz to where it is now, and the decisions worth not re-litigating. `Overview.md` is the spec for what it does *today*; this file is the journey and the open threads.

---

## Phases 1–8 — From quiz to platform

- Started as a single-file app with two challenge types drawing on **40 Pokémon**. Grew to the full National Dex: **1,021 species** (Gen 1–9, minus Nidoran♀/♂, Farfetch'd and Mr. Mime, whose names don't fit the plain-letter spelling mechanic). Data pulled from PokéAPI, verified by hashing an existing file against a fresh download before trusting a bulk fetch.
- Added **Math Patterns** (4 related problems checked at once) and **Visual Math** (the same operations drawn as Pokémon icons rather than numerals).
- Reworked sessions: one total challenge count, every slot drawn at random from the active modes, never the same mode twice in a row. Per-mode config moved to a Settings screen, and everything persists to `localStorage`.
- Added **Battle mode** — pick a winner, watch a short fight. Upgraded from a coin flip to a stat- and type-weighted roll using real base stats and a full 18-type effectiveness chart.
- Added the **Play Streak**, the **grass encounter** mechanic, and the **Pokédex**. Catching is **generation-gated**: only the lowest generation not yet complete can appear, so the collection moves through the Dex in order. Spelling and Reading pools respect the same gate.
- Pulled the Pokopia item catalogue to **922 items** across 12 categories, after dropping 121 near-duplicate variant names.
- Cached all artwork locally, so nothing is fetched from a fan site at runtime.

## Phases 9–12 — Lesson Trails, and the curriculum

Ad-hoc difficulty settings were replaced by four independent progressive tracks. Design rationale lives in `LessonTrails.md`; the durable decisions:

- **Four tracks** — Add/Subtract (8 levels), Multiply↔Divide (12 interleaved steps), Spelling (14), Reading (6) — sharing one progression engine.
- **A daily blend, not one difficulty at a time**: Review 20% / Current 60% / Stretch 20% around each track's frontier. Interleaved practice beats blocked practice for retention, even though blocked feels easier.
- **Promotion on clean answers only** (right first try, no hints): 10 in a row instantly, or 16 of the last 20. No demotion — a rough patch is absorbed by the Review band. Tracking is invisible; retrying still works exactly as before.
- Math progressions validated against Common Core K–3; phonics against Wilson Fundations / Words Their Way, with the item catalogue audited word-by-word for patterns that actually have enough real, image-backed examples.
- **Match Challenge was removed** rather than kept — it was guessable by elimination as pairs cleared, and the Reading Ladder is its real replacement.
- Built the **Dashboard**: per-track level, days at level, Last-10/Last-20 bars, and a trend chart with promotion markers.
- Investigated a "stuck on level 1" report and confirmed it wasn't a bug — a 10-question session splits across 4 tracks and only 60% of a track's questions are frontier-eligible, so promotion is simply slow by design.

## Phase 13 — Onto the web, and the read-aloud rule

- The project moved to GitHub and sessions now run in Claude Code on the web, which resolved the old `gh auth` blocker and made real browser testing possible for the first time.
- **Settled Reading's read-aloud rule**, which the code and docs had disagreed on. The rule: **pictures may be named aloud; words never are.** Read & Choose prompts with a picture, so a speaker names it for a child who can't identify the artwork. Reverse Read & Choose prompts with the written word, so it gets no speaker at all — speaking the prompt handed over the answer — and each of its five picture options carries its own instead. Either way the child still has to connect a spoken name to a written one.
- A picture speaker does **not** break a "clean" answer: identifying artwork isn't the skill Reading tests, so it's accessibility rather than a hint.
- Split the docs by role (below), after `Overview.md` had accumulated its own progress log and gone quietly stale.

## Phase 14 — Pokédex detail and NEW badges

- Pokédex entries are tappable, opening a detail popup with larger artwork, Dex number, name, types and a speaker. Reuses the existing catch modal rather than duplicating it.
- **Uncaught entries open but keep their secret** — silhouette, "???", no types, no read-aloud. Tapping a silhouette and getting nothing reads as broken; revealing the name would undercut the collection loop.
- New catches carry a **NEW** badge until opened, stored under its own key so existing saves start with nothing flagged.
- **Unified read-aloud into one affordance**: a speaker on the picture itself, everywhere it appears, rather than a labelled button in an action row.

## Phase 15 — Build identity

Settings has an **About** card: `Build` (hand-maintained), `Published`, and `This file` (`document.lastModified`). The last is the one that catches a stale cache — a cached page reports the *old* file's date — and it needs no maintenance. Added after a merged fix appeared broken because the deploy finished ~80s after the merge and the browser had cached the old build.

## Phase 16 — Pronunciations

`speechSynthesis` reads invented names as English words and mangles many. No usable web source of spoken names exists — PokéAPI's "cries" are sound effects, Forvo's coverage is thin and its terms forbid redistribution, and every wiki with a guide is blocked by this environment's egress proxy (web *search* reaches their content; `raw.githubusercontent.com` is fetchable). So the fix is local: hand the synthesiser a phonetic respelling.

- `data/pronunciations.csv` maps name → `say_as`, with a `source` column recording whether it was verified (`checked`) or reasoned from etymology (`unverified`). **Speech only** — every display still shows the real name.
- `u.lang = "en-US"` is set explicitly; without it the OS default voice applies another language's phonetics to English spellings.
- Values stay lowercase and space-separated: some engines read an all-caps syllable as an initialism and spell it out, and the Web Speech API offers no usable SSML for stress.
- Hyphenated slugs (`great-tusk`, `iron-bundle`) are de-hyphenated **in code**, covering ~25 names and any added later.
- **The key lesson, from a real ear-audit**: the failure mode was *over-syllabification* — "jer af ah rig", "toe geh pee", "ar kuh nine", chopping up names the engine already handled. The map peaked at 251 entries and was pruned to **184** (138 checked, 46 unverified). **An override is a liability unless it earns its place**: it should exist only where the plain spelling is genuinely misread, never merely where it looks like it might be. If a respelling sounds wrong, **drop it rather than re-guess** — the plain spelling is a known state.
- `tools/pronounce.html` is a dev-only audit page: every name with Before/After playback, an editable respelling to try by ear, and a copyable list of what to change.

## Phase 17 — Data out of index.html

`index.html` was 236KB, roughly half of it data literals. All three blocks moved to `data/*.csv`, fetched and parsed at startup so they can be maintained in a spreadsheet, roughly **halving the file**.

- **The trade-off**: `fetch` is blocked on `file://`, so the app must be **served over http** rather than opened by double-clicking. A missing CSV shows a legible error instead of booting with silently empty pools.
- Boot is async. Listeners bind immediately; anything reading the roster waits for data.
- Columns favour the spreadsheet: `type1`/`type2` rather than a delimited cell, and a bare image slug so the folder convention lives in one place. `data/README.md` documents the editing traps.

## Phase 18 — Legendary call-outs

`rarity` in `data/pokemon.csv`, sourced from PokéAPI's `pokemon_species.csv` — **71 legendary, 23 mythical**, joined on name with zero mismatches. Gold cell and ✨ badge in the grid, a chip in the detail popup, a per-generation tally in each header, and a "✨ Legendary Catch!" banner. The marker shows on **uncaught** slots too: it reveals nothing about which Pokémon lives there, and flagging the slot is the point.

## Phase 19 — Pokédex image loading

A single broken tile on the live site never reproduced locally — the file was valid and tracked, and all 1,021 rendered fine individually. The mechanism was clear even so: the Pokédex fired **1,021 image requests at once**, which a real network throttles, and a dropped `<img>` never retries. Now lazy-loaded (**39 requests on open**) with a single retry per image. A fix for the probable cause rather than a confirmed diagnosis — if a tile still breaks, that means two consecutive failures and points elsewhere.

## Phase 20 — The hint allowance was off by one

Reported as "the UI says 3 hints but you only get 2." True, and worse at higher levels: the bail-out fired when you **spent** your last hint rather than when you **asked for one you didn't have**, so the final hint was revealed and the same click locked the board and swapped the word. A 3-hint word gave 2 usable hints; Fluency 5, whose allowance is 1, gave **none** — its only hint voided the word every time.

Fixed by moving the check into the guard, so every hint in the allowance is usable. The word-swap escape hatch was then **removed** rather than rebound to an extra press: it existed to stop a stuck child stalling, but there is no stall to rescue — the tile rack holds exactly the word's letters and wrong ones are rejected, so any word can always be finished unaided. The button simply greys out at zero. `outOfHints()` and the now-unread `pool` field on spelling challenges went with it.

---

## Phase 21 — Evolution families in the Pokédex

National Dex order already puts 83% of evolution families side by side, but cross-generation evolutions can sit hundreds of slots apart — Pichu is #172 while Pikachu is #25, and Eevee's family spans #133 to #700. Within Gen 1 there are no splits at all, so this only starts mattering at Gen 2.

An `evolves_from` column in `data/pokemon.csv` (from PokéAPI, 479 links) drives a strip in the detail popup: one step back, every step forward, current entry highlighted. Each member is tappable and reopens the popup on itself, so a three-stage line is two taps rather than a wall of sprites — which matters for Eevee's eight branches. Relatives not yet caught show as silhouettes, turning the strip into a motivator rather than a spoiler; an uncaught entry shows no strip at all. Four rows are deliberately blank (Nidorina, Nidorino, Sirfetch'd, Mr. Rime) because their real parent is one of the four species excluded from the roster, and a link that can't be followed is worse than none.

## Phase 22 — Home tiles, an honest results screen, and a pity timer

- **The Play Streak card became three tiles.** Seven rows reading "Not played yet" took ~420px and pushed Start Playing below the fold; three tappable tiles (Rounds Today / Pokémon / Day Streak) take ~90px. The stored data already turned out to be rounds-per-day — `recordDailyCompletion()` fires once per finished session — so nothing needed migrating. Daily counts are no longer pruned to 7 days, which would have silently capped the streak at the window length. Settings gained **Rounds per day** (default 2) and renamed the old count to **Questions per round** (default 10), naming two units that had been implied.
- **The streak holds until the day ends**, counting consecutive days ending today *or yesterday*, rather than resetting to zero at midnight before the child has played.
- **The results screen dropped its score**, because the score could never be anything but 100%: every mode retries until correct, so `correct` always equalled `total`. "Perfect! You're a Champion!" fired every round and the other three tiers were unreachable code. The perfect-run reward was worse — it announced "You earned Mewtwo!" and called no `addToCollection`, a broken promise on every round. The screen is now "Round finished!", the three tiles, and the Pokémon actually caught this round as tappable chips. `LEGENDARY_IDS` went with it, having listed Dragonite, which isn't legendary.
- **A pity timer caps encounter droughts.** At rate R an encounter is guaranteed one question short of the average wait (at 10%, the 9th question). The counter resets each round, so a cold streak never follows the child into the next one. Verified deterministically at 5/10/25/50% — and the first version of that test proved nothing, because `rand` is a `const` arrow that can't be replaced from outside; stubbing `Math.random`, which it actually calls, was what made it real.

## Where things stand

Everything speced is built: four Lesson Trails promoting, the Dashboard, the Pokédex with detail and legendary call-outs, Battle, and all game data in editable CSVs. Published on GitHub Pages.

Open threads:

- **46 unverified pronunciations**, all Gen 8–9 — none yet heard, each with a stated reason for existing. They'll surface as the collection reaches them; `tools/pronounce.html` filters to exactly this set.
- **~820 un-eyeballed Pokopia items**, for name/image mismatches like the "Bill"/CD one. Easier now that it's a spreadsheet.
- **`APP_BUILD` is bumped by hand.** No build step stamps it, and a stale number defeats the About card's purpose. The `This file` timestamp beside it is automatic and can't go stale.

Parked, not scheduled: a service worker for genuine offline install; moving the type chart to CSV if it ever needs editing; and two deferred Reading modes — **Rhyme Match** (most Pokémon names are invented and don't reliably rhyme, so it would need the Phase A real-word list) and **Clue Words** (needs per-item colour/size/material data that doesn't exist).

## Doc roles

- `Overview.md` — what the app does today. No history, no status, no plans.
- `progress.md` — this file: how it got here, and what's open.
- `LessonTrails.md` — curriculum design rationale.
- `data/README.md` — CSV columns and the editing traps that aren't obvious.

## Tooling note

Real browser testing works in web sessions: Node, Playwright and Chromium are preinstalled. Serve the folder and drive it rather than opening a `file://` URL — which the CSV loading now requires anyway.

```js
// The preinstalled build is older than a fresh `npm i playwright` expects, so
// launch with an explicit path and do NOT run `npx playwright install`.
chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' })
```

Calling the app's own functions via `page.evaluate()` — `mkReading()`, `renderPokedex()`, then asserting on the DOM — reaches any mode or level directly without playing to it. But check screenshots too: two bugs this session passed every structural assertion while being visibly broken on screen.
