# Progress Log — Poké Learning

How the project got from a basic spelling/math quiz to where it is now, and the decisions worth not re-litigating. `Overview.md` is the spec for what it does *today*; this file is the journey and the open threads.

---

## Where things stand

Everything speced is built and published on GitHub Pages: ten Lesson Trails promoting, My progress, the Pokédex with detail, tabs and legendary call-outs, Battle, and every piece of content and every ladder in editable CSVs.

**Maths is eight tracks over 57 levels** — add, subtract, multiply, divide and a skip-counting pattern track for each — with prerequisites and promotion gates authored in the spreadsheet. Tracks open on each other's progress rather than in sequence, so the ladder widens as it is climbed. Home and My progress collapse the eight into two families, `+ / −` and `× / ÷`.

The Spelling and Reading trails share one graded vocabulary — all **807 distinct item words** and **819 item names** — climbed by **25 spelling levels** and **10 reading levels**, all authored in a spreadsheet and read at boot. **No ladder, word list or promotion gate remains in code**, maths included.

## Open threads

Roughly by how much they'd bite.

### 1. A round can fail to end — known, accepted for now

A round finishes after N questions answered with at most `Mistakes allowed` slips (default 1). A child who averages **more** slips than that earns no credits at all and plays forever: simulated to a 400-question guard without finishing. **There is no cap.**

It lands hardest on exactly the child the change was built for — spam hard enough and the app never lets you out — so it is a real risk, not a theoretical one. Shipped knowingly, to see whether a progress bar that visibly refuses to move is enough on its own before adding machinery.

Two shapes a fix could take, neither built:

- **A ceiling.** The round ends after some number of questions regardless — a hard stop, or a soft one where the tail draws from the Review band so the last few get easier until they clear.
- **Scale the allowance to the question.** The allowance is per question, but questions are not the same size: a maths question takes one answer, a pattern set four, a Full Spelling word one placement per chunk, and Missing Letters up to eighteen blanks at the top of the ladder. One slip is a far harder bar on a nine-chunk word than on a single sum, which makes Spelling quietly the strictest mode.

Demotion on repeated failure was discussed alongside this and deliberately **not** built: "wrong many times in a row" is the spam signature as much as the too-hard signature, and tuning a demotion rule against that noise would mean tuning it against the very behaviour this change is meant to remove. Worth revisiting once the behaviour settles.

### 2. The maths sheet's remaining tight spots

The three rows the first cut of the sheet could not satisfy have been fixed at source: `PatternSubtract` levels 1 and 2 now anchor at 5–9 and 10–19 instead of 0–9, and `MathAdd` level 4 is no longer `visual`. A 114,000-question audit against the corrected CSV finds **0 violations**, and every pattern step now has at least one usable anchor — level 2 uses both step 2 and step 3, which it could not before.

Two rows still clear the bar only just: `pattern_sub` level 2 step 3 loses 2 anchors of 10 to the clamp, level 3 step 5 loses 1 of 11. Raising either `step` without widening the anchor range would silently drop the step again.

The tallest visual question left is **`div` level 5** — 25 ÷ 5 draws 25 icons over five groups, 919px on a 390×844 phone. It reads fine and does not overflow sideways; it is 75px below the fold, which the old 19 + 9 case beat at 956px.

### 3. The phoneme respellings still have not been heard

A first pass written on paper turned out to be 30% unspeakable; the rewrite measures at 1%, but *measured* only against a rough test for whether a string can be said at all — not whether it says the **right** sound. `tools/phonemes.html` plays every row and takes about five minutes. `ee` is the one to listen to first.

### 4. Smaller, and each self-contained

