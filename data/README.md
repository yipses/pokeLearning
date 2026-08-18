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
| `name` | Lowercase, no spaces. Used for spelling, reading and display (capitalised at render time) |
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
| `name` | Capitalised, may contain spaces. Only single plain-letter words are usable for spelling |
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
