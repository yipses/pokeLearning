# Poké Learning — Product Requirements Document

**Owner:** Derek Yip
**Platform:** Web app — one page (`index.html`) plus `data/*.csv` and local artwork. Served over http(s), works offline once loaded, mobile-first
**Audience:** Young learner(s) practicing spelling, reading, and math, themed around Pokémon

> This document describes **what the app does today** — nothing else. How it got here, what changed when and why, what's still open, and what might come next all live in `progress.md`. The curriculum design rationale behind Lesson Trails lives in `LessonTrails.md`.

---

## 1. Summary

Poké Learning is a no-build, no-dependency HTML/CSS/JS app — one page plus a folder of CSV data and local artwork — that turns spelling, reading, and math practice into short, randomized, Pokémon-themed mini-games. A session mixes challenges from whichever modes are turned on, tracks a score, and ends with a results screen.

Difficulty is not a setting a parent picks and re-picks. Ten **Lesson Trails** — Spelling, Reading, and eight maths tracks — each hold their own level and advance on their own based on real performance. Alongside the practice modes: a Pokédex-style collection game (catch Pokémon hiding in the grass as you answer correctly, generation by generation), a daily play streak, a progress screen, and a separate, unscored Battle mode where the player picks a Pokémon and watches a stat/type-based "who would win" prediction play out.

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
| **Start** | One line carrying three counters, the wordmark and the gear, a 2×2 panel of current levels, one of your Pokémon shown big with its generation count, then "Start Playing" and "Pokémon Battle" |
| **Settings** | The chrome, then per-mode toggles and each trail's frontier control |
| **Play** | One challenge at a time, progress bar, grass encounter strip, ✕ to quit |
| **Results** | The three status tiles, what was caught this round, replay controls |
| **Battle** | Standalone Pokémon-vs-Pokémon prediction game; its session record sits beside the screen name |
| **Pokédex** | The HUD, a ✕ beside **POKÉDEX**, generation tabs, then one generation's grid — caught in colour, uncaught as grey silhouettes |
| **My progress** | The chrome, a 7-day rounds chart, a card each for Spelling and Reading, then one card per maths family |

Settings, Lesson Trails progress, the Pokédex collection, and the play streak persist to `localStorage` and are restored on load.

## 5. Sessions

**A round ends after N questions answered well enough, not after N questions shown.** Every mode retries until the answer is right, so counting questions *shown* meant a round could be finished by guessing through it. A question counts toward the round when it is answered with at most **`Mistakes allowed`** slips — a Settings value, default 1, where a slip is a wrong tap *or* a hint. Hints count because hinting through a word to reach the end of a round is the same loophole in a different costume.

**Two different bars, deliberately kept apart.** The Lesson Trails still promote only on a **spotless** question — nothing wrong at all, no hints — exactly as before. `Mistakes allowed` governs only whether a question moves the *round* along. Loosening the round does not loosen the ladder.

**The progress bar measures credits**, so guessing your way through a question leaves it exactly where it was. That is the feedback the change exists to give.

Each mode toggles on/off in Settings. A session of **N** challenges is **split in thirds** — spelling, reading, maths — rather than drawn evenly across every track, and never repeats the same mode back-to-back. The maths third is shared among whichever maths tracks are currently open; without the split, a fully-unlocked child would get eight questions in ten as maths purely because maths has the most tracks. A mode with nothing enabled inside it drops out of the pool automatically.

## 6. Lesson Trails

Each core skill has its own **track** — an ordered sequence of levels — that advances on its own. There are ten: **Spelling**, **Reading**, and eight maths tracks (§7.3). All of them share one progression engine; a track supplies only its level list and generator functions. Home and My progress collapse the eight maths tracks into two families, `+ / −` and `× / ÷`, so the screens stay readable — but every track keeps its own level, its own rolling window and its own promotion.

**Difficulty blend.** Each track has a **frontier** — the level being worked on. Its question pool blends three bands: **Review** (20%, below frontier), **Current** (60%), **Stretch** (20%, above). Deliberately not "master level N, then jump to N+1"; see `LessonTrails.md`.

**Promotion.** Only **clean** answers count — right on the first attempt, no wrong guesses, no hints. A track promotes on **100% of the last 5, or 80% of the last 10**, whichever lands first — short windows, so a child who has the level isn't made to prove it twenty times, and one they haven't got comes back through the Review band anyway. Both percentages are **per level**, read from the Spelling and Reading CSVs, so the two trails can be tuned apart without touching code; Maths has its own table with three gates — 5 at 100%, 10 at 90%, 20 at 85%. No demotion; a rough patch is absorbed by the Review band. The tracking is invisible: retrying or using a hint still works and still advances the session, it just doesn't count.

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

- **Above 0% it's Missing Letters** — the word appears with that share of its letters showing and the rest as blanks, filled by tapping from a bank of **chunks**. Blanks are placed by a `chunkWord()` tokenizer that treats digraphs, blends, vowel teams and r-controlled vowels as atomic, so a blank never splits a sound; whole chunks are hidden until the level's letter target is reached, always leaving one chunk visible.

  **The bank is padded with decoys to a floor of four tiles.** Holding only the missing chunks made a one-blank word a guaranteed tap — `MEW` showed `M` and a single `EW` tile — which was 9% of all Missing Letters questions and 45% of level 2. Four blanks or more get no decoys, so the hard end is untouched. Each decoy is drawn from the same phonics class as a chunk it competes with — single vowels, vowel teams, r-controlled vowels, digraphs, blends, single consonants — and is never a chunk the word contains. Class matters: beside a vowel team, `str` can be ruled out by eye without knowing the answer, and `oo` cannot. A wrong tap shakes the tile, says so, and costs the clean answer.
- **At 0% it's Full Spelling** — empty slots, the whole word built from shuffled tiles (tap or keyboard). Controls: 🔊 on the picture, 💡 Hint, Backspace, Clear.

