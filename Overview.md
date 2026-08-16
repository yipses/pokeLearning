# Poké Learning — Product Requirements Document

**Status:** Implemented (living document — reflects current shipped state)
**Owner:** Derek Yip
**Platform:** Single-file web app (`index.html`), works offline, mobile-friendly
**Audience:** Young learner(s) practicing spelling and math, themed around Pokémon

---

## 1. Summary

Poké Learning is a self-contained, no-build, no-dependency HTML/CSS/JS app that turns spelling and math practice into a set of short, randomized, Pokémon-themed mini-games. A session mixes challenges from whichever modes are turned on, tracks a score, and ends with a results screen. Alongside the practice modes: a Pokédex-style collection game (catch Pokémon hiding in the grass as you answer correctly, generation by generation), a daily play streak, and — in progress — **Lesson Trails**, a four-track progressive curriculum (Add/Subtract, Multiply↔Divide, Spelling, Reading) that replaces flat difficulty settings with a real, self-adjusting progression. A separate, unscored Battle mode lets the player pick a Pokémon and watch a stat/type-based "who would win" prediction game.

## 2. Goals

- Make repetitive spelling/math drilling feel like play, not homework.
- Support a range of skill levels and question styles (abstract numbers, visual/concrete representations, patterns, picture recall) rather than one fixed format.
- **Ramp difficulty automatically**, per skill, based on real performance — not a single manually-set difficulty a parent has to keep adjusting.
- Work fully offline and load fast — no build step, no external runtime dependencies, no account/login.
- Let a parent/guardian tune difficulty and content per mode without touching code.
- Remember settings and progress between visits.

## 3. Non-goals

- Not a full curriculum or progress-tracking system across sessions in the traditional sense (no accounts, no cloud sync) — though Lesson Trails now keeps a real per-skill progress record locally.
- Not a competitive/multiplayer game.
- Battle mode is not a real Pokémon battle simulator — it's a lightweight, fun prediction game, not a move-by-move damage calculator.

## 4. App Structure

Six top-level screens, all within one `index.html`:

| Screen | Purpose |
|---|---|
| **Start** | Play Streak, "Start Playing," "Pokémon Battle," "My Pokédex," "Settings" |
| **Settings** | Per-mode toggles and configuration, including the Math Trails and Spelling Trail frontier controls |
| **Play** | One challenge at a time, progress bar, grass encounter strip, quit button |
| **Results** | Score, tiered feedback (with a special reveal for a perfect run), replay controls |
| **Battle** | Standalone Pokémon-vs-Pokémon prediction game with its own back button |
| **Pokédex** | Every Pokémon, organized by generation, caught ones in color, uncaught ones as grey silhouettes |

Settings and Lesson Trails progress persist automatically to `localStorage` and are restored on load — nothing resets between visits unless browser storage is cleared.

## 5. Challenge Modes

Every mode below can be independently toggled on/off in Settings. When a session starts, the app builds a pool of active modes and, for each of the **N** total challenges (set in Settings), randomly draws from that pool — with the rule that **the same mode never repeats back-to-back** when more than one mode is active. If a mode is toggled on but has nothing enabled within it, it's excluded from the pool automatically.

### 5.1 Spelling Challenge
- Shows a mystery Pokémon's (or Pokopia item's) artwork; the player spells its name using shuffled letter tiles (tap) or the keyboard.
- Controls: 🔊 Say it (speaks the name aloud), 💡 Hint (reveals the next correct letter, capped at 3 uses per word — running out swaps in a new word from the same pool rather than leaving the player stuck), Backspace, Clear.
- Wrong letters are rejected immediately with a shake animation; correct letters lock in a slot.
- Configurable: min/max name length, drawn from a curated pool of **1,021 Pokémon** (984 of which have plain, single-word names suitable for the tile mechanic) and, if enabled, **922 Pokopia items** filtered by category (also restricted to plain single-word names).
- **Generation-gated**: the Pokémon word pool only draws from the lowest generation not yet fully caught in the Pokédex (see §5.6), so spelling content and catching progress advance together.
- **Planned, not yet built**: the Spelling *Phonics Ladder* — an early sequence of real-word levels (CVC → blends → digraphs → silent-e → vowel teams → r-controlled → compound words → multisyllabic) ahead of the current name-length-based practice, plus a *Missing Letter* mode (word mostly shown, fill in 1–5 chunk-aware blanks, no hints) staggered against full tile-spelling. See §7.

