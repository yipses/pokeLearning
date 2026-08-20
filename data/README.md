# Data files

These CSVs are the source of truth for the app's Pokémon data. `index.html`
fetches them at startup, so editing a CSV changes the app — no code change and
no build step. They are plain comma-separated UTF-8 with a header row, designed
to be opened, sorted and edited in Google Sheets or Excel and exported straight
back.

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

The Pokopia item catalogue, used by Spelling's Phonics Ladder and by Reading.

| Column | Notes |
|---|---|
| `name` | Sentence case (first word capitalised, the rest lowercase — `Sea glass fragments`), may contain spaces. Render keeps that casing as given; only the all-lowercase Pokémon names get per-word capitals |
| `image` | Bare filename with no folder or extension: `honey` → `items/honey.png` |
| `category` | One of 12 groupings (Materials, Food, Blocks, …) |

The `items/` folder and `.png` extension are added by the loader, so the column
stays short and the convention lives in exactly one place. An `image` value with
no matching file gives a broken image in-game, not an error — check the file
exists when adding a row.

Some names are referenced by the phonics word lists in `index.html`; renaming
one there without updating both will silently drop it from Spelling.

## pronunciations.csv — 184 rows

Respellings handed to the speech synthesiser instead of the real name, because
it reads invented names as though they were English words.

| Column | Notes |
|---|---|
| `name` | Must match a `name` in `pokemon.csv`, or the row silently never fires |
| `say_as` | Lowercase, syllables separated by spaces |
| `source` | `checked` = verified against a published guide. `unverified` = derived from the name's etymology, unconfirmed |



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

Shared columns: `word_level` (single-word items at or below this level), `compound_level` (multi-word items at or below this; `0` = none), `pokemon_letters` (name length cap, still generation-gated), `promote_5_pct` and `promote_10_pct` (the two promotion gates, per level).

Spelling adds `hinted_pct` — the share of the word shown, where `0` means the empty-tile task — and `max_hints`.

Reading adds `wrong_answers` (decoy count) and `distractor_level`, which names **another reading level** whose pool supplies the wrong answers. Keep it at or above the row's own level, or decoys end up easier than the target.

Traps: rows are read in file order but `level` is what the app reports, so keep them consistent. A `distractor_level` pointing at a level that doesn't exist falls back to the row itself. Regenerating `word_levels.csv` does not rewrite these — they are hand-authored from the design spreadsheet.
Keep `say_as` lowercase: some speech engines read an all-caps syllable as an
initialism and spell it out letter by letter. Spaces are the only stress control
available — the Web Speech API has no usable SSML in most browsers.

Only names the synthesiser actually gets wrong belong here. A respelling that
matches what it already produces does nothing, and one that differs can make a
correct name worse, so ordinary English-readable names are deliberately absent.

Use `tools/pronounce.html` to try a respelling by ear before committing it.

## Caveat

Because the app fetches these, `index.html` must be **served over http(s)**, not
opened as a file — browsers block `fetch` on `file://` as cross-origin. GitHub
Pages serves it fine; double-clicking the file will show a load error instead.

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
| `visual` | `yes` if this rung can be drawn as pictures. Set it honestly: it is trusted, and 19 + 9 means 28 icons on screen |
| `num1_min`, `num1_max` | first operand. On a **pattern** row this is the fixed anchor; on a **division** row it is the dividend |
| `num2_min`, `num2_max` | second operand. On a division row, the divisor |
| `num3_min`, `num3_max` | reserved for three-operand questions. Null everywhere, and nothing reads them |
| `pattern` | pattern rows only: the steps to choose from, comma-separated |

`math_promotion.csv` — `questions,percent`, any one of which promotes. Applies to every maths track. Spelling and Reading keep their own per-level percentages instead.

**Traps.**

- **A subtraction pattern needs room to descend.** Four rows of `step` means the anchor must be at least `step × 4`, or the set goes below zero. Where only part of `num1_min`–`num1_max` qualifies the anchor is drawn from that part; where none does, that step is silently skipped — a level can lose a step without any error. Every `pattern_sub` row currently has at least one usable anchor per step, but two rows only just: level 2 step 3 loses 2 anchors of 10, level 3 step 5 loses 1 of 11. Widen `num1_min`–`num1_max` before raising a `step`, not after.
- **Division is always exact.** The quotient is chosen first, from those whose dividend lands inside `num1`, so a row can be written that has no valid question at all — check that some multiple of the divisor falls in the dividend range.
- **A prerequisite can point past its track's last level**, which locks the dependent forever. Nothing validates this; `tools/` has no checker for it yet.