**Both tasks answer the same way, in the same units: tap a tile holding a chunk.** `torch` is three slots and three tiles — `T`, `OR`, `CH` — in both. A chunk is the thing with a sound, so a tile can say what it is, and the same group is the same group on every screen. Typing still works in Full Spelling: keystrokes buffer until they complete the chunk that comes next, so `t-o-r-c-h` fills `T`, then `OR`, then `CH`.

### 7.1a Sounding out

**A correct placement plays the sound of what was just completed**, and a wrong one is silent — a child who taps for the noise must not be rewarded for guessing. In Full Spelling a tile is one letter, so a sound plays only when that letter *finishes* a chunk: spelling `shutter` says /sh/ when the h lands, never /s/ then /h/.

**The sound depends on the word, not just the letter.** `a` is one sound in `cat`, another in `cake`, and a third in `car`. The chunker has already made `ar` a single unit, so r-controlled vowels, vowel teams, digraphs and blends are context-free. Four chunks are not, and each reads the letters around it:

| chunk | rule |
| --- | --- |
| lone vowel | a vowel followed by one consonant and a final `e` is long, otherwise short. The final `e` says nothing at all, which is the correct thing to teach |
| `c` | /s/ before `e`, `i` or `y` — `city`, `ice`, `dance`. Otherwise /k/ |
| `y` | /ee/ ending a word that has another vowel (`berry`), /igh/ when it is the word's only vowel (`fly`), short /i/ inside a word (`crystal`), consonant /y/ at the start (`yamper`) |
| `ow` | /oh/ at the end of a word — `snow`, `arrow`. /ow/ elsewhere — `flower` |

Position is measured **within the word**, not the whole name, so the silent `e` in `Ice cream` is still at an end.

`g` looks like it wants the same rule as `c` and deliberately doesn't have one: across the game's vocabulary soft-g would be wrong more often than right — `geodude`, `gengar`, `gyarados`, `gible` are all hard. `oo` and `ea` are genuinely ambiguous — `moon` vs `book`, `bead` vs `bread` — and English has no positional rule for either, so they keep one sound rather than guess.

**When the word is complete it is spoken whole** — /k/ /a/ /t/ … "cat". Sounding out, then blending back. **The round waits for it to finish** before moving on, rather than talking over its own advance; a beat follows so the change isn't abrupt. If the browser never reports the utterance ending, a timeout takes over, and with no speech support at all the round simply continues — it can't hang on a voice that isn't there.

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
- **`distractor_level`** — *another reading level*, whose pool supplies the wrong answers. It always points at or above the level's own row, so decoys are drawn from a superset of the target pool and the child meets harder words as options before ever being asked to read them. Difficulty comes from pool breadth rather than from hand-picking same-length decoys.

**Read-aloud rule: pictures may be named aloud; words never are.** Read & Choose prompts with a picture, which a child may not recognize, so a 🔊 Say it names it — resolving the prompt while leaving the written options to be read. Reverse Read & Choose prompts with the written word and therefore has no speaker on the prompt at all; each picture option carries its own instead. In both modes the child must connect a spoken name to a written one, and nothing ever reads a word aloud to them. There are no hints on either mode.

**Finding the right word speaks it**, and the round waits for that too. This doesn't breach the rule above: the rule guards the *prompt*, and by the time it's spoken the child has already answered, so it confirms rather than tells.

A Reading answer is **clean** when the first tap was the correct one. Using a picture's speaker does not affect cleanliness.

### 7.3 Math Trails

**Eight tracks**, every level of every one read from `data/math_levels.csv` — add, subtract, multiply, divide, and a skip-counting pattern track for each. 57 levels in total. Nothing about maths difficulty lives in code.

**Tracks open on prerequisites rather than in sequence.** `data/math_tracks.csv` gives each track the track and level that unlocks it. The four operations chain — subtract at add 5, multiply at add 7, divide at multiply 5 — and **each pattern track hangs off its own operation at level 3**, so counting by 3s opens once subtracting has started rather than waiting on an unrelated track. Add is open from the start, and **everything open has a chance to come up**, so the ladder widens as it is climbed instead of marching through one list. Liveness is transitive — a track whose own prerequisite hasn't opened can't open the next.

| column | means |
|---|---|
| `num1_min` / `num1_max` | first operand's range. On a pattern track, the fixed anchor |
| `num2_min` / `num2_max` | second operand's range. On a division row, the divisor |
| `num3_min` / `num3_max` | reserved for three-operand questions; null throughout, and unbuilt |
| `pattern` | on a pattern track, the steps to choose from |
| `visual` | whether this rung is one a picture can carry (§7.4) |

**Division never leaves a remainder.** The row gives a dividend range and a divisor; the quotient is chosen first, from those that land the dividend inside the range, so `3 ÷ 2` can never be asked.

**A pattern set is an anchor and a step, four rows.** Anchor 2 with step 2 gives `2+2, 2+4, 2+6, 2+8` — the second operand stepping. Divide mirrors multiply so every answer stays whole. A subtraction pattern has to start high enough to take every step without going below zero (anchor ≥ step × 4); where only part of a row's anchor range can, the anchor comes from that part, and where none can, that step is skipped.

**Promotion is its own table**, `data/math_promotion.csv`: **5 at 100%, 10 at 90%, 20 at 85%**, whichever lands first, per track. That is stricter at ten than the word trails' 80% and adds a twenty-question window they don't have.

**A round is split in thirds** — spelling, reading, maths — not evenly across every track. Maths has eight tracks to the others' one each, so an even split would hand a fully-unlocked child eight questions in ten as maths. The maths third is shared among whichever tracks are open.

**Answers are picked from six numbers**, two rows of three, styled like the spelling tiles — it is the same act as picking a chunk, so it looks like it. Every maths mode answers this way: plain Math, Visual Math, and Math Pattern. There is no keypad and no input box.

