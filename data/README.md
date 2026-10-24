# Data files

These CSVs are the source of truth for the app's Pokémon data. `index.html`
fetches them at startup, so editing a CSV changes the app — no code change and
no build step.

**The ladders come from the design sheet** — spelling, reading, alphabet,
sentences and all eight maths tracks, including which track unlocks which — and
so do the Sentences trail's facts and word list (tabs *Sentence Level*,
*Pokémon Facts*, *Sentence Words*):

<https://docs.google.com/spreadsheets/d/1MtlBnXPMFt3x_LpcMmWe7LIeISjoC9wJddhTM8_zbVY/edit>

Edit there and export, rather than hand-editing the ladder CSVs, or the two
copies drift. The other files here (roster, items, pronunciations, phonemes)
have no upstream and are edited directly. They are plain comma-separated UTF-8 with a header row, designed
to be opened, sorted and edited in Google Sheets or Excel and exported straight
back.

**Keep the line endings a file already has.** Some of these came out of a
spreadsheet as CRLF (`item_levels`, `pokemon`, `pronunciations`, `word_levels`)
and the rest are LF. Rewriting one with a script that changes them turns a
nine-cell edit into a whole-file diff, which buries the actual change in review.
Python's `csv.writer` defaults to CRLF — pass `lineterminator="\n"`, or check
`git diff --stat` before committing.

## pokemon.csv — 1,021 rows

