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
| **Start** | Three status tiles, one of your Pokémon shown big, then "Start Playing," "Pokémon Battle," "My Pokédex," "My Progress," "Settings" |
| **Settings** | Per-mode toggles and each trail's frontier control |
| **Play** | One challenge at a time, progress bar, grass encounter strip, quit button |
| **Results** | The three status tiles, what was caught this round, replay controls |
| **Battle** | Standalone Pokémon-vs-Pokémon prediction game with its own back button |
| **Pokédex** | Every Pokémon, one generation per tab, caught ones in color, uncaught ones as grey silhouettes |
| **Dashboard** | One progress card per Lesson Trail |

Settings, Lesson Trails progress, the Pokédex collection, and the play streak persist to `localStorage` and are restored on load.

## 5. Sessions

Each mode toggles on/off in Settings. A session draws each of its **N** challenges at random from the active modes, never repeating the same mode back-to-back. A mode with nothing enabled inside it drops out of the pool automatically.

## 6. Lesson Trails

Each core skill has its own **track** — an ordered sequence of levels — that advances on its own. There are four: **Spelling**, **Reading**, **Add/Subtract**, and **Multiply↔Divide**. All four share one progression engine; a track supplies only its level list and generator functions.

**Difficulty blend.** Each track has a **frontier** — the level being worked on. Its question pool blends three bands: **Review** (20%, below frontier), **Current** (60%), **Stretch** (20%, above). Deliberately not "master level N, then jump to N+1"; see `LessonTrails.md`.

**Promotion.** Only **clean** answers count — right on the first attempt, no wrong guesses, no hints. A track promotes on **100% of the last 5, or 80% of the last 10**, whichever lands first — short windows, so a child who has the level isn't made to prove it twenty times, and one they haven't got comes back through the Review band anyway. Both percentages are **per level**, read from the Spelling and Reading CSVs, so the two trails can be tuned apart without touching code; Math has no CSV yet and uses those same figures as its fallback. No demotion; a rough patch is absorbed by the Review band. The tracking is invisible: retrying or using a hint still works and still advances the session, it just doesn't count.

**Manual placement.** Every frontier is editable in Settings in either direction. Moving one resets that track's rolling window.

## 7. Challenge Modes

### 7.1 Spelling Trail

**25 levels, defined entirely in `data/spelling_levels.csv`.** Nothing about the ladder lives in code: each row names the pools its level draws from and how much help it gives.

Every row selects words three ways at once:

| Column | Selects |
|---|---|
| `word_level` | single-word items graded at or below this phonics level (1–9) |
| `compound_level` | multi-word items whose hardest component word is at or below this; `0` switches compounds off |
| `pokemon_letters` | Pokémon names up to this many letters, generation-gated as ever |

Pokémon are gated by length rather than by phonics level because invented names have no decoding pattern to grade — length is the only honest measure for them. Item words do have one: the grading lives in `data/word_levels.csv` and is rolled up per item in `data/item_levels.csv` (§13).

The ladder is nine tiers of three, and within a tier only **`hinted_pct`** changes — the share of the word given away, 50% → 25% → 0%:

- **Above 0% it's Missing Letter** — the word appears with that share of its letters showing and the rest as blanks, filled by tapping from a bank of the missing **chunks**. Blanks are placed by a `chunkWord()` tokenizer that treats digraphs, blends, vowel teams and r-controlled vowels as atomic, so a blank never splits a sound; whole chunks are hidden until the level's letter target is reached, always leaving one chunk visible.
- **At 0% it's Full Spelling** — empty slots, the whole word built from shuffled tiles (tap or keyboard). Controls: 🔊 on the picture, 💡 Hint, Backspace, Clear.

**Both tasks answer the same way, in the same units: tap a tile holding a chunk.** `torch` is three slots and three tiles — `T`, `OR`, `CH` — in both. A chunk is the thing with a sound, so a tile can say what it is, and the same group is the same group on every screen. Typing still works in Full Spelling: keystrokes buffer until they complete the chunk that comes next, so `t-o-r-c-h` fills `T`, then `OR`, then `CH`.