**The five wrong options are built from the mistakes the operation invites**, not sampled from the level's range. Sampling would put 40 beside 7 and let a child pick by size without doing the sum. Each operation has its own error shapes, ordered nearest-first and taken from the front of that list:

| operation | wrong options come from |
|---|---|
| `+` | ±1, ±2, `a − b` (subtracted instead), ±3, and ±10 / ±9 once the answer reaches two digits |
| `−` | ±1, ±2, `a + b` (added instead), ±3, `b − a`, ±10 |
| `×` | the neighbouring table rows — `a×(b±1)`, `(a±1)×b` — then ±1, `a + b`, ±10 |
| `÷` | ±1, ±2, the divisor, `a − b`, ±3, the dividend |

**A tens-column slip is only offered once there is a tens column** — 17 beside an answer of 7 is not a near miss, it is a giveaway.

**The six are shown in order, and the answer's position is deliberately varied.** A shuffled grid makes finding the answer a visual search rather than a sum; sorted, the six read as a stretch of number line and the child compares against neighbours. Sorting alone is not enough, because the wrong options straddle the answer and so centre it — leaving the middle two positions worth guessing. **The split is chosen first** — how many of the five sit below the answer — and each side is drawn to match, which spreads the answer across all six places. Where the answer is small there may not be three whole numbers below it, so division still leans early; the alternative is offering negatives, which is not a mistake a five-year-old makes.

**A wrong tap is spent**: that option dims and goes dead, so the same mistake can't be made twice and the field narrows as the child reasons. It also marks the answer unclean, exactly as a wrong entry did before, so promotion is unaffected.

Once the answer is right the choices **hide** rather than greying out — they have nothing left to do, and on a phone that is what lifts the ✅ above the fold. A correct answer shows a large animated ✅ and no caption text, then the round moves on by itself after a short beat. **There is no Next button anywhere**: with the choices gone there is nothing left on screen to act on, so a tap to continue would buy the child nothing. Maths advances exactly as Spelling and Reading do.

**The eight tracks and where they lead:**

| track | levels | runs from | to |
|---|---|---|---|
| `add` | 8 | `0–3 + 0–3` | `20–39 + 20–39` |
| `sub` | 7 | `0–5 − 0–5` | `20–29 − 20–29` |
| `mul` | 6 | `1–2 × 1–2` | `1–5 × 1–5` |
| `div` | 6 | `2–4 ÷ 2` | `6–30 ÷ 6` |
| `pattern_add` | 8 | count by 1 from 0–3 | any step to 10 from 10–19 |
| `pattern_sub` | 8 | count back by 1 from 5–9 | count back by 10 from 79–99 |
| `pattern_mul` | 7 | ×1–2 | the whole 1–10 table |
| `pattern_div` | 7 | ÷1–2 | the whole 1–10 table |

**A pattern track is its own track, not a dice roll inside another one.** Skip-counting has four tracks with their own levels, prerequisites and frontiers, so counting by 3s is practised at its own pace rather than turning up at random. **All four equations stay on screen** — seeing `3×1, 3×2, 3×3, 3×4` stacked is the point of the mode — but only one row is open at a time, and the six choices belong to that row, built from its own equation. Each answered row fills in, the next opens, and a fresh six appear.

### 7.4 Visual Math

Not a separate question source — a **rendering** of Math Trails questions as pictures of Pokémon instead of bare numbers, to build number-sense alongside abstract arithmetic. **Which rungs can be drawn is data**: the `visual` column in `data/math_levels.csv` says so per level, rather than the code guessing from the numbers. It leads the early levels and stops where the sheet says it should.

**Icons scale to how many there are.** Above twelve icons they shrink, above twenty-four they shrink again — a picture that has to be scrolled is not a picture. The tallest the sheet asks for is `div` level 5: `25 ÷ 5`, twenty-five icons over five groups, 919px on a 390×844 phone. Grouped layouts (× and ÷) get their own narrower boxes, sized so a group of five still sits on one line and two groups fit side by side: without that, four groups of five became four stacked rows.

- **Addition** — two boxes of Pokémon icons side by side, joined by "+".
- **Subtraction** — one box showing all the icons, with the subtracted amount crossed out by a bold drawn X.
- **Multiplication** — several equally-sized boxes joined by "+" signs, always at least 2 groups, since a single group doesn't demonstrate repeated addition.
- **Division** — separate bordered boxes, one per equal group.

The equation (e.g. "5 × 5 = ?") is shown **before** the picture. There is no instructional caption text.

## 8. Pokédex & Catching