- **46 unverified pronunciations**, all Gen 8–9, each with a stated reason for existing. They surface as the collection reaches them; `tools/pronounce.html` filters to exactly this set.
- **`fonts/OFL.txt` is missing.** The Open Font Licence requires its text to travel with the font files; `fonts/README.md` says where to get it. A licence obligation, not a runtime one.
- **Settings overflows horizontally at 360px wide** — measured 115px, from the level `<select>` elements taking their width from the longest option text. The culprit is now Reading's *"Level 10 — Words to level 9 + 9-word, 5 to choose from"* at 352px, not the maths option it used to be. A `max-width` and text-overflow would settle it.
- **The word grading is a first pass.** `tools/classify_words.py` reproduces 91 of the 100 originally hand-graded words; the rest are flagged `differs`. Several words match three patterns at once. `word_levels.csv` is the file to correct — item levels follow from it.
- **~820 un-eyeballed Pokopia items**, for name/image mismatches. Shared artwork is caught automatically now, but an item whose picture is *unique and still wrong* is not.
- **The answer's position leans early on three of the four operations.** Re-measured against the CSV ladder, 3,000 questions per level:

  | track | 1st | 2nd | 3rd | 4th | 5th | 6th |
  |---|---|---|---|---|---|---|
  | `add` | 19.7% | 18.3% | 17.2% | 16.0% | 14.5% | 14.2% |
  | `sub` | 29.0% | 22.5% | 16.0% | 12.9% | 10.5% | 9.1% |
  | `mul` | 23.3% | 22.0% | 19.3% | 14.4% | 12.4% | 8.6% |
  | `div` | 30.1% | 29.6% | 19.0% | 11.2% | 6.8% | 3.2% |

  The cause is the same everywhere: small answers have no room for five wrong options below them. `add` is near-flat because its answers get large; `div` is worst because its quotients run 1–5 on most rows. This was previously recorded as division-only, which the new ladder's smaller `mul` and `sub` answers made untrue. Flattening it means offering negatives, which is not a mistake a five-year-old makes.
- **Three-operand questions are unbuilt.** `num3_min`/`num3_max` are carried through the CSV and are null on every row; nothing reads them yet.
- **`APP_BUILD` is bumped by hand.** No build step stamps it. The `This file` timestamp beside it is automatic and cannot go stale.

Parked, not scheduled: a service worker for genuine offline install; moving the type chart to CSV if it ever needs editing; recorded phoneme audio instead of synthesised respellings; and two deferred Reading modes — **Rhyme Match**, which needs a real-word list and now has one in `word_levels.csv`, and **Clue Words**, which needs per-item colour/size/material data that does not exist.

---

## Lessons this codebase keeps teaching

Each of these cost real time at least once.

**One file, one namespace — grep before you name.** Three collisions so far, every one silent. A `.tiles` rule reflowed the spelling letter bank into three columns. A second `placeChunk` meant every tap in one mode reached the other mode's function and returned with no sound, no error and nothing on screen. `.count-badge` was nearly deleted as dead when it was still the Battle screen's win/loss record. `grep -o "^function [a-zA-Z0-9_]*" index.html | sort | uniq -d` catches the second kind in a second, and it has since caught a splice that duplicated 160 lines.

**Centring is not reflowing.** A layout that looks fine on a phone and is merely *centred* at every larger size is width-blind, not responsive. The home trophy card read as mostly empty on a tablet because it was a 360px stack sitting in the middle of a 724px card, using 27% of it. Nothing was stretched and nothing was broken, which is why it survived so long.

**Measure before designing, and measure the thing that actually matters.** The pity timer was fixed by simulation rather than reasoning. Six answer choices only worked once the answer *space* per level was counted — four division levels have fewer than six possible answers. And sorting those choices was verified by measuring where the answer *landed*, which turned up an exploit the change itself would never have shown: sorted alone, the answer sat 3rd or 4th in 75% of questions.

**Structural assertions are not enough — look at it.** Several bugs passed every DOM assertion while being visibly broken. The reverse happens too: reported misaligned HUD icons measured *correct* on every number available, and the real cause — different ink inside identical boxes — was obvious the moment the row was rendered at 4×.

**Prefer the rule with no floor to the rule that runs out.** Distractors drawn from "other answers at this level" cannot work where a level has four of them; distractors drawn from *the mistakes the operation invites* always can. Same shape of reasoning as excluding items by shared artwork rather than by eyeballing 922 of them.

**A persisted object rebuilt from a whitelist drops whatever is not on the list.** `loadProgress()` reassembled `progress` from `TRACK_IDS`, so the `ladderVersion` stamp was written, saved, and thrown away on read — and the migration it guarded re-ran on its own output at every load, inflating a level the parent had just set. No amount of reading the migration would have shown it; the hole was in the loader.

**One value cannot serve both a decision and a display.** `pctOf` returned `null` for a partial window, which is correct for a promotion gate and nonsense for a chart, where `?? 0` turned *not enough data yet* into *scored zero*. The two wanted different answers to the same question and got one. Splitting them was the whole fix.

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

