# Poké Learning — Product Requirements Document

**Owner:** Derek Yip
**Platform:** Web app — one page (`index.html`) plus `data/*.csv` and local artwork. Served over http(s), works offline once loaded, mobile-first
**Audience:** Young learner(s) practicing spelling, reading, and math, themed around Pokémon

> This document describes **what the app does today** — nothing else. How it got here, what changed when and why, what's still open, and what might come next all live in `progress.md`. The curriculum design rationale behind Lesson Trails lives in `LessonTrails.md`.

---

## 1. Summary

Poké Learning is a no-build, no-dependency HTML/CSS/JS app — one page plus a folder of CSV data and local artwork — that turns spelling, reading, and math practice into short, randomized, Pokémon-themed mini-games. A session mixes challenges from whichever modes are turned on, tracks a score, and ends with a results screen.

Difficulty is not a setting a parent picks and re-picks. Eleven **Lesson Trails** — Spelling, Reading, Alphabet, and eight maths tracks — each hold their own level and advance on their own based on real performance. Alongside the practice modes: a Pokédex-style collection game (catch Pokémon hiding in the grass as you answer correctly, generation by generation), a daily play streak, a progress screen, and a separate, unscored Battle mode where the player picks a Pokémon and watches a stat/type-based "who would win" prediction play out.

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
| **Start** | A meadow carrying two counters and the gear, with one of your Pokémon on its hill; a name card with the generation count; five trail tiles; then "Start playing" and "Battle" |
| **Settings** | The chrome, then per-mode toggles and each trail's frontier control |
| **Play** | One challenge at a time, progress bar, grass encounter strip, ✕ to quit |
| **Results** | The HUD and "Round finished!" over the meadow, what was caught this round, replay controls |
| **Battle** | Standalone Pokémon-vs-Pokémon prediction game; its session record sits beside the screen name |
| **Pokédex** | The HUD, a ✕ beside **POKÉDEX**, generation tabs, then one generation's grid — caught in colour, uncaught as grey silhouettes |
| **My progress** | The chrome, a 7-day rounds chart, a card each for Spelling and Reading, then one card per maths family |

Settings, Lesson Trails progress, the Pokédex collection, and the play streak persist to `localStorage` and are restored on load.

## 5. Sessions

**A round ends after N questions answered well enough, not after N questions shown.** Every mode retries until the answer is right, so counting questions *shown* meant a round could be finished by guessing through it. How a question earns that credit depends on the mode. In **maths, reading and alphabet** it counts when answered with at most **`Mistakes allowed`** wrong taps — a Settings value, default 1. **Spelling scores differently**: wrong taps are free, and what is counted is how many letters the word had to *show* (§5.1).

**Two different bars, deliberately kept apart.** The Lesson Trails still promote only on a **spotless** question — nothing wrong at all, nothing shown — in every mode, spelling included. The round bar governs only whether a question moves the *round* along. Loosening the round does not loosen the ladder.

**Failure is bounded: after `Show the answer after` wrong taps on one step, the right answer lights up and the child still has to tap it.** Every mode blocks until the answer is right and there is no skip — deliberately, since being told the answer costs the struggle that makes it stick. But that left a dead end: a question resting on something never taught has no exit, and tapping every option in turn is the only move the screen offers. That is not a child giving up, it is the only input the app accepts.

The answer lights in a pulse — never a still highlight, because a correct answer never moves. **Maths and Reading light amber**, deliberately not the green those modes already use for "you got it". **Spelling, Alphabet and Pattern light green** instead, because amber is taken there: the blank being filled — a spelling slot, the alphabet gap, the open pattern row — wears an amber ring as a cursor on every question, from the moment it loads and with nothing wrong. Two near-identical ambers meant a parent watching could not tell *you are here* from *here is the answer* — the help was invisible, which is the one thing it must not be. Green is free on the answers in those modes: a correct answer turns the **slot** green, never the option, so nothing in the bank wears green to mean "right".

Three properties make the light safe:

- **It cannot become a give-up button, because it is not a button.** It is triggered by failing rather than chosen, so there is nothing to press early.
- **Outside spelling it can never pay to fail on purpose.** The reveal lands at least one mistake past `Mistakes allowed`, so by the time it appears the question has already stopped counting toward the round. The Settings value is raised to enforce that if it is set too low. Spelling buys the same guarantee through its own budget instead (§5.1), so it is exempt from the raise.
- **It counts the current *challenge*, and what that means differs by mode.** A Pattern row and an Alphabet gap are each a single answer, so two slips spread across two rows never light up the second one. A **spelling word accumulates across the whole word**, not per letter.
- **The light is spent when it pays out.** Taking the lit tile re-arms the counter, so the next blank costs its own wrong taps.

**Spelling lights a tile in the bank** — the chunk that comes next in Full Spelling, the one that fills the next blank in Missing Letters — counted across the **whole word**. Counting per letter looked consistent and was wrong in practice: a seven-blank word took two slips on the *same* letter before anything lit, so a child scattering one wrong tap across five different blanks was five mistakes deep, had already lost the credit, and had been offered no help at all — which is exactly the flailing this exists to catch.

**But the light is spent when it pays out.** Leaving it on walked a child through the entire rest of the word: two wrong taps on `soft mat` lit its six blanks one after another, and he tapped six letters without spelling any of them. Taking a lit tile now re-arms the counter, so the next blank has to earn its own light. Struggling still gets help on every letter that needs it; coasting pays for each one.

### 5.1 Spelling credit

Every other mode asks *how many times did you get it wrong*. Spelling asks **how many letters did you have to be told**, and forgives wrong taps entirely. A letter bank invites tapping — with six tiles on screen, trying one is how a five-year-old explores, and punishing that punishes the wrong thing. Being shown a letter is the honest signal, so that is what is counted.

The budget scales with the word, because two letters told out of twelve is not the same event as two out of two. It is **`blanks ÷ 3`, rounded down**:

| Blanks | Free | Share of spelling questions |
| --- | --- | --- |
| 1–2 | 0 | 30% |
| 3–5 | 1 | 47% |
| 6+ | 2, and up — 18 blanks earns 6 | 23% |

The mix moves on its own as the ladder climbs: levels 1–2 are **100%** short words, level 25 is **70%** long ones, so the rule grows more generous exactly where the words get harder, with nothing to tune per level.

Spam is still caught, indirectly: spam earns lights, lights spend the budget. At the default of two wrong taps per light that works out at roughly **one free wrong tap per blank** — two on a two-blank word, twelve on a twelve. Busting it only ever means the round runs one question longer.