- Every challenge screen shows a decorative grass strip. At a configurable rate (Settings, default 10%), it shakes to signal a Pokémon is hiding.
- **A pity timer caps droughts.** A pure per-question roll can go cold for a long stretch, which to a young child reads as the feature being broken rather than unlucky, so an encounter is *guaranteed* the moment a drought runs **one question past the average wait** — the 11th question at 10%, the 3rd at 50%. The counter **resets at the start of every round** — each round is its own experience, so a cold streak never follows the child into the next one.
- **The Settings field is the outcome, not the dice roll.** A guarantee adds encounters on top of the roll, so a raw roll of R always produces more than R — and "longer than average" is a one-in-three event, not a rare one, so the gap is several points (a raw 25% roll with this pity lands at 33%). The app therefore solves for the roll that *lands* on the number: for a drought capped at `k`, the encounter rate is `p / (1 - (1-p)^k)`, which increases with `p`, so a short binary search finds it. Set 25% and the roll used is 11.2%, with the pity making up the difference. Measured over 200,000 questions per setting, every value from 1% to 100% lands on itself.
- Answering the current question correctly catches it: a popup shows **"Caught!"**, the Pokémon's artwork, Dex number, name, and type badges, dismissed with an **Okay** button (no auto-dismiss timer) — the only button on the card, from every entry. **The name is said aloud**, shortly after the card appears — see the popup rule in §9. This doesn't breach the read-aloud rule in §7.2, which guards the *prompt*: the question is already answered, and what's being named is a picture. A **catch is celebrated**: confetti falls through the card and a burst of light blooms behind the artwork. Rarer catches get half again as many pieces and a gold palette, so the fuss itself signals the rarity to a child who can't yet read the chip. It fires on real catches only — browsing the Pokédex opens the same card dozens of times, and confetti every time would be noise — and is switched off entirely under `prefers-reduced-motion`. Catching a legendary or mythical species changes the banner to **"✨ Legendary Catch!"** / **"✨ Mythical Catch!"**.
- Encounters are **generation-gated** — only the lowest generation not yet fully caught can appear, so progress moves through the National Dex in order rather than randomly across all 1,021 at once. The Pokémon side of both the Spelling and Reading pools respects the same gate.
- **The screen opens straight onto the collection.** The HUD, then a ✕ beside **POKÉDEX**, then the tabs, then the grid — the first cell sits about 240px down at every supported width. It used to carry a full card headed *"My Pokédex"* with a `60 / 1021 caught` pill under it, which pushed the grid most of a screen down to state a total nobody is working toward: the generation is the unit being filled, and its own header already says where it stands.
- **The HUD comes first, unchanged.** It is persistent chrome and reads as belonging to the app, so it sits where it always does and says what it always says.
- **Below it, the ✕ on its own line beside the screen's name.** That row names the place you are in and gets you out of it — two different jobs from the HUD's, and mixing them into one line made the ✕ read as a fourth counter. Closing is a ✕ rather than "← Back", matching the round screen: same control, same corner, same meaning.
- The **Pokédex screen** is organized into **generation tabs** — `Gen 1` … `Gen 9`, one row that scrolls sideways on a phone — showing one generation's grid at a time. It opens on whichever generation the collection gate is currently on, not always Gen 1, and a tab whose generation is fully caught is outlined in green. All nine tabs fit the content column on a desktop window; below that width the strip scrolls, and **‹ › arrow buttons appear** — a touchscreen can swipe the strip but a mouse cannot, so the arrows are the desktop affordance. They exist only while the strip actually overflows and each one greys out at its end. One generation at a time keeps the visible grid to at most 160 cells instead of 1,021 and puts Gen 9 one tap away instead of a very long scroll.
- Within a tab: caught entries show in full colour with their name; uncaught ones are a grey silhouette (a `brightness(0)` filter on the same artwork, no separate asset) with **no name text at all** — the outline and the Dex number say it, where a row of `???` would be a word to decode for no payoff (§14.1). A live X/Y caught count sits in the generation header.
- **A bar under each generation header** shows how full that generation is, in the same colour and the same `.level-bar` the home card and the level tiles use. It replaces the dashed rule the header used to carry: the rule separated the header from the grid, and the bar does that *and* says how far along you are — `58 / 147` is exactly the sort of fraction that cannot be felt without one.
- **Legendary and mythical species are called out**: a gold cell with a ✨ badge in the grid, a matching chip above the type badges in the detail popup, and a per-generation tally in each generation header (`✨ 2/5 · 3 / 147`). The marker shows on **uncaught** slots too — it reveals nothing about which Pokémon lives there, and flagging the slot is the point: it marks something worth hunting for rather than only rewarding the find afterwards. Name and rarity chip stay hidden until it's caught.
- **Every entry is tappable**, opening a detail popup. A caught entry reads: larger artwork, the Dex number, the name, type badges, any rarity chip, a 🔊 speaker, and its **evolution family**. No greeting and no caption — the dex is a list you page through, and a sentence on every entry is one to skip past thirty times in a row.
- **The family shows whether or not this one is caught**, and each relative reveals itself independently: caught ones in colour with their names, uncaught ones as silhouettes. It gives away nothing an uncaught entry is holding back, and it answers what the card is opened to ask — what is this, and what does it become. An uncaught base with the strip hidden looked like a species with no evolutions at all.
- **The family is the whole family, from wherever you are standing in it.** The strip climbs to the root of the line and then walks down breadth-first, one group per stage with an arrow between stages — so Bulbasaur, Ivysaur and Venusaur all show the same three, and Eevee shows all eight of its second stage. Siblings stay grouped inside their stage, and a wide stage wraps within its own group so the arrow keeps meaning *this stage becomes that stage* rather than pointing at one sibling. Depth is capped and the climb is bounded, since `evolves_from` is hand-editable and a cycle would otherwise hang the popup.
- **Opening an entry says its name aloud.** One rule covers every way in — tapping a Pokédex cell, tapping a relative in the evolution family, tapping a catch on the results screen, and the catch popup itself. A name a child has only ever read is a name they can't yet use, and the picture is on screen at the moment it's said.
  - It hangs off *opening*, not rendering: re-rendering a card that is already on screen stays silent, because a name repeated without a new thing to look at is noise rather than teaching.
  - The 🔊 button covers repeats, and an uncaught entry has none — it gives up the outline, its number, its **type** and its family strip, and nothing else: no name, no greeting, no read-aloud. Type is the one thing shown either way; it is a single short word, it says something useful about a slot still to fill, and it doesn't name what's hiding in it.
- **The popup navigates to itself, and there is no Back.** Tapping a relative replaces what's on screen with that relative; **Okay** is the only button, from every entry. A back trail is unnecessary now the strip shows the *whole* family from wherever you land in it — every relative you could have come from is still one tap away, so walking a line in either direction uses the same control.
- **Why the strip earns its place:** National Dex order already puts 83% of families side by side, but cross-generation evolutions can sit hundreds of slots apart — Pichu is #172 and Pikachu #25 — and no amount of scrolling the grid makes that relationship visible.
- A newly caught Pokémon is flagged with a **NEW** badge in the grid until its entry is opened, so a catch made mid-session can be found again without hunting through a thousand entries. The flag is stored separately from the collection itself.

