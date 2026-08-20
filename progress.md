# Progress Log — Poké Learning

How the project got from a basic spelling/math quiz to where it is now, and the decisions worth not re-litigating. `Overview.md` is the spec for what it does *today*; this file is the journey and the open threads.

---

## Where things stand

Everything speced is built and published on GitHub Pages: four Lesson Trails promoting, My progress, the Pokédex with detail, tabs and legendary call-outs, Battle, and every piece of content and both word ladders in editable CSVs.

The Spelling and Reading trails share one graded vocabulary — all **807 distinct item words** and **819 item names** — climbed by **25 spelling levels** and **10 reading levels**, all four tables authored in a spreadsheet and read at boot. No word ladder, word list or promotion gate remains in code.

## Open threads

Roughly by how much they'd bite.

### 1. The maths ladder is the last thing still hardcoded

Both tracks' levels live in `ADDSUB_LEVELS` / `MULDIV_LEVELS` in `index.html`, and promotion falls back to the Spelling/Reading CSV figures because Maths has no table of its own. Moving it to a CSV with a min and a max per level is the next piece of work.

**A min/max is necessary and not sufficient**, which is the thing to carry into that work. Measured with each frontier parked at the top of its track:

| track at top level | trivial questions |
|---|---|
| Add/Subtract, "Within 100, with regrouping" | 4.1% |
| Multiply/Divide, "Full range (÷)" | **29.5%** |

The two tracks fail for different reasons:

- **Multiply/Divide is identities, not range.** 90% of top-level questions come from the frontier itself, not the review band, and that level yields `n ÷ 1` or `n ÷ n` **28%** of the time. Level 11 is 27.6% `something × 1`. Level 7 is *labelled* "Harder tables only" and is still 20.4% `1 × 6`, because `mkMul(1,5,6,10)` floors the hard operand at 6 and leaves the other free to be 1. Identities sit *inside* any sane range.
- **Add/Subtract is mostly the review band.** Levels 4a–5b do draw both operands from `randInt(0, ceiling)`, but two draws from 0–100 are rarely both small — "both operands ≤ 2" measures 0% there. The `1 + 1` seen at high difficulty is review deliberately serving 20% of questions from earlier levels, which a range cannot reach.

This matters more since answers became six visible choices: a trivial question with the answer on screen is easier still than one you had to type.

`makeMath(op,min,max)` has no callers and is the obvious thing to mistake for the live path.

### 2. The phoneme respellings still have not been heard

A first pass written on paper turned out to be 30% unspeakable; the rewrite measures at 1%, but *measured* only against a rough test for whether a string can be said at all — not whether it says the **right** sound. `tools/phonemes.html` plays every row and takes about five minutes. `ee` is the one to listen to first.

### 3. Smaller, and each self-contained

- **46 unverified pronunciations**, all Gen 8–9, each with a stated reason for existing. They surface as the collection reaches them; `tools/pronounce.html` filters to exactly this set.
- **`fonts/OFL.txt` is missing.** The Open Font Licence requires its text to travel with the font files; `fonts/README.md` says where to get it. A licence obligation, not a runtime one.
- **Settings overflows horizontally at 360px wide** — about 115px, from the level `<select>` elements taking their width from the longest option text ("Within 100, with regrouping"). A `max-width` and text-overflow would settle it.
- **The word grading is a first pass.** `tools/classify_words.py` reproduces 91 of the 100 originally hand-graded words; the rest are flagged `differs`. Several words match three patterns at once. `word_levels.csv` is the file to correct — item levels follow from it.
- **~820 un-eyeballed Pokopia items**, for name/image mismatches. Shared artwork is caught automatically now, but an item whose picture is *unique and still wrong* is not.
- **The answer's position leans early on the division levels** — 30% first of six, 2.6% last, because those answers run 1–10 and there are not five whole numbers below 2. Flat everywhere else. Flattening it means offering negatives, which is not a mistake a five-year-old makes.
- **`APP_BUILD` is bumped by hand.** No build step stamps it. The `This file` timestamp beside it is automatic and cannot go stale.

Parked, not scheduled: a service worker for genuine offline install; moving the type chart to CSV if it ever needs editing; recorded phoneme audio instead of synthesised respellings; and two deferred Reading modes — **Rhyme Match**, which needs a real-word list and now has one in `word_levels.csv`, and **Clue Words**, which needs per-item colour/size/material data that does not exist.

---

## Lessons this codebase keeps teaching

Each of these cost real time at least once.