Four bugs in the same stretch, each reported from a screenshot: a `.tiles` class collision reflowed the letter bank; filled Missing Letters boxes rendered lowercase; **21 Pokémon names were graded as ordinary vocabulary** and had to be excluded from Spelling, since an invented name is memorised rather than decoded; and the pity timer overwrote the drop rate — 50% produced an encounter every single time. That last one is now calibrated so the setting *is* the measured outcome, pity included.

### Phases 30–36 — one way to answer, and sounds attached to it

Both spelling tasks answer the same way: tap a tile holding a **chunk**. `torch` is `T` `OR` `CH` in both. A correct placement says the sound of what was completed, and the whole word is blended back afterwards — the round now waits for the voice to finish rather than talking over it.

**A third of all spoken sounds were unpronounceable.** Respellings with no vowel (`ch`, `th`) or repeated letters (`lll`) get spelled out by a synthesiser: 2,799 of 9,302 events broken. Rewritten as syllables, measured at 1%.

Then four context rules — `c`, `y` (twice) and `ow` reading the word around them, 395 chunk instances changed — and a bug found while building them: context was measured against the whole *name*, not the word, so no vowel in a multi-word item was ever at an end and `Ice cream` came out "ih-kuh-eh".

**97 items share byte-identical artwork**, found by hashing all 922 files. One generic building icon serves ten place names, which is why one screen offered both `Boutique` and `Snowbelle City` for the same picture. Ninety leave both trails: a picture that names two things names neither.

Missing Letters' bank held exactly the missing chunks, so a one-blank word offered **one tile** — 9% of all such questions, 45% of level 2. It is padded with same-phonics-class decoys to a floor of four.

### Phases 37–41 — self-hosted type, spoken names, and the week

(Phase 37 was an investigation that deliberately changed no code; its findings are Open thread 1 above.)

The webfont was never loading in the dev sandbox, which meant **every screenshot taken over several days rendered in a fallback face**. Self-hosting was the better answer anyway for an app aimed at a child on a tablet: latin subset, four weights, 87 KB, and the page now makes no external requests at all.

Opening any Pokémon entry says its name aloud — one rule covering the catch popup, a Pokédex tap, an evolution tap and the results screen, hung off *opening* rather than *rendering* so walking back is silent. The timing was traced with a stubbed 900ms voice: the blend-back ends at 3464ms and the name starts at 4267ms.

**My progress** leads with rounds per day over the last 7 days. No new storage was needed — the streak record has always kept `{date: rounds}` uncapped, so the chart was correct from the day it shipped.

### Phases 42–48 — the home screen, and maths by choice

The home screen was laid out against what comparable apps do rather than from taste: **HUD → wordmark → levels → Pokémon → buttons**, and all of it above the fold down to 360×640. Everything there is a fixed cost except the Pokémon, so that is the part that gives way — its frame is sized from viewport *height* and shrinks from 196px to 86px.

The three stat cards became a **HUD**: icon and number, no cards, no labels. Its icons are drawn as inline SVG rather than typed as emoji, because emoji ink differs inside identical boxes and the metrics belong to whichever font the device has — there is no offset that is right everywhere. The four level tiles followed, with `123` on both maths rows and the operation in the label.

Maths answers became **six numbers in order** instead of a keypad. The wrong five are built from the mistakes each operation invites, not sampled from the level's range. Two things had to be measured to get it right: the range could not be the source at all, because four division levels have fewer than six possible answers; and sorting the six centred the answer until the *split* — how many sit below it — was chosen first.

The trade, on the record: a blind guess now lands 1 in 6, and a round can be brute-forced in about three taps. Promotion resists it, since every wrong tap marks the attempt unclean, but the practice is weaker than composing the number was.

### Phases 49–52 — the Pokédex family, the maths ladder, and a bug eating progress

**The evolution strip showed two of three (49–50).** It walked one hop each way, which is the whole family only if you happen to be standing in the middle of a three-stage line. **269 of 1,021 species saw a family missing at least one member** — measured, because "it only shows 2" could have been one bad row rather than a structural fault. It climbs to the root and walks down breadth-first now; the count is zero. A follow-up report, *"the base Pokémon doesn't show evos anymore"*, was a different case from the one I first reproduced: mine had the species caught and the strip was there, theirs was **uncaught**, where the strip had never rendered at all. The screenshot settled in seconds what the description could not. **Back went with it** — the trail existed because following a line was once a one-way trip, and with the whole family on screen every relative is one tap away.

