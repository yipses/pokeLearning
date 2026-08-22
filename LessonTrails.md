# Poké Learning — Lesson Trails (Curriculum Design)

> **Status:** This is the curriculum design document (originally published as a Claude artifact, "Poké Learning — Lesson Trails," v2), kept for the design reference that `Overview.md`'s higher-level summary doesn't duplicate: exact word lists, level tables and the reasoning behind them. Everything described here is built. For how it got built and what's still open, see `progress.md`.
>
> **The maths half was redesigned.** The two strands below became **eight CSV-defined tracks** — see *Maths* — and the level tables that used to sit here are now `data/math_levels.csv`. The Spelling and Reading halves are current.

**Spelling** and **Reading** share one graded vocabulary but climb it at their own pace. **Maths** is eight tracks that open on each other's progress. Every trail has its own frontier and advances on its own schedule.

A round is split in thirds — spelling, reading, maths — with the maths third shared among whichever maths tracks are open. Splitting evenly across all ten tracks instead would make a fully-unlocked round 80% maths.

Nothing here is a hard gate a kid must fully clear before moving on — see the mix model below.

## How a day actually works

**Not blocks — a blend.** Every round mixes three bands around each trail's **frontier** (the level currently being worked on), reshuffled into one queue rather than played in order.

**Two ways to promote.** Tracking **clean** answers only (right on the first try, no hints) — **5/5** clean in a row promotes instantly; otherwise **8/10** (80%) clean in the rolling window promotes. Whichever hits first. No demotion — Review keeps old levels sharp instead.

These windows are deliberately short. A child who has a level shouldn't have to prove it twenty times to leave it, and one they haven't got keeps coming back through the Review band anyway. The 80% bar is unchanged from the original 16/20 — the same standard on half the evidence, which trades a little precision for a lot less grinding. The percentages are **per level**, read from the Spelling and Reading CSVs, so the two trails can be tuned apart without touching code. Maths has its own table in `data/math_promotion.csv` and a different shape — three gates: 5 at 100%, 10 at 90%, 20 at 85%. My progress draws one bar per gate, from whichever row the track is on.

**You can place the pin.** The frontier is editable in Settings, in either direction — up if a kid's already ahead, down if a level was set too high. Moving it resets that track's Last 5 / Last 10 windows.

**Mix:** Review — 20%, below frontier · Current — 60%, at frontier · Stretch — 20%, above frontier

### What counts as "right"

The app itself never changes — every question can still be retried until it's solved, same as always, no new fail state. But for the purposes of promotion tracking, an answer only counts as **correct** if it's right on the **first attempt**, with **no wrong guesses and no hints used**. Getting there on the second try, or after a hint, still feels like success to the kid and still moves the session on — it just doesn't count toward Last 5 / Last 10. **This is the only definition used anywhere in this document**, and it is the strict one.

The app has a second, looser bar that this file is not about: a question counts toward **finishing a round** if it took at most `Mistakes allowed` slips (a Settings value, default 1). That governs how long a round runs, never what promotes. Loosening the round does not loosen the ladder — see `Overview.md` §5.

---

## Maths

Eight tracks — add, subtract, multiply, divide, and a skip-counting pattern track for each. Levels live in `data/math_levels.csv`, prerequisites in `data/math_tracks.csv`, promotion gates in `data/math_promotion.csv`.

