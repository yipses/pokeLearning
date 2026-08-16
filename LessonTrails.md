# Poké Learning — Lesson Trails (Curriculum Design)

> **Status:** This is the original curriculum design document (originally published as a Claude artifact, "Poké Learning — Lesson Trails," v2). All four trails described below — Add/Subtract, Multiply↔Divide, Spelling, and Reading — plus the Dashboard have since been fully built; this file is kept as detailed design reference (exact word lists, level tables, promotion rules) that isn't fully duplicated in `Overview.md`'s higher-level summary. For current build status, see `progress.md`.

Math splits into two independent strands — **Add/Subtract** and an interleaved **Multiply↔Divide** — plus **Spelling**, which starts with real, phonetically-patterned words before moving into Pokémon-name fluency, plus **Reading**, its own ladder built to fix a real flaw in the old Match mode (since removed). Each trail has its own frontier and advances on its own schedule.

20 questions/day, split across all 4 tracks — about **5 questions/day per track**. Multiply↔Divide counts as one track for this split (it shares a single frontier), so each of its ~5 daily picks independently rolls whether it lands on a × or ÷ step.

Nothing here is a hard gate a kid must fully clear before moving on — see the mix model below.

## How a day actually works

**Not blocks — a blend.** Every round mixes three bands around each trail's **frontier** (the level currently being worked on), reshuffled into one queue rather than played in order.

**Two ways to promote.** Tracking **clean** answers only (right on the first try, no hints) — **10/10** clean in a row promotes instantly; otherwise **16/20** (80%) clean in the rolling window promotes. Whichever hits first. No demotion — Review keeps old levels sharp instead.

**You can place the pin.** The frontier is editable in Settings, in either direction — up if a kid's already ahead, down if a level was set too high. Moving it resets that track's Last 10 / Last 20 windows.

**Mix:** Review — 20%, below frontier · Current — 60%, at frontier · Stretch — 20%, above frontier

### What counts as "right"

The app itself never changes — every question can still be retried until it's solved, same as always, no new fail state. But for the purposes of promotion tracking, an answer only counts as **correct** if it's right on the **first attempt**, with **no wrong guesses and no hints used**. Getting there on the second try, or after a hint, still feels like success to the kid and still moves the session on — it just doesn't count toward Last 10 / Last 20. This is the only definition of "correct" used anywhere in this document.

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

## Spelling

Two phases on one trail — the daily mix just pulls from wherever Spelling's single frontier currently sits, same as every other track. Phase A actually teaches phonics using real words pulled from Pokopia items. Phase B is fluency practice on words already known by ear (Pokémon names) — no new decoding skill, just recall.

Interacts with Pokédex generation-gating like this: that gate only ever applied to *Pokémon names*, so Phase A's items were never subject to it — an item word is available the moment its pattern-level unlocks, full stop. Phase B's Pokémon names still respect it: a word can't appear in Phase B until its species has been caught, on top of the length/hint ceiling for the current level.

### Phase A — Phonics Ladder (real words, ordered like school does it)

| # | Pattern | Skill | Words available | Examples |
|---|---|---|---|---|
| 1 | Short-vowel CVC | Simplest decoding — one consonant, one short vowel, one consonant. | 4 — thin | Fan, Mug, Sign, Sink |
| 2 | Floss-rule doubles | ll / ss / ff after a short vowel. | 3 — thin | Bell, Bill, Moss |
| 3 | Consonant blends | Two consonants blended smoothly — fl, gl, gr. | 3 — thin | Fluff, Glass, Gravel |
| 4 | Digraphs | Two letters, one sound — sh, ch, th, wh. | 9 | Shutter, Torch, Perch, Wheat… |
| 5 | Silent-e (magic e) | Trailing e makes the vowel say its name. | 10 | Bike, Rope, Slide, Wire… |
| 6 | Vowel teams | Two vowels, one sound — ay, ea, oo. | 11 | Clay, Leaf, Seaweed, Book… |
| 7 | R-controlled vowels | ar / er / or reshape the vowel sound entirely. | 14 | Cart, Barrel, Fern, Letter… |
| 8 | Compound words | Two known words joined — its own real skill. | 18 | Bathtub, Campfire, Mailbox… |
| 9 | Multisyllabic | Longer real vocabulary, several syllables. | 24 | Computer, Refrigerator, Treasure… |

Counts are audited against the actual item catalog, not guessed — every word already has a real image. **Patterns 1–3 are genuinely thin** (3–4 words each): early levels will repeat words more than later ones. That's normal for beginning practice, not a bug, but it's why those levels won't feel as fresh as Multisyllabic or Compound Words, which are the deepest pools by far. No invented words anywhere — if a pattern doesn't have real catalog words, it doesn't get a level. Dropped from the source list: *Wyndon* (a place name) and *Tinkagear* (invented game jargon).