**The maths ladder moved into CSV (51).** The last hardcoded one. Two tracks of 8 and 12 levels became **eight tracks over 57 levels**, with prerequisites and promotion gates authored in the spreadsheet. Tracks open on each other's progress rather than in sequence, so the ladder widens as it is climbed. Four things were found by generating rather than reasoning: modelling the sheet first caught three rows it could not satisfy; **114,000 generated questions** caught every addition returning `ans: null`; liveness was not transitive, so a locked track's stored frontier could open its dependent; and `19 + 9` drawn as pictures was 956px tall. The sheet was then **corrected at source** rather than worked around. A round is split in thirds — eight maths tracks against one each for spelling and reading would have made a round 80% maths without anyone choosing it.

**Setting a level made it climb (52).** Set spelling to 5, back out, read 8; refresh, 14, then 25. `migrateFrontiers()` stamps `progress.ladderVersion` so its one-off rescale runs once — but `loadProgress()` rebuilds the object from `TRACK_IDS` alone, and the stamp is not a track. Every load looked unstamped and the migration re-ran on its own output. Modelled before fixing: 5 → 8 → 14 → 25, exactly as reported. The same line was silently wiping the new maths frontiers on every load; nobody would have called that a bug, maths simply never seemed to stick.

### Phases 53–57 — one way to advance, My progress rebuilt, and the trophy band

**No Next button (53).** Spelling and Reading advanced on their own; maths waited for a tap. What settled it was what the screen actually held — `.choices.done` hides the grid the moment an answer is right, so a solved question was `7 + 5 = ?`, a checkmark, and a button with one possible action. The word trails can afford their pause because it carries something: the word is spoken aloud while the round is held open. Maths had no such payload. All three maths modes route through `lockAndAdvance()` now, which also disabled every control during the beat and took a tap out of the catch reveal. Given up, on the record: self-pacing — the beat is fixed at 850ms whether or not the child is done looking.

**My progress split maths into its two families (54).** One card per live track was fine at one track and unreadable at eight. Two group cards now, `+ / −` and `× / ÷`, each headed with the summed level the home tile shows, then a slim row per track that opens into the detail. Locked tracks are listed greyed with what opens them — the **immediate** prerequisite, since that is the one a reader can act on. Two layout bugs came out of rendering at 4× rather than from the assertions, which passed: `:last-of-type` counts per *element type*, so a live row being a `<button>` and a locked one a `<div>` stripped the separator from the wrong row; and a `nowrap` unlock note won a squeeze against the track name at 360px, breaking the wrong half.

**The trend charts came out (56).** Two cards reported a minute apart were one bug: `pctOf` returns `null` until a window is full — right for promotion, since 3 clean out of a gate of 5 must not promote — but the same value fed the chart, where `?? 0` turned *not enough data yet* into *scored zero*. Spelling showed bars of 3/3 beside a chart of 0%; Reading showed four fake zeros beside the one real 100% that earned its star. Fixed by splitting the two. Then the charts went entirely, because simulating a real learner showed what they were drawing: rolling accuracy **resets at every promotion** and a level lasts 5–10 attempts, so the line was a sawtooth of fixed period and the gate lines were crossed once per tooth. If a chart returns it should plot **level over time** — a staircase that accumulates, where a flat stretch means stuck. That is the journey; rolling accuracy never was. The level at any point can be reconstructed from the stored `promoted` flags, verified against a real sequence, so nothing was lost.

**Hint caps and the trophy band (55, 57).** `max_hints` came down from the sheet to a cap of 3 from level 11 — nine cells, the only column that had moved. The showcase gained `GENERATION 1` over `3 / 147`: a caught Pokémon shown big says *you have this one*, not *and here is the set it belongs to*. It names the generation of the Pokémon **on screen**, since that differs from the hunted one whenever a freshly opened generation is still empty. It cost 44px on a screen with none spare, and the documented trade applied rather than being renegotiated — the frame gives way, 115px to 86px on the shortest supported screen.

**"Missing Letter" was reported as wrong, and it was — but not the way it looked (57).** The screenshot showed Doduo with four blanks and one letter given, which reads like over-blanking. It is correct: 25%-shown is what eight of the levels ask for. Measuring the mode settled which half was wrong — **96% of its questions have more than one blank**, so the singular was wrong almost always. Renamed in the app and in every doc and comment, since a mode called one thing on screen and another in its own source is the drift this repo keeps paying for.