**Promotion is untouched** and still demands a spotless question: zero wrong taps, nothing told. Letting a told letter promote would inflate the ladder and strand a child on a rung they cannot actually spell, which is the cliff all of this exists to avoid. The budget governs the progress bar, never the trail.

**The light is the only help spelling offers.** There is no hint button: help is earned by failing, never chosen, so there is nothing to press when a child would rather opt out. That makes `Show the answer after` the single dial governing how long a stuck child flails before a letter appears.

Where the reason is on screen — Alphabet's run of letters, Reading's picture — there is something to infer from. Bare arithmetic is the weak case: lighting up `5` for `14 − 9` shows the fact and not the borrowing, and that wants its own support, which it does not have yet.

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
| `name_letters` | **the longest name the level may serve — items and Pokémon alike.** Pokémon stay generation-gated on top of it |

Pokémon are gated by length rather than by phonics level because invented names have no decoding pattern to grade — length is the only honest measure for them. Item words do have one: the grading lives in `data/word_levels.csv` and is rolled up per item in `data/item_levels.csv` (§13).

The ladder is nine tiers of three, and within a tier only **`hinted_letters`** changes — **the number of letters given away** before the child starts, falling as the tier climbs.

A count, not a share, and the difference matters. As a percentage the help scaled with the word, so a twelve-letter name at 50% still handed over six letters and the hardest words stayed the most supported. Two letters is two letters, so a long word is now genuinely harder than a short one — which is the thing being taught.

- **Above 0% it's Missing Letters** — the word appears with that share of its letters showing and the rest as blanks, filled by tapping from a bank of **chunks**. Blanks are placed by a `chunkWord()` tokenizer that treats digraphs, blends, vowel teams and r-controlled vowels as atomic, so a blank never splits a sound; whole chunks are hidden until the level's letter target is reached, always leaving one chunk visible.

  **The bank is padded with decoys to a floor of four tiles.** Holding only the missing chunks made a one-blank word a guaranteed tap — `MEW` showed `M` and a single `EW` tile — which was 9% of all Missing Letters questions and 45% of level 2. Four blanks or more get no decoys, so the hard end is untouched. Each decoy is drawn from the same phonics class as a chunk it competes with — single vowels, vowel teams, r-controlled vowels, digraphs, blends, single consonants — and is never a chunk the word contains. Class matters: beside a vowel team, `str` can be ruled out by eye without knowing the answer, and `oo` cannot. A wrong tap shakes the tile, says so, and costs the clean answer.
- **At 0 it's Full Spelling** — empty slots, the whole word built from shuffled tiles (tap or keyboard). Controls: the speaker on the picture, Backspace, Clear. **No level currently asks for 0**, so this task does not appear in play; the mechanism is kept and a `0` in the column brings it back.

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

**Pokémon-branded items are excluded from Spelling.** 25 item names are built from a Pokémon name — `Hoppip water bottle`, `Pikachu doll` — and their phonics level is fiction: an invented proper noun is memorised, not decoded, so asking a child to produce one isn't spelling practice. They're flagged `proper_noun` in `data/item_levels.csv` and skipped here. Reading keeps them, because recognising a name the child already knows by sight is a fair reading task, and the names themselves remain reachable through the Pokémon pool under the generation gate.

The earliest levels have single-figure pools, so the generator never repeats the immediately-previous word for a track when there's an alternative.

### 7.2 Reading Trail

**10 levels, defined entirely in `data/reading_levels.csv`,** selecting words by exactly the same three columns as Spelling — one vocabulary grading feeds both trails, so a word met in Reading at level 4 is a word Spelling asks for at level 4. The two frontiers move independently, which lets Reading run ahead: recognising a word is easier than producing it.

Two formats, picked at random per question in equal share:

- **Read & Choose** — one picture, N word options.
- **Reverse Read & Choose** — one written word, N picture options.

Alphabet used to be a third format here. It is now **its own trail** (§6.3), with its own ladder, frontier, promotion and Settings switch.

Difficulty ramps on two columns of its own:

- **`wrong_answers`** — how many decoys, so the choice count is 3 at level 1, 4 at level 2, and 5 from level 3 on.
- **`distractor_level`** — *another reading level*, whose pool supplies the wrong answers. It always points at or above the level's own row, so decoys are drawn from a superset of the target pool and the child meets harder words as options before ever being asked to read them. Difficulty comes from pool breadth rather than from hand-picking same-length decoys.

**Read-aloud rule: pictures may be named aloud; words never are.** Read & Choose prompts with a picture, which a child may not recognize, so a speaker button names it — resolving the prompt while leaving the written options to be read. Reverse Read & Choose prompts with the written word and therefore has no speaker on the prompt at all; each picture option carries its own instead, **directly below the picture and outside its tap area**, so a near-miss on the speaker can never count as a wrong answer. In both modes the child must connect a spoken name to a written one, and nothing ever reads a word aloud to them. There are no hints on either mode.

**Finding the right word speaks it**, and the round waits for that too. This doesn't breach the rule above: the rule guards the *prompt*, and by the time it's spoken the child has already answered, so it confirms rather than tells.

A Reading answer is **clean** when the first tap was the correct one. Using a picture's speaker does not affect cleanliness.

### 6.3 Alphabet — its own trail

A run of consecutive letters is laid out left to right, each shown as a Pokémon whose name starts with it, and some of them are gaps. The child works out which letter a gap is and picks the Pokémon whose name starts with it. Gaps open one at a time, left to right, and the run stays on screen while it fills — the sequence *is* the question, so hiding the letters already found would turn "what comes after C" into a guess.

**The run prints its letters; the options do not.** That split is the whole exercise: the run says what is being asked for, and the only way to answer is to read an option's name and see what it starts with. Printing the letter on the options too would leave nothing to read.

**It has its own ladder, not Reading's.** It used to sit inside Reading and read its shape off the reading row, and that could not survive the sheet: the alphabet ladder has **eleven** levels to Reading's **ten**, and a track indexes its levels by its own frontier — so at Reading 8, 9 and 10 there was no alphabet row to read at all. It carries its own promotion percentages too, which a borrowed ladder would never consult. Two arithmetic reasons, not a matter of taste. Knowing the alphabet and reading words are different skills moving at different speeds, which is the same argument that already gives Spelling and Reading separate frontiers.

Eleven levels in `data/alphabet_levels.csv` — two tiers, a run of 4 then a run of 5 — with three columns controlling them:

- **`alpha_length`** — how much of the alphabet is on screen. **Shorter is harder**, not easier: a run of 4 gives three letters to count along, a run of 2 gives one.
- **`alpha_blanks`** — how many of those are gaps.
- **`alpha_blank_position`** — where the gaps may fall:
  - `last` / `first` — the solid block at that end.
  - `middle` — every gap strictly inside the run, never touching an end.
  - `random` — **every shape, nothing filtered out.** Gaps can split (`_x_x_`), sit at an end, or land anywhere between, each shape equally likely. This is the only setting that produces *non-contiguous* gaps, and the only one a child cannot pre-empt: there is no "the gap is always at the back" to lean on.
  - `mixed` — anything that is neither the first block nor the last one. Narrower than `random` — it is `random` minus the two end blocks. **No level uses it**; it is kept as the only way to ask for three gaps in a run of four without them forming a solid end.

  Each tier walks `last` → `middle` → `first` → `random`, which is the order of difficulty: continuing a sequence forward is what the alphabet song practises, `first` asks what comes *before* and has no song to lean on, and `random` withholds even the knowledge of which way the next question will run.

Two things are fixed in code rather than in the sheet: there are always **four options**, and they are **spread at least four letters apart** — from each other and from the answer.

**The options are spread because the distractors are not where the difficulty lives.** A child answers by reciting from the song, deriving "M", and then going looking for it — the options play no part in deriving it. Crowding them around the answer would only add a second, unrelated task afterwards, telling M from N, O and P in a lineup, which is letter-shape recognition: work out M, tap Noivern, and the failure says nothing about which step broke. M N O P is the slurred stretch of the alphabet song besides, so a gap after L would draw its options from exactly the letters least likely to have been pulled apart yet. Spread out, a correctly derived answer is unambiguously findable and a guess is unlikely to land, so the derivation is what decides right or wrong. Difficulty rides on the three sheet columns instead.

**A round is split evenly between the modes that are on.** With spelling, reading, alphabet and maths all switched on that is a quarter each — the maths quarter then shared among whichever maths tracks are live. As one third of Reading's third, alphabet was about **11%** of a round; as a mode of its own it is **25%**. The Settings switch is how to turn it back down.

Letters already on screen are excluded as well, worked out per gap rather than once per question because the run fills in as it is answered: given or filled a moment ago, a visible letter can be ruled out by looking, so it is a free elimination.

The mode draws from the **whole roster, not the caught generations**. There are 23 runs of four consecutive letters and 22 of five; the full roster fills every one of them, a single generation only 7–13. Gating this the way the word pools are gated would leave most of the alphabet unreachable. Nothing is spoiled by this — the question is which letter comes next, not which Pokémon the child owns.

**Nothing is read aloud in this mode.** Every name on screen is a first letter, so speaking any of them would hand over the sort the child is doing. This is the read-aloud rule above applied, not an exception to it.

A row that cannot produce a question is rejected at load rather than papered over at play time: more gaps than letters, a run shorter than two, a `middle` asking for more gaps than the run has interior slots, an unknown position, or a run length the roster cannot fill.

### 7.3 Math Trails

**Eight tracks**, every level of every one read from `data/math_levels.csv` — add, subtract, multiply, divide, and a skip-counting pattern track for each. Nothing about maths difficulty lives in code: how many levels a track has, what ranges each one asks for, and which track unlocks which are all sheet values.

**Tracks open on prerequisites rather than in sequence.** Each row of `data/math_tracks.csv` names the track and level that unlocks it; one track opens from the start. **Everything open has a chance to come up**, so the ladder widens as it is climbed instead of marching through one list, and liveness is transitive — a track whose own prerequisite hasn't opened can't open the next.