**The numbers are not in this file.** How many levels a track has, what ranges each asks for, and which track unlocks which are all authored in [the design sheet](https://docs.google.com/spreadsheets/d/1MtlBnXPMFt3x_LpcMmWe7LIeISjoC9wJddhTM8_zbVY/edit) and exported to those CSVs. This file is the *why*; the sheet is the *what*, and restating it here only gives it somewhere to drift.

### What replaced the two strands

The old design was **Add/Subtract, 8 levels** and an interleaved **Multiply↔Divide, 12 steps sharing one frontier**, with skip-counting patterns woven in as roughly 30% of questions on both. Three things were wrong with it:

- **A shared frontier hides a real gap.** Multiply and divide moved together, so a child fluent at `4×3` and lost at `12÷4` had one number describing both, and could not practise the weaker one without re-proving the stronger.
- **Patterns as a 30% dice roll cannot be practised.** Counting by 3s turned up when it turned up. As its own track it has its own levels, its own frontier and its own promotion, so it can be worked at.
- **The ladder was a queue, not a map.** One list marched through in order. Tracks now **open on prerequisites**: the four operations chain (subtract at add 5, multiply at add 7, divide at multiply 5) and each pattern track hangs off its own operation at level 3 — so the ladder *widens* as it is climbed and everything open has a chance to come up. Liveness is transitive: a track whose own prerequisite has not opened cannot open the next.

**Regrouping is no longer controlled for.** The old levels 4a–5b used rejection sampling on whether the ones digit carried, making "no regrouping" and "with regrouping" distinct rungs rather than wider ranges. The CSV ladder expresses difficulty as operand ranges only. That is a real loss of precision, traded for a ladder a parent can edit in a spreadsheet without touching code — and the reason it is written down here rather than quietly dropped.

**Visual Math leads the early rungs and stops where the sheet says.** It is a rendering of the same questions, not a source of its own, and `visual` is a column per level rather than the code guessing from the numbers. Multiplication visuals always show at least 2 groups — a single group (`5×1`) doesn't demonstrate repeated addition.

**Division never leaves a remainder.** The quotient is chosen first, from those that land the dividend inside the row's range.

**A subtraction pattern has to start high enough to take every step** without going below zero — anchor ≥ step × 4. Where only part of a row's anchor range qualifies, the anchor is drawn from that part; where none does, that step is skipped silently, which is a trap worth knowing when editing the sheet (see `data/README.md`).

---

## Spelling and Reading

Both trails now sit on one vocabulary grading, and both are defined entirely in CSV — `data/spelling_levels.csv` (25 levels) and `data/reading_levels.csv` (10). Nothing about either ladder lives in code.

### What replaced Phases A and B

Spelling used to run nine phonics levels over 100 hand-picked single-word items, then five fluency levels over Pokémon names graded by length. The word "phase" bundled four independent things — where words came from, how they were graded, which task was used, and whether the generation gate applied — and the seam was broken: the phonics half ended on *Refrigerator* (12 letters) and the fluency half began on a 3-letter cap, which in Gen 1 means `mew` and `muk`. Hard, then trivial, then climbing again. It also reached only 100 of 909 usable item names, because the rest are multi-word and it had no way to grade them. The four things are four columns now, and one ladder runs end to end.

It also wasted the catalogue. Only 100 of 909 usable item names were reachable, because the other 809 are multi-word and the phonics ladder had no way to grade them.

The four things are now four columns, and one ladder runs end to end.

### How a level selects words

| Column | Selects |
|---|---|
| `word_level` | single-word items graded at or below this phonics level (1–9) |
| `compound_level` | multi-word items whose hardest component is at or below this; `0` switches compounds off |
| `pokemon_letters` | Pokémon names up to this many letters, generation-gated as before |

Pokémon keep a length gate rather than a phonics level because invented names have no decoding pattern to grade. Item words do: **`data/word_levels.csv`** grades all 807 distinct words in the catalogue against the nine patterns, and **`data/item_levels.csv`** rolls that up per item — a single-word item takes its own level, a multi-word item takes its hardest component's. `Copper ore` is level 7 because `copper` is; `Log bed` is level 1 because both halves are.

The split between "single" and "multi-word" is the one the child can see: a **space or hyphen** makes it multi-word, because the spelling screen draws separate slot groups either side of one. `Birdhouse` is a single word graded 8 by the compound-words *pattern*; `Black charcoal` is a multi-word item graded by its parts. Two different senses of "compound", and they don't interact.

### The nine phonics patterns

Unchanged as a grading scheme, now applied to the whole catalogue rather than 100 words:

| Level | Pattern | Words graded | Items reachable |
|---|---|---|---|
| 1 | Short-vowel CVC | 58 | 13 |
| 2 | Floss doubles | 8 | 3 |
| 3 | Consonant blends | 67 | 33 |
| 4 | Digraphs | 79 | 37 |
| 5 | Silent-e | 52 | 44 |
| 6 | Vowel teams | 107 | 116 |
| 7 | R-controlled | 117 | 164 |
| 8 | Compound words | 101 | 145 |
| 9 | Multisyllabic | 218 | 354 |

Grading is generated by `tools/classify_words.py` and corrected by hand in the spreadsheet. It reproduces 91 of the original 100 hand-graded words; the rest are flagged `differs` in the CSV, and they are genuinely arguable — several words match three patterns at once and which one a teacher would name is a judgement rules only approximate.

Note that a word's level and an *item's* level pull apart: 58 words are level 1, but only 13 items are, because an item takes its hardest word. `bed` is level 1 and appears in 15 item names — only `Log bed` is playable at level 1; the rest are dragged up by their partner (`Iron bed` is 7, `Luxury bed` is 9).

### Spelling — 25 levels

Nine tiers of three. Within a tier only **`hinted_pct`** moves, the share of the word given away: 50% → 25% → 0%. Above zero the task is Missing Letters; at zero it is Full Spelling from empty tiles. **`max_hints`** rises as `hinted_pct` falls — the level that shows least offers most help finding the rest.

Blanking is chunk-aware. The word is tokenized first (`sh`, `ck`, blends and vowel teams count as one unit), then whole chunks are hidden until the level's letter target is reached, always leaving one chunk showing. So the percentage is a target to reach, not a quota to hit exactly: a blank never splits a sound.

Level 1 is a single rung rather than three, so the opening six words are five questions rather than fifteen.

**Both tasks answer the same way, in the same units:** tap a tile holding a chunk. `torch` is three slots and three tiles — `T`, `OR`, `CH` — whether it is being built from nothing or repaired. Input method and difficulty are deliberately independent: `hinted_pct` is the difficulty knob, and how a child answers should have nothing to do with it. Two earlier splits welded them together — first tiles for one task and a typed box for the other, which put an on-screen keyboard over most of the ladder; then chunk tiles on one screen and letter tiles on the other, so `CH` was one group in one place and two in another. Typing still works in Full Spelling: keystrokes buffer until they complete the chunk that comes next.

### Sounding out

A correct placement plays the sound of the chunk it just completed; a wrong one is silent, because a child who finds that tapping makes noises will tap for noises. Completing the word speaks it whole — sound out, then blend back, which is the actual phonics move.

The sound has to come from the word, not the letter: `a` differs in `cat`, `cake` and `car`. The chunker already makes `ar` a single unit, so r-controlled vowels, vowel teams, digraphs and blends are context-free; only lone vowels need deciding, by the shape of the word around them — vowel, one consonant, final `e` is long, otherwise short. The final `e` says nothing, which is the correct thing to teach. Respellings live in `data/phonemes.csv`, and a chunk with no row is **silent by design**: a wrong sound teaches a wrong thing, silence teaches nothing.

**Pokémon-branded item names are excluded from Spelling.** `Hoppip water bottle` and `Pikachu doll` carry a phonics level like anything else, but it is fiction — an invented proper noun is memorised, not decoded, so producing one letter by letter isn't spelling practice. Reading keeps them, since recognising a name a child knows by sight is fair, and the names stay reachable as Pokémon proper under the generation gate.

### Reading — 10 levels

Same three selection columns, two of its own:

- **`wrong_answers`** — decoy count. Choices run 3, 4, then 5 from level 3 on.
- **`distractor_level`** — *another reading level*, whose pool supplies the wrong answers. Always at or above the level's own row, so decoys come from a superset of the target pool. A child meets harder words as options before being asked to read them, and it fixes the thinness at the bottom: level 1 targets from 6 words but draws decoys from 12.

This replaced a "tricky distractor" flag that hand-picked same-length or same-first-letter decoys. Difficulty now comes from pool breadth instead, and the two formats (Read & Choose, Reverse Read & Choose) are chosen at random per question rather than being rungs of their own.

### Why the frontiers are separate

Same grading, two frontiers. Reading will naturally run ahead of Spelling, and that is the intended shape: recognise a word, then produce it. The old trails drew from unrelated pools, so nothing one taught reinforced the other.

### Promotion

Both `promote_5_pct` and `promote_10_pct` are per level, read from the row. Currently 100% and 80% everywhere, matching what the engine used to hardcode — but they can now differ per level and per trail without touching code.

## My progress

One status page per kid — where each trail's frontier sits right now, how close it is to promoting, and the trend behind that number. A week of daily round counts comes first, then **Spelling** and **Reading** get a card each and **maths gets two**, one per family, because eight full cards is a scroll nobody reads.

A card, or a maths track opened out of its family row, shows:

- Track name and current level label
- Days at the current level
- One progress bar per promotion gate, with exact fractions — Last 5 and Last 10 on the word trails, Last 5 / 10 / 20 on maths

There is no per-track accuracy chart. Rolling accuracy resets at every promotion, so charting it across levels drew a sawtooth against gate lines that were crossed once per tooth. The bars answer what the screen is for. `trend` is still recorded per attempt; nothing draws it.

The two maths cards are headed with the family's summed level — `+ / −` out of 31, `× / ÷` out of 26 — then list their four tracks as rows. Locked tracks are listed too, greyed, with what opens them.

---

**Original status footer (superseded):** *"Status: Math is live, the rest is still this document."* — kept here for historical accuracy; see the status note at the top of this file and `progress.md` for what's actually built now.