### Phase 58 — the home trophy card stops being a phone layout in a wide box

Reported as *"the layout here has a lot of white space"*, from a tablet screenshot. It was, and the measurement said where: the showcase card **never used more than 32% of its own width**, and 27% at 768px — **264px dead on each side**. The cause was not the card, which is content-height and never stretched. It was the content: a centred vertical stack is a 360px phone layout centred inside a card that grows to 724px. Centring is not reflowing.

**Four candidates were measured before one was built**, and the obvious one lost. Growing the trophy — the first instinct, since the disc is the emptiest thing on the card — *cost* 41px of height at 360×640 and still reached only 28% at 768, because the frame is clamped against viewport height and a 1024-tall screen has none spare to give it. Capping the card to its content width worked but only moved the emptiness onto the page background. Adding a bar under the generation count scored 91% at phone width, which flattered it: that was the bar alone spanning the card, with the text still a narrow column behind it.

What shipped is the two-column layout with the bar: **88–93% of card width used at every supported size**, verified at 360×640, 390×844, 414×736, 360×780, 768×1024 and 1280×900. No breakpoint — the frame and the text both clamp, so one arrangement covers the range.

**The trophy got bigger, not smaller**, which was the objection to a left-hand thumbnail and turned out to be backwards. Moving the text out from under the frame frees more height than a larger frame spends: the circle goes 86px → 122px at 360 and 196px → 225px at 768, *and* the card still shortens, leaving Start Playing 58px more clearance above the fold than the centred stack gave it.

**One prototype detail was dropped on measurement.** The mock also raised the image cap inside the circle from 68% to 78% of the frame. A square image centred in a circle keeps its corners inside only up to 1/√2 — **70.7%** — so 78% would have clipped artwork on any zero-padding sprite, and the existing 68% is already at the geometric limit. The frame growth alone made the picture bigger anyway: 58px → 83px at 360.

Two things fell out for free. The `max-width:480px` frame override is gone, because `min(22vh, 34vw)` covers short and narrow with one rule. And caught and uncaught card heights are now **identical** (154px at 360) where they differed by 22px, so Start stops shifting when the shelf is empty — something §8c claimed and only roughly had.

Still true and not fixed: a landscape phone (740×360) scrolls. It scrolled before too — Start at 577 against a 360px viewport, now 486 — and 360px of height cannot hold the HUD, wordmark, levels, card and buttons. The supported set is portrait.

### Phase 59 — the wordmark stops owning a row

Reported the same way as the card: *"we don't need a large obvious logo like this on its own row."* It moves into the HUD line, right-aligned with the gear beside it.

**The first measurement of the free space was wrong, and the wrong number nearly decided the design.** `.hud-item` matches the results screen's HUD as well as home's, and the hidden copies were counted at zero width while still contributing gaps — which reported **41px free at 360** and made the wordmark look impossible at every width. Scoped to `#homeTiles` the real figure is **60px at 360, 130 at 430, 291 at 591, 460 at 768**. The words were never impossible; they were impossible *on a phone*. A screenshot saying "I see lots of space" is what prompted the re-measure.

Ball plus words needs 150px even at 14px, so the cut is at the sheet's existing **480px** breakpoint — below it the words go and the ball stands alone. 480 rather than a fourth breakpoint value: the row actually needs 452px, and 28px is not worth another number to keep in step. An attempt at 449px wrapped the counters onto a second line at exactly 450, caught only because the row height came back as 68px instead of 31.

Height freed: **46px more clearance above the fold at 360**, on top of the 58px the two-column card had already bought. Start Playing now sits at 456 of 640, where it was 560 two changes ago.

**Six screens lost their logo, and that is the change worth looking at**, not the home screen. `.brand` sat outside `#homeTop`, so it rendered on all seven; inside it, it renders on one. Settings, Pokédex, My progress and Battle each open with their own **← Back**, and a round now opens with the ✕ and the progress bar — which is what `Overview.md` §8b already said that screen should hold and never quite did.

### Phase 58 — Two headings, and the collection counter moves where it is explained

The home screen's two cards had no headings, so a panel of four levels and a card holding one Pokémon both began mid-sentence. **Your progress** and **Your Pokémon** now label them, set through `text-transform` so the accent survives.

