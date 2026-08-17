# Poké Learning — Product Requirements Document

**Owner:** Derek Yip
**Platform:** Web app — one page (`index.html`) plus `data/*.csv` and local artwork. Served over http(s), works offline once loaded, mobile-first
**Audience:** Young learner(s) practicing spelling, reading, and math, themed around Pokémon

> This document describes **what the app does today** — nothing else. How it got here, what changed when and why, what's still open, and what might come next all live in `progress.md`. The curriculum design rationale behind Lesson Trails lives in `LessonTrails.md`.

---

## 1. Summary

Poké Learning is a no-build, no-dependency HTML/CSS/JS app — one page plus a folder of CSV data and local artwork — that turns spelling, reading, and math practice into short, randomized, Pokémon-themed mini-games. A session mixes challenges from whichever modes are turned on, tracks a score, and ends with a results screen.

Difficulty is not a setting a parent picks and re-picks. Four **Lesson Trails** — Spelling, Reading, Add/Subtract, and Multiply↔Divide — each hold their own level and advance on their own based on real performance. Alongside the practice modes: a Pokédex-style collection game (catch Pokémon hiding in the grass as you answer correctly, generation by generation), a daily play streak, a progress dashboard, and a separate, unscored Battle mode where the player picks a Pokémon and watches a stat/type-based "who would win" prediction play out.

## 2. Goals

- Make repetitive spelling/reading/math drilling feel like play, not homework.
- Support a range of question styles — abstract numbers, concrete pictures, patterns, word recall — rather than one fixed format.
- Ramp difficulty automatically, per skill, on real performance, and let a parent override placement without touching code.
- Load fast, remember everything between visits, and keep working without a network once loaded. No build step, no runtime dependencies, no account.

## 3. Non-goals

- No accounts and no cloud sync. Progress is local to the browser.
- Not a competitive/multiplayer game.
- Battle mode is not a Pokémon battle simulator — it's a lightweight prediction game, not a move-by-move damage calculator.

## 4. App Structure

Seven top-level screens, all within one `index.html`:

| Screen | Purpose |
|---|---|
| **Start** | Play Streak, "Start Playing," "Pokémon Battle," "My Pokédex," "My Progress," "Settings" |
| **Settings** | Per-mode toggles and each trail's frontier control |
| **Play** | One challenge at a time, progress bar, grass encounter strip, quit button |
| **Results** | Score, tiered feedback (with a special reveal for a perfect run), replay controls |
| **Battle** | Standalone Pokémon-vs-Pokémon prediction game with its own back button |
| **Pokédex** | Every Pokémon, organized by generation, caught ones in color, uncaught ones as grey silhouettes |
| **Dashboard** | One progress card per Lesson Trail |

Settings, Lesson Trails progress, the Pokédex collection, and the play streak persist to `localStorage` and are restored on load.

## 5. Sessions

Each mode toggles on/off in Settings. A session draws each of its **N** challenges at random from the active modes, never repeating the same mode back-to-back. A mode with nothing enabled inside it drops out of the pool automatically.

## 6. Lesson Trails

Each core skill has its own **track** — an ordered sequence of levels — that advances on its own. There are four: **Spelling**, **Reading**, **Add/Subtract**, and **Multiply↔Divide**. All four share one progression engine; a track supplies only its level list and generator functions.

**Difficulty blend.** Each track has a **frontier** — the level being worked on. Its question pool blends three bands: **Review** (20%, below frontier), **Current** (60%), **Stretch** (20%, above). Deliberately not "master level N, then jump to N+1"; see `LessonTrails.md`.

**Promotion.** Only **clean** answers count — right on the first attempt, no wrong guesses, no hints. A track promotes on 10 clean in a row, or 16 of the last 20, whichever lands first. No demotion; a rough patch is absorbed by the Review band. The tracking is invisible: retrying or using a hint still works and still advances the session, it just doesn't count.

**Manual placement.** Every frontier is editable in Settings in either direction. Moving one resets that track's rolling window.

## 7. Challenge Modes

### 7.1 Spelling Trail

One graduated trail of 14 levels across two phases.

**Phase A — Phonics Ladder (9 levels)**, using real, audited single-word items from the Pokopia catalog. Not generation-gated: a pattern's words are available as soon as its level unlocks.

The nine patterns run CVC → floss-rule doubles → blends → digraphs → silent-e → vowel teams → r-controlled → compound words → multisyllabic. Level detail, including how many real words back each pattern, is in `LessonTrails.md`.

The easiest patterns have genuinely small pools (a few real words each), so the generator never repeats the immediately-previous word for a given pattern.

**Phase B — Fluency (5 levels)**, practicing Pokémon names the child already knows by ear, generation-gated the same way grass encounters are. Each level staggers two task types:

