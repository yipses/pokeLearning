# Progress Log — Poké Learning

A running summary of how this project got from a basic spelling/math quiz to where it is now. See `Overview.md` for the current feature spec (PRD); this file is about the journey.

---

## Phase 1 — Foundation

- Started from an existing single-file app (`index.html`) with two challenge types: Pokémon spelling and basic math, drawing from a hardcoded list of **40 Pokémon**.
- Expanded the roster to the full original **151 Pokémon**, then trimmed it to **147** by removing four species whose names don't work with the plain-letter spelling mechanic (Nidoran♀, Nidoran♂, Farfetch'd, Mr. Mime).

## Phase 2 — New game modes

- **Match Challenge** added: a picture-to-name matching round (tap one tile, then its pair), with instant feedback on right/wrong guesses.
- **Math Patterns** added: instead of one equation at a time, present a set of 4 related problems that follow a numeric pattern (e.g. a fixed number with a steadily increasing partner), and check all four at once.
  - Fixed a bug where clearing a wrong answer and leaving it blank re-triggered the "wrong" message instead of a "fill in the blanks" message.
- **Visual Math** added: the same four operations, but shown as pictures of Pokémon instead of bare numbers — grouped boxes for addition/multiplication, crossed-out icons for subtraction, sliced groups for division.
- Sessions were updated so the **same mode never repeats back-to-back** when more than one mode is active.

## Phase 3 — UX and settings overhaul

- Reworked how a session is put together: instead of each mode having its own separate challenge count, there's now **one total "Number of Challenges"** setting, and every challenge slot is randomly drawn from whichever modes are currently active.
- Moved every mode's configuration off the main screen into a dedicated **Settings page**, so the Start screen only shows the challenge count plus Start / Battle / Settings buttons.
- Math, Math Patterns, and Visual Math were all switched from "type an answer, press Check" to **auto-checking as you type** (waiting for enough digits before judging), with a **Next ▶** button that only activates once the answer is correct — replacing the old fixed-delay auto-advance.
- Added **settings persistence**: every toggle, min/max, and count now saves to `localStorage` automatically and restores on the next visit.
- Results screen got a pass: fixed a CSS bug that was silently left-aligning the "Champion" title, replaced the plain trophy emoji with an animated Pokéball + random legendary Pokémon reveal on a perfect run, and added an editable challenge-count field so **Play Again** doesn't require a trip back to Settings.
- Match mode gained a configurable "Pokémon per round" setting and a 🔊 button per picture to hear the name spoken aloud (later simplified so tapping the whole tile both plays the sound and registers the match, rather than needing a separate tap on the icon).
- Basic Math and Visual Math both gained independent **Min and Max** number settings per operation (not just Max), specifically to cut out trivially easy problems.

## Phase 4 — Content expansion & offline support

- Pulled a curated list of **150 items from Pokémon Pokopia** (materials, food, badges, fossils, classic held items) and added them as an optional pool that mixes into Match mode alongside Pokémon.
- Built and published a standalone visual verification page to confirm all 150 item images actually load — useful for catching broken links before shipping.
- Downloaded and locally cached **all 147 Pokémon artwork images and all 150 item images**, and rewired the app to reference the local copies instead of remote URLs — the app now works fully offline and doesn't depend on any external site staying up.

## Phase 5 — Battle mode

- Added a standalone **Battle mode**: pick two random Pokémon, predict a winner, watch a short old-school-style fight animation (shake effects, move-name flavor text), and see the result — with a 🔊 button to hear each name.
- Upgraded the winner logic from a plain coin flip to a **stat- and type-weighted roll**: fetched real base stats and types for all 147 Pokémon once (cached locally, not a live lookup), built a full type-effectiveness chart, and now the stronger/type-advantaged Pokémon wins more often without it being a guaranteed outcome.
- Added a spoken + banner **winner announcement** ("PIKACHU WINS!") and a running **session win/loss record** shown at the top of the Battle screen.

## Phase 6 — Polish and documentation