| Column | Notes |
|---|---|
| `id` | National Dex number. Also picks the artwork: id `25` → `pokemon/25.png` |
| `name` | Lowercase. Used for spelling, reading and display (capitalised at render time — an all-lowercase name gets a capital on **every** word, so `iron hands` renders as "Iron Hands"). **The separator is load-bearing:** a space means two real words (`iron hands`, `tapu koko`) and unlocks the Spelling trail's higher multi-word length ceiling; a hyphen means one word that happens to contain one (`ho-oh`, `kommo-o`, `porygon-z`) and follows the ordinary ceilings. These arrived from PokéAPI as hyphenated slugs and were separated by hand — don't "normalise" them back |
| `type1` | Required. Drives Battle type effectiveness and the Pokédex badges |
| `type2` | Blank for single-type species — leave the cell empty, don't write "none" |
| `base_stat_total` | Integer. Weights the Battle winner roll |
| `evolves_from` | Name of the species this evolves **from**, or blank. Must match a `name` in this file — the four rows whose real parent is an excluded species (Nidorina, Nidorino, Sirfetch'd, Mr. Rime) are deliberately blank, since a link that can't be followed is worse than none. The reverse direction is derived at load time, so branching families need no extra data |
| `rarity` | `legendary`, `mythical`, or blank. Drives the ✨ marker in the Pokédex and the catch banner. Sourced from PokéAPI's `pokemon_species.csv` (`is_legendary` / `is_mythical`), joined on name with all 1,021 matching and no id mismatches |

Rows may be in any order; the app sorts by `id` where order matters. Adding a
row makes that Pokémon appear — as long as `pokemon/<id>.png` exists.

## items.csv — 922 rows

The Pokopia item catalogue, used by the Spelling and Reading trails.

| Column | Notes |
|---|---|
| `name` | Sentence case (first word capitalised, the rest lowercase — `Sea glass fragments`), may contain spaces. Render keeps that casing as given; only the all-lowercase Pokémon names get per-word capitals |
| `image` | Bare filename with no folder or extension: `honey` → `items/honey.png` |
| `category` | One of 12 groupings (Materials, Food, Blocks, …) |

The `items/` folder and `.png` extension are added by the loader, so the column
stays short and the convention lives in exactly one place. An `image` value with
no matching file gives a broken image in-game, not an error — check the file
exists when adding a row.

Renaming an item silently drops it from both trails unless `word_levels.csv`
and `item_levels.csv` are regenerated with it — the grading is keyed on the
name. `index.html` holds no copy of any word list, so it never needs touching.

## pronunciations.csv — 184 rows

Respellings handed to the speech synthesiser instead of the real name, because
it reads invented names as though they were English words.

| Column | Notes |
|---|---|
| `name` | Must match a `name` in `pokemon.csv`, or the row silently never fires |
| `say_as` | Lowercase, syllables separated by spaces |
| `source` | `checked` = verified against a published guide. `unverified` = derived from the name's etymology, unconfirmed |

Keep `say_as` lowercase: some speech engines read an all-caps syllable as an
initialism and spell it out letter by letter. Spaces are the only stress control
available — the Web Speech API has no usable SSML in most browsers.

Only names the synthesiser actually gets wrong belong here. A respelling that
matches what it already produces does nothing, and one that differs can make a
correct name worse, so ordinary English-readable names are deliberately absent.

Use `tools/pronounce.html` to try a respelling by ear before committing it.

---

## `word_levels.csv` — the vocabulary grading

Every distinct word in the item catalogue, split on spaces and hyphens, graded 1–9 against the nine phonics patterns. **This is the file to correct**: an item's level is derived from it, so changing `sea` from 6 to 5 re-grades every item containing it.

| Column | Notes |
|---|---|
| `word` | lowercase, one row per distinct word |
| `level` | 1–9. The only column the app reads |
| `pattern` | the level's name, for humans |
| `letters`, `syllables` | reference only |
| `compound_parts` | the split found for a closed compound (`bath + tub`), blank otherwise |
| `also_matches` | every pattern the word hit, so a grading can be second-guessed |
| `proper_noun` | `yes` if the word is a Pokémon name (`hoppip`, `pikachu`). Its phonics level is fiction — an invented name is memorised, not decoded — so Spelling skips any item containing one. Set automatically by cross-referencing `pokemon.csv` |
| `used_in_items` | how many item names use it — a correction here moves that many items |
| `previous_level`, `review` | what the original hand-graded list said, and `differs` where the two disagree |

## `item_levels.csv` — the per-item view

Derived from `word_levels.csv`; regenerate rather than edit. A single-word item takes its own word level; a multi-word item takes its **hardest component's**. Items with a blank `level` can't be spelt at all (apostrophes, accents, digits) and are dropped from both trails, as are those flagged `shared_art`.

| Column | Notes |
|---|---|
| `item` | the catalogue name, exactly as in `items.csv` |
| `level` | 1–9, or blank for unspellable |
| `kind` | `single` or `compound` — a space or hyphen makes it compound |
| `components`, `component_levels` | the parts and their levels, for checking the roll-up |
| `proper_noun` | `yes` if any component is a Pokémon name. Excluded from Spelling, kept in Reading |
| `shared_art` | `yes` if this item's picture is byte-identical to another item's. **Excluded from both trails** — one generic building icon serves ten place names, so `Boutique` and `Snowbelle City` are the same image and neither can be asked for. Set automatically by hashing every file in `items/`; 97 items, 90 of them otherwise usable |
| `longest_word` | reference only |

## `spelling_levels.csv` and `reading_levels.csv` — the ladders

The Spelling (25) and Reading (10) trails, one row per level. **These are the ladders** — `index.html` holds no copy, so editing a row changes the game.

Shared columns: `word_level` (single-word items at or below this level), `compound_level` (multi-word items at or below this; `0` = none), `name_letters` (**the longest name the level may serve, items and Pokémon alike** — Pokémon stay generation-gated on top of it), `promote_5_pct` and `promote_10_pct` (the two promotion gates, per level).

Spelling adds `hinted_letters` — **a count of letters shown, not a share**.

**Why `name_letters` covers items too.** It used to cap only Pokémon, and items were admitted on phonics alone. That let `Pink hut kit` — three level-1 CVC words — into spelling level 5, because **a compound is graded by its hardest component word and never by how many of them there are**. Ten letters and nine blanks, in a pool whose median item was five. `word_level` answers *has he been taught this pattern*; nothing in it can answer *how much is there to hold in your head*. The two are independent axes, and level 5 of the phonics ladder is typically **shorter** than level 4, so one cannot stand in for the other.

Watch the interaction with `compound_level`: the shortest multi-word item is `Log bed` at six letters, so a row with `compound_level` above 0 and `name_letters` below 6 switches compounds on and gets none. The load check does not catch that — it is legal data, just inert.

`hinted_letters` is the one difficulty column in these files that is an absolute number rather than something scaled to the item. Two letters is two letters, so the same value is much harsher on a twelve-letter name than a four-letter one; that is the point, and it is why the counts rise again at the top of the ladder where the words get long. A count larger than the word is safe — at least one blank always remains — and `0` means the empty-tile Full Spelling task, which no level currently asks for.

Reading adds `wrong_answers` (decoy count) and `distractor_level`, which names **another reading level** whose pool supplies the wrong answers. Keep it at or above the row's own level, or decoys end up easier than the target.

### `data/alphabet_levels.csv`

The **Alphabet** trail — eleven levels, its own ladder. It shares none of the word pools above: a run of consecutive letters is shown as Pokémon whose names start with them, some of them blank, and the child picks the Pokémon for the missing letter.

It was carved out of `reading_levels.csv`, where it could not stay: the two ladders are different lengths — eleven against Reading's ten — so neither can index the other, and its own `promote_5_pct` / `promote_10_pct` would never have been read.

| column | meaning |
| --- | --- |
| `alpha_length` | how many consecutive letters are on screen. **Shorter is harder** — fewer letters to count along — so this column runs the opposite way to every other difficulty column in these files |
| `alpha_blanks` | how many of those are gaps. Must be fewer than `alpha_length` |
| `alpha_blank_position` | `first`, `last`, `middle`, `random` or `mixed`. `first`/`last` are the solid block at that end; `middle` is every gap strictly inside the run; **`random` is every shape with nothing filtered out** — gaps may split (`_x_x_`), sit at an end, or fall anywhere, each equally likely, and it is the only setting producing non-contiguous gaps; `mixed` is any shape that is neither end block, i.e. `random` minus the two end blocks, and is the only setting that fits three gaps into a run of four without them forming a solid end |
| `promote_5_pct`, `promote_10_pct` | the two promotion gates, as everywhere else |

Every row is checked at load, and one that cannot produce a question **stops the app with a message naming the level** rather than failing quietly: no row may have `alpha_blanks` at or above `alpha_length`, and `middle` needs a run of 5 before it can hold 3 blanks — in a run of 4 there are only two interior slots, so a third blank would have to touch an end, at which point it is `first` or `last`.

The option count (4) and the rule the wrong answers follow — every option at least four letters from every other, the answer included — are **not** in this file; they live in `index.html`.

Traps for `reading_levels.csv`: rows are read in file order but `level` is what the app reports, so keep them consistent. A `distractor_level` pointing at a level that doesn't exist falls back to the row itself. Regenerating `word_levels.csv` does not rewrite these — they are hand-authored from the design spreadsheet.

## The Sentences trail — `sentence_levels.csv`, `pokemon_facts.csv`, `sentence_words.csv`

A Pokémon's picture and a sentence about it with words missing, filled from a bank of word tiles. The three files are the sheet's *Sentence Level*, *Pokémon Facts* and *Sentence Words* tabs.

### `sentence_levels.csv` — 9 rows

| column | meaning |
| --- | --- |
| `level` | 1-based |
| `blanks` | how many words are blank — `1`–`4` or `all`. **Must match `frame`** (it documents it; the frame decides); a mismatch stops the app naming the level |
| `frame` | which words are blank. Two Pokémon: `and_are` *Pikachu and Psyduck ___ yellow* · `compare` *Onix is ___ than Pikachu* · `grows_into` *Charmander grows into ___*. One Pokémon: `last1` *Pikachu is ___* · `last2` *Pikachu ___ ___* · `not1` *Pikachu is not ___*, and only "not" sentences · `given` two blanks around a given word, *Onix ___ very ___*, *Onix ___ a ___ type* · `last3` the last three words · `type_given` *Onix ___ ___ rock ___* · `last4` *Onix ___ ___ ___ ___* · `verb_given` *___ can ___*, the name a tile · `all` every word, the name included |
| `stretch` | how far past the child's **Reading** word level the words may go. Every word in the sentence and the bank, the name aside, must be at or under Reading's `word_level` + this |
| `spare_tiles` | wrong tiles in the bank, 0–8. When a sentence can't find that many it settles for one, rather than not being asked |
| `spoken_tiles` | `yes` / `no`. On `yes` every word tile carries its own speaker for its own word; on `no` the tiles have none. The picture's speaker always says only the name. Tapping a tile never speaks it |
| `promote_5_pct`, `promote_10_pct` | the two promotion gates, as everywhere else |

### `pokemon_facts.csv` — 147 rows

One row per original-151 Pokémon the roster has (no Nidoran♀/♂, Farfetch'd or Mr. Mime). **These decide what is right**, so they are worth getting right.

| column | meaning |
| --- | --- |
| `id`, `name` | `id` must be in `pokemon.csv` (a row that isn't is skipped with a console warning); `name` is for reading the sheet — the app takes the name from `pokemon.csv` |
| `colours` | main body colours, `\|`-separated. Colour sentences are built around these, and in a *not* sentence they are the trap. Never empty |
| `also` | other colours that count as **right if picked** — judgement calls (Bulbasaur blue) and markings (Pikachu's red cheeks). Never offered as a wrong tile, and never used in a *not* sentence. Adding a colour here can only make the trail friendlier |
| `size` | `very small`, `small`, `big`, `very big`, or blank. Blank means no size sentence at all — use it for the borderline ones. `very small` also accepts *small*, `very big` also accepts *big* |
| `can` | `fly`, `swim`, `run`, `jump`, `dig` it **certainly** does. `fly` also unlocks *can fly high* |
| `cannot` | actions it clearly can't — these are the only wrong action tiles. Something debatable goes in **neither** list, so it is never asked and never marked wrong |

The type comes from `pokemon.csv`'s `type1`/`type2`; either counts.

**Colours** must be one of `red pink black white blue green yellow brown gray orange purple` (note `gray`). **Eyes never count** — leave them out of both colour columns. A word in both `can` and `cannot` stops the app.

### `sentence_words.csv` — 30 rows

Reading levels (1–9, the same scale as `word_levels.csv`) for the words Sentences and Riddles use that the phonics list doesn't grade: `is am are a an not very can high type`, `run dig swim fly`, `purple`, the type words, `i yes no` (Riddles), and `than bigger smaller grows into` (two-Pokémon sentences). **`word_levels.csv` wins** where both have a word — the duplicate is skipped with a console warning, never an error, because regenerating `word_levels.csv` can add a word at any time. A word in neither file has no level and **never appears**; the console names it. `note` is for humans.

Traps: `type` is graded 5, so the type levels (6–7) have nothing to ask below Reading 3 — the trail then serves the nearest level that has a question, and that question doesn't count toward promotion. Lowering `type` opens them earlier.

Trap: `and` is graded **9** in `word_levels.csv`, which wins, so the *and* level (10) waits for Reading 7. Correcting it there regrades every item containing "and".

## `riddle_levels.csv` — the Riddles trail, 8 rows

| column | meaning |
| --- | --- |
| `level` | 1-based |
| `mode` | `yesno`, `whoami` or `fixit` |
| `clues` | Who am I?: how many clues, 1–3 |
| `choices` | Who am I?: how many pictures (2–6). Fix it: how many tiles for the fix (2–5), though grammar fixes may offer fewer. Yes or No ignores it |
| `facts` | which facts questions and clues may use, `\|`-separated: `colour`, `size`, `can`, `type`, and `not` ("I am not blue", Who am I? only — when listed, one clue is always a "not") |
| `wrong` | Fix it: `fact`, `grammar` or `fact\|grammar` |
| `stretch` | words may go this far past the child's Reading word level, as in Sentences |
| `spoken_tiles` | `yes`: a speaker reads the question or clues aloud (Fix it: each fix tile gets a speaker). The picture's speaker always names only the Pokémon |
| `promote_5_pct`, `promote_10_pct` | the two promotion gates |

Every row is checked at load; a bad mode, fact, clue or choice count stops the app naming the level.

## `word_pair_levels.csv` — the Word Pairs trail, 5 rows

| column | meaning |
| --- | --- |
| `level` | 1-based |
| `pairs` | how many pairs on a board, 3–6 |
| `same_start` | `yes`: every word on the board starts with the same letter |
| `promote_5_pct`, `promote_10_pct` | the two promotion gates |

The words are the **Reading** level's pool, not a list of their own. Traps: a board can't have more pairs than Reading has words (Reading 1 has four), and a `same_start` board needs that many words sharing a first letter — below Reading 3 there are none, so the board quietly becomes an ordinary one.

## `math_pair_levels.csv` — the Maths Pairs trail, 5 rows

| column | meaning |
| --- | --- |
| `level` | 1-based |
| `pairs` | how many pairs on a board, 3–6 |
| `mix` | `one` (one maths track per board), `addsub` (the open + and − tracks mixed) or `all` (every open single-sum track mixed) |
| `promote_5_pct`, `promote_10_pct` | the two promotion gates |

The sums come from each maths track **at the level reached**; pattern tracks are never used. Every answer on a board is different, so a level with few possible answers (Subtract 1 has three, Divide 1 two) shrinks the board and then borrows from the other open tracks. Every row is checked at load: `pairs` outside 3–6 or an unknown `mix` stops the app naming the level.

## `phonemes.csv` — what each chunk says out loud

Spoken when a child places a letter or chunk correctly. Keyed on `chunk` **and** `context`, because a letter's sound depends on the word it's in.

| Column | Notes |
|---|---|
| `chunk` | the letter or chunk, lowercase — matches what `chunkWord()` produces |
| `context` | which sound of that chunk this row is. `any` covers everything the chunker has already made into a single unit — digraphs, blends, vowel teams, r-controlled vowels — and most consonants. The rest are chosen from the word around the chunk: lone vowels take `short`, `long` or `silent`; `c` takes `any` (hard) or `soft`; `y` takes `any` (consonant), `ending`, `long` or `short`; `ow` takes `any` or `end` |
| `say_as` | a respelling, not a phoneme — a speech synthesiser handed `b` says "bee", so it gets `buh`. **Blank means silent**, which is how the final `e` is taught |
| `notes` | free text, ignored by the app |

Traps: **every `say_as` must be a pronounceable syllable.** A synthesiser handed `ch` says "see-aitch" and handed `lll` says "ell ell ell" — a respelling needs a vowel in it, so /ch/ is written `chuh` and /l/ is `luh`. Check any edit with `tools/phonemes.html`, which plays each row aloud. A context the code never asks for is dead weight, and one it asks for with no row is **silent** — so the context names above are fixed by `chunkSound()` in `index.html` and cannot be invented here. A chunk with no row is silent, deliberately — a wrong sound teaches a wrong thing, silence teaches nothing, so leave a row out rather than guess. And they have still not all been checked by ear — `ee` is the one a rough test can't settle.

## `math_tracks.csv`, `math_levels.csv`, `math_promotion.csv` — the maths ladder

**These are the maths ladder.** `index.html` holds no copy; editing a row changes the game.

`math_tracks.csv` — one row per track. `prereq_track` and `prereq_level` decide when it opens; leave both blank for a track that is open from the start. `group` is `addsub` or `muldiv` and only decides which of the two home tiles it counts toward. `kind` is `single` or `pattern`.

`math_levels.csv` — one row per level of per track.

| Column | Notes |
|---|---|
| `track` | must match a `track` in `math_tracks.csv` |
| `level` | 1-based, and the number a prerequisite refers to |
| `visual` | `yes` if this rung can be drawn as pictures. Set it honestly: it is trusted, and the count is the operands, not the answer — `div` level 5 puts 25 icons on screen for `25 ÷ 5`, which is the tallest the sheet currently asks for. On a **pattern** row it draws each of the three rows as Pokémon with the step highlighted (add and multiply patterns only; subtract and divide ignore it) — `pattern_add` 1–4 and `pattern_mul` 1–3 are set |
| `num1_min`, `num1_max` | first operand. On a **pattern** row this is the fixed anchor; on a **division** row it is the dividend |
| `num2_min`, `num2_max` | second operand. On a division row, the divisor |
| `num3_min`, `num3_max` | reserved for three-operand questions. Null everywhere, and nothing reads them |
| `pattern` | pattern rows only: the steps to choose from, comma-separated |

`math_promotion.csv` — `questions,percent`, any one of which promotes. Applies to every maths track. Spelling and Reading keep their own per-level percentages instead.

**Traps.**

- **A subtraction pattern needs room to descend.** Four rows of `step` means the anchor must be at least `step × 4`, or the set goes below zero. Where only part of `num1_min`–`num1_max` qualifies the anchor is drawn from that part; where none does, that step is silently skipped — a level can lose a step without any error. Every `pattern_sub` row currently has at least one usable anchor per step, but two rows only just: level 2 step 3 loses 2 anchors of 10, level 3 step 5 loses 1 of 11. Widen `num1_min`–`num1_max` before raising a `step`, not after.
- **Division is always exact.** The quotient is chosen first, from those whose dividend lands inside `num1`, so a row can be written that has no valid question at all — check that some multiple of the divisor falls in the dividend range.
- **A prerequisite can point past its track's last level**, which locks the dependent forever. Nothing validates this; `tools/` has no checker for it yet.

## Caveat

Because the app fetches these, `index.html` must be **served over http(s)**, not
opened as a file — browsers block `fetch` on `file://` as cross-origin. GitHub
Pages serves it fine; double-clicking the file will show a load error instead.