Which track waits on which is tuning, not spec: it is authored in [the design sheet](https://docs.google.com/spreadsheets/d/1MtlBnXPMFt3x_LpcMmWe7LIeISjoC9wJddhTM8_zbVY/edit) and read from the CSV. This document does not restate it, because a value written in two places drifts and the CSV is the one the app obeys.

| column | means |
|---|---|
| `num1_min` / `num1_max` | first operand's range. On a pattern track, the fixed anchor |
| `num2_min` / `num2_max` | second operand's range. On a division row, the divisor |
| `num3_min` / `num3_max` | reserved for three-operand questions; null throughout, and unbuilt |
| `pattern` | on a pattern track, the steps to choose from |
| `visual` | whether this rung is one a picture can carry (§7.4) |

**Division never leaves a remainder.** The row gives a dividend range and a divisor; the quotient is chosen first, from those that land the dividend inside the range, so `3 ÷ 2` can never be asked.

**A pattern set is an anchor and a step, three rows.** Anchor 2 with step 2 gives `2+2, 2+4, 2+6` — the second operand stepping. Four rows made a single question four answers long, which is a long time on one screen and left the mode disproportionate to every other kind; three still shows a sequence, since two steps is a pattern and one is a coincidence. Divide mirrors multiply so every answer stays whole. A subtraction pattern has to start high enough to take every step without going below zero (anchor ≥ step × the row count); where only part of a row's anchor range can, the anchor comes from that part, and where none can, that step is skipped.

**Promotion is its own table**, `data/math_promotion.csv` — any number of windows, whichever lands first, applied to every maths track. It currently holds three (5 at 100%, 10 at 90%, 20 at 85%), but the gates themselves are sheet values, not spec. That is stricter at ten than the word trails' 80% and adds a twenty-question window they don't have.

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

**A pattern track is its own track, not a dice roll inside another one.** Skip-counting has four tracks with their own levels, prerequisites and frontiers, so counting by 3s is practised at its own pace rather than turning up at random. **Every equation stays on screen** — seeing `3×1, 3×2, 3×3` stacked is the point of the mode — but only one row is open at a time, and the six choices belong to that row, built from its own equation. Each answered row fills in, the next opens, and a fresh six appear.

**A pattern rung marked `visual` draws each row as Pokémon**, in place of the decorative Pokémon at the top, and **highlights what the pattern added on that row** in sun yellow. For `+` the fixed number is drawn plain — no frame, because in Visual Maths addition a blue box is always five wide, and a seven-wide one read as a five that had overflowed; the "+" already separates it — and the growing one follows it: the previous row's Pokémon, then the step's worth of new ones highlighted. For `×` each row is an array with one line per group, its newest group highlighted. Every row highlights the step, the first included — it is the step's first appearance — so the stack reads as "the same as last time, and these". Nothing is drawn as a blank: an empty space reads as *missing*, not *new*. Rows below the open one are dimmed and not drawn yet. When a `+` row is too wide for one line, the fixed number keeps the first line and the growing part moves under it whole, so the highlight is never split from the rest; past a dozen Pokémon the icons shrink. Only `+` and `×` patterns can be drawn. Add patterns 1–4 and multiply patterns 1–3 are marked; at 360×640, 390×844 and 820×1180 every one of those fits without scrolling.

### 7.4 Visual Math

Not a separate question source — a **rendering** of Math Trails questions as pictures of Pokémon instead of bare numbers, to build number-sense alongside abstract arithmetic. **Which rungs can be drawn is data**: the `visual` column in `data/math_levels.csv` says so per level, rather than the code guessing from the numbers. It leads the early levels and stops where the sheet says it should.

**Icons scale to how many there are.** Above twelve icons they shrink, above twenty-four they shrink again — a picture that has to be scrolled is not a picture. The tallest the sheet asks for is `div` level 5: `25 ÷ 5`, twenty-five icons over five groups, 919px on a 390×844 phone. Grouped layouts (× and ÷) get their own narrower boxes, sized so a group of five still sits on one line and two groups fit side by side: without that, four groups of five became four stacked rows.

- **Addition** — two standard boxes joined by "+".
- **Subtraction** — one standard box showing all the icons, with the subtracted amount crossed out by a bold drawn X.
- **Multiplication** — several equally-sized boxes joined by "+" signs, always at least 2 groups, since a single group doesn't demonstrate repeated addition.
- **Division** — separate bordered boxes, one per equal group.

**The standard box.** Single-digit addition and subtraction draw into a box of a fixed shape: **always five columns wide, one row up to five and two rows from six.** Exactly two sizes exist per screen width — 250×66 and 250×112 on a phone, 196×56 and 196×91 above it — and every box in every question is one of them. On a phone the two boxes are stacked anyway (below), so each takes the width and its Pokémon are 40px; above 560px they are 30px, side by side.

Boxes used to shrink-wrap their contents, which made the same kind of sum a different shape every time: addition ranged 76px to 220px wide, and the two operands of one question rarely matched each other. With a fixed box, `4 + 5` is two identical frames, one with a single space left and one with none, and how far each is from five is something to see rather than count.

**Contents sit flush left, never centred.** Four icons centred in a five-wide box float with a half gap either side, which reads as a different arrangement rather than as *one short*. Filling from the left puts the shortfall in one place, always the same place.

**The empty places are drawn.** Every place a box has left over shows the same Pokémon as a faint solid shape (12% black), after the real ones. An empty frame beside two Pokémon read as a box that was simply too wide; filled with shapes it reads as *five places, two taken*. A shape rather than a dashed blank, because a blank says "nothing here" rather than "room for one more". In subtraction the crossed-out Pokémon are still the real ones: shapes only stand where nothing was drawn, so `7 − 3` is seven Pokémon, three crossed, and three shapes completing the ten.

**Below 560px the two operands stack, with the operator between them.** Two five-wide boxes need more width than a phone card has — 250px each against 280px of card — so they used to *wrap*, which left the "+" stranded beside the first box with the second underneath. That is the same marooned-operator problem the ten-box layout stacks to avoid, reached by accident rather than on purpose. Stacking is now deliberate and the operator sits between the two, the way a column sum does. Above 560px they sit side by side.

Multiplication and division are untouched: they already draw one fixed-width box per group, sized so five icons sit on one line.

The equation (e.g. "5 × 5 = ?") is shown **before** the picture. There is no instructional caption text.

**Tens and ones.** Addition and subtraction draw any count of ten or more as full **ten-boxes** — ten icons in a framed 5×2 grid — plus the remainder loose beside them, tens on one row and ones on the next. This is what makes two-digit questions drawable at all: one icon per unit scales with *magnitude*, so `29 + 19` is forty-eight of them, while tens-and-ones scales with *digits* and the same question is three boxes and eighteen loose — twenty-one objects instead of forty-eight.

The count is the lesser point. Twenty-five identical icons have to be counted one at a time; "two full boxes and nine" is read. The **frame** does that work, not the legibility of what is inside — at this size the icons are texture, and that is fine. They are the same Pokémon as the loose ones deliberately: "one box and four Pokémon" is only fourteen Pokémon if the box contains Pokémon.

Two constraints the layout exists to satisfy. Operands **stack** with the operator between them once either reaches ten, because a flex row leaves the operator marooned beside the first operand while the second wraps underneath. And nine loose ones must fit on **one line** — wrapped as eight-then-one they read as "eight and one", and nine-versus-ten is the comparison the whole layout exists to make visible. The operand's own frame is dropped in this layout so that a frame means exactly one thing: *this is ten*. For the same reason the frame is blue rather than amber, which already means "this is the answer, tap it".

**Subtraction crosses into the boxes.** A box is not an atom — it is ten visible icons in a frame — so a subtraction needing more than the loose ones can supply simply crosses into a box, and the ten is visibly raided. `15 − 9` is one box with four crossed inside it and all five loose ones crossed, leaving six. There is no special case for borrowing.

The **loose ones are spent first**, and only then a box. That is what keeps a whole box meaning ten: at `19 − 9` the box is left untouched, so the answer reads as one full box rather than having to be counted, and only a real borrow ever breaks a box open. Within a box and within the loose row alike, **survivors are drawn before casualties** so the answer gathers at the start, and boxes are spent from the right so whole ones stay on the left.

This shows the borrow as a *fact* — the ten was dipped into — rather than as an *action*. A tappable box that opened into ten loose ones would show the trade itself, and is deliberately not built: much more machinery for one increment of understanding, and nothing here rules it out.

**Live from the sheet.** Every level of the add and subtract ladders is now `visual`, so two-digit questions are drawn rather than left as bare numerals. Measured across those ladders, roughly three questions in ten use a ten-box, and the tallest that does is 227px — shorter than the tallest grouped multiply, so the boxes cost no height.

## 8. Pokédex & Catching

- Every challenge screen shows a decorative grass strip. At a configurable rate (Settings, default 10%), it shakes to signal a Pokémon is hiding.
- **A pity timer caps droughts.** A pure per-question roll can go cold for a long stretch, which to a young child reads as the feature being broken rather than unlucky, so an encounter is *guaranteed* the moment a drought runs **one question past the average wait** — the 11th question at 10%, the 3rd at 50%. The counter **resets at the start of every round** — each round is its own experience, so a cold streak never follows the child into the next one.
- **The Settings field is the outcome, not the dice roll.** A guarantee adds encounters on top of the roll, so a raw roll of R always produces more than R — and "longer than average" is a one-in-three event, not a rare one, so the gap is several points (a raw 25% roll with this pity lands at 33%). The app therefore solves for the roll that *lands* on the number: for a drought capped at `k`, the encounter rate is `p / (1 - (1-p)^k)`, which increases with `p`, so a short binary search finds it. Set 25% and the roll used is 11.2%, with the pity making up the difference. Measured over 200,000 questions per setting, every value from 1% to 100% lands on itself.
- **The question has to earn it.** A Pokémon is a reward for answering, not for arriving: the encounter is rolled *before* the question is attempted, and a question that does not count toward the round (§5) does not pay one out. It is **kept rather than spent** — the grass keeps rustling and the next question can still claim the same Pokémon. Keeping it matters for more than kindness: the drought counter resets when an encounter is *rolled*, not when one is caught, so discarding an unclaimed encounter would quietly push the real catch rate below the rate the pity timer guarantees. Because nothing is discarded, **every encounter rolled is eventually caught** — measured at 20,000 questions per setting, rolled and caught are equal in every run. What a struggling child loses is timing, not Pokémon: at the default 10% drop, a child failing 30% of questions still catches 9.5% and waits at worst 17 questions instead of 11.
- Answering the current question well enough catches it, and **the catch takes the whole screen**: the artwork large on the hill of **the home screen's own meadow** (the same drawing, cloned in at start-up, so the two never drift apart) in a burst of light with its speaker, then on **a white card raised onto the hill** the Dex number, name, type badges and its evolution line, dismissed with one button that says **✓ Caught!** (no auto-dismiss timer). The word lives on the button rather than as a ribbon in the sky: the ribbon carried the raised edge that means "tap me" and did nothing, and floated well away from everything else. Browsing the Pokédex, or walking to a relative from a catch, the same button says **Okay**. Opening a catch again from the results screen shows it the same way; browsing the Pokédex opens the same card as a sheet over the grid instead. **The Pokémon is sized to the sky**, not fixed: 440px on a tablet or desktop window, 320px on a 390×844 phone, about 166px under 820px tall, where the sky and the artwork give way first so the family and the button always fit. A fixed 250px left a desktop window two-thirds empty sky. When the line splits and the card carries a stacked column (Gloom, Tyrogue), the Pokémon steps down a size so it stays clear of the top. From 700×1000 up the card and button scale up with the picture. **The name is said aloud**, shortly after the card appears — see the popup rule in §9. This doesn't breach the read-aloud rule in §7.2, which guards the *prompt*: the question is already answered, and what's being named is a picture. A **catch is celebrated**: confetti falls through the card and a burst of light blooms behind the artwork. Rarer catches get half again as many pieces and a gold palette, so the fuss itself signals the rarity to a child who can't yet read the chip. It fires on real catches only — browsing the Pokédex opens the same card dozens of times, and confetti every time would be noise — and is switched off entirely under `prefers-reduced-motion`. Catching a legendary or mythical species turns the button gold and changes it to **"Legendary catch!"** / **"Mythical catch!"**.
- **A catch shows only the line it is on**: the forms it came from, then everything it can still become. Vaporeon shows Eevee → Vaporeon; Bulbasaur shows Bulbasaur → Ivysaur → Venusaur; Gloom shows Oddish → Gloom → Vileplume and Bellossom stacked in one column. The whole family is the Pokédex's job: on a catch, Eevee's eight second-stage forms wrapped into a grid that buried the one just caught. A stage too wide to draw — only Eevee's, of all 1,021 — is **one grey shape with the count on it** ("8"), which can't be tapped.
- Encounters are **generation-gated** — only the lowest generation not yet fully caught can appear, so progress moves through the National Dex in order rather than randomly across all 1,021 at once. The Pokémon side of both the Spelling and Reading pools respects the same gate.
- **The screen opens straight onto the collection.** The HUD, then a ✕ beside **POKÉDEX**, then the tabs, then the grid — the first cell sits about 240px down at every supported width. It used to carry a full card headed *"My Pokédex"* with a `60 / 1021 caught` pill under it, which pushed the grid most of a screen down to state a total nobody is working toward: the generation is the unit being filled, and its own header already says where it stands.
- **The HUD comes first, unchanged.** It is persistent chrome and reads as belonging to the app, so it sits where it always does and says what it always says.
- **Below it, the ✕ on its own line beside the screen's name.** That row names the place you are in and gets you out of it — two different jobs from the HUD's, and mixing them into one line made the ✕ read as a fourth counter. Closing is a ✕ rather than "← Back", matching the round screen: same control, same corner, same meaning.
- The **Pokédex screen** is organized into **generation tabs** — `Gen 1` … `Gen 9`, one row that scrolls sideways on a phone — showing one generation's grid at a time. It opens on whichever generation the collection gate is currently on, not always Gen 1, and a tab whose generation is fully caught is outlined in green. All nine tabs fit the content column on a desktop window; below that width the strip scrolls, and **‹ › arrow buttons appear** — a touchscreen can swipe the strip but a mouse cannot, so the arrows are the desktop affordance. They exist only while the strip actually overflows and each one greys out at its end. One generation at a time keeps the visible grid to at most 160 cells instead of 1,021 and puts Gen 9 one tap away instead of a very long scroll.
- Within a tab: caught entries show in full colour with their name; uncaught ones are a grey silhouette (a `brightness(0)` filter on the same artwork, no separate asset) with **no name text at all** — the outline and the Dex number say it, where a row of `???` would be a word to decode for no payoff (§14.1). A live X/Y caught count sits in the generation header.
- **A bar under each generation header** shows how full that generation is, in the same colour and the same `.level-bar` the home card and the level tiles use. It replaces the dashed rule the header used to carry: the rule separated the header from the grid, and the bar does that *and* says how far along you are — `58 / 147` is exactly the sort of fraction that cannot be felt without one.
- **Legendary and mythical species are called out**: a gold cell with a **five-point star** badge in the grid (a four-point sparkle read as a "+", which says "tap me" rather than "rare") and a matching chip above the type badges in the detail popup. The generation header used to tally them too (`★ 3/5 · 74 / 147`); nobody could tell what the 3/5 meant, and the gold cells already show caught and uncaught at a glance, so the header now gives only the generation's count. The marker shows on **uncaught** slots too — it reveals nothing about which Pokémon lives there, and flagging the slot is the point: it marks something worth hunting for rather than only rewarding the find afterwards. Name and rarity chip stay hidden until it's caught.
- **Every entry is tappable**, opening a detail popup. A caught entry reads: larger artwork, the Dex number, the name, type badges, any rarity chip, a speaker, and its **evolution family**. No greeting and no caption — the dex is a list you page through, and a sentence on every entry is one to skip past thirty times in a row.
- **The family shows whether or not this one is caught**, and each relative reveals itself independently: caught ones in colour with their names, uncaught ones as silhouettes. It gives away nothing an uncaught entry is holding back, and it answers what the card is opened to ask — what is this, and what does it become. An uncaught base with the strip hidden looked like a species with no evolutions at all.
- **The family is the whole family, from wherever you are standing in it.** The strip climbs to the root of the line and then walks down breadth-first, one group per stage with an arrow between stages — so Bulbasaur, Ivysaur and Venusaur all show the same three, and Eevee shows all eight of its second stage. Stages sit side by side and **a stage that splits stacks in its own column**, so the arrow keeps meaning *this stage becomes that stage* rather than pointing at one sibling; Wurmple's two branches line up as pairs, Silcoon → Beautifly over Cascoon → Dustox. Wrapping used to strand the first stage on a line of its own with an arrow pointing at nothing. **Eevee's family alone runs downward** — Eevee, an arrow turned to point down, then the eight in a four-wide grid — because eight is too many for a column. 72 species are in a family that splits; the other 266 families are straight lines and look as they did. On screens under 700px tall the strip's pictures drop from 42px to 34px, so the tallest families still fit a 360×640 phone. Depth is capped and the climb is bounded, since `evolves_from` is hand-editable and a cycle would otherwise hang the popup.
- **Opening an entry says its name aloud.** One rule covers every way in — tapping a Pokédex cell, tapping a relative in the evolution family, tapping a catch on the results screen, and the catch popup itself. A name a child has only ever read is a name they can't yet use, and the picture is on screen at the moment it's said.
  - It hangs off *opening*, not rendering: re-rendering a card that is already on screen stays silent, because a name repeated without a new thing to look at is noise rather than teaching.
  - The speaker button covers repeats, and an uncaught entry has none — it gives up the outline, its number, its **type** and its family strip, and nothing else: no name, no greeting, no read-aloud. Type is the one thing shown either way; it is a single short word, it says something useful about a slot still to fill, and it doesn't name what's hiding in it.
- **The popup navigates to itself, and there is no Back.** Tapping a relative replaces what's on screen with that relative; **Okay** is the only button, from every entry. A back trail is unnecessary now the strip shows the *whole* family from wherever you land in it — every relative you could have come from is still one tap away, so walking a line in either direction uses the same control.
- **Why the strip earns its place:** National Dex order already puts 83% of families side by side, but cross-generation evolutions can sit hundreds of slots apart — Pichu is #172 and Pikachu #25 — and no amount of scrolling the grid makes that relationship visible.
- A newly caught Pokémon is flagged with a **NEW** badge in the grid until its entry is opened, so a catch made mid-session can be found again without hunting through a thousand entries. The flag is stored separately from the collection itself.

## 8b. Home HUD

The home screen opens on a **meadow**: sky, sun and clouds, three rolling hills with trees on the far one, bushes and flowers on the near one, and a mound in the middle for the Pokémon to stand on — one drawing, cropped from the sides as the screen narrows so the middle is always in view. The HUD rides on its sky — two counters on the left, the Pokéball mark and the gear on the right — and one of the child's own Pokémon stands on its hill (§8c).

**No logo is drawn.** The words "Poké Learning" stay in the page as its heading for anything reading it, but nothing of the brand is on screen. A 28px Pokéball mark used to sit beside the gear; in a row of round buttons it looked tappable and did nothing, and the app's name tells a child nothing they need. The other screens open with the shared chrome (a ✕ beside the screen's name), and a round with the ✕ and progress bar.