## 8b. Home HUD

A **HUD** on the very first line of the page — icon and number sitting straight on the background with no card around them — with the **wordmark and the gear sharing that same line**, pushed to the right.

**The logo does not get a row of its own.** A full-width mark cost 40–46px of height to tell a five-year-old the name of the app they had just opened, which is the argument that removed the tagline applied to the thing the tagline sat under. It rides in the HUD instead, at a 26px ball and 15–20px of type. Below the sheet's **480px** breakpoint the words drop and the ball stands alone: the row holds 60px of free space at 360 and 130 at 430, while the ball and words together need 150px even at an already-too-small 14px, so there is no size at which the full mark fits a phone.

Because the mark now lives in the HUD, it is **home-only** — the other six screens have no logo. Four of them open with the shared chrome instead (a ✕ beside the screen's name), and a round opens with the ✕ and progress bar §8b says should be the only things there.

**The icons are drawn, not typed** — inline SVG on one 24×24 grid, taking their colour from the counter they belong to via `currentColor`. Emoji cannot do this job: their em-boxes align but their *ink* does not, and the metrics belong to whichever emoji font the device happens to have, so there is no offset that is right everywhere. Drawn, every icon has the same optical size and the same centre on every device. The wordmark beside them is set in **caps** — via `text-transform`, so "POKÉ" keeps its accent rather than losing it to a retype — and carries **no tagline**: "Spell, count, and catch!" was a sentence for whoever installed the app, read once and then in the way of the thing it introduced.

### Screen chrome

**Every screen you can back out of wears the same two rows**: the HUD, then a ✕ beside the screen's name in caps — `SETTINGS`, `BATTLE`, `POKÉDEX`, `MY PROGRESS`. The HUD is persistent chrome and reads as belonging to the app; the row under it names the place you are in and gets you out of it. Those are different jobs, which is why they are different rows — on one line the ✕ read as a fourth counter.

It is **declared once, not written per screen.** A `SCREEN_CHROME` map holds each screen's title and, optionally, something to show beside it; `show()` renders it. Adding a screen is a row in that map rather than another copy of two rows of markup, and the ✕ cannot drift out of step with the one next to it. Only Battle uses the extra slot, for its session record.

**A screen with chrome does not also carry a heading card.** My progress and the Pokédex both had one, stating a name the chrome now states; both are gone, and both screens start most of a screen higher.

The HUD is **identical wherever it appears** — home, results, and every chrome screen. Three counters, the same three, in the same order. A counter that differs by screen is not persistent chrome, it is several similar things.

**Not on a round**: that has its own progress bar and ✕, and a second row of counters there would be two things to read at once.

**The round's top bar is a ✕ and a bar, nothing else.** The bar's fill says how far along the round is, so a `3 / 10` beside it would be the same fact written twice — and neither number means anything to a child who cannot yet read them. Quitting is an icon rather than the word "Quit" for the same reason. The ✕ keeps an `aria-label`. Every screen you can back out of now closes the same way, so this is the same control everywhere rather than a round-only exception.

| Counter | Shows | Goes to |
|---|---|---|
| target | rounds finished today against the daily goal; the number turns **green** once met | My progress |
| flame | consecutive days that met the rounds goal | My progress |
| dex | caught/total for the **current generation only** — the one the collection gate is on | Pokédex |

**The collection counter appears twice on the home screen, deliberately.** The HUD's is chrome: same corner, every screen, a fixed route to the Pokédex. The Pokémon card's (§8c) names the generation it is counting and belongs to the Pokémon above it. Same numbers, two jobs — and both derive from roster members rather than stored ids, so they cannot disagree.

**No labels.** "TODAY", "STREAK" and "GEN 1" were words a five-year-old wasn't reading; the icon says which counter it is and colour carries the one state worth noticing — green when the day's goal is met. Each counter keeps its own `aria-label` for anything that needs the meaning spelled out.

The same HUD appears on the results screen, centred rather than left-aligned to match that card. The gear is home-only.

A "round" is one full session; how many questions make up a round, and how many rounds a day the streak needs, are both Settings values.

**The streak holds until the day actually ends.** It counts consecutive days ending today *or yesterday*, so a streak earned yesterday still reads correctly at 8am before anything has been played, and only breaks once a whole day has passed without meeting the goal. Daily round counts are kept indefinitely rather than pruned to a window — pruning would silently cap the streak at the window's length.

## 8c. Home Showcase

Headed **"Your Pokémon"**, the middle band of the Start screen shows **one of the child's own**, big: artwork in a circular frame on the left, and beside it everything that labels it — Dex number, name, **type badges**, then the generation count. Number before name, because the number is the slot in the collection and the name is what fills it.

**Types show whether or not it is caught.** On a caught card they are one more fact about a Pokémon already on the shelf; on an uncaught one they are the only thing the card gives up besides the outline.

**The card holds two targets, so it is not itself a button.** Tapping the picture re-rolls the pick, as does every return to the home screen; tapping the count row below opens the Pokédex. A button inside a button is invalid and browsers disagree about what to do with one, so the card is a plain container with two buttons in it.

**Two columns at every width, with no breakpoint** — the frame and the text both clamp, so one arrangement holds from 360 to 1280 and uses 88–93% of the card at every supported size. The frame is the larger for it: putting the text beside the trophy rather than under it frees more height than a bigger circle spends.

**Last in that column, the generation and how much of it is filled** — the Pokédex icon, then `GENERATION 1` over `3 / 147`, over a bar in the Pokédex's colour. It sits under the Pokémon it describes rather than spanning the card, because a full-width row reads as a footer belonging to the whole card instead of to the one species above it. The bar is the level tiles' own `.level-bar`: `3 / 147` has exactly the problem the panel above already argues a bar solves.

It names the generation of the Pokémon **on screen**, not the one being hunted. Those differ whenever a freshly opened generation is still empty and the shelf falls back to the last one, and a count from a different generation than the picture above it would be two subjects on one card. The trophy says *you caught this one*; the count says *and here is the set it belongs to*.

It is a trophy shelf, not a teaser: it only ever shows a species already caught. It prefers the generation being worked on but falls back to the whole collection, so a freshly opened generation — where nothing is caught yet — still shows off the previous one's catches rather than going blank.

**Before anything at all is caught** there is no trophy to show, so the right-hand column falls back to the **type badges** beside a silhouette — an outline and one short word, no sentence (§14.1). The mystery shape is the invitation; a line of text telling a pre-reader to press Start is not. The generation count still shows, at `0 / 147`, because a goal is a number rather than a sentence.

## 8d. Home Levels

Headed **"Your progress"**, a panel of four tiles in a 2×2 grid — Spelling, Reading, Add / Sub, × and ÷ — each showing the track's icon, its **current level**, the number of levels on that trail, and a coloured bar for how far along it is.

Both home cards carry a heading, set through `text-transform` rather than typed in capitals so "Pokémon" keeps its accent instead of losing it to a retype — the same reason the wordmark does it.

**The icons are drawn, on the same 24×24 grid as the HUD's** and for the same reason. Spelling is `Aa`, Reading an open book, and **both maths tracks carry `123`** — the icon's job is to say *this is maths*, and the label beside it (`+ / −`, `× / ÷`) says which operation. Two different symbols there made them read as unrelated subjects. Each takes the colour of its own progress bar. The numerals are set in the app's own webfont rather than drawn as paths — it is self-hosted, so it is certainly present, and `123` at 17px reads as *numbers* in a way three hand-drawn digits at 6px each would not. `text-transform` has to be reset on the SVG text: the label beside it is uppercase and SVG inherits that, which turns `Aa` into `AA`.

**The bar is there because the number can't do the job alone.** Level 3 of 25 and level 3 of 10 are not the same place, and the number by itself implies they are.

A 2×2 grid rather than four rows: the same four facts at about half the height, scanned in one look instead of read down a list.

### The fold is the constraint the whole screen is laid out against

Order is HUD, levels, Pokémon, buttons — the wordmark rides in the HUD rather than taking a row between it and the levels — and **all of it fits on screen without scrolling**, down to 360×640. That matters because the primary action must stay visible: a panel of statistics is worth putting above the Pokémon, but not at the cost of pushing **Start Playing!** off the bottom.

Everything on the screen is a fixed cost except one thing. The HUD, the wordmark, four levels and two buttons all have to be legible at their size. **The Pokémon is the only element that can be smaller without losing what it says**, so it is the part that gives way: `.showcase-frame` takes whichever axis is scarcer — `22vh` keeps it clear of the fold on a short screen, `34vw` keeps it from crowding the text column on a narrow one — and runs from 225px down to 122px. One rule covers both, so the `max-width: 480px` override this used to need is gone; a `max-height: 700px` query still tightens the generation block. Measured at 360×640, 390×844, 414×736, 768×1024 and 360×780: no vertical scroll on any of them, and no horizontal scroll either.

**The panel is rebuilt on the way into home, not by whoever changed something.** `show("setup")` re-renders it, so setting a level in Settings, quitting a round after a promotion, or finishing one all show the current figure. Hanging it off each caller instead is what left the panel showing a stale level after a Settings change.

## 9. My progress

Reached from either home box, and headed by the chrome — `MY PROGRESS` beside the ✕, with no card and no subtitle.

**This week** comes first: a bar chart of rounds played on each of the last 7 days, today last, with a dashed line at the daily goal and a count above each bar. Days that met the goal are green, days that fell short are blue, and days with no play are left as an empty slot rather than dropped — the gaps are the point. Above it, the week's total and how many days it was spread over.

The streak tile answers *am I still going*; this answers *how has the week gone*, which a single day counter cannot show — two quiet days and one strong day read identically from one number. It uses the same `{date: rounds}` record the streak is computed from, which has always been kept in full rather than pruned to a window, so the chart is correct from the day it ships rather than starting empty.

Then **Spelling** and **Reading** get a card each, showing:

- The track's current level, in plain language.
- Days at the current level.
- One clean-answer progress bar per promotion gate, with exact fractions — Last 5 and Last 10 for the word trails, Last 5 / 10 / 20 for maths. The bar fills against however many answers the window actually holds, so three clean out of three reads full.

**There is no per-track accuracy chart.** The bars are the whole of it. Rolling accuracy resets at every promotion, so it cannot be plotted across levels as a trend — the reasoning is in `progress.md`.

**Maths gets two cards, one per family** — `+ / −` and `× / ÷` — rather than eight. Each is headed with the same summed level the home tile shows (*Level 7 of 31*), then lists its four tracks as a slim row: name, level out of that track's own total, and a bar of how far through it the child is.

- **Tapping a row opens the full detail** — level in plain language, days at it, and every gate bar. Only one tap's worth is built at a time.
- **Locked tracks are listed too**, greyed, with what opens them: *Opens at Multiply 5*. The road ahead is worth seeing, and the section keeps its shape instead of re-flowing under the reader every time something unlocks.

## 10. Battle Mode

A separate, unscored, replayable mini-game reached from the Start screen:

1. Two random, distinct Pokémon are shown, **A vs. B**, each with a 🔊 button to hear its name.
2. The player predicts a winner by tapping "Pick [Name]!"
3. A short "old-school" battle animation plays: both sprites shake, generic move-announcement text appears line by line.
4. The winner is decided by a **stat- and type-weighted random roll**: each Pokémon's real Base Stat Total represents its power level, a full 18-type effectiveness chart determines typing advantage, and `P(A wins) = powerA / (powerA + powerB)`. Both fighters' types are shown as colored badges.
5. The result is announced out loud and shown as a banner, along with whether the prediction was correct.
6. A running **session record** is shown at the top of the screen and persists across replays until the page is reloaded.

## 11. Results Screen

- A heading — **"Round finished!"** — and the same HUD as the Start screen, centred, so finishing a round shows the progress it just moved.
- **What was caught this round**, as large tappable cards that open the full detail popup — the reward is the point of this screen, so the artwork is sized to be looked at. Three fit a row at any phone width; more wrap. When nothing was caught, a plain line says so rather than inventing a consolation prize.
- **Play Again**, which starts another round at the length set in Settings, and **Go Back**.

**There is deliberately no score.** Every mode retries until the answer is correct, so a finished round is always 100%: a score would be a number that cannot vary, and any praise it drove would fire every single time. Nor is there a perfect-run reward — a promise of a Pokémon that the Pokédex would then not contain. Performance is measured where it means something: clean answers driving the Lesson Trails, shown on My progress.

## 12. Settings & Persistence

- **General**: Questions per round (how many must be answered well enough to finish, default 10), **Mistakes allowed** (slips a question may take and still count, default 1; `0` means it must be right first time), Rounds per day (the streak goal, default 2), and **Expected drop** — out of 100 questions, roughly how many hide a Pokémon. It is the measured outcome, pity timer included, not the underlying roll (§8).
- **Per mode**: an on/off toggle for Spelling, Reading, Math, and Visual Math.
- **Per trail**: a frontier dropdown showing the current level in plain language — *Level 1 — Words to level 1, 25% shown*, *Level 1 — 0–3 + 0–3* — which doubles as the manual placement control. All ten trails are listed, maths one row per track rather than per family, since this screen is read by a parent placing a child precisely. A maths track that has not met its prerequisite yet is shown locked with what opens it.
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
| `data/item_levels.csv` | 922 | `item`, `level`, `kind`, `words`, `components`, `component_levels`, `proper_noun`, `shared_art`, `letters`, `longest_word`, `spellable` |
| `data/spelling_levels.csv` | 25 | `level`, `word_level`, `compound_level`, `pokemon_letters`, `hinted_pct`, `max_hints`, `promote_5_pct`, `promote_10_pct` |
| `data/reading_levels.csv` | 10 | `level`, `word_level`, `compound_level`, `pokemon_letters`, `wrong_answers`, `distractor_level`, `promote_5_pct`, `promote_10_pct` |
| `data/phonemes.csv` | 91 | `chunk`, `context`, `say_as`, `notes` |
| `data/math_tracks.csv` | 8 | `track`, `label`, `symbol`, `kind`, `group`, `prereq_track`, `prereq_level` |
| `data/math_levels.csv` | 57 | `track`, `level`, `visual`, `num1_min`, `num1_max`, `num2_min`, `num2_max`, `num3_min`, `num3_max`, `pattern` |
| `data/math_promotion.csv` | 3 | `questions`, `percent` |

- **Pokémon roster**: the full National Dex, Gen 1–9, minus 4 species whose names don't fit the plain-letter spelling mechanic (Nidoran♀/♂, Farfetch'd, Mr. Mime). **1,020 of the 1,021 are spellable** — a name may contain a space or a hyphen, so Iron Hands and Ho-Oh both work; only Type: Null is excluded, for its colon. `rarity` marks **71 legendary** and **23 mythical** species.
- **Pokopia items**: **922** items across 12 categories, of which **819** reach the word trails. 13 carry an apostrophe, accent, period or digit; **90 share their artwork with another item** and are dropped from both trails, because a picture that names two things names neither — one generic building icon serves ten place names, so `Boutique` and `Snowbelle City` are the same picture. A few are plain mislabels: `Acrylic poster` and `Campfire` are one image. The rule is mechanical — `tools/classify_words.py` hashes every PNG and flags any file that appears twice — so it needs no eyeballing. **25 are excluded from Spelling** as Pokémon-branded (§7.1). The `image` column holds a bare slug — the `items/` folder and `.png` extension are added by the loader.
- **Offline, but served**: all artwork is stored locally in `pokemon/` and `items/` and referenced by relative path, the webfont is in `fonts/`, and nothing is fetched from PokéAPI, GitHub, Google or any fan site at runtime — **there are no external requests at all**, verified by loading the page with every non-local host blocked. Because the CSVs are fetched, though, the page must be **served over http(s)** — browsers block `fetch` on `file://` as cross-origin, so opening `index.html` by double-clicking it shows a load error instead. Once loaded, the browser cache covers repeat visits.
- **The ladders are data, not code.** `index.html` holds no level list, no word list and no promotion constant — it reads every ladder from CSV at boot. There is deliberately no fallback copy compiled in: a ladder that exists in two places drifts, and the spreadsheet is the one that gets edited.
- **Word grading**: `word_levels.csv` grades every distinct word in the item catalogue against the nine phonics patterns; `item_levels.csv` is the derived per-item view, where a single-word item takes its own level and a multi-word item takes its hardest component's. Both are regenerated by `tools/classify_words.py`. `word_levels.csv` is the file to correct — the item view follows from it.
- **Failure is loud**: a missing or empty CSV replaces the page with a legible error rather than booting an app with silently empty pools.
- **Storage keys**: Lesson Trails progress, the Pokédex collection, the set of caught-but-not-yet-viewed Pokémon, the play streak, and general settings each persist under their own `localStorage` key.