### 7.1a Sounding out

**A correct placement plays the sound of what was just completed**, and a wrong one is silent — a child who taps for the noise must not be rewarded for guessing. In Full Spelling a tile is one letter, so a sound plays only when that letter *finishes* a chunk: spelling `shutter` says /sh/ when the h lands, never /s/ then /h/.

**The sound depends on the word, not just the letter.** `a` is one sound in `cat`, another in `cake`, and a third in `car`. The chunker has already made `ar` a single unit, so r-controlled vowels, vowel teams, digraphs and blends are context-free; that leaves lone vowels, and the rule reads the word around them — a vowel followed by one consonant and a final `e` is long, otherwise short. The final `e` says nothing at all, which is the correct thing to teach.

**When the word is complete it is spoken whole** — /k/ /a/ /t/ … "cat". Sounding out, then blending back.

Respellings live in `data/phonemes.csv` (§13), keyed by chunk and context, because a speech synthesiser can't be handed a bare phoneme. Every one must be a **pronounceable syllable**: a synthesiser given `ch` or `lll` spells them out — "see-aitch", "ell ell ell" — so they are written `chuh` and `luh`. The schwa on a continuant is the standard phonics compromise; a synthesiser cannot produce a clean /l/. Anything with no row stays **silent** rather than guessing: a wrong sound teaches a wrong thing.

`tools/phonemes.html` plays every row for checking by ear, shading the ones a rough test thinks may not be pronounceable and collecting whatever is marked wrong.

**`max_hints`** is per level and applies to both tasks. It rises as `hinted_pct` falls, so the level that gives away least of the word offers most help finding the rest. A hint costs the answer its "clean" status either way.

**Pokémon-branded items are excluded from Spelling.** 25 item names are built from a Pokémon name — `Hoppip water bottle`, `Pikachu doll` — and their phonics level is fiction: an invented proper noun is memorised, not decoded, so asking a child to produce one isn't spelling practice. They're flagged `proper_noun` in `data/item_levels.csv` and skipped here. Reading keeps them, because recognising a name the child already knows by sight is a fair reading task, and the names themselves remain reachable through the Pokémon pool under the generation gate.

The earliest levels have single-figure pools, so the generator never repeats the immediately-previous word for a track when there's an alternative.

### 7.2 Reading Trail

**10 levels, defined entirely in `data/reading_levels.csv`,** selecting words by exactly the same three columns as Spelling — one vocabulary grading feeds both trails, so a word met in Reading at level 4 is a word Spelling asks for at level 4. The two frontiers move independently, which lets Reading run ahead: recognising a word is easier than producing it.

Two formats, picked at random per question:

- **Read & Choose** — one picture, N word options.
- **Reverse Read & Choose** — one written word, N picture options.

Difficulty ramps on two columns of its own:

- **`wrong_answers`** — how many decoys, so the choice count is 3 at level 1, 4 at level 2, and 5 from level 3 on.
- **`distractor_level`** — *another reading level*, whose pool supplies the wrong answers. It always points at or above the level's own row, so decoys are drawn from a superset of the target pool and the child meets harder words as options before ever being asked to read them. This replaced an older "tricky distractor" flag: difficulty now comes from pool breadth rather than from hand-picking same-length decoys.