**The icons are drawn, not typed** — inline SVG on one 24×24 grid, taking their colour from the counter they belong to via `currentColor`. Emoji cannot do this job: their em-boxes align but their *ink* does not, and the metrics belong to whichever emoji font the device happens to have. The same holds for every other icon in the app — speakers, ticks and crosses, the play and battle marks, the rarity star — which are drawn too, so no screen depends on an emoji font.

**Each counter is a white pill carrying an icon, a number and one short word**: `1 of 2 today`, `4 days`. Bare numbers read as scores to a grown-up glancing over, and the word costs a child nothing — the icon and colour still carry the meaning. **Below 380px wide the words drop and the numbers stay**: two pills, the ball and the gear need about 330px with words, which a 360px phone does not have.

### Screen chrome

**Every screen you can back out of wears the same two rows**: the HUD, then a ✕ beside the screen's name in caps — `SETTINGS`, `BATTLE`, `POKÉDEX`, `MY PROGRESS`. The HUD is persistent chrome and reads as belonging to the app; the row under it names the place you are in and gets you out of it. Those are different jobs, which is why they are different rows — on one line the ✕ read as a fourth counter.

It is **declared once, not written per screen.** A `SCREEN_CHROME` map holds each screen's title and, optionally, something to show beside it; `show()` renders it. Only Battle uses the extra slot, for its session record — a ✓ count and a ✗ count, each in its own pill.