Inside the Pokémon card: the **number goes above the name** — the number is the slot in the collection, the name is what fills it — and **"Welcome back!" is gone**, which read as a caption with nothing to caption once the card had a heading of its own.

**The collection counter moved out of the HUD.** Its dex slot said `5/147` with no label, and the card below it said `GENERATION 1` over `5 / 147` — the same two numbers twice on one screen, one of them explaining nothing. The icon and the tap moved down to the count row, which names the generation it is counting. The results screen keeps its counter, having no card to move it into.

That forced a structural change: the card **was** one big button, so tapping anywhere re-rolled the Pokémon. A button inside a button is invalid and browsers disagree about what to do with one, so the card is a plain container now with two buttons in it — the picture re-rolls, the count row opens the Pokédex. Verified there are zero nested buttons and both taps do what they claim.

Two headings cost height, and 360×640 went over by 3px. Taken back from the gap under a six-letter label rather than from the Pokémon, which has given way enough.

### Phase 59 — The count moves under the Pokémon, and types come back

The generation count spanned the whole card, below both columns, which read as a footer belonging to the card rather than to the one species above it. It sits in the right-hand column now, under the name — the frame leaves that column plenty of room, and the card came out *shorter* for it.

**Type badges show on a caught card too.** They had been the uncaught state's consolation, the one thing a card gave up besides the outline. On a caught card they are one more fact about something already on the shelf, and the column had the space.

**One thing that looked like a bug and was not.** The empty state's silhouette appeared to be missing — a blank circle where the outline should be. Rendered at 4× it is plainly there: `brightness(0) opacity(.28)` on a cream ground is faint at a phone's own scale and washes out entirely in a screenshot. The reverse of the usual trap, and the same fix — magnify before concluding.

### Phase 60 — The Pokédex opens onto the collection

It opened onto a card headed *"My Pokédex"* with a `60 / 1021 caught` pill under it, which pushed the first row of the grid most of a screen down to state a total nobody is working toward — the generation is the unit being filled, and its own header already said where it stood. The card is gone and the grid starts about **195px down** at every supported width.

Three things replaced it, each doing a job the card was not:

- **The HUD follows you here, unchanged.** It is persistent chrome, so it sits where it always does and says what it always says. That settled an inconsistency left over from the previous phase: the counter had been two items on home and three on results. It is **two everywhere** now — the collection count lives on the Pokémon card and in the generation header, both of which name what they are counting, and a counter that differs by screen is not persistent chrome but three similar things.
- **Below the HUD, the ✕ on its own line beside POKÉDEX.** That row names the place you are in and gets you out of it — different work from the HUD's, and putting the ✕ on the HUD line made it read as a fourth counter. A ✕ rather than "← Back", matching the round screen.
- **A bar under each generation header**, the same `.level-bar` the home card and the level tiles use. It replaces the dashed rule the header carried — the rule separated header from grid, the bar does that *and* says how full the generation is. `58 / 147` is exactly the fraction that cannot be felt without one.

One thing checked rather than assumed: the tab strip clips its last pill at the scroll edge, which looks like the ‹ › arrow overlapping it. The arrows are flex siblings, not overlays — that is the strip scrolling, and it predates this change.

### Phase 61 — The chrome becomes one thing, on every screen

Settings, Battle, the Pokédex and My progress each had their own hand-written top bar: three said "← Back", one said ✕, one carried a badge, and none carried the HUD. They wear **the same two rows** now — the HUD, then a ✕ beside the screen's name.

**Declared once rather than per screen.** A `SCREEN_CHROME` map holds each title and, optionally, something to show beside it; `show()` renders it. Four sections went from five to nine lines of markup each down to one `<div class="chrome"></div>`, and the four separately-bound back buttons went with them. Adding a screen is now a row in that map.

Two things the change turned up:

- **Battle's record was written before the chrome existed.** `newBattle()` calls `updateBattleRecord()` and only then `show()`, so the slot it wrote into was still null. Making the extra slot part of the map — a function the chrome calls on every render — fixed it at the shape level rather than by reordering two calls, and `updateBattleRecord` is now one line that re-renders the chrome.
- **My progress said its own name twice**, once in the chrome and once in a card below it. That card is gone, for the same reason the Pokédex's was.

One false alarm worth recording: a regression check reported the Pokédex HUD as empty. The HUD was fine — the *test* still queried `#dexTiles`, an id the chrome no longer emits. A stale selector reads exactly like a broken feature, so the check was fixed rather than the app.