- Visual tweaks throughout: bigger, clearer crossed-out icons in Visual Math; hover states and alignment fixes on the matching grid; type badges shown on Battle fighters.
- Wrote `Overview.md`, a PRD-style document covering the full current feature set.
- Wrote this file.

## Phase 7 — Daily engagement & collection

- Added a **Play Streak** card to the home screen: one star per full session completed via Start Playing (Battle doesn't count), tracked per day for a rolling 7-day window in `localStorage`.
- Added a **grass encounter** mechanic to every challenge screen: a decorative grass strip (built with layered CSS/SVG blade shapes, no external image assets) that shakes when a Pokémon is hiding nearby, at a drop rate configurable in Settings (default 10%). Answering the current question correctly catches it — no auto-dismiss timer, a proper "Caught!" popup shows the Pokémon's artwork, Dex number, name, and type badges, dismissed with an Okay button.
- Added a **Pokédex** screen, organized by generation, showing every Pokémon either in full color (caught) or as a grey silhouette with its name hidden as "???" (uncaught) — the silhouette reuses the existing transparent-background artwork with a `brightness(0)` filter rather than needing a separate asset.
- Catching is **generation-gated**: only the lowest generation not yet fully caught can appear in the grass, so a session can't skip ahead to a later region before finishing an earlier one. Spelling's word pool respects the same gate.
- Fixed a rendering bug where extreme-aspect-ratio item images (e.g. a very tall "Rope" sprite) got cropped to just their top few pixels in the Spelling picture frame — `width/height:88%` doesn't reliably constrain both axes inside a CSS grid; switched to the standard `max-width/max-height` + `width/height:auto` pattern.

## Phase 8 — Full National Dex & a much bigger item catalog

- Pulled the remaining **874 Pokémon** (dex 152–1025, Gen 2 through Gen 9) from the same source as the original 147 — PokéAPI's sprites repository, confirmed by hashing an existing file against a fresh download before trusting it for a bulk pull. Roster is now **1,021** Pokémon.
- Spelling's plain-letter-name filter now spans the full roster: 984 of 1,021 names are spellable; the other 37 (Ho-Oh, the Tapu guardians, most Gen 9 Paradox Pokémon, etc.) are excluded from Spelling specifically but still usable everywhere else.
- Investigated the original 150-item Pokopia set and found it was a curated "resources" subset (materials/food/badges/held items), not the full in-game catalog. Pulled the rest from `pokopiahabitats.com` — checked against the existing set first (same artwork, meaningfully higher resolution) — with category data sourced from Bulbapedia's own item table. After removing 121 items with parenthetical variant names ("Antique wall (middle)", "Copper deposit (Beach)") that were mostly near-duplicate wallpaper/flooring swatches, the catalog landed at **922 items** across 12 categories.
- Added a **per-category toggle grid** to Settings so Match and Spelling's item pools can be filtered (e.g. turning off Blocks, the most repetitive category).

## Phase 9 — Lesson Trails: a real curriculum

- Designed a **progressive curriculum** to replace ad-hoc difficulty settings — four independent tracks (Add/Subtract, Multiply↔Divide, Spelling, Reading), each with its own ordered sequence of levels and its own "frontier" (the level currently being worked on). Captured as a living design artifact, iterated extensively before any code was written.
- Validated the math progression against actual Common Core K–3 standards (not assumed) and the phonics progression against real structured-literacy scope-and-sequence (Wilson Fundations / Words Their Way) — audited the existing item catalog word-by-word for which phonics patterns actually have enough real, image-backed examples, rather than inventing words.
- Settled the daily mechanic: a **blend**, not one difficulty at a time — Review (20%, below frontier) / Current (60%, at frontier) / Stretch (20%, above frontier) — with promotion via **either** 10/10 "clean" answers in a row (instant) or 16/20 (80%) in a rolling window (standard pace). "Clean" means right on the first try with no hints; tracked invisibly alongside the existing retry-until-correct flow so answering a question doesn't feel any different than before.
- **Built and shipped**: the shared progression engine (per-track frontier storage in `localStorage`, clean/labored tracking, Last-10/Last-20 rolling windows, the dual-threshold promotion rule, the review/current/stretch band picker), plus:
  - **Add/Subtract**, 8 levels from "within 5" through "within 100 with regrouping," using rejection sampling to specifically control for carrying/borrowing rather than leaving it to chance.
  - **Multiply↔Divide**, 12 interleaved steps — revised from an initial 10 after live testing showed jumping straight to 1–5×1–5 with division interleaved immediately was too much; multiplication now gets two full steps (1–3, then 1–5) before division is introduced at all, and division gets the same two-step ramp once it starts.
- Replaced the old fixed min/max Math settings with two frontier dropdowns that double as manual override — moving one resets that track's rolling windows, in either direction.
- Rolled the previously-standalone **Math Patterns** mode into both trails (~30% of questions become a 4-in-a-row skip-counting set) rather than dropping it, after reconsidering that it teaches something — actual counting-by-N — the single-equation format doesn't. Generalized the step size from a fixed small set to *any* value where 4 repetitions fit the level's range, so counting by 2s, 3s, up to 25s all become possible depending on the level.
- Fixed two Visual Math issues surfaced while building this: multiplication could generate a degenerate single-group problem ("5×1" shown as one box with no repetition visible) — now always shows at least 2 groups, matching the guard division already had; and the equation rendered *after* the `+`-joined picture even for multiplication, visually contradicting the `×` symbol shown right below — reordered to equation-first across all four operations. Also removed all instructional caption text from Visual Math and Math Patterns screens, since a pre-reading child can't use text they can't read and the numbers/pictures already carry the meaning.

## Phase 10 — Spelling Trail, and a settings cleanup pass

- **Built and shipped the Spelling Trail**, replacing the old fixed-length/item-toggle Spelling settings entirely — one frontier, 14 levels:
  - **Phase A, Phonics Ladder (9 levels)**: hand-audited real single-word Pokopia items, classified into CVC → floss-rule doubles → blends → digraphs → silent-e → vowel teams → r-controlled → compound words → multisyllabic. 101 of the catalog's 108 single-word items placed (7 dropped as unsuitable — irregular/foreign spellings or exact duplicates); verified by script against the live `ITEMS` array (no typos, no dupes, no orphans) before wiring in. Not generation-gated — a pattern's words are available the moment its level unlocks.
  - **Phase B, Fluency (5 levels)**: Pokémon-name practice, still generation-gated like grass encounters, staggering two tasks per challenge — the existing tile-based Full Spelling, and a new **Missing Letter** mode. Missing Letter blanks whole phonics *chunks* (a `chunkWord()` tokenizer treats digraphs/blends/vowel-teams/r-controlled vowels as one atomic unit, so a blank never splits a sound), no hints, with its own per-level length ceiling and blank-count range from the design spec.
  - Same promotion engine as the math trails (10/10 instant or 16/20 rolling, review/current/stretch blend) — `recordAttempt` now fires for spelling too, tracking clean = no wrong letters and no hints used.
- **Tied Visual Math to the Math Trails frontiers** instead of its own independent per-operation on/off + min/max settings (removing that whole settings block) — ranges stay fixed and small for legibility, and division only joins the pool once the Multiply↔Divide trail has actually introduced it.
- **Replaced "✅ Correct! Tap Next to continue." with just a bigger animated ✅** across Math, Visual Math, and Math Patterns — a pre-reading kid can't parse the text, and the Next button already implies what to do next.
- **Fixed a corner-clipping bug** in the circular `.poke-frame`: `max-width/max-height:88%` let a near-square, low-padding image's bounding-box corners poke outside the circle's radius (found via the word "Bell," whose item art fills its canvas much tighter than official Pokémon sprites do). Dropped to 65%, which keeps even a worst-case zero-padding square image's corners inside the frame.
- **Removed Match Challenge entirely** (settings card, render/click logic, CSS, and the Pokopia Item Categories filter grid that had no other consumer once Match was gone) — it wasn't being used, and unlike the math/spelling tracks it had no ladder to sit on; the still-unbuilt Reading Ladder is the actual fix for the flaw Match had (guessable-by-elimination as pairs clear).
- No working headless/interactive browser tooling in the agent's sandbox this session — see the Tooling note below. Verification instead relied on: a script auditing every Phase A word against the live item catalog, syntax-checking the extracted `<script>` via `osascript -l JavaScript`, and running the real app code under a minimal in-memory DOM/localStorage shim to exercise actual logic (chunking, pool generation, promotion thresholds, `buildQueue()` blending).

---

## Phase 11 — Reading Ladder, and getting the project onto GitHub

- **Built and shipped the Reading Trail**, the 4th and last speced Lesson Trails track — 6 levels, sharing the same generation-gated Pokémon pool as Spelling's Fluency phase (no new content curation needed):
  - **Read & Choose** (see a picture, pick the matching word from 5) and **Reverse Read & Choose** (see a word, pick the matching picture from 5) — fixed-choice formats specifically so difficulty never shrinks over a round the way the old Match mode's pool did.
  - Ramps on two independent axes: word length (3–6 letters for levels 1–4, 7–10 for levels 5–6) and distractor difficulty ("easy" = random, "tricky" = the 4 wrong options share the target's first letter or length, with a fallback to random if the gen-gated pool is too small to find 4 tricky matches).
  - Levels 1–4 are single-mode (alternating Choose/Reverse level by level); levels 5–6 mix both modes randomly within the level.
  - Deliberately **no hints and no read-aloud** on either mode — the whole point is confirming the child actually read the word, not shape- or sound-matching it. *(Superseded in Phase 13: the shipped code never actually matched this, and the rule is now "pictures may be named aloud, words never are" — Read & Choose keeps a speaker on its picture prompt, Reverse Read & Choose drops it from the word and gives one to each picture option.)*
  - Same promotion engine as every other track. Verified with a script: every generated round has exactly 5 unique options including the target; the "tricky" distractor rule holds in 198/200 sampled rounds (the other 2 correctly hit the documented small-pool fallback); 10/10-clean promotion fires correctly; and directly exercised the click handler for three scenarios — correct-first-try (records clean), wrong-then-correct (records not-clean, doesn't double-advance), and clicking again after a round is already won (guarded, no double score).
- **Started moving the project onto GitHub** at your request, so you can access it by URL and I can push updates directly instead of you copying files around:
  - Committed everything that had built up uncommitted (both full asset folders, `Overview.md`, `progress.md`, and all of today's `index.html` work) as the real second commit — the original "initial commit" predates almost all of this.
  - Added a `.gitignore` and untracked `.claude/settings.local.json` (local machine prefs, not project state — no secrets in it, just not something to keep committing).
  - Installed `gh` (GitHub CLI) via Homebrew so I can create the remote repo and push directly once authenticated, rather than walking you through the web UI by hand.
  - Decided: **public** repo (you're not worried about the Pokémon/item art being visible) + **GitHub Pages** for hosting, since it needs no third-party account beyond GitHub itself. Repo is ~182MB, comfortably under GitHub's 100MB-per-file hard limit and its ~1GB soft repo-size guidance — no Git LFS needed.
  - **Paused here**: `gh auth login` needs an interactive browser step only you can do. Once that's done, still to do: `gh repo create` + push, then flip on Pages in the repo settings. *(Resolved in Phase 13 — the repo is on GitHub and sessions now run against it directly, so `gh` was never needed. Pages is still unconfirmed.)*

## Phase 12 — Bug fixes from real play, and the Dashboard

A batch of fixes surfaced by actually playing the app, plus the last speced piece:

- **Fixed a real data bug**: the item named "Bill" was actually a picture of a music CD (a real Pokopia item category, just mislabeled during the original scrape) — renamed the file and catalog entry to "CD", removed it from the Spelling floss-pattern list since it was never a real decodable word to begin with (floss is down to 2 real words now: Bell, Moss).
- **Fixed a real rendering bug**: Visual Math's division layout tried to show one shared box with an internal dashed divider between "slices," which broke down and collapsed into a confusing grid once the icons didn't fit one row (e.g. 9÷3). Rebuilt it to use separate bordered boxes per group, the same proven layout multiplication already used.
- **Fixed a real gap**: Reading's word pool was Pokémon-only — missed that the spec calls for the same combined Pokémon+item pool Match mode used. Added items back in, and fixed a case-sensitivity bug in "tricky" distractor matching that the item/Pokémon name-casing mix surfaced (Pokémon names are lowercase, item names are Capitalized).
- **Fixed a real repetition bug**: Phase A's phonics pools are tiny (2-4 words at the easiest patterns), so pure independent random sampling clustered hard — a 3-word pool has a ~34% chance of repeating the same word back-to-back. Added a "never repeat the immediately-previous word for this pattern" guard.
- **Investigated a "still stuck on level 1" report** and confirmed it wasn't a bug: simulated 400 realistic multi-track sessions using the actual `buildQueue()` — under perfect play all 4 tracks promoted twice within 13 sessions, and progress correctly round-trips through a simulated page reload. The real cause is just volume dilution: a 10-question session splits across 4 tracks, and only 60% of a track's own questions are frontier-eligible, so any one track gets maybe 1.5 promotion-eligible attempts per session.
- **Built the Dashboard** — the last unbuilt piece from the Lesson Trails artifact. One card per track (current level, days at that level, Last-10/Last-20 bars, and a live SVG trend chart with 80%/100% gate lines, a gold star marker for instant 10/10 promotions, and a dashed "Leveled up" line for 16/20 promotions) — reachable from a new "📊 My Progress" button on the home screen. Required extending the progress data model with two new per-track fields, `trend` (a capped rolling log of Last-10/Last-20 % at each frontier attempt) and `frontierSince` (a timestamp, for the days-at-level count) — verified old pre-Dashboard save data migrates cleanly, keeping existing frontier/history exactly and just backfilling the two new fields, so no one's real progress gets lost by this update.

## Phase 13 — Moved to Claude Code on the web, and the Reading read-aloud rule

- **The repo is on GitHub and the session now runs there**, not on the Mac — which resolves Phase 11's blocker. `gh auth login` never happened and no longer needs to: the web environment clones the repo itself and pushes over its own credentials. Everything built through Phase 12 is on `origin/main`, squashed into the single `Initial Commit`.
- **Real browser QA works now** — the long-standing blocker below is gone in this environment (see the rewritten Tooling note). Verified it by actually serving `index.html` and driving it in headless Chromium: home screen renders, `Start Playing` advances to a live challenge, clean console, no failed requests. This is the first time the app has been confirmed working by *running* it rather than by reasoning about the code under a DOM shim.
- **Settled the Reading read-aloud question**, which the code and the docs disagreed on. Phase 11 recorded the decision as "deliberately no hints and no read-aloud on either mode," but the shipped code put a 🔊 Say it on *both* modes, and the code comment justified it as "an optional aid, same as Spelling's." Neither was quite right. The rule now is **pictures may be named aloud; words never are**:
  - **Read & Choose** (picture → pick the word) **keeps** its Say it. The picture is the prompt, and a lot of the artwork — obscure Gen 8/9 species, unfamiliar Pokopia items — isn't reliably identifiable by a small child. Without a way to resolve *what the picture is*, the question isn't a reading test, it's a guess. Naming the picture resolves the prompt and leaves the five written options still to be read.
  - **Reverse Read & Choose** (word → pick the picture) **loses** it. Here the prompt *is* the written word, so speaking it handed over the answer outright and left nothing to decode — the single worst version of this. Each of the five picture options now carries its own small speaker instead, so a child who can't identify the artwork can still hear it.
  - Net effect: in both modes the child still has to connect a spoken name to a written one, and nothing ever reads a *word* to them. Implemented with the speaker as a **sibling** of each option button rather than a child — a `<button>` inside a `<button>` is invalid HTML and browsers restructure it.
  - Verified in a real browser: Read & Choose renders 1 prompt speaker and 0 per-option speakers, Reverse renders 0 and 5, no nested buttons in either; tapping all five option speakers neither answers the question nor marks the attempt as non-clean; and picking the correct picture still records a clean attempt.
- **Decided: Read & Choose's Say it does not break "clean."** Spelling counts a hint against a clean answer, so it was worth asking whether the picture speaker should count the same way. It doesn't, and shouldn't — identifying artwork isn't the skill Reading is testing, so the speaker is an accessibility affordance rather than a hint. A child can tap it on every question and still promote at 10/10.
- **Confirmed GitHub Pages is live.** It couldn't be checked by URL (the sandbox proxy blocks outbound to both `github.com` and `github.io`), but the GitHub API shows a `pages build and deployment` run against `main` at `19eef77`, completed successfully. The site builds from **`main`**, so work on a feature branch isn't live until it's merged.
- **Split the docs by role.** `Overview.md` had been carrying progress inside it — "planned," "not yet built," "Status: two of four tracks built," a Match-mode removal note, and a Possible Future Directions section — which meant every shipped feature left it quietly wrong. It's now strictly a description of what the app does today, with a header line saying so and pointing here. Everything time-bound lives in this file instead. Rewriting it against the actual code also caught several things it had wrong: it still described Spelling as configured by min/max name length (the Spelling Trail replaced that in Phase 10), still described Visual Math as having its own per-operation toggles and ranges (Phase 10 rewired it to render Math Trails questions), listed six screens rather than seven, and carried a broken cross-reference to a "§5.6" that didn't exist.

### Ideas parked here, previously in `Overview.md`

Not scheduled work — surfaced during development and kept for reference:

- **Rhyme Match** (given a word, pick which of three others rhymes) — deferred because most Pokémon names are invented and don't reliably rhyme; it would need to draw from the Phase A real-word list instead.
- **Clue Words** (a few descriptors shown at once — BIG, RED, METAL — pick the matching item) — deferred because it needs per-item attribute data (color, size, material) that doesn't exist yet.
- Sentence-level reading comprehension, beyond single-word Read & Choose.
- Per-session or historical stats beyond the in-memory Battle record and the Dashboard.
- Difficulty presets that bundle several settings at once.

## Phase 14 — Pokédex entry detail, NEW badges, and one read-aloud affordance

- **Pokédex entries are tappable now**, opening a detail popup with larger artwork, Dex number, name, type badges, and a speaker. Rather than build a second modal, generalized the existing "Caught!" one — it already showed exactly this content — into `showPokeModal(poke, {caption, revealed, dismissOnBackdrop})`, with `showCatchModal()` reduced to a thin wrapper. The catch reveal's behaviour is unchanged: it still requires the Okay button, because that button's handler is what runs the pending catch callback. Backdrop-dismissal is opt-in and only the dex uses it, since browsing means opening and closing a lot of these.
- **Uncaught entries open but keep their secret** — silhouette, "???", no type badges, no read-aloud. Tapping a silhouette and getting nothing would read as broken, but revealing the name would undercut the whole generation-gated collection loop, so the popup confirms the tap without spoiling anything.
- **New catches are flagged NEW in the grid until opened.** A session can catch something several hundred entries deep, and finding it again afterwards meant scrolling a thousand cells. Unseen ids are stored under their own key rather than bolted onto the collection, so existing saves simply start with nothing flagged. Opening an entry clears its badge in place rather than re-rendering the dex, which would throw away scroll position.
- Made dex cells real `<button>`s instead of divs, so they're keyboard-reachable and get native tap semantics, with `aria-label`s carrying the name/number (and "not caught yet" for silhouettes).
- **Unified the read-aloud affordance.** It had drifted into three shapes: a labelled "🔊 Say it" in the action row at the bottom of Spelling and Missing Letter, another in Read & Choose, and the small per-picture speakers added to Reverse Read & Choose in Phase 13. It's now one thing everywhere — a round speaker sitting on the lower-right rim of the picture frame (`.frame-wrap` / `.frame-say`), which is also what the new Pokédex popup uses. Reverse keeps its five smaller per-option speakers, which is the same idea applied per picture.
  - One bug caught by actually looking at a screenshot rather than trusting the assertions: `.frame-wrap` started as `display:inline-block`, which let the preceding kind-tag ("Spelling") share its line and shoved the picture off-centre. All the structural checks passed while the layout was visibly broken. Fixed with `width:max-content; margin:0 auto`.
- **Favicon is now the app's own Pokéball mark**, inlined as an SVG data URI — no extra file, and the app stays a single self-contained page. Also stops the `/favicon.ico` 404 that browsers were generating.
- Verified in a real browser across all four speaker placements (present, inside the frame wrapper, none stranded in an action row, and geometrically overlapping the frame), plus the dex flows: badge count on load, badge cleared on open and persisting across a reload, a fresh catch re-flagging, caught vs. uncaught popup contents, and backdrop dismissal. No console errors, no failed requests.

## Phase 15 — Build identity in Settings

Prompted by a real incident: after merging the Pokédex work, tapping entries did nothing on the live site. Everything checked out — the code was on `main`, the deploy succeeded, and the exact user path reproduced fine locally on a fresh profile with an empty collection and a real touch tap. The cause was that the Pages deploy finished ~80 seconds *after* the merge, so an early check cached the old build. In that build dex cells were plain `<div>`s with no handler at all, which is precisely the "nothing happens" symptom.

The diagnosis took a round trip only because there was no way to tell from inside the app which version was running. So:

- Added an **About card** at the bottom of Settings with three rows: **Build** (a hand-maintained integer), **Published** (that build's date), and **This file** (`document.lastModified`).
- The third row is the one that actually catches a stale cache: `document.lastModified` reports the Last-Modified of the copy the browser actually loaded, so a cached page shows the *old* file's date rather than today's. Comparing it against the published date is a self-service answer to "am I running the new version?" without needing a reference value.
- **`APP_BUILD` must be bumped by hand on every change that ships.** There's no build step to stamp it automatically, and a stale number is worse than no number at all, since the whole point is distinguishing fresh from cached. The constant carries that warning in a comment. Build 1 = PR #1, build 2 = PR #2, build 3 = this change.

Worth recording for its own sake: this was the second time in two sessions that a problem was invisible to assertions and obvious in a screenshot (the first being the `inline-block` layout break in Phase 14). Structural checks confirm what's in the DOM; they don't confirm the user can see or reach it.

## Phase 16 — Pronunciation overrides

The read-aloud was mispronouncing a fair number of Pokémon names. Checked whether a web source of spoken names exists to fall back on, and there isn't one worth using:

- **PokéAPI has a `cries` field**, which is the obvious near-miss — those are the games' electronic sound effects, not a voice saying the name.
- **Forvo** has human recordings and an API, but coverage thins out badly across Gen 8/9, and its terms restrict redistributing or caching the audio — which is exactly what bundling it in the repo would be.
- **Wiktionary/Commons** covers real words, essentially nothing invented. Official anime audio is copyrighted and not an API.

So the fix is local: hand `speechSynthesis` a phonetic respelling instead of the real spelling. Chosen over pre-generating audio files because it keeps the app a single offline page with no new assets and no TTS account.

- Added `SPEECH_OVERRIDES` (name → respelling) and `sayAs()`, routed through `speakName()` and the Battle winner line — the two places names reach the synthesiser. **Speech only**: every display still uses the real name, which a test asserts directly.
- Also set `u.lang = "en-US"`, which was never set before. Without it the OS default voice is used, so a device configured for another language applies that language's phonetics to English spellings — and would make the respellings behave unpredictably. This was the "option A" quick win, folded in because the respellings depend on a predictable voice.
- Conventions, recorded in a comment on the map: values stay lowercase, because some engines read an all-caps syllable as an initialism and spell it out letter by letter; syllables are space-separated, which is the only stress control available since the Web Speech API has no usable SSML.
- Seeded 29 entries from documented pronunciations. **These are unverified by ear** — this sandbox has no speech voices installed at all (`getVoices()` returns empty), so they can't be heard here. Some may be wrong, or may be "fixing" names that were already fine.
- Built **`tools/pronounce.html`** to close that gap: a dev-only page listing all 1,021 names with a play button, a voice picker, filters, and a "✗ Wrong" toggle that collects flagged names into a copyable list. Flags persist to `localStorage` so a pass can be done across several sittings. It reads the roster and the override map out of `index.html` via a hidden iframe rather than duplicating them, so it can't drift — at the cost of needing to be served over `http://`.
- A test asserts every override key matches a real Pokémon name. A typo'd key is otherwise invisible: it just never fires, and the name keeps being mispronounced.

The division of labour from here: the flagged list comes back, each fix is a one-line addition. Guessing at respellings for names nobody has listened to risks making good ones worse.

**Then reworked the tool around A/B comparison**, which turns out to be the more useful shape. Each row now plays **Before** (the raw spelling, unaided) and **After** (the respelling), plus **A/B** to hear them back to back with a beat between — without the pause the two utterances run together and can't be told apart. The respelling sits in an editable box, so a fix can be tried by ear on the spot; an edited value is collected in the output list ready to paste straight back.

That changes the loop meaningfully. Flagging alone reports *that* something is wrong and leaves the fix to be guessed at blind, which is the same problem that seeded 29 unheard entries. An edited box reports what actually sounds *right* on the device the child uses — turning the person with ears from a reporter into the one who solves it, and removing the blind guess from the loop entirely.

---

**Where things stand:** All four Lesson Trails tracks are live and promoting, the Dashboard shows real progress for all of them, the app is confirmed running in a browser, and it's published on GitHub Pages. What's left:
- An offered-but-not-yet-done audit of the ~820 remaining Pokopia items for other name/image mismatches like the CD/Bill one (only the 101 used in Spelling have been individually eyeballed).

**Doc roles, so this doesn't drift again:**
- `Overview.md` — what the app does *today*. No history, no status, no plans.
- `progress.md` — how it got here, what changed and why, what's still open, ideas parked.
- `LessonTrails.md` — the curriculum design rationale behind the four trails.

---

## Tooling note — browser QA works in web sessions, not in the local Mac sandbox

**Current state (Claude Code on the web): real browser testing works.** Node 22, Playwright, and Chromium are all preinstalled. The working pattern is: serve the folder (`python3 -m http.server`) and drive it with Playwright, rather than opening a `file://` URL. One gotcha worth remembering — the preinstalled Chromium build (`chromium-1194`) is older than the one a fresh `npm i playwright` expects (1234), so a plain `chromium.launch()` fails with "Executable doesn't exist." Launch with an explicit path instead, and do **not** run `npx playwright install`:

```js
chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' })
```

Being able to call the app's own functions through `page.evaluate()` — `mkReading()`, `renderReading()`, then assert on the resulting DOM — turned out to be more useful than clicking through the UI, since it reaches any mode or level directly without playing to it.

**Historical (the local Mac sandbox), kept because it explains how Phases 9–12 were verified.** On the Mac there was no headless toolchain at all — no `node`, no `npm`, no Python `playwright`, only `python3` — and GUI automation didn't work either: `open -a Safari` reported success and Safari was confirmed running, but `osascript -e 'tell application "System Events" ...'` timed out (`AppleEvent timed out (-1712)`) and `tell application "Safari" to activate` never actually brought a window forward. The likely cause was that the process hosting the Bash tool lacked macOS Automation/Accessibility permission, so the calls silently no-opped rather than prompting. `screencapture` did work, so a screenshot could confirm visual state if the app was already frontmost — but the agent couldn't reliably focus a window or click into it.

That's why everything through Phase 12 was verified indirectly: syntax-checking the extracted `<script>` via `osascript -l JavaScript` (JavaScriptCore, no browser), and running the real app code under a minimal in-memory DOM/localStorage shim to exercise actual logic — data pools, chunking, trail promotion, `buildQueue()`. Those shim harnesses are still useful for pure-logic checks, but visual and interaction bugs now have a real browser to catch them. To get the same on the Mac, either grant Automation + Accessibility permission via System Settings → Privacy & Security, or install a headless toolchain locally.
