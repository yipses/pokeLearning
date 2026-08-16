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

Rows may be in any order; the app sorts by `id` where order matters. Adding a
row makes that Pokémon appear — as long as `pokemon/<id>.png` exists.

## pronunciations.csv — 251 rows

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