**Read-aloud rule: pictures may be named aloud; words never are.** Read & Choose prompts with a picture, which a child may not recognize, so a 🔊 Say it names it — resolving the prompt while leaving the written options to be read. Reverse Read & Choose prompts with the written word and therefore has no speaker on the prompt at all; each picture option carries its own instead. In both modes the child must connect a spoken name to a written one, and nothing ever reads a word aloud to them. There are no hints on either mode.

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
- **A pity timer caps droughts.** A pure per-question roll can go cold for a long stretch, which to a young child reads as the feature being broken rather than unlucky, so an encounter is *guaranteed* the moment a drought runs **one question past the average wait** — the 11th question at 10%, the 3rd at 50%. The counter **resets at the start of every round** — each round is its own experience, so a cold streak never follows the child into the next one.
- **The Settings field is the outcome, not the dice roll.** A guarantee adds encounters on top of the roll, so a raw roll of R always produces more than R — and "longer than average" is a one-in-three event, not a rare one, so the gap is several points (a raw 25% roll with this pity lands at 33%). The app therefore solves for the roll that *lands* on the number: for a drought capped at `k`, the encounter rate is `p / (1 - (1-p)^k)`, which increases with `p`, so a short binary search finds it. Set 25% and the roll used is 11.2%, with the pity making up the difference. Measured over 200,000 questions per setting, every value from 1% to 100% lands on itself.
- Answering the current question correctly catches it: a popup shows **"Caught!"**, the Pokémon's artwork, Dex number, name, and type badges, dismissed with an **Okay** button (no auto-dismiss timer). A **catch is celebrated**: confetti falls through the card and a burst of light blooms behind the artwork. Rarer catches get half again as many pieces and a gold palette, so the fuss itself signals the rarity to a child who can't yet read the chip. It fires on real catches only — browsing the Pokédex opens the same card dozens of times, and confetti every time would be noise — and is switched off entirely under `prefers-reduced-motion`. Catching a legendary or mythical species changes the banner to **"✨ Legendary Catch!"** / **"✨ Mythical Catch!"**.
- Encounters are **generation-gated** — only the lowest generation not yet fully caught can appear, so progress moves through the National Dex in order rather than randomly across all 1,021 at once. The Pokémon side of both the Spelling and Reading pools respects the same gate.
- The **Pokédex screen** is organized into **generation tabs** — `Gen 1` … `Gen 9`, one row that scrolls sideways on a phone — showing one generation's grid at a time. It opens on whichever generation the collection gate is currently on, not always Gen 1, and a tab whose generation is fully caught is outlined in green. All nine tabs fit the content column on a desktop window; below that width the strip scrolls, and **‹ › arrow buttons appear** — a touchscreen can swipe the strip but a mouse cannot, so the arrows are the desktop affordance. They exist only while the strip actually overflows and each one greys out at its end. One generation at a time keeps the visible grid to at most 160 cells instead of 1,021 and puts Gen 9 one tap away instead of a very long scroll.
- Within a tab: caught entries show in full colour with their name; uncaught ones are a grey silhouette (a `brightness(0)` filter on the same artwork, no separate asset) with **no name text at all** — the outline and the Dex number say it, where a row of `???` would be a word to decode for no payoff (§14.1). A live X/Y caught count sits in the generation header.
- **Legendary and mythical species are called out**: a gold cell with a ✨ badge in the grid, a matching chip above the type badges in the detail popup, and a per-generation tally in each generation header (`✨ 2/5 · 3 / 147`). The marker shows on **uncaught** slots too — it reveals nothing about which Pokémon lives there, and flagging the slot is the point: it marks something worth hunting for rather than only rewarding the find afterwards. Name and rarity chip stay hidden until it's caught.
- **Every entry is tappable**, opening a detail popup. A caught entry reads: larger artwork, the Dex number, the name, **"Welcome back!"**, type badges, any rarity chip, a 🔊 speaker, and its **evolution family**. An uncaught one gets the outline, its number and its **type** — nothing else: no name, no greeting, no read-aloud. Type is the one thing shown either way; it is a single short word, it says something useful about a slot still to fill, and it doesn't name what's hiding in it.
- **The popup keeps a back trail.** Tapping a relative replaces what's on screen with that relative, so the primary button becomes **← Back** and walks the hops in reverse; **Okay** returns only once you're back at the entry you opened. There is never more than one button. This matters most on a catch reveal, where Okay also advances the round: while you're a hop deep in the family tree, Back is the only exit, so the catch can't be skipped from a screen that isn't the catch.
- **The evolution strip** shows one step back and every step forward, with the current entry highlighted. Relatives not yet caught appear as unlabelled silhouettes, and every member is tappable — so a three-stage line is two taps rather than a wall of sprites, and branching families (Eevee's eight) simply wrap. National Dex order puts 83% of families side by side already, but cross-generation evolutions can sit hundreds of slots apart (Pichu is #172, Pikachu #25), which is what this makes visible. Uncaught entries open too, but keep their secret — silhouette and type only, no name and no read-aloud — so browsing can't spoil what's still out there to find.
- A newly caught Pokémon is flagged with a **NEW** badge in the grid until its entry is opened, so a catch made mid-session can be found again without hunting through a thousand entries. The flag is stored separately from the collection itself.

## 8b. Home Tiles

Three tiles across the top of the Start screen, each tappable:

| Tile | Shows | Goes to |
|---|---|---|
| 🎯 **Rounds Today** | rounds finished today, against the daily goal; turns green once met | Dashboard |
| 📕 **Pokémon** | caught/total for the **current generation only** — the one the collection gate is on | Pokédex |
| 🔥 **Day Streak** | consecutive days that met the rounds goal | Dashboard |

A "round" is one full session; how many questions make up a round, and how many rounds a day the streak needs, are both Settings values.

**The streak holds until the day actually ends.** It counts consecutive days ending today *or yesterday*, so a streak earned yesterday still reads correctly at 8am before anything has been played, and only breaks once a whole day has passed without meeting the goal. Daily round counts are kept indefinitely rather than pruned to a window — pruning would silently cap the streak at the window's length.

## 8c. Home Showcase

Below the tiles, the middle band of the Start screen shows **one of the child's own Pokémon**, big: artwork in a circular frame, its name, its Dex number, and **"Welcome back!"**. The whole card is a button — tapping it re-rolls the pick, as does every return to the home screen.

It is a trophy shelf, not a teaser: it only ever shows a species already caught. It prefers the generation being worked on but falls back to the whole collection, so a freshly opened generation — where nothing is caught yet — still shows off the previous one's catches rather than going blank.

**Before anything at all is caught** there is no trophy to show, so the band falls back to a silhouette and its **type badges** — an outline and one short word, no sentence (§14.1). The mystery shape is the invitation; a line of text telling a pre-reader to press Start is not.

## 9. Dashboard

Reached from "📊 My Progress" on the home screen. One card per Lesson Trail, each showing:

- The track's current level, in plain language.
- Days at the current level.
- Last-10 and Last-20 clean-answer progress bars.
- A live SVG trend chart of rolling accuracy, with gate lines at 80% and 100%, a gold star marker at each instant 5/5 promotion, and a dashed "Leveled up" line at each 8/10 promotion.

## 10. Battle Mode

A separate, unscored, replayable mini-game reached from the Start screen:

1. Two random, distinct Pokémon are shown, **A vs. B**, each with a 🔊 button to hear its name.
2. The player predicts a winner by tapping "Pick [Name]!"
3. A short "old-school" battle animation plays: both sprites shake, generic move-announcement text appears line by line.
4. The winner is decided by a **stat- and type-weighted random roll**: each Pokémon's real Base Stat Total represents its power level, a full 18-type effectiveness chart determines typing advantage, and `P(A wins) = powerA / (powerA + powerB)`. Both fighters' types are shown as colored badges.
5. The result is announced out loud and shown as a banner, along with whether the prediction was correct.
6. A running **session record** is shown at the top of the screen and persists across replays until the page is reloaded.

## 11. Results Screen

- A heading — **"Round finished!"** — and the same three status tiles as the Start screen, so finishing a round shows the progress it just moved.
- **What was caught this round**, as large tappable cards that open the full detail popup — the reward is the point of this screen, so the artwork is sized to be looked at. Three fit a row at any phone width; more wrap. When nothing was caught, a plain line says so rather than inventing a consolation prize.
- **Play Again**, which starts another round at the length set in Settings, and **Go Back**.

**There is deliberately no score.** Every mode retries until the answer is correct, so a finished round is always 100% — a score would be a number that cannot vary, and the tiered praise it drove ("Perfect! You're a Champion!") fired every single time. The old perfect-run reward went with it: it announced "You earned Mewtwo!" and granted nothing, so a child who went looking for it in their Pokédex never found it. Performance is measured where it means something — clean answers driving the Lesson Trails, shown on the Dashboard.

## 12. Settings & Persistence

- **General**: Questions per round (session length across all active modes, default 10), Rounds per day (the streak goal, default 2), and **Expected drop** — out of 100 questions, roughly how many hide a Pokémon. It is the measured outcome, pity timer included, not the underlying roll (§8).
- **Per mode**: an on/off toggle for Spelling, Reading, Math, and Visual Math.
- **Per trail**: a frontier dropdown showing the current level in plain language ("Level 4a — Within 40, no regrouping"), which doubles as the manual placement control.
- **About**: a build number, the date that build was published, and the Last-Modified date of the HTML file this device actually loaded. Because a cached page reports the cached copy's date rather than today's, the two together tell a stale copy apart from a fresh one — the app is one static file that browsers cache aggressively, so "am I even running the new version?" is a real question. The build number has no build step behind it and is maintained by hand.
- Everything saves to `localStorage` on every change and reloads automatically on the next visit. Settings degrade gracefully: if storage is unavailable (e.g. private browsing) the app uses defaults instead of erroring.

## 13. Data & Offline Assets

All game data lives in **`data/*.csv`**, fetched and parsed at startup rather than embedded in code, so it can be maintained in a spreadsheet without touching the app. `data/README.md` documents every column and the editing traps. Rows may be reordered freely; the app sorts where order matters.

| File | Rows | Columns |
|---|---|---|
| `data/pokemon.csv` | 1,021 | `id`, `name`, `type1`, `type2`, `base_stat_total`, `rarity`, `evolves_from` |
| `data/items.csv` | 922 | `name`, `image`, `category` |
| `data/pronunciations.csv` | 184 | `name`, `say_as`, `source` |
| `data/word_levels.csv` | 807 | `word`, `level`, `pattern`, `letters`, `syllables`, `compound_parts`, `also_matches`, `proper_noun`, `used_in_items`, `previous_level`, `review` |
| `data/item_levels.csv` | 922 | `item`, `level`, `kind`, `words`, `components`, `component_levels`, `proper_noun`, `letters`, `longest_word`, `spellable` |
| `data/spelling_levels.csv` | 25 | `level`, `word_level`, `compound_level`, `pokemon_letters`, `hinted_pct`, `max_hints`, `promote_5_pct`, `promote_10_pct` |
| `data/reading_levels.csv` | 10 | `level`, `word_level`, `compound_level`, `pokemon_letters`, `wrong_answers`, `distractor_level`, `promote_5_pct`, `promote_10_pct` |
| `data/phonemes.csv` | 86 | `chunk`, `context`, `say_as`, `notes` |

- **Pokémon roster**: the full National Dex, Gen 1–9, minus 4 species whose names don't fit the plain-letter spelling mechanic (Nidoran♀/♂, Farfetch'd, Mr. Mime). **1,020 of the 1,021 are spellable** — a name may contain a space or a hyphen, so Iron Hands and Ho-Oh both work; only Type: Null is excluded, for its colon. `rarity` marks **71 legendary** and **23 mythical** species.
- **Pokopia items**: **922** items across 12 categories, of which **909** can be spelt — the other 13 carry an apostrophe, accent, period or digit and are dropped from both word trails. **25 are excluded from Spelling** as Pokémon-branded (§7.1). The `image` column holds a bare slug — the `items/` folder and `.png` extension are added by the loader.
- **Offline, but served**: all artwork is stored locally in `pokemon/` and `items/` and referenced by relative path, and nothing is fetched from PokéAPI, GitHub or any fan site at runtime. The one external request is the Google Fonts stylesheet (§14), which degrades to a fallback stack if it fails. Because the CSVs are fetched, though, the page must be **served over http(s)** — browsers block `fetch` on `file://` as cross-origin, so opening `index.html` by double-clicking it shows a load error instead. Once loaded, the browser cache covers repeat visits.
- **The ladders are data, not code.** `index.html` holds no level list, no word list and no promotion constant — it reads all four from CSV at boot. There is deliberately no fallback copy compiled in: a ladder that exists in two places drifts, and the spreadsheet is the one that gets edited.
- **Word grading**: `word_levels.csv` grades every distinct word in the item catalogue against the nine phonics patterns; `item_levels.csv` is the derived per-item view, where a single-word item takes its own level and a multi-word item takes its hardest component's. Both are regenerated by `tools/classify_words.py`. `word_levels.csv` is the file to correct — the item view follows from it.
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
- **Type**: the UI is set in **M PLUS Rounded 1c**, the closest freely-licensed match to FOT-Rodin — the rounded Japanese gothic the Pokémon Switch games use — so the app reads as a sibling of the games it borrows from. Loaded from Google Fonts with `display=swap` and a rounded fallback stack (`Baloo 2`, `Varela Round`, `Trebuchet MS`), so the page never blocks on it and never falls back to something angular. This one stylesheet is the app's **only** external dependency; no scripts, no other styles — everything else ships in `index.html` plus the local `data/` and image folders.