## 14. Design Notes

- Warm, pastel, "cozy life-sim" visual style (leaf greens, sky blues, cream, sun yellow, berry pink) consistent across every mode.
- Mobile-first responsive layout: touch targets sized for small screens, a dedicated `@media (max-width:480px)` breakpoint, no horizontal page scroll.
- **Pinch and double-tap zoom are off.** A small child holding a tablet triggers them by accident and cannot undo them, and a screen stuck at 2.4× is a broken app to them. It takes three mechanisms because no one of them covers every browser: `user-scalable=no` on the viewport meta, `touch-action: pan-x pan-y` on `html,body`, and `preventDefault` on Safari's non-standard `gesture*` events. Panning and scrolling are untouched. The obvious fourth — cancelling any `touchend` within 300ms of the last, to stop double-tap zoom — is deliberately **not** used: it also cancels the click that follows, and this game is played by tapping tiles in quick succession.
- Speech synthesis is used in Spelling, Battle, Reading and the Pokédex — in Reading, only ever to name a picture (§7.2). Utterances are pinned to `en-US`, since otherwise the OS default voice applies its own language's phonetics to English spellings. Names the synthesiser mangles are respelled via `data/pronunciations.csv` (§13); overrides affect **speech only**.
- Read-aloud has one consistent affordance: a round speaker button sitting **on the picture itself**, at the lower-right of the circular frame, rather than a labelled button in the action row below. That holds across Spelling, Missing Letters, Read & Choose, and the Pokédex popup; Reverse Read & Choose applies the same idea at smaller scale, one speaker per picture option.
- The favicon is the app's own Pokéball mark, inlined as an SVG data URI so it needs no extra file.
- Instructional text is treated as a UX smell for this audience: a pre-reading child can't use text they can't read, so captions are omitted wherever the numbers, pictures, or controls already carry the meaning.
- Circular `.poke-frame` images are capped at 65% rather than fitted to the frame, so that even a zero-padding square image's bounding-box corners stay inside the circle's radius. On the maths screens the frame takes a `compact` modifier and drops from 220px to 96px: the answer choices need the room, and the Pokémon is decoration on a sum, so it is what gives way.
- Rules for the Settings panel's number fields are scoped to `.field`. Unscoped, `input[type="number"]` outranks `.math-input` and `.pattern-input` on specificity — an attribute selector beats a class — and every answer box in the game silently rendered at settings size with 16px text.
- **Type**: the UI is set in **M PLUS Rounded 1c**, the closest freely-licensed match to FOT-Rodin — the rounded Japanese gothic the Pokémon Switch games use — so the app reads as a sibling of the games it borrows from. **Served from `fonts/`, not a CDN**: this is an app for a child on a tablet, and a typeface is not something to need a network for. Latin subset only, four weights, 87 KB — M PLUS Rounded 1c is a Japanese family whose full webfont spans roughly 590 subset files, and nothing in the page or in `data/*.csv` uses a character above U+00FF. `font-display:swap` and a rounded fallback stack (`Baloo 2`, `Varela Round`, `Trebuchet MS`) mean the page never blocks on it and never falls back to something angular. See `fonts/README.md` for how to pull a further subset if one is ever needed.