### 5.2 Math — Lesson Trails (Add/Subtract, Multiply↔Divide)
Two of the four Lesson Trails tracks (see §7) are live and have replaced the old fixed min/max Math settings:

- **Add/Subtract** — 8 levels, from "within 5" through "within 100 with regrouping," each level auto-generating a mix of addition and subtraction problems within that level's range. Levels 4a–5b specifically control for whether the ones-digit carries/borrows, so "no regrouping" and "with regrouping" are genuinely distinct difficulty steps, not just wider ranges.
- **Multiply↔Divide** — 12 interleaved steps sharing one frontier, starting at 1–3×1–3 and building up through 1–5, before division is introduced (also ramping 1–3 → 1–5), then continuing through harder-tables-only, flipped-orientation, and full-range steps for both operations.
- **~30% of questions** on either track become a 4-in-a-row skip-counting *pattern set* instead of a single equation (the previously-standalone Math Patterns mode, now woven directly into both trails) — step size is dynamic, any value where 4 repetitions fit the level's number range, so a low level only offers counting-by-1 while a high level can offer counting by up to 25.
- Auto-checks as the player types (waits until enough digits are entered to match the answer's length before judging). A **Next ▶** button appears once the answer is correct.
- Settings shows the current level for each track in plain language ("Level 4a — Within 40, no regrouping") via a dropdown that also serves as a manual override — moving it resets that track's progress window (see §7).

### 5.3 Visual Math
- Represents the same four operations as **pictures of Pokémon** instead of bare numbers, to build number-sense before/alongside abstract arithmetic:
  - **Addition**: two boxes of Pokémon icons side by side, joined by "+".
  - **Subtraction**: one box showing all the icons, with the subtracted amount crossed out by a bold drawn X.
  - **Multiplication**: several boxes of equal size joined by "+" signs — always **at least 2 groups**, since a single group (e.g. "5×1") doesn't actually demonstrate repeated addition.
  - **Division**: one box sliced into equal groups by divider lines.
- The equation (e.g. "5 × 5 = ?") is shown **before** the picture, not after — for multiplication specifically, showing the `+`-joined picture first and the `×` symbol second was visually contradictory.
- No instructional caption text (e.g. "How many in all?") — a pre-reading child can't use text they can't read, and the equation + picture already carry the meaning.
- Each operation has its own on/off toggle and independent Min/Max bounds (kept small, 1–6, so icon counts stay legible).
- Not yet tied to the Add/Subtract trail's frontier automatically — still configured via its own settings, though the design intent (§7) is for it to serve as the early concrete/pictorial lead-in and then fade to a review-only role once ranges exceed what's legible.

### 5.4 Match Challenge — Removed
Formerly a "concentration"-style picture-to-name matching round (N configurable pairs, optional Pokopia item mix-in with a 12-category toggle grid). Retired rather than kept as free play — it wasn't being used, and its core flaw (as pairs clear, the last couple become guessable by elimination rather than genuine reading) is exactly what the still-unbuilt **Reading Ladder** (§7) is meant to fix properly with a real trail. All of its settings and the Pokopia Item Categories filter grid — which had no other consumer once Match was gone — were deleted along with it.

### 5.5 Pokédex & Catching
- Every challenge screen shows a decorative grass strip. At a configurable rate (Settings, default 10%), it shakes to signal a Pokémon is hiding.
- Answering the current question correctly catches it: a popup shows **"Caught!"**, the Pokémon's artwork, Dex number, name, and type badges, dismissed with an **Okay** button (no auto-dismiss timer).
- Encounters are **generation-gated** — only the lowest generation not yet fully caught can appear, so progress moves through the National Dex in order rather than randomly across all 1,021 at once.
- The **Pokédex screen** (reachable from the home screen) shows every Pokémon organized by generation: caught ones in full color with their name, uncaught ones as a grey silhouette (`brightness(0)` filter on the same artwork, no separate asset) with the name hidden as "???", plus a live X/Y caught count per generation.

## 6. Battle Mode

A separate, unscored, replayable mini-game reached from the Start screen:

1. Two random, distinct Pokémon are shown, **A vs. B**, each with a 🔊 button to hear its name.
2. The player predicts a winner by tapping "Pick [Name]!"
3. A short "old-school" battle animation plays: both sprites shake, generic move-announcement text appears line by line.
4. The winner is decided by a **stat- and type-weighted random roll**:
   - Each Pokémon's real Base Stat Total (fetched once from PokéAPI and cached locally) represents its "power level."
   - A full 18-type effectiveness chart determines typing advantage.
   - `P(A wins) = powerA / (powerA + powerB)`.
   - Both fighters' types are shown as colored badges.
5. The result is **announced out loud** and shown as a banner, along with whether the player's prediction was correct.
6. A running **session record** is shown at the top of the screen and persists across replays until the page is reloaded.

## 7. Lesson Trails — Progressive Curriculum

**Status: two of four tracks built and live; the rest fully speced but not yet in code.**

Rather than one flat difficulty a parent sets and forgets (or has to keep manually adjusting), Lesson Trails gives each core skill its own **track** — an ordered sequence of levels — that advances on its own based on real performance. There are four tracks: **Add/Subtract**, **Multiply↔Divide** (built, §5.2), **Spelling** (planned), and **Reading** (planned, new).

**How a session mixes difficulty.** Each track has a **frontier** — the level currently being worked on. Rather than only ever asking frontier-level questions, each track's question pool blends three bands: **Review** (20%, a level below frontier — keeps old skills sharp), **Current** (60%, at frontier), **Stretch** (20%, a level above — light exposure to what's coming). This is deliberately not "master level N completely, then jump to level N+1" — interleaved practice across nearby difficulty outperforms single-difficulty blocked practice for retention, even though blocked practice feels easier in the moment.