**One file, one namespace — grep before you name.** Three collisions so far, every one silent. A `.tiles` rule reflowed the spelling letter bank into three columns. A second `placeChunk` meant every tap in one mode reached the other mode's function and returned with no sound, no error and nothing on screen. `.count-badge` was nearly deleted as dead when it was still the Battle screen's win/loss record. `grep -o "^function [a-zA-Z0-9_]*" index.html | sort | uniq -d` catches the second kind in a second, and it has since caught a splice that duplicated 160 lines.

**Measure before designing, and measure the thing that actually matters.** The pity timer was fixed by simulation rather than reasoning. Six answer choices only worked once the answer *space* per level was counted — four division levels have fewer than six possible answers. And sorting those choices was verified by measuring where the answer *landed*, which turned up an exploit the change itself would never have shown: sorted alone, the answer sat 3rd or 4th in 75% of questions.

**Structural assertions are not enough — look at it.** Several bugs passed every DOM assertion while being visibly broken. The reverse happens too: reported misaligned HUD icons measured *correct* on every number available, and the real cause — different ink inside identical boxes — was obvious the moment the row was rendered at 4×.

**Prefer the rule with no floor to the rule that runs out.** Distractors drawn from "other answers at this level" cannot work where a level has four of them; distractors drawn from *the mistakes the operation invites* always can. Same shape of reasoning as excluding items by shared artwork rather than by eyeballing 922 of them.

**Fix on the way in, not at each caller.** The home levels panel showed a stale level after a Settings change; the same hole existed for quitting a round after a promotion. Rebuilding on entry to the screen fixed both and any third.

**A wrong sound teaches a wrong thing; silence teaches nothing.** Anything with no row in `data/phonemes.csv` stays silent rather than guessing. The same instinct killed the "You earned Mewtwo!" reward that granted nothing.

**Never write a long sentence.** One to four words per line. A five-year-old cannot read "Play a round to catch it!" — the mystery shape is the invitation.

---

## How it got here

### Phases 1–22 — the road here

Condensed. Where a later phase replaced one of these outright — the Phase A/B spelling ladder, the old promotion gates, the first pity timer — only the lesson is kept, not the mechanism.

**Building out (1–8).** Two challenge types over 40 Pokémon grew into the full National Dex: **1,021 species**, Gen 1–9, minus the four whose names don't fit a plain-letter mechanic (Nidoran♀/♂, Farfetch'd, Mr. Mime). Data from PokéAPI, verified by hashing an existing file against a fresh download before trusting a bulk fetch. Added Math Patterns, Visual Math, Battle (a stat- and type-weighted roll off real base stats, not a coin flip), the Play Streak, grass encounters and the Pokédex. **Catching is generation-gated** — only the lowest incomplete generation appears, so the collection moves through the Dex in order, and the Pokémon side of both word pools respects the same gate. Item catalogue pulled to **922** after dropping 121 near-duplicate variants. All artwork cached locally; nothing is fetched from a fan site at runtime.

**Lesson Trails (9–12).** Ad-hoc difficulty settings became four independent progressive tracks on one engine. The durable decisions: a **daily blend rather than one difficulty at a time** — Review 20% / Current 60% / Stretch 20% around each frontier, because interleaved practice beats blocked practice for retention even though blocked feels easier; **promotion on clean answers only** (right first try, no hints) with **no demotion**, since a rough patch is absorbed by the Review band; and progressions validated against Common Core K–3 and Wilson Fundations / Words Their Way rather than invented. **Match Challenge was removed** rather than kept — it was guessable by elimination as pairs cleared. A "stuck on level 1" report turned out not to be a bug: a session splits across four tracks and only 60% of a track's questions are frontier-eligible, so promotion is slow by design.

**The read-aloud rule (13).** Code and docs had disagreed; settled as **pictures may be named aloud, words never are**. Read & Choose prompts with a picture, so a speaker names it for a child who can't identify the artwork; Reverse Read & Choose prompts with the written word and gets no speaker at all, because speaking the prompt hands over the answer. A picture speaker does **not** break a clean answer — identifying artwork isn't the skill being tested, so it's accessibility, not a hint. Docs were split by role in the same pass, after `Overview.md` had grown its own progress log and gone stale.