**A screen with chrome does not also carry a heading card.** It sits on cream paper rather than the meadow: the meadow is for the screens that have a stage — home, a question, the results, a catch and the battle arena.

**Not on a round**: that has its own progress bar and ✕, and a second row of counters there would be two things to read at once.

**The round's top bar is a ✕ and a bar, nothing else**, sitting on a strip of meadow above the question card. The ✕ — here and beside each screen's name — is the drawn cross icon at 28px, not the ✕ character, which came out about 9px across in its 44px circle. **The bar is one segment per question** for rounds of up to 20: answered ones green, the one being answered amber, the rest white, so a round reads as a number of steps. It counts credits, not questions seen, so a guessed answer leaves it where it was. A longer round (Settings allows up to 50) keeps a continuous bar, since 50 segments on a phone are 3px each; 20 are 9.5px at 360 wide. **The card ends where its question ends**, with paper below it; feedback and the ✓ appear under the answers, so when they arrive only the card's bottom edge moves. Where the screen has room to spare the question's contents scale up rather than leaving the card half empty — 1.15× from 440×820, 1.35× from 700×960. The bar's fill says how far along the round is, so a `3 / 10` beside it would be the same fact written twice. It is one continuous green fill on a white track — not a row of segments, because the round length is a setting from 1 to 50. The ✕ keeps an `aria-label`.

