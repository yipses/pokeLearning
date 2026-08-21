# Progress Log — Poké Learning

How the project got from a basic spelling/math quiz to where it is now, and the decisions worth not re-litigating. `Overview.md` is the spec for what it does *today*; this file is the journey and the open threads.

---

## Where things stand

Everything speced is built and published on GitHub Pages: ten Lesson Trails promoting, My progress, the Pokédex with detail, tabs and legendary call-outs, Battle, and every piece of content and every ladder in editable CSVs.

**Maths is eight tracks over 57 levels** — add, subtract, multiply, divide and a skip-counting pattern track for each — with prerequisites and promotion gates authored in the spreadsheet. Tracks open on each other's progress rather than in sequence, so the ladder widens as it is climbed. Home and My progress collapse the eight into two families, `+ / −` and `× / ÷`.

The Spelling and Reading trails share one graded vocabulary — all **807 distinct item words** and **819 item names** — climbed by **25 spelling levels** and **10 reading levels**, all authored in a spreadsheet and read at boot. **No ladder, word list or promotion gate remains in code**, maths included.

**A round ends after ten questions answered well enough, not ten shown** — at most `Mistakes allowed` slips each, default 1 — and the progress bar measures those credits, so guessing does not move it. Promotion is a stricter bar and unchanged: still spotless only.

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

**Scope a measurement to the thing being measured.** `.hud-item` matches the results screen's HUD as well as the home one, and hidden copies measure at zero width while still contributing flex gaps. That reported 41px of free space on the home row when the real figure was 60px, and it nearly settled a layout decision on a number that was measuring the wrong element. A measurement is a query, and a query with a loose selector lies confidently.

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

### Phases 58–60 — the home screen earns its width

**The trophy card was a phone layout centred in a wide box.** Reported as *"a lot of white space"* from a tablet screenshot, and the measurement said where: the card used **32% of its own width at 360px and 27% at 768** — 264px dead on each side. The card was never the problem; a centred vertical stack is a 360px layout no matter how wide the box grows. Centring is not reflowing.

**Four candidates were measured and the obvious one lost.** Growing the disc — the emptiest thing on the card — *cost* 41px of height at 360×640 and still reached only 28% at 768, because the frame clamps against viewport height and a tall screen has none to spare. What shipped is two columns: **88–93% of card width used at every supported size**, verified at six of them, with no breakpoint. And the trophy got *bigger*, which was the objection to a left-hand thumbnail and turned out backwards — moving the text out from under the frame frees more height than a larger frame spends, so the circle went 86px → 122px at 360 while the card still *shortened*, buying Start Playing 58px of clearance.

One prototype detail was dropped on measurement: the mock raised the image cap inside the circle from 68% to 78%. A square image centred in a circle keeps its corners inside only up to **1/√2 = 70.7%**, so 78% would have clipped any zero-padding sprite. 68% was already at the geometric limit.

**The wordmark moved into the HUD row**, and the first measurement of the free space was wrong in a way that nearly decided the design. `.hud-item` matches the results screen's HUD as well as home's, and hidden copies counted as zero width while still contributing gaps — reporting **41px free at 360** and making the wordmark look impossible at every width. Scoped to `#homeTiles` the real figure is 60px at 360 and 460px at 768: the words were never impossible, only impossible *on a phone*. Below the sheet's existing 480px breakpoint the words go and the ball stands alone. Another 46px of clearance, putting Start at 456 of 640 where it had been 560.

**Then the card was named and reordered.** Both home cards took headings — `YOUR PROGRESS` and `YOUR POKÉMON`, set through `text-transform` so the accent survives. Inside the second: the **number above the name** (the number is the slot, the name is what fills it), **"Welcome back!" gone** once the card had a heading of its own, **type badges shown whether or not it is caught**, and the generation count moved into the right-hand column under the Pokémon it describes rather than spanning the card as a footer.

### Phases 61–63 — one chrome, one HUD, and zoom off

**The Pokédex opened onto a card, not the collection.** A full card headed *"My Pokédex"* with a `60 / 1021 caught` pill pushed the first grid row most of a screen down, to state a total nobody works toward — the generation is the unit being filled, and its own header already said where it stood. The card went; the grid now starts about **240px** down at every width. In its place: a ✕ matching the round screen, the HUD, and a bar under each generation header — the same `.level-bar` the home card uses, replacing the dashed rule the header carried. The rule separated header from grid; the bar does that *and* says how full the generation is.

**The chrome became one thing.** Settings, Battle, the Pokédex and My progress each had a hand-written top bar: three said "← Back", one said ✕, one carried a badge, none carried the HUD. They now share two rows — the HUD, then a ✕ beside the screen's name — declared once in a `SCREEN_CHROME` map and rendered by `show()`. Four sections dropped from five-to-nine lines of markup each to a single `<div class="chrome"></div>`, and four separately-bound back buttons went with them.

Two things that shook out: **Battle's record was written before the chrome existed** (`newBattle()` calls `updateBattleRecord()` and only then `show()`), fixed by making the extra slot part of the map — a function the chrome calls on every render — rather than by reordering two calls. And **My progress said its own name twice**, once in the chrome and once in a card, so that card went the way the Pokédex's had.

**The collection counter was removed from the HUD and then put back**, which is worth recording as a misread rather than a redesign: *"the HUD should stay persistent and the same"* meant *leave it alone*, and was taken as *make it uniform across screens*. It is three counters everywhere again, and the Pokémon card keeps its own count — the HUD's is chrome with a fixed route to the Pokédex, the card's names the generation it counts.

**Putting the two side by side immediately exposed a bug.** The HUD read `58/147` and the card `60/147` on the same screen: the card counted stored ids inside the generation's number range, the HUD counted roster members, and two ids in the test collection (Nidoran♀ and ♂) are excluded from the roster. Real play cannot store them, which is why nothing had caught it. The duplication the change introduced is what surfaced it.

**Pinch and double-tap zoom are off.** Three mechanisms, because no single one covers every browser: `user-scalable=no` (ignored by iOS Safari, which treats pinch-zoom as an accessibility guarantee), `touch-action: pan-x pan-y`, and `preventDefault` on Safari's non-standard `gesture*` events. A fourth was written and deleted before it shipped — cancelling any `touchend` within 300ms of the last also cancels the click that follows, and this game is played by tapping tiles in quick succession, so it would have eaten real taps. Switching off an accessibility guarantee is right for a game a child holds and cannot undo a gesture on; it would be wrong for a page of text.

### Phase 64 — A round is ten answered, not ten shown

Reported as a child spamming answers until he could move on. Tracing it first changed what the fix had to be: **every mode already retries until the answer is right**, verified in all six — a wrong tap never advances anything. So a round already ended after ten *correct* answers, and spamming never skipped a question, it only resolved one faster. The Lesson Trails were **already immune** too, since `recordAttempt` counts only spotless questions. What was actually being farmed was the round ending and the Pokémon being caught.

A round now ends after **N questions answered with at most `Mistakes allowed` slips** — a Settings value, default 1, counting wrong taps and hints alike, because hinting through a word to reach the end is the same loophole in a different costume. The queue tops up a batch at a time rather than being built once, keeping `buildQueue`'s thirds and no-repeat rule. **The progress bar measures credits**, which is the honest number and also the lesson: guessing leaves the bar where it was.

**Two definitions of clean, deliberately separate.** `spotless()` — nothing wrong at all — still gates promotion, unchanged. `countsForRound()` — at most the allowance — gates only the round. Conflating them would have quietly loosened the ladder while nobody was looking at it.

The risk this shipped with is open thread #1.

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