**What counts as progress.** An answer only counts toward promotion if it's **clean** — correct on the first attempt, no wrong guesses, no hints. This tracking is invisible to the player: retrying until correct, or using a hint, still works exactly as it always has and still advances the session normally — it just doesn't count toward the promotion window. A track promotes to the next level via **either** 10 clean answers in a row (instant promotion) **or** 16 of the last 20 (80%) clean (standard pace) — whichever happens first. There's no demotion; a rough patch is absorbed by the Review band instead of rolling the frontier back. The frontier is also directly editable in Settings in either direction, for a parent who wants to place a kid ahead of (or behind) where auto-progression would put them — moving it resets that track's rolling window.

**Add/Subtract and Multiply↔Divide** are built exactly as described in §5.2, including Math Patterns woven into both as an occasional (~30%) alternate question shape rather than a separate mode.

**Spelling (planned)** splits into two phases on one trail: **Phase A**, a Phonics Ladder of 9 levels using real, audited words from the item catalog (CVC → floss-rule doubles → blends → digraphs → silent-e → vowel teams → r-controlled → compound words → multisyllabic — genuinely thin at the easiest 3 levels, only 3–4 real words each, richest at Compound Words and Multisyllabic with 18–24); **Phase B**, fluency practice on Pokémon names already known by ear, staggering two tasks per level — Full Spelling (empty tiles) and Missing Letter (word mostly shown, fill 1–5 chunk-aware blanks, no hints) — with Missing Letter always reaching a couple letters further than Full Spelling can, since it's an easier per-word task.

**Reading (planned)** is a new track, not gated to Spelling, built to fix the guessable-by-elimination flaw the now-removed Match mode had (§5.4): **Read & Choose** (one picture, five word options) and **Reverse Read & Choose** (one word, five pictures), ramping across word length and distractor difficulty (obviously-different vs. same-first-letter/length) across 6 levels. Two further modes are deliberately deferred as future work: **Rhyme Match** (blocked on most Pokémon names not reliably rhyming) and **Clue Words** (blocked on the app not having attribute data — color, size, material — tagged per Pokémon/item).