### Phase 62 — The collection counter comes back to the HUD

Removed over two phases: first by reading *"move the Pokédex icon beside the collection numbers"* as literally moving it out of the HUD, then by reading *"the HUD should stay persistent and the same"* as *the same across screens* rather than *unchanged*. The second was a misread — the instruction was to leave the HUD alone, and it was taken as licence to strip the last counter out of it.

It is back, three counters on every screen that shows the HUD. **The Pokémon card keeps its own count as well**, and the duplication is the point: the HUD's is chrome — same corner, every screen, a fixed route to the Pokédex — while the card's names the generation it counts and belongs to the Pokémon above it.

**Putting them side by side immediately exposed a bug.** The HUD read `58/147` and the card `60/147` on the same screen. The card counted *stored ids* falling inside the generation's number range; the HUD counted *roster members*. Two ids in the test collection — 29 and 32, Nidoran♀ and ♂ — are excluded from the roster, so the card counted catches that cannot exist. Real play cannot store them, which is why nothing had caught it. Both derive from the roster now and cannot disagree.

A second thing that looked wrong and was not: a caught Pokémon appeared in an empty frame. The screenshot fired before the image decoded. Waiting on `img.complete && naturalWidth > 0` rather than a fixed delay shows the artwork every time, and is what the check does now.

### Phase 63 — Zoom off

Pinch and double-tap zoom are disabled. A five-year-old holding a tablet triggers both by accident and cannot undo either, and a screen stuck at 2.4× is a broken app to them.

It takes three mechanisms, because no single one covers every browser: `user-scalable=no` on the viewport meta (honoured by Chrome and Android, **ignored by iOS Safari**, which treats pinch-zoom as an accessibility guarantee), `touch-action: pan-x pan-y` on `html,body` (the standards-based half, and what actually stops the gesture in Chrome), and `preventDefault` on Safari's non-standard `gesture*` events, which is the only thing that stops it on iOS. Other browsers never fire those, so it costs them nothing.

**One version of this was written and then deleted before it shipped.** The usual recipe for killing double-tap zoom is to `preventDefault` any `touchend` within 300ms of the last. It also cancels the synthesised click that follows — and this game is played by tapping letter tiles in quick succession, so it would have eaten real taps. `touch-action` already covers double-tap zoom everywhere it is supported, iOS included, so the hack bought nothing and would have cost gameplay. Checked by tapping two different controls 80ms apart: both still register.

Worth being clear about the trade: this is an accessibility guarantee being switched off on purpose. It is right for a game held by a child who cannot undo an accidental gesture, and it would be wrong for a page of text.

### Phase 64 — A round is ten answered, not ten shown

Reported as a child spamming answers until he could move on. Tracing it first changed what the fix had to be: **every mode already retries until the answer is right**, verified in all six — a wrong tap never advances anything. So a round already ended after ten *correct* answers, and spamming never skipped a question, it only resolved one faster.

What spamming actually bought was narrower than it looked. The Lesson Trails were **already immune** — `recordAttempt` counts only spotless questions. What was being farmed was the round ending and the Pokémon being caught, since an encounter resolves on a correct answer however many wrong taps came first.

A round now ends after **N questions answered with at most `Mistakes allowed` slips** — a Settings value, default 1, counting wrong taps and hints alike. The queue tops up a batch at a time rather than being built once, so it keeps `buildQueue`'s thirds and no-repeat rule. **The progress bar measures credits**, which is the honest number and also the lesson: guessing leaves the bar where it was.

**Two definitions of clean, deliberately separate.** `spotless()` — nothing wrong at all — still gates promotion, unchanged. `countsForRound()` — at most the allowance — gates only the round. Conflating them would have quietly loosened the ladder while nobody was looking at it. The eight places that set a boolean flag now increment a count on the question instead, so both rules read the same number.

Two things measurement turned up that are worth deciding on rather than discovering later:

- **A round can fail to end.** At allowance 1, a child averaging two slips a question earns no credits at all and plays forever. Simulated to a 400-question guard without finishing. There is no cap.
- **The allowance is per question, but questions are not the same size.** A maths question takes one answer; a pattern set takes four; a Full Spelling word takes one placement per chunk, and Missing Letters runs to eighteen blanks at the top of the ladder. One slip allowed is a far harder bar on a nine-chunk word than on a single sum.

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