**Pokédex detail (14, 18, 19, 21).** Entries are tappable, reusing the catch modal rather than duplicating it; new catches carry a **NEW** badge until opened. `rarity` from PokéAPI marks **71 legendary and 23 mythical**, and the marker shows on **uncaught** slots too — it reveals nothing about which Pokémon lives there, and flagging the slot is the point. An `evolves_from` column (479 links) drives the family strip: National Dex order already puts 83% of families side by side, but Pichu is #172 while Pikachu is #25, and Eevee's spans #133 to #700. Four rows are deliberately blank, because their real parent is one of the four excluded species and a link that can't be followed is worse than none. A broken tile on the live site never reproduced locally, but the mechanism was clear: **1,021 image requests at once**, throttled by a real network, and an `<img>` never retries. Lazy loading cut it to 39 on open, with one retry each — a fix for the probable cause, not a confirmed diagnosis.

**Build identity (15).** Settings shows `Build`, `Published`, and `This file` (`document.lastModified`). The last is the one that catches a stale cache — a cached page reports the *old* file's date — and it needs no maintenance. Added after a merged fix appeared broken because the deploy finished ~80s after the merge.

**Pronunciations (16).** `speechSynthesis` reads invented names as English and mangles many, and no usable source of spoken names exists — PokéAPI's "cries" are sound effects, and every wiki with a guide is blocked by this environment's egress proxy (web *search* reaches their content; `raw.githubusercontent.com` is fetchable). So respellings live in `data/pronunciations.csv`, speech-only, with a `source` column recording `checked` or `unverified`. `u.lang = "en-US"` is set explicitly, or the OS voice applies another language's phonetics. Values stay lowercase — some engines read an all-caps syllable as an initialism and spell it out. **The lesson, from a real ear-audit:** the failure mode was *over-syllabification* — "toe geh pee", "ar kuh nine" — chopping up names the engine already said correctly. The map peaked at 251 entries and was pruned to **184**. An override is a liability unless it earns its place, and **if a respelling sounds wrong, drop it rather than re-guess** — the plain spelling is a known state.

**Data out of the file (17).** `index.html` was 236KB, roughly half data literals. Moving it all to `data/*.csv` roughly halved the file and made the content editable in a spreadsheet. The trade-off: `fetch` is blocked on `file://`, so **the app must be served**, not double-clicked. A missing CSV shows a legible error rather than booting with silently empty pools.

**The hint allowance was off by one (20).** Reported as "the UI says 3 hints but you only get 2." The bail-out fired when you *spent* your last hint rather than when you *asked for one you didn't have*, so the final hint revealed a letter and the same click locked the board. A 1-hint level gave none at all. Fixed in the guard — and the word-swap escape hatch was **removed** rather than rebound: it existed to stop a stuck child stalling, but the tile rack holds exactly the word's letters and wrong ones are rejected, so any word can always be finished unaided.

**An honest results screen (22).** The score could never be anything but 100% — every mode retries until correct — so "Perfect! You're a Champion!" fired every round and three tiers were unreachable code. The perfect-run reward was worse: it announced "You earned Mewtwo!" and granted nothing, a broken promise every round. Replaced with the three status tiles and the Pokémon actually caught. The Play Streak card became those tiles in the same pass, taking ~90px where seven rows of "Not played yet" took ~420 and pushed Start Playing below the fold. **The streak holds until the day ends**, counting days ending today *or yesterday*, rather than resetting at midnight before the child has played.

### Phases 23–29 — CSV ladders, and four bugs found by looking

The Spelling and Reading trails moved wholesale into `data/*.csv`: word levels, item levels, both ladders, and the promotion gates. Nothing about difficulty remains in code. The old Phase A/B ladder had a broken seam — the phonics half ended on *Refrigerator* (12 letters) and the fluency half began on a 3-letter cap — and grading items by their **hardest component word** brought all 909 usable names into play instead of 100.

Four bugs in the same stretch, each reported from a screenshot: a `.tiles` class collision reflowed the letter bank; filled Missing Letter boxes rendered lowercase; **21 Pokémon names were graded as ordinary vocabulary** and had to be excluded from Spelling, since an invented name is memorised rather than decoded; and the pity timer overwrote the drop rate — 50% produced an encounter every single time. That last one is now calibrated so the setting *is* the measured outcome, pity included.

### Phases 30–36 — one way to answer, and sounds attached to it

Both spelling tasks answer the same way: tap a tile holding a **chunk**. `torch` is `T` `OR` `CH` in both. A correct placement says the sound of what was completed, and the whole word is blended back afterwards — the round now waits for the voice to finish rather than talking over it.

**A third of all spoken sounds were unpronounceable.** Respellings with no vowel (`ch`, `th`) or repeated letters (`lll`) get spelled out by a synthesiser: 2,799 of 9,302 events broken. Rewritten as syllables, measured at 1%.