> *(Build note: during implementation, "Sign," "Pizza," and "Tires" were also dropped as too irregular/redundant for phonics teaching, and "Bill" turned out to be a mislabeled picture of a music CD rather than a real word — fixed by renaming that catalog entry to "CD" and removing it from this list. Floss-rule doubles ended up with 2 real words instead of 3 as a result. See `progress.md` Phase 12.)*

### Phase B — Fluency (Pokémon names, staggered by task)

Full Spelling (empty tiles, build the whole word) and Missing Letter (word shown, fill the gaps) run at different word-length ceilings on the same level — Missing Letter is strictly easier per word, so it reaches further ahead.

| Level | Full Spelling | Hints (Full Spelling) | Missing Letter | Blanks | Hints (Missing Letter) |
|---|---|---|---|---|---|
| 1 | up to 3 letters | 3 | up to 5 letters | 1 | none |
| 2 | up to 5 letters | 3 | up to 7 letters | 2–3 | none |
| 3 | up to 7 letters | 2 | up to 9 letters | 2–4 | none |
| 4 | up to 9 letters | 2 | up to 10 (max) | 3–4 | none |
| 5 | up to 10 (max) | 1 | up to 10 (max) | 3–5 | none |

Missing Letter never gets hints — most of the word is already visible, so a hint would trivialize the one thing being tested. Blank *count* is a range so two 9-letter words in the same round don't always feel identical.

**Blank placement is chunk-aware, not random.** Blanks are chosen so they never split a digraph, blend, or vowel team — the word is chunked first (sh / ch / th / wh / ck, common blends, vowel teams all count as one unit), then whole chunks are blanked. A raw random-letter approach can produce a blank that erases half a sound and leaves a meaningless fragment.

- ✓ Chunk-aware: `S [HU] [_] T T E R` (blanks the "sh" digraph as one unit)
- ✗ Raw random: `S [_] H T T E R` (splits the digraph in half)

---

## Reading

The 4th track, with its own frontier and its own ladder. It exists to fix a genuine flaw in the old Match mode: as pairs clear, the last couple of matches become guessable by elimination instead of actually reading the word. Fixed-choice formats don't have that problem.

| Mode | Description | Why |
|---|---|---|
| **Read & Choose** | One picture, five word options, pick the match. | Fixed difficulty — always 5 choices, no shrinking pool |
| **Reverse Read & Choose** | One written word, five pictures, pick the match. | Confirms real reading, not shape-matching |
| **Rhyme Match** *(future)* | Given a word, pick which of three others rhymes. | Deferred — most Pokémon names are invented and won't reliably rhyme; would need to draw from the Phase A real-word list instead. |
| **Clue Words** *(future)* | A few descriptor words shown at once — BIG, RED, METAL — pick the matching item from several pictures. | Deferred — needs attribute data (color, size, material) per Pokémon/item that doesn't exist yet. |

### Reading Ladder — two difficulty levers, not one

Ramps on two independent axes: word length (reuses the same Pokémon/item pool as Spelling) and distractor difficulty — whether the 4 wrong options are obviously different or deliberately close (same starting letter, similar length).

| Level | Mode | Word length | Distractors |
|---|---|---|---|
| 1 | Read & Choose | 3–6 letters | Easy — obviously different |
| 2 | Reverse Read & Choose | 3–6 letters | Easy — obviously different |
| 3 | Read & Choose | 3–6 letters | Tricky — same first letter or length |
| 4 | Reverse Read & Choose | 3–6 letters | Tricky — same first letter or length |
| 5 | Read & Choose + Reverse, mixed | 7–10 letters | Easy — obviously different |
| 6 | Read & Choose + Reverse, mixed | 7–10 letters | Tricky — same first letter or length |

*(Build note: the old Match mode was ultimately removed entirely rather than kept as untimed free play — it wasn't being used, and this Reading Ladder is its real replacement. See `progress.md` Phase 10.)*

---

## Dashboard

One status page per kid — where each trail's frontier sits right now, how close it is to promoting, and the trend behind that number. Each card shows:

- Track name and current level label
- Days at the current level
- Last-10 and Last-20 progress bars with exact fractions
- A rolling-accuracy trend chart plotting Last-10 and Last-20 % over recent attempts, with dashed threshold lines at the 80% (Last-20 gate) and 100% (Last-10 gate) promotion thresholds
- A ★ marker wherever a 10/10 instant promotion happened, and a dashed "Leveled up" line wherever the slower 16/20 path fired instead

---

**Original status footer (superseded):** *"Status: Math is live, the rest is still this document."* — kept here for historical accuracy; see the status note at the top of this file and `progress.md` for what's actually built now.