- **Full Spelling** — the mystery Pokémon's artwork is shown and the player spells its name from shuffled letter tiles (tap) or the keyboard. Controls: 🔊 (a speaker on the picture, speaks the name), 💡 Hint (reveals the next correct letter; greys out once the allowance is spent), Backspace, Clear. Wrong letters are rejected immediately with a shake; correct letters lock into a slot.
- **Missing Letter** — the word is mostly shown with blanks to fill and no hints at all. Blanks are placed by a `chunkWord()` tokenizer that treats digraphs, blends, vowel teams, and r-controlled vowels as single atomic units, so a blank never splits a sound.

Each Phase B level sets its own Full Spelling length ceiling, hint allowance, Missing Letter length ceiling and blank count. Hints tighten as levels rise (3 → 3 → 2 → 2 → 1), and Missing Letter's ceiling runs ahead of Full Spelling's at the earlier levels, since blanking part of a shown word is easier than spelling it from nothing. Per-level parameters are in `LessonTrails.md`.

Phase A words use the default allowance of 3 hints.

### 7.2 Reading Trail

Two fixed 5-choice formats, so difficulty stays constant round to round rather than shrinking as a round progresses:

- **Read & Choose** — one picture, five word options.
- **Reverse Read & Choose** — one written word, five picture options.

Draws from a combined pool of Pokémon (generation-gated, same as Phase B) and Pokopia items (not gated — items aren't part of the Pokédex collection loop). Ramps on two independent axes: word length, and distractor difficulty ("easy" = random, "tricky" = the four wrong options share the target's first letter or length, falling back to random when the gated pool is too small to find four tricky matches).

Six levels: word length holds at 3–6 letters through level 4 then jumps to 7–10, while distractors go from easy to tricky. Levels 1–4 are single-mode and alternate; 5–6 mix both. Full table in `LessonTrails.md`.

**Read-aloud rule: pictures may be named aloud; words never are.** Read & Choose prompts with a picture, which a child may not recognize, so a 🔊 Say it names it — resolving the prompt while leaving the five written options to be read. Reverse Read & Choose prompts with the written word and therefore has no speaker on the prompt at all; each of its five picture options carries its own instead. In both modes the child must connect a spoken name to a written one, and nothing ever reads a word aloud to them. There are no hints on either mode.

A Reading answer is **clean** when the first tap was the correct one. Using a picture's speaker does not affect cleanliness.

### 7.3 Math Trails