Then four context rules — `c`, `y` (twice) and `ow` reading the word around them, 395 chunk instances changed — and a bug found while building them: context was measured against the whole *name*, not the word, so no vowel in a multi-word item was ever at an end and `Ice cream` came out "ih-kuh-eh".

**97 items share byte-identical artwork**, found by hashing all 922 files. One generic building icon serves ten place names, which is why one screen offered both `Boutique` and `Snowbelle City` for the same picture. Ninety leave both trails: a picture that names two things names neither.

Missing Letter's bank held exactly the missing chunks, so a one-blank word offered **one tile** — 9% of all such questions, 45% of level 2. It is padded with same-phonics-class decoys to a floor of four.

### Phases 37–41 — self-hosted type, spoken names, and the week

(Phase 37 was an investigation that deliberately changed no code; its findings are Open thread 1 above.)

The webfont was never loading in the dev sandbox, which meant **every screenshot taken over several days rendered in a fallback face**. Self-hosting was the better answer anyway for an app aimed at a child on a tablet: latin subset, four weights, 87 KB, and the page now makes no external requests at all.

Opening any Pokémon entry says its name aloud — one rule covering the catch popup, a Pokédex tap, an evolution tap and the results screen, hung off *opening* rather than *rendering* so walking back is silent. The timing was traced with a stubbed 900ms voice: the blend-back ends at 3464ms and the name starts at 4267ms.

**My progress** leads with rounds per day over the last 7 days. No new storage was needed — the streak record has always kept `{date: rounds}` uncapped, so the chart was correct from the day it shipped.

### Phase 49 — The Pokédex family showed two of three

The evolution strip walked one hop back and one hop forward, which is the whole family only if you happen to be standing in the middle of a three-stage line. From Bulbasaur it showed Bulbasaur and Ivysaur and stopped; from Venusaur, Ivysaur and Venusaur. **269 of the 1,021 species saw a family missing at least one member** — measured, because "it only shows 2" could have been one bad row rather than a structural fault.

Now it climbs to the root and walks down breadth-first, one group per stage. Eevee's nine render as one plus eight, Wurmple's branch keeps `silcoon, cascoon → beautifly, dustox` in the right stages, and the count of species seeing an incomplete family is zero.

### Phases 42–48 — the home screen, and maths by choice

The home screen was laid out against what comparable apps do rather than from taste: **HUD → wordmark → levels → Pokémon → buttons**, and all of it above the fold down to 360×640. Everything there is a fixed cost except the Pokémon, so that is the part that gives way — its frame is sized from viewport *height* and shrinks from 196px to 115px.

The three stat cards became a **HUD**: icon and number, no cards, no labels. Its icons are drawn as inline SVG rather than typed as emoji, because emoji ink differs inside identical boxes and the metrics belong to whichever font the device has — there is no offset that is right everywhere. The four level tiles followed, with `123` on both maths rows and the operation in the label.

Maths answers became **six numbers in order** instead of a keypad. The wrong five are built from the mistakes each operation invites, not sampled from the level's range. Two things had to be measured to get it right: the range could not be the source at all, because four division levels have fewer than six possible answers; and sorting the six centred the answer until the *split* — how many sit below it — was chosen first.

The trade, on the record: a blind guess now lands 1 in 6, and a round can be brute-forced in about three taps. Promotion resists it, since every wrong tap marks the attempt unclean, but the practice is weaker than composing the number was.


## Doc roles

- `Overview.md` — what the app does today. No history, no status, no plans.
- `CLAUDE.md` — the working agreement, and where everything lives. Loaded automatically at the start of a session.
- `progress.md` — this file: how it got here, and what's open.
- `LessonTrails.md` — curriculum design rationale.
- `data/README.md` — CSV columns and the editing traps that aren't obvious.

## Tooling note

Real browser testing works in web sessions: Node, Playwright and Chromium are preinstalled. Serve the folder and drive it rather than opening a `file://` URL — which the CSV loading now requires anyway.

```js
// The preinstalled build is older than a fresh `npm i playwright` expects, so
// launch with an explicit path and do NOT run `npx playwright install`.
chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' })
```

Calling the app's own functions via `page.evaluate()` — `mkReading()`, `renderPokedex()`, then asserting on the DOM — reaches any mode or level directly without playing to it. But check screenshots too, and zoom in: several bugs here passed every structural assertion while being visibly broken, and one — misaligned HUD icons — measured *correct* on every number available and was obvious the moment the row was rendered at 4×.
