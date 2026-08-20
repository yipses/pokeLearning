# Poké Learning — Lesson Trails (Curriculum Design)

> **Status:** This is the original curriculum design document (originally published as a Claude artifact, "Poké Learning — Lesson Trails," v2). All four trails described below — Add/Subtract, Multiply↔Divide, Spelling, and Reading — plus My progress (the dashboard screen) have since been fully built; this file is kept as detailed design reference (exact word lists, level tables, promotion rules) that isn't fully duplicated in `Overview.md`'s higher-level summary. For current build status, see `progress.md`.

Math splits into two independent strands — **Add/Subtract** and an interleaved **Multiply↔Divide** — plus **Spelling** and **Reading**, which share one graded vocabulary but climb it at their own pace. Each trail has its own frontier and advances on its own schedule.

20 questions/day, split across all 4 tracks — about **5 questions/day per track**. Multiply↔Divide counts as one track for this split (it shares a single frontier), so each of its ~5 daily picks independently rolls whether it lands on a × or ÷ step.

Nothing here is a hard gate a kid must fully clear before moving on — see the mix model below.

## How a day actually works

**Not blocks — a blend.** Every round mixes three bands around each trail's **frontier** (the level currently being worked on), reshuffled into one queue rather than played in order.

**Two ways to promote.** Tracking **clean** answers only (right on the first try, no hints) — **5/5** clean in a row promotes instantly; otherwise **8/10** (80%) clean in the rolling window promotes. Whichever hits first. No demotion — Review keeps old levels sharp instead.

These windows are deliberately short. A child who has a level shouldn't have to prove it twenty times to leave it, and one they haven't got keeps coming back through the Review band anyway. The 80% bar is unchanged from the original 16/20 — the same standard on half the evidence, which trades a little precision for a lot less grinding. The percentages are **per level**, read from the Spelling and Reading CSVs, so the two trails can be tuned apart without touching code; Math has no CSV yet and falls back to the same figures. My progress's labels and gate lines are drawn from whichever row the track is on.

**You can place the pin.** The frontier is editable in Settings, in either direction — up if a kid's already ahead, down if a level was set too high. Moving it resets that track's Last 5 / Last 10 windows.

**Mix:** Review — 20%, below frontier · Current — 60%, at frontier · Stretch — 20%, above frontier

### What counts as "right"

The app itself never changes — every question can still be retried until it's solved, same as always, no new fail state. But for the purposes of promotion tracking, an answer only counts as **correct** if it's right on the **first attempt**, with **no wrong guesses and no hints used**. Getting there on the second try, or after a hint, still feels like success to the kid and still moves the session on — it just doesn't count toward Last 5 / Last 10. This is the only definition of "correct" used anywhere in this document.

---

## Math

Two independent strands, each with its own frontier — a kid can be ahead on one and building up the other.

### Add / Subtract — 8 levels

| # | Level | Skill | Range | Example |
|---|---|---|---|---|
| 1 | Within 5 | Single digits, smallest sums. | 0–5 & 0–5 | |
| 2 | Within 10 | Single digits, full range. | 0–10 & 0–10 | |
| 3a | Teen + Ones | A teen number plus a single digit — often no carry. | 10–20 & 0–9 | 12+7 |
| 3b | Teen + Teen | Two teens together — regularly crosses 20. | 10–20 & 10–20 | 12+15 |
| 4a | Within 40, no regrouping | Two-digit numbers, ones don't carry. | 0–40 & 0–40 | 23+15=38 |
| 4b | Within 40, with regrouping | Same range, ones now carry into tens. | 0–40 & 0–40 | 27+15=42 |
| 5a | Within 100, no regrouping | Full two-digit range, ones don't carry. | 0–100 & 0–100 | 53+34=87 |
| 5b | Within 100, with regrouping | The Grade-2 fluency target — full range, real carrying. | 0–100 & 0–100 | 57+34=91 |

**Visual Math** (picture-grouped Pokémon) covers Levels 1–2 as the concrete/pictorial lead-in, then drops out of "current" once ranges exceed what's legible (icon counts stay legible only up to ~6–8) — it stays available forever as a low-stakes Review option. Multiplication visuals always show at least 2 groups — a single group (e.g. "5×1") doesn't actually demonstrate repeated addition.

**Patterns** weave into every level instead of being a separate mode — ~30% of questions become a 4-in-a-row skip-counting set instead of one equation. Step size isn't a fixed list; it's any value where 4 repetitions still fit the level's range, so Level 1 only offers step-1, but Level 5b opens up to step-25.

### Multiply ↔ Divide — 12 steps, interleaved

| # | Op | Step | Range | Example |
|---|---|---|---|---|
| 1 | × | Tiny facts | 1–3 × 1–3 | 2×3=6 |
| 2 | × | Small facts | 1–5 × 1–5 | 4×3=12 |
| 3 | ÷ | Tiny facts, inverse | quotient 1–3, divisor 1–3 | 6÷2=3 |
| 4 | ÷ | Small facts, inverse | quotient 1–5, divisor 1–5 | 12÷4=3 |
| 5 | × | Small anchor, mixed | 1–5 × 1–10 | 4×8=32 |
| 6 | ÷ | Small anchor, mixed | quotient 1–5, divisor 1–10 | 32÷4=8 |
| 7 | × | Harder tables only | 1–5 × 6–10 | 3×9=27 |
| 8 | ÷ | Harder tables only | divisor 6–10, quotient 1–5 | 27÷9=3 |
| 9 | × | Flipped orientation | 1–10 × 1–5 | 8×4=32 |
| 10 | ÷ | Flipped orientation | quotient 1–10, divisor 1–5 | 32÷4=8 |
| 11 | × | Full range | 1–10 × 1–10 | 7×9=63 |
| 12 | ÷ | Full range | quotient 1–10, divisor 1–10 | 63÷9=7 |

**Visual Math** (equal-groups pictures) leads Steps 1–2 as the "why multiplication works" concept, then fades to Review the same way — capped at 1–6, can't represent 6–10 range facts legibly.

**Patterns** only weave into Steps 1–6 and 11–12 — the fixed ×1..×4 shape can't represent "harder tables only" (7–8) or "flipped orientation" (9–10), which depend on a specific second-operand range the pattern structure can't express.

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

Nine tiers of three. Within a tier only **`hinted_pct`** moves, the share of the word given away: 50% → 25% → 0%. Above zero the task is Missing Letter; at zero it is Full Spelling from empty tiles. **`max_hints`** rises as `hinted_pct` falls — the level that shows least offers most help finding the rest.

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

One status page per kid — where each trail's frontier sits right now, how close it is to promoting, and the trend behind that number. Each card shows:

- Track name and current level label
- Days at the current level
- Last-10 and Last-20 progress bars with exact fractions
- A rolling-accuracy trend chart plotting Last-10 and Last-20 % over recent attempts, with dashed threshold lines at the 80% (Last-20 gate) and 100% (Last-10 gate) promotion thresholds
- A ★ marker wherever a 5/5 instant promotion happened, and a dashed "Leveled up" line wherever the slower 8/10 path fired instead

---

**Original status footer (superseded):** *"Status: Math is live, the rest is still this document."* — kept here for historical accuracy; see the status note at the top of this file and `progress.md` for what's actually built now.