**Dashboard (planned)** — a status screen with one card per track: current level, Last-10/Last-20 progress bars, days at the current level, and a trend chart of rolling accuracy against both promotion thresholds.

## 8. Results Screen

- Shows a score pill (`X / Y correct`) and a tiered message/emoji based on performance.
- A **perfect run** gets a special animated reveal: the plain trophy emoji is replaced by the app's Pokéball icon "popping" in, followed by a randomly chosen legendary Pokémon with a "You earned [Name]!" caption.
- Includes an editable "Number of challenges" field so **Play Again** can start a new round at a different length.
- "Go Back" returns to the home screen.

## 9. Data & Offline Assets

- **Pokémon roster**: **1,021** Pokémon (the full National Dex, Gen 1–9, minus 4 species whose names don't fit the plain-letter spelling mechanic: Nidoran♀/♂, Farfetch'd, Mr. Mime). Each entry carries its name, National Dex ID, real type(s), and real Base Stat Total. Sourced from PokéAPI's sprites repository (verified byte-identical against the original 147 before the bulk pull).
- **Pokopia items**: **922** curated items (name, image, category) across 12 categories, sourced from `pokopiahabitats.com` for artwork and Bulbapedia's item table for category/name data, cross-referenced for accuracy (149/150 exact-name matches against the original curated set before trusting the source).
- **Fully offline**: all Pokémon and item artwork is downloaded and stored locally (`pokemon/` and `items/` folders) and referenced by relative path — the app does not depend on PokéAPI, GitHub, Bulbapedia, or Pokopia fan sites being reachable at runtime.
- **Lesson Trails progress** and the **Pokédex collection** are stored in `localStorage` under their own keys, separate from general settings.

## 10. Settings & Persistence

- A single **"Number of Challenges"** count governs session length across all active modes, now living in Settings under General rather than the home screen.
- Math Trails frontier (Add/Subtract, Multiply↔Divide) is shown and editable per track.
- All per-mode toggles, min/max bounds, and the grass encounter rate save to `localStorage` on every change and reload automatically on next visit.
- Settings degrade gracefully: if storage is unavailable (e.g. private browsing) the app just uses defaults instead of erroring.

## 11. Design Notes

- Warm, pastel, "cozy life-sim" visual style (leaf greens, sky blues, cream, sun yellow, berry pink) consistent across every mode.
- Mobile-first responsive layout: touch targets sized for small screens, a dedicated `@media (max-width:480px)` breakpoint, no horizontal page scroll.
- Speech synthesis (`speechSynthesis` API) used throughout — spelling and battle mode — for read-aloud support.
- Instructional text is treated as a UX smell for this audience: captions a pre-reading child can't parse have been removed from Visual Math and Math Patterns in favor of letting the numbers/pictures speak for themselves.
- No external font/script/style dependencies; everything needed to render and run ships in the one HTML file plus the local image folders.

## 12. Technical Architecture

- **Stack**: vanilla HTML/CSS/JS, no framework, no build step, no package manager.
- **State**: in-memory JS objects for the active session/battle; `localStorage` for persisted settings, Lesson Trails progress, the Pokédex collection, and the play streak.
- **Rendering**: each mode has its own `render*()`/`make*()` function pair; a shared `buildQueue()` assembles the session from whichever modes are active.
- **Lesson Trails engine**: each track is an ordered array of level objects (`{id, label, gen}`), with a shared `pickBand()`/`recordAttempt()`/`setFrontier()` layer handling the review/current/stretch mix and promotion logic identically across tracks — a track only needs to supply its level list and generator functions.
- **Assets**: local `pokemon/*.png` and `items/*.png`, referenced via relative paths from `index.html`.

## 13. Possible Future Directions

*(Not committed — ideas surfaced during development, not scheduled work.)*

- **Rhyme Match** and **Clue Words** reading modes (see §7) — both deliberately deferred pending real-word/attribute data.
- Per-session or historical stats beyond the in-memory Battle record and the Lesson Trails Dashboard.
- Sentence-level reading comprehension, beyond single-word Read & Choose.
- Difficulty presets that bundle several settings at once.
- Tying Visual Math's active range directly to the Add/Subtract trail's frontier, rather than configuring it independently.