### 14.1 Copy rules

The reader is five and still learning to read. Every word on a child-facing screen costs them effort, so:

- **Never write a long sentence.** One to four words per line. `Try again!` — not `Not quite, try that blank again!`.
- **Words have to earn their place.** A name, a number, `Welcome back!` — things worth the effort of decoding. Anything a picture, a number, or a control already says gets no text at all.
- **Never make the child read a placeholder.** No `???`, no `Not Caught`. A grey outline already says "you haven't found this one".
- **Say it plainly, not cleverly.** No wordplay, no encouragement paragraphs, no "Oops".
- **Adult-facing screens are exempt.** Settings, the Dashboard and `data/README.md` are read by a parent and can explain themselves at length.

## 15. Technical Architecture

- **Stack**: vanilla HTML/CSS/JS, no framework, no build step, no package manager.
- **Data loading**: `loadData()` fetches the three CSVs in parallel at startup and parses them with a small RFC-4180-ish parser that handles quoted fields, so a spreadsheet export round-trips. Boot is therefore async: event listeners bind immediately since they only fire on interaction, but anything reading the roster waits for the data.
- **State**: in-memory JS objects for the active session/battle; `localStorage` for everything persisted.
- **Rendering**: each mode has its own `render*()`/`mk*()` function pair; a shared `buildQueue()` assembles the session from whichever modes are active.
- **Lesson Trails engine**: each track is an ordered array of level objects (`{id, label, gen}`), with a shared `pickBand()` / `recordAttempt()` / `setFrontier()` layer handling the review/current/stretch mix and promotion logic identically across all four tracks. Per-track progress records the frontier, rolling clean/labored history, a capped `trend` log, and a `frontierSince` timestamp.
- **Assets**: local `pokemon/*.png` and `items/*.png`, referenced via relative paths from `index.html`. A Pokémon's artwork is found by `id` (`25` → `pokemon/25.png`); an item's by its `image` slug.
- **`tools/phonemes.html`**: a development-only audit page for `data/phonemes.csv`. Every row with a play button, using the app's own voice settings so it audits what a child actually hears; a rough pronounceability test shades the doubtful ones amber and can play only those; anything marked wrong collects into a copyable list. Built after a third of all spoken sounds turned out to be respellings a synthesiser spells out rather than says.
- **`tools/pronounce.html`**: a development-only audit page, not part of the app. Lists every name with a play button and collects the ones that sound wrong. It reads `POKEMON` and `SPEECH_OVERRIDES` out of a hidden `index.html` iframe, and provenance from `data/pronunciations.csv`, rather than keeping its own copy, so it cannot drift out of sync. Each row plays **Before** (the raw spelling) and **After** (the respelling) with an A/B comparison, and the respelling is editable so a fix can be tried by ear and copied back out.