Two tracks. Answers auto-check as the player types (waiting until enough digits are entered to match the answer's length before judging); a **Next ▶** button appears once the answer is correct. A correct answer shows a large animated ✅ and no caption text.

**Add/Subtract — 8 levels**, from *within 5* to *within 100 with regrouping* (see `LessonTrails.md`). Each level auto-generates a mix of addition and subtraction within its range. Levels 4a–5b use rejection sampling to control specifically for whether the ones digit carries or borrows, making "no regrouping" and "with regrouping" genuinely distinct steps rather than just wider ranges.

**Multiply↔Divide — 12 interleaved steps sharing one frontier**, from tiny facts (×1–3) to full range (÷1–10) (see `LessonTrails.md`). Multiplication gets two full steps before division is introduced at all, and division gets the same two-step ramp once it starts.

**Skip-counting pattern sets.** On both tracks, roughly 30% of questions become a 4-in-a-row skip-counting set instead of a single equation, checked all at once. Step size is any value where four repetitions fit the level's number range, so a low level offers only counting by 1 while a high level can offer counting by up to 25.

### 7.4 Visual Math

Not a separate question source — a **rendering** of Math Trails questions as pictures of Pokémon instead of bare numbers, to build number-sense alongside abstract arithmetic. When it's on, any Math Trails question whose numbers are still small enough to draw legibly (operands capped at 6, with at least 2 groups required for × and ÷) is drawn instead of written. It therefore leads the early levels automatically and fades on its own as a trail's numbers outgrow what pictures can show.

- **Addition** — two boxes of Pokémon icons side by side, joined by "+".
- **Subtraction** — one box showing all the icons, with the subtracted amount crossed out by a bold drawn X.
- **Multiplication** — several equally-sized boxes joined by "+" signs, always at least 2 groups, since a single group doesn't demonstrate repeated addition.
- **Division** — separate bordered boxes, one per equal group.

The equation (e.g. "5 × 5 = ?") is shown **before** the picture. There is no instructional caption text.

## 8. Pokédex & Catching

- Every challenge screen shows a decorative grass strip. At a configurable rate (Settings, default 10%), it shakes to signal a Pokémon is hiding.
- Answering the current question correctly catches it: a popup shows **"Caught!"**, the Pokémon's artwork, Dex number, name, and type badges, dismissed with an **Okay** button (no auto-dismiss timer). Catching a legendary or mythical species changes the banner to **"✨ Legendary Catch!"** / **"✨ Mythical Catch!"**.
- Encounters are **generation-gated** — only the lowest generation not yet fully caught can appear, so progress moves through the National Dex in order rather than randomly across all 1,021 at once. Spelling's Phase B pool and Reading's Pokémon pool respect the same gate.
- The **Pokédex screen** shows every Pokémon organized by generation: caught ones in full color with their name, uncaught ones as a grey silhouette (a `brightness(0)` filter on the same artwork, no separate asset) with the name hidden as "???", plus a live X/Y caught count per generation.
- **Legendary and mythical species are called out**: a gold cell with a ✨ badge in the grid, a matching chip above the type badges in the detail popup, and a per-generation tally in each generation header (`✨ 2/5 · 3 / 147`). The marker shows on **uncaught** slots too — it reveals nothing about which Pokémon lives there, and flagging the slot is the point: it marks something worth hunting for rather than only rewarding the find afterwards. Name, types and the rarity chip all stay hidden until it's caught.
- **Every entry is tappable**, opening a detail popup with larger artwork, the Dex number, the name, type badges, any rarity chip, a 🔊 speaker, and its **evolution family**.
- **The evolution strip** shows one step back and every step forward, with the current entry highlighted. Relatives not yet caught appear as silhouettes with "???", and every member is tappable — so a three-stage line is two taps rather than a wall of sprites, and branching families (Eevee's eight) simply wrap. National Dex order puts 83% of families side by side already, but cross-generation evolutions can sit hundreds of slots apart (Pichu is #172, Pikachu #25), which is what this makes visible. Uncaught entries open too, but keep their secret — silhouette, "???", no types and no read-aloud — so browsing can't spoil what's still out there to find.
- A newly caught Pokémon is flagged with a **NEW** badge in the grid until its entry is opened, so a catch made mid-session can be found again without hunting through a thousand entries. The flag is stored separately from the collection itself.

## 9. Dashboard

Reached from "📊 My Progress" on the home screen. One card per Lesson Trail, each showing:

- The track's current level, in plain language.
- Days at the current level.
- Last-10 and Last-20 clean-answer progress bars.
- A live SVG trend chart of rolling accuracy, with gate lines at 80% and 100%, a gold star marker at each instant 10/10 promotion, and a dashed "Leveled up" line at each 16/20 promotion.

## 10. Battle Mode

A separate, unscored, replayable mini-game reached from the Start screen:

1. Two random, distinct Pokémon are shown, **A vs. B**, each with a 🔊 button to hear its name.
2. The player predicts a winner by tapping "Pick [Name]!"
3. A short "old-school" battle animation plays: both sprites shake, generic move-announcement text appears line by line.
4. The winner is decided by a **stat- and type-weighted random roll**: each Pokémon's real Base Stat Total represents its power level, a full 18-type effectiveness chart determines typing advantage, and `P(A wins) = powerA / (powerA + powerB)`. Both fighters' types are shown as colored badges.
5. The result is announced out loud and shown as a banner, along with whether the prediction was correct.
6. A running **session record** is shown at the top of the screen and persists across replays until the page is reloaded.

## 11. Results Screen

- A score pill (`X / Y correct`) and a tiered message/emoji based on performance.
- A **perfect run** gets a special animated reveal: the plain trophy emoji is replaced by the app's Pokéball icon "popping" in, followed by a randomly chosen legendary Pokémon with a "You earned [Name]!" caption.
- An editable "Number of challenges" field, so **Play Again** can start a new round at a different length.
- "Go Back" returns to the home screen.

## 12. Settings & Persistence

- **General**: Number of Challenges (governs session length across all active modes) and Wild Pokémon rate (grass encounter chance).
- **Per mode**: an on/off toggle for Spelling, Reading, Math, and Visual Math.
- **Per trail**: a frontier dropdown showing the current level in plain language ("Level 4a — Within 40, no regrouping"), which doubles as the manual placement control.
- **About**: a build number, the date that build was published, and the Last-Modified date of the HTML file this device actually loaded. Because a cached page reports the cached copy's date rather than today's, the two together tell a stale copy apart from a fresh one — the app is one static file that browsers cache aggressively, so "am I even running the new version?" is a real question. The build number has no build step behind it and is maintained by hand.
- Everything saves to `localStorage` on every change and reloads automatically on the next visit. Settings degrade gracefully: if storage is unavailable (e.g. private browsing) the app uses defaults instead of erroring.

## 13. Data & Offline Assets

All game data lives in **`data/*.csv`**, fetched and parsed at startup rather than embedded in code, so it can be maintained in a spreadsheet without touching the app. `data/README.md` documents every column and the editing traps. Rows may be reordered freely; the app sorts where order matters.

| File | Rows | Columns |
|---|---|---|
| `data/pokemon.csv` | 1,021 | `id`, `name`, `type1`, `type2`, `base_stat_total`, `rarity` |
| `data/items.csv` | 922 | `name`, `image`, `category` |
| `data/pronunciations.csv` | 184 | `name`, `say_as`, `source` |

- **Pokémon roster**: the full National Dex, Gen 1–9, minus 4 species whose names don't fit the plain-letter spelling mechanic (Nidoran♀/♂, Farfetch'd, Mr. Mime). 984 of the 1,021 names are plain single words suitable for the tile-spelling mechanic; the other 37 (Ho-Oh, the Tapu guardians, most Gen 9 Paradox Pokémon) are excluded from Spelling specifically but usable everywhere else. `rarity` marks **71 legendary** and **23 mythical** species.
- **Pokopia items**: **922** items across 12 categories. 108 are plain single words; 101 of those are placed across the Phonics Ladder's 9 patterns. The `image` column holds a bare slug — the `items/` folder and `.png` extension are added by the loader.
- **Offline, but served**: all artwork is stored locally in `pokemon/` and `items/` and referenced by relative path, and nothing is fetched from PokéAPI, GitHub or any fan site at runtime. Because the CSVs are fetched, though, the page must be **served over http(s)** — browsers block `fetch` on `file://` as cross-origin, so opening `index.html` by double-clicking it shows a load error instead. Once loaded, the browser cache covers repeat visits.
- **Failure is loud**: a missing or empty CSV replaces the page with a legible error rather than booting an app with silently empty pools.
- **Storage keys**: Lesson Trails progress, the Pokédex collection, the set of caught-but-not-yet-viewed Pokémon, the play streak, and general settings each persist under their own `localStorage` key.

## 14. Design Notes

- Warm, pastel, "cozy life-sim" visual style (leaf greens, sky blues, cream, sun yellow, berry pink) consistent across every mode.
- Mobile-first responsive layout: touch targets sized for small screens, a dedicated `@media (max-width:480px)` breakpoint, no horizontal page scroll.
- Speech synthesis is used in Spelling, Battle, Reading and the Pokédex — in Reading, only ever to name a picture (§7.2). Utterances are pinned to `en-US`, since otherwise the OS default voice applies its own language's phonetics to English spellings. Names the synthesiser mangles are respelled via `data/pronunciations.csv` (§13); overrides affect **speech only**.
- Read-aloud has one consistent affordance: a round speaker button sitting **on the picture itself**, at the lower-right of the circular frame, rather than a labelled button in the action row below. That holds across Spelling, Missing Letter, Read & Choose, and the Pokédex popup; Reverse Read & Choose applies the same idea at smaller scale, one speaker per picture option.
- The favicon is the app's own Pokéball mark, inlined as an SVG data URI so it needs no extra file.
- Instructional text is treated as a UX smell for this audience: a pre-reading child can't use text they can't read, so captions are omitted wherever the numbers, pictures, or controls already carry the meaning.
- Circular `.poke-frame` images are capped at 65% rather than fitted to the frame, so that even a zero-padding square image's bounding-box corners stay inside the circle's radius.
- No external font/script/style dependencies; everything needed to render and run ships in `index.html` plus the local `data/` and image folders.

## 15. Technical Architecture

- **Stack**: vanilla HTML/CSS/JS, no framework, no build step, no package manager.
- **Data loading**: `loadData()` fetches the three CSVs in parallel at startup and parses them with a small RFC-4180-ish parser that handles quoted fields, so a spreadsheet export round-trips. Boot is therefore async: event listeners bind immediately since they only fire on interaction, but anything reading the roster waits for the data.
- **State**: in-memory JS objects for the active session/battle; `localStorage` for everything persisted.
- **Rendering**: each mode has its own `render*()`/`mk*()` function pair; a shared `buildQueue()` assembles the session from whichever modes are active.
- **Lesson Trails engine**: each track is an ordered array of level objects (`{id, label, gen}`), with a shared `pickBand()` / `recordAttempt()` / `setFrontier()` layer handling the review/current/stretch mix and promotion logic identically across all four tracks. Per-track progress records the frontier, rolling clean/labored history, a capped `trend` log, and a `frontierSince` timestamp.
- **Assets**: local `pokemon/*.png` and `items/*.png`, referenced via relative paths from `index.html`. A Pokémon's artwork is found by `id` (`25` → `pokemon/25.png`); an item's by its `image` slug.
- **`tools/pronounce.html`**: a development-only audit page, not part of the app. Lists every name with a play button and collects the ones that sound wrong. It reads `POKEMON` and `SPEECH_OVERRIDES` out of a hidden `index.html` iframe, and provenance from `data/pronunciations.csv`, rather than keeping its own copy, so it cannot drift out of sync. Each row plays **Before** (the raw spelling) and **After** (the respelling) with an A/B comparison, and the respelling is editable so a fix can be tried by ear and copied back out.