### 14.1 Copy rules

The reader is five and still learning to read. Every word on a child-facing screen costs them effort, so:

- **Never write a long sentence.** One to four words per line. `Try again!` — not `Not quite, try that blank again!`.
- **Words have to earn their place.** A name, a number, `GENERATION 1` over a count — things worth the effort of decoding, or things that label a number so it means something. Anything a picture, a number, or a control already says gets no text at all.
- **Never make the child read a placeholder.** No `???`, no `Not Caught`. A grey outline already says "you haven't found this one".
- **Say it plainly, not cleverly.** No wordplay, no encouragement paragraphs, no "Oops".
- **Adult-facing screens are exempt.** Settings, My progress and `data/README.md` are read by a parent and can explain themselves at length.

## 15. Technical Architecture

- **Stack**: vanilla HTML/CSS/JS, no framework, no build step, no package manager.
- **Data loading**: `loadData()` fetches **ten** of the eleven CSVs in parallel at startup — `word_levels.csv` is the grading source, not a runtime file; the app reads the per-item view rolled up from it — and parses them with a small RFC-4180-ish parser that handles quoted fields, so a spreadsheet export round-trips. Boot is therefore async: event listeners bind immediately since they only fire on interaction, but anything reading the roster waits for the data.
- **State**: in-memory JS objects for the active session/battle; `localStorage` for everything persisted.
- **Rendering**: each mode has its own `render*()`/`mk*()` function pair; a shared `buildQueue()` assembles the session from whichever modes are active.
- **Lesson Trails engine**: each track is an ordered array of level objects (`{id, label, gen}`), with a shared `pickBand()` / `recordAttempt()` / `setFrontier()` layer handling the review/current/stretch mix and promotion logic identically across all ten tracks. Per-track progress records the frontier, rolling clean/labored history, a capped `trend` log, and a `frontierSince` timestamp.
- **Assets**: local `pokemon/*.png` and `items/*.png`, referenced via relative paths from `index.html`. A Pokémon's artwork is found by `id` (`25` → `pokemon/25.png`); an item's by its `image` slug.
- **`tools/phonemes.html`**: a development-only audit page for `data/phonemes.csv`. Every row with a play button, using the app's own voice settings so it audits what a child actually hears; a rough pronounceability test shades the doubtful ones amber and can play only those; anything marked wrong collects into a copyable list. Built after a third of all spoken sounds turned out to be respellings a synthesiser spells out rather than says.
- **`tools/pronounce.html`**: a development-only audit page, not part of the app. Lists every name with a play button and collects the ones that sound wrong. It reads `POKEMON` and `SPEECH_OVERRIDES` out of a hidden `index.html` iframe, and provenance from `data/pronunciations.csv`, rather than keeping its own copy, so it cannot drift out of sync. Each row plays **Before** (the raw spelling) and **After** (the respelling) with an A/B comparison, and the respelling is editable so a fix can be tried by ear and copied back out.