| Counter | Shows | Goes to | Where |
|---|---|---|---|
| target | rounds finished today against the daily goal; neutral until the goal is met, then **green** | My progress | everywhere |
| flame | consecutive days that met the rounds goal | My progress | everywhere |
| dex | caught/total for the **current generation only** — the one the collection gate is on | Pokédex | chrome screens and results |

**The collection counter is not on the home HUD.** Home already shows it on the Pokémon's name card (§8c), as a full-width row that is the way into the Pokédex from home; a second copy in the corner of the same screen was the same number twice. Every other screen with a HUD keeps it, as its fixed route to the Pokédex.

Today stays neutral until the day's goal is met, because **green means done** and nothing else on that row. Each counter keeps its own `aria-label`, which spells out what the number is.

The same HUD appears on the results screen, centred over the meadow. The gear is home-only.

A "round" is one full session; how many questions make up a round, and how many rounds a day the streak needs, are both Settings values.

**The streak holds until the day actually ends.** It counts consecutive days ending today *or yesterday*, so a streak earned yesterday still reads correctly at 8am before anything has been played, and only breaks once a whole day has passed without meeting the goal. Daily round counts are kept indefinitely rather than pruned to a window — pruning would silently cap the streak at the window's length.

## 8c. Home Showcase

**One of the child's own Pokémon stands on the meadow's hill**, as big as the screen allows, with a white **name card** tucked under the hill below it: name and Dex number, **type badges**, then a row for the Pokédex.

**Types show whether or not it is caught.** On a caught Pokémon they are one more fact about it; on an uncaught one they are the only thing the card gives up besides the outline.

**Two targets, so neither is itself a button inside a button.** Tapping the Pokémon re-rolls the pick, as does every return to the home screen; tapping the Pokédex row opens the Pokédex.

**The Pokédex row is the whole width of the card and at least 46px tall** — the Pokédex icon, `Generation 1 · 14 of 147`, a small bar in the Pokédex's colour, and `Pokédex ›`. It is the only way into the Pokédex from home, so it is a finger-sized target rather than a link at the end of a line. Below 400px wide the small bar drops so the words stay on one line. The bar is the level tiles' own `.level-bar`: `14 of 147` has exactly the problem the progress panel argues a bar solves.

It names the generation of the Pokémon **on screen**, not the one being hunted. Those differ whenever a freshly opened generation is still empty and the shelf falls back to the last one, and a count from a different generation than the picture above it would be two subjects on one card.

It is a trophy shelf, not a teaser: it only ever shows a species already caught. It prefers the generation being worked on but falls back to the whole collection, so a freshly opened generation — where nothing is caught yet — still shows off the previous one's catches rather than going blank.

**Before anything at all is caught** there is no trophy to show, so the hill holds a grey outline and the card shows its Dex number and **type badges** — an outline and one short word, no sentence (§14.1). The generation count still shows, at `0 of 147`, because a goal is a number rather than a sentence.

## 8d. Home Levels

Headed **"Your progress"**, five small white cards — Spelling, Reading, Alphabet, **Add & take away** and **Times & share** — two across on a phone and three from 640px (two again in the right-hand column of the wide layout), each showing the track's icon, its **current level**, the number of levels on that trail, and a coloured bar for how far along it is. A maths family that has not opened says **Locked**.

The heading is set through `text-transform` rather than typed in capitals, the same reason the wordmark is.

**Each icon is a small square in the trail's own colour with a white mark** — `Aa` for Spelling, an open book for Reading, `ABC` for Alphabet, `+−` and `×÷` for the two maths families. With the families named in words, the icon no longer has to say *this is maths*; the colour does that, and the operators say which. The trail colours are the same ones the question screens use for their mode tags: Spelling blue, Reading violet, Alphabet teal, Add & take away berry, Times & share amber. `text-transform` is reset on the SVG text, which would otherwise inherit the label's.

**The bar is there because the number can't do the job alone.** Level 3 of 25 and level 3 of 10 are not the same place, and the number by itself implies they are.

### The fold is the constraint the whole screen is laid out against

Order is meadow (HUD and Pokémon), name card, progress, then **Start playing** and **Battle** side by side, directly under the trails — and **all of it fits on screen without scrolling**, down to 360×640. The primary action must stay visible. On a screen 700px tall or less the trail cards go back to plain tiles, because the cards' padding costs the Pokémon more height than a short phone has.

**From 900px wide the screen splits in two**: the meadow fills the left side, full height, with the Pokémon up to 340px tall; the name card, the trails and the buttons sit in a column on the right, centred vertically. A phone layout stretched across a landscape window was mostly empty sky.

Everything on the screen is a fixed cost except one thing. The HUD, the name card, five levels and two buttons all have to be legible at their size. **The meadow is the only part that can be smaller without losing what it says**, so it is the part that gives way: it takes only the height left once everything below it is laid out (a zero flex basis, at least 150px, and no ceiling — on a tall screen the spare height is more meadow, never a gap above the buttons), and the Pokémon is sized to the meadow, up to 260px. Measured at 360×640, 390×844, 414×736, 768×1024, 360×780, 820×1180, 1000×575, 1280×800 and 1440×900: no vertical scroll and no horizontal scroll on any of them. At 360×640 the Pokémon is 165px tall and Start's bottom edge sits at 622 of 640.

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
- **Locked tracks are listed too**, greyed, with what opens them — *Opens at &lt;track&gt; &lt;level&gt;*, read from the CSV. The road ahead is worth seeing, and the section keeps its shape instead of re-flowing under the reader every time something unlocks.

## 10. Battle Mode

A separate, unscored, replayable mini-game reached from the Start screen:

1. Two random, distinct Pokémon are shown on the meadow, **A vs. B**, each with a speaker button on its picture to hear its name.
2. The player predicts a winner by tapping "Pick [Name]!"
3. A short "old-school" battle animation plays: both sprites shake, generic move-announcement text appears line by line.
4. The winner is decided by a **stat- and type-weighted random roll**: each Pokémon's real Base Stat Total represents its power level, a full 18-type effectiveness chart determines typing advantage, and `P(A wins) = powerA / (powerA + powerB)`. Both fighters' types are shown as colored badges.
5. The result is announced out loud and shown as a banner, along with whether the prediction was correct.
6. A running **session record** is shown at the top of the screen and persists across replays until the page is reloaded.

## 11. Results Screen

- A heading — **"Round finished!"** — and the same HUD as the Start screen, centred, so finishing a round shows the progress it just moved.
- **What was caught this round**, under a quiet "Caught this round" label, as large tappable cards in a three-column grid that open the full catch screen — the reward is the point of this screen, so the artwork is sized to be looked at. Three fit a row at any phone width; more wrap. A catch not yet opened anywhere carries the same **NEW** badge as the Pokédex. When nothing was caught, a plain line — "No catch this time" — says so rather than inventing a consolation prize.
- **Play Again**, which starts another round at the length set in Settings, and **Go Back**.

**There is deliberately no score.** Every mode retries until the answer is correct, so a finished round is always 100%: a score would be a number that cannot vary, and any praise it drove would fire every single time. Nor is there a perfect-run reward — a promise of a Pokémon that the Pokédex would then not contain. Performance is measured where it means something: clean answers driving the Lesson Trails, shown on My progress.

## 12. Settings & Persistence

- **General**: Questions per round (how many must be answered well enough to finish, default 10), **Mistakes allowed** (wrong taps a maths, reading or alphabet question may take and still count, default 1; `0` means it must be right first time — spelling is scored on letters told instead, §5.1), **Show the answer after** (wrong taps before the answer lights up, default 2; the light goes out once taken, so the next one is earned again — outside spelling it is always held at least one above `Mistakes allowed`, so a shown answer never counts toward the round), Rounds per day (the streak goal, default 2), and **Expected drop** — out of 100 questions, roughly how many hide a Pokémon. It is the measured outcome, pity timer included, not the underlying roll (§8).
- **Per mode**: an on/off toggle for Spelling, Reading, Alphabet, Math, and Visual Math. **With every mode off, Start opens a short notice** — "Nothing to play yet", with a button straight to Settings — rather than a browser alert, which a child cannot read and which looks like the page broke.
- **Per trail**: a frontier dropdown showing the current level in plain language, built from that level's own CSV row — which doubles as the manual placement control. All ten trails are listed, maths one row per track rather than per family, since this screen is read by a parent placing a child precisely. A maths track that has not met its prerequisite yet is shown locked with what opens it.
- **About**: a build number, the date that build was published, and the Last-Modified date of the HTML file this device actually loaded. Because a cached page reports the cached copy's date rather than today's, the two together tell a stale copy apart from a fresh one — the app is one static file that browsers cache aggressively, so "am I even running the new version?" is a real question. The build number has no build step behind it and is maintained by hand.
- Everything saves to `localStorage` on every change and reloads automatically on the next visit. Settings degrade gracefully: if storage is unavailable (e.g. private browsing) the app uses defaults instead of erroring.

## 13. Data & Offline Assets

All game data lives in **`data/*.csv`**, fetched and parsed at startup rather than embedded in code, so it can be maintained in a spreadsheet without touching the app. **The ladders are authored in [the design sheet](https://docs.google.com/spreadsheets/d/1MtlBnXPMFt3x_LpcMmWe7LIeISjoC9wJddhTM8_zbVY/edit)** and exported here; `data/README.md` documents every column and the editing traps. Rows may be reordered freely; the app sorts where order matters.

| File | Rows | Columns |
|---|---|---|
| `data/pokemon.csv` | 1,021 | `id`, `name`, `type1`, `type2`, `base_stat_total`, `rarity`, `evolves_from` |
| `data/items.csv` | 922 | `name`, `image`, `category` |
| `data/pronunciations.csv` | 184 | `name`, `say_as`, `source` |
| `data/word_levels.csv` | 807 | `word`, `level`, `pattern`, `letters`, `syllables`, `compound_parts`, `also_matches`, `proper_noun`, `used_in_items`, `previous_level`, `review` |
| `data/item_levels.csv` | 922 | `item`, `level`, `kind`, `words`, `components`, `component_levels`, `proper_noun`, `shared_art`, `letters`, `longest_word`, `spellable` |
| `data/spelling_levels.csv` | 25 | `level`, `word_level`, `compound_level`, `name_letters`, `hinted_letters`, `promote_5_pct`, `promote_10_pct` |
| `data/reading_levels.csv` | 10 | `level`, `word_level`, `compound_level`, `name_letters`, `wrong_answers`, `distractor_level`, `promote_5_pct`, `promote_10_pct` |
| `data/alphabet_levels.csv` | 11 | `level`, `alpha_length`, `alpha_blanks`, `alpha_blank_position`, `promote_5_pct`, `promote_10_pct` |
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

- **"Crafted storybook" style.** Screens with a stage — home, a question, the results, a catch, the battle arena — sit under a flat meadow: sky, rolling hills, and on a question the grass strip as the meadow's own grass. Everything else is cream paper with white cards outlined in a warm line. Flat colour throughout — no gradients, glows or glossy buttons; pressable things sit on a solid edge that collapses when tapped. Colours come from one set of tokens (leaf, sky, sun, berry, violet, teal, warm neutrals) and every text colour holds at least 4.5:1 on the surface it sits on. The tokens, components and mockups of every screen live in the design system artifact.
- Mobile-first responsive layout: touch targets sized for small screens, a dedicated `@media (max-width:480px)` breakpoint, no horizontal page scroll.
- **Pinch and double-tap zoom are off.** A small child holding a tablet triggers them by accident and cannot undo them, and a screen stuck at 2.4× is a broken app to them. It takes three mechanisms because no one of them covers every browser: `user-scalable=no` on the viewport meta, `touch-action: pan-x pan-y` on `html,body`, and `preventDefault` on Safari's non-standard `gesture*` events. Panning and scrolling are untouched. The obvious fourth — cancelling any `touchend` within 300ms of the last, to stop double-tap zoom — is deliberately **not** used: it also cancels the click that follows, and this game is played by tapping tiles in quick succession.
- Speech synthesis is used in Spelling, Battle, Reading and the Pokédex — in Reading, only ever to name a picture, and never in its Alphabet mode (§7.2). Utterances are pinned to `en-US`, since otherwise the OS default voice applies its own language's phonetics to English spellings. Names the synthesiser mangles are respelled via `data/pronunciations.csv` (§13); overrides affect **speech only**.
- Read-aloud has one consistent affordance: a round **sun-yellow speaker button at least 44px across** sitting **on the picture itself**, at the lower-right of the circular frame, rather than a labelled button in the action row below. That holds across Spelling, Missing Letters, Read & Choose, the catch screen, the Pokédex popup and both Battle fighters. Reverse Read & Choose gives each picture option its own, just below the picture rather than on it (§7.2). Alphabet has no speaker anywhere — every name on screen is a first letter, so speaking one would give the answer away.
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
