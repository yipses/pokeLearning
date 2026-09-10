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

### 2. The maths sheet's remaining tight spots — closed

Both tight rows are gone, at source. The Phase 66 retune gave every `pattern_sub` level a **single** step matching its level number (level 4 steps by 4), against anchor ranges that clear four rows of it, so the clamp no longer eats anchors anywhere: measured, **every pattern step in all four pattern tracks can use its whole anchor range**, where `pattern_sub` level 2 step 3 used to lose 2 of 10 and level 3 step 5 lost 1 of 11.

What made the old rows tight is worth keeping in mind for the next edit: a pattern shows four rows, so a step of *k* needs its anchor to survive *4k*. Pairing a large step with a low anchor range silently drops the step rather than failing.

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

### Phase 65 — Prerequisites re-pointed, and the docs stop restating the sheet

Two cells changed in the tuning sheet and nothing else: `pattern_sub` now opens at **subtract 3** rather than subtract 6, and `pattern_div` at **divide 3** rather than multiply-pattern 5. Everything else in it — all 57 maths levels, both word ladders, the promotion gates — already matched, checked cell by cell rather than by eye.

The second change is the interesting one: it re-points a dependency at a **different track**, not just a different level. The graph is symmetric now — the four operations chain, and each pattern track hangs off its own operation at level 3 — where `pattern_div` used to wait on `pattern_mul`, a sibling rather than its own subject.

The unlock order moves with it:

```
was:  add → pattern_add → sub → mul → pattern_mul → pattern_sub → div → pattern_div
now:  add → pattern_add → sub → pattern_sub → mul → pattern_mul → div → pattern_div
```

Skip-counting backwards now arrives with subtraction instead of trailing three tracks behind it. Re-verified after the change: no cycles, no prerequisite pointing past its track's last level, all eight reachable, and the audit still clean at 114,000 questions with 0 violations.

**Then the docs stopped restating the sheet.** Updating those two cells meant editing the unlock order in two files, and it had been wrong in both since the previous sheet change — the second time this has happened. `Overview.md` and `LessonTrails.md` now describe the *mechanism* and link to the sheet instead of listing the values: the prerequisite chain, the eight-row table of level counts and ranges, the promotion percentages and the Settings dropdown example are all gone. The sheet URL was nowhere in the repo at all; it now sits in `data/README.md` for whoever is editing, and in Overview §13.

The rule that fell out of it: **a tunable value written in prose is a value with somewhere to drift.** Overview describes what the app does with a number, never what the number is.

### Phase 66 — The maths sheet retuned, and an alphabet mode

**Twenty-three cells changed in the tuning sheet**, all of them in `add`, `pattern_add`, `sub` and `pattern_sub`; multiply, divide, both their pattern tracks, all eight prerequisites and the promotion gates were already identical. Checked cell by cell against a transcription of the sheet rather than by eye, which is how the count is exact.

Subtraction is the substantial one. It used to jump to two-digit work at level 3 and spend its top five levels there; it now spends four levels inside 0–9 before crossing ten, and its ceiling comes down from 20–29 minus 20–29 to 10–20 minus 0–20. Addition shifts the same way one rung at a time. `pattern_sub` drops its step *pairs* for a single step per level — level 4 steps by 4 — which is what closed open thread 2 above.

Re-verified after the change: 114,000 questions, **0 violations**; no cycles, no prerequisite past its track's last level, all eight tracks reachable; and every pattern step now uses its whole anchor range.

**Then a third Reading mode: Alphabet.** A run of consecutive letters, each shown as a Pokémon whose name starts with it, some of them gaps. The child works out which letter a gap is and picks the Pokémon for it. Three new columns in `data/reading_levels.csv` drive it — `alpha_length`, `alpha_blanks`, `alpha_blank_position` — and the ten rows walk the gaps from the end of the run to the start and then anywhere.

Three decisions worth not re-litigating:

- **The run prints its letters; the options do not.** That split *is* the exercise — the run says what is being asked for, and the only way to answer is to read an option's name and see what it starts with. Printing the letter on the options too would leave nothing to read.
- **Whole roster, not the caught generations.** Measured before designing: the full roster covers **every** run — 23 of 23 at four letters, 22 of 22 at five — where a single generation covers only **7–13**. Gating this the way the word pools are gated would leave most of the alphabet unreachable.
- **Nothing is spoken.** Every name on screen is a first letter, so a speaker anywhere would hand over the sort.

Two things the screenshots caught that the assertions did not, both about the run: it **wrapped to a second line** at 360px, which reads as a new sequence rather than the end of this one — the cards share the width now and never wrap, whatever the row's length; and a long name **broke mid-word** ("Houndston/e"), so the run's names clip with an ellipsis instead. The letter above them is what's being read; the name is context.

One defect the audit caught only after it was extended: distractors excluded the letters *given* in the run, but not the ones the child had **just filled in** — so at `G H _ _` the gap for I could offer a G, dead on arrival. The exclusion is now recomputed per gap rather than per question.

Verified at 30,000 questions across all ten rows: 0 violations against slot count, gap count, consecutive letters, the position rule, answer-in-options, distinct initials, the per-gap exclusion and the nearest-letter rule; all 26 letters reachable; every level reaching all 23 runs. Load-time guards reject the five ways a row can be unanswerable.

**Then the distractor rule was measured, argued, and replaced.** Two things were measured, and they are different questions about the same four tiles. *On-screen position* — which tile the answer physically sits in — was flat at ~25% each on every level, so the shuffle was fine. Its *alphabetical rank* — where the answer sits when you sort the four options' letters — was not: on the `last` levels the answer was the alphabetically-lowest option **87%** of the time, and on the `first` levels the highest 87%. That fell straight out of the rule: nearest letters, minus the visible ones, means that when the visible letters are all below the gap the nearest available ones are all above it.

The defence of near distractors was that they test precision — with M N O P you have to know M comes *immediately* after L, where random distractors would let "somewhere around M" win. **That defence is wrong, and it is worth writing down why**, because it is an easy thing to talk yourself into:

> It only describes a child answering by comparing the options against the run — elimination. Elimination needs the alphabet you are still teaching. A learner recites from the song, derives "M", and then goes looking for it; the distractors take no part in deriving the answer.

So crowding them around the answer doesn't harden the step being taught. It bolts on a second, unrelated one — telling M from N, O and P in a lineup, which is letter-shape recognition — and a child who derives M correctly and then taps Noivern has failed at something the mode isn't about, with no way to tell from the result which step broke. Worse than generic: **M N O P is the slurred stretch of the alphabet song**, the one a five-year-old is least likely to have pulled apart, so a gap right after L was building its options out of exactly the letters still fused together in the recall being used to answer it.

The rule now is **spacing**: every option at least four letters from every other, the answer included, drawn from anywhere not already on screen. A correctly derived answer is unambiguously findable, a guess is unlikely to land, and what decides right or wrong is the derivation. Difficulty rides on the three sheet columns, which is where it belongs.

Re-measured after the change: the closest any two options ever come is **4 letters** — the spacing never has to ease — and the 87% rank lean is gone, the four ranks now running roughly 14 / 29 / 29 / 28. The residual is geometric, not a rule: `last` gaps sit high in the alphabet on average, so there is more room below them than above, and `first` gaps mirror it. At its worst that is a 3-point edge over chance, against 62 before.

**The reading ladder was then rebuilt in the sheet**, and the guard earned its keep on the first try. The new shape is a grid: gap counts 1, 2 and 3, each walked across `last` → `middle` → `first`, then `mixed` last. The first cut of it put all ten rows at `alpha_length 4`, and level 8 — `middle` with 3 gaps — **has no valid shape there**. A run of 4 has exactly two interior slots, so `middle` caps at two gaps; a third has to touch an end, and then it *is* `first` (`___x`) or `last` (`x___`). Measured across the whole grid, it was the only empty cell of the twelve. The load guard rejected the row by name rather than letting the app start and fail at play time, and the fix was in the sheet: levels 7–10 moved to `alpha_length 5`, the shortest run where `middle`/3 exists at all (`x___x`).

That bought variety as a side effect: `mixed`/3 goes from 2 shapes at length 4 to **8** at length 5, so the top rung stops repeating itself. Runs of 5 have 22 windows rather than 23, and the roster fills all of them. The strip holds five cards on one row down to 360px — measured at 51px a card, worst case being the longest name under every letter, which clips to an ellipsis under a letter that stays legible.

**The lesson, which is the one this repo keeps relearning.** The lean was found by measuring, but measuring only said the distribution was skewed — it could not say the rule was wrong. What did that was asking who the question is actually for and how they answer it. Numbers rule things out; they don't tell you what the exercise is.

### Phase 67 — Failure gets a floor

The dead end this closes was watched, not theorised: a question resting on something he has never been taught, and spamming every option because **that is all he CAN do**. Not gaming, not frustration — the only input the screen accepts. Every mode blocks until correct, there is no skip, and only Spelling has hints.

Now, after `Show the answer after` wrong taps on a step, the right answer lights in an amber pulse and he still has to tap it himself.

**Two rejected designs, both worth not revisiting.** An "I don't know" button was the obvious move and is wrong twice over: it becomes the fast path out of every question, and being told the answer costs the productive struggle that makes it stick. A *reveal after failing* has neither problem, because it is not chosen — there is nothing to press early, so it cannot be spammed.

**Why it can never pay to fail on purpose.** The reveal is held at least one mistake past `Mistakes allowed`, so by the time it appears the credit is already gone. Verified across all 36 allowance × threshold combinations: a revealed answer never counts toward the round and never counts as spotless, and the floor never over-corrects — a question at exactly the allowance still counts in all six cases.

**It counts the step, not the question.** A Pattern row and an Alphabet gap are each their own challenge; two slips spread across two rows must not light the second one. Verified in both modes.

**Where it teaches, and where it only rescues.** In Alphabet the run of letters is on screen, so a lit answer has a visible reason; the same in Reading, where the pairing is the lesson. Bare arithmetic is the weak case — lighting `5` for `14 − 9` shows the fact, not the borrowing. Switching those to their visual form on reveal is the obvious fix, `toVisual()` already exists, and it is deliberately **not** built yet.

Wired once for Maths, Visual Math and Pattern by giving `wireMathChoices` the answer, and inline for Reading and Alphabet, which build their own options.

**Then spelling, where the obvious wiring would have been wrong.** The instinct was to light the tiles once `max_hints` runs out — he has failed by then, so the credit is gone. It isn't: `max_hints` is **1** at spelling levels 1, 2 and 5, and with `Mistakes allowed` at its default 1, spending that single hint leaves the question *still counting clean*. Wiring the light to hint-exhaustion would have handed out free credits at the three easiest levels — the exploit the whole floor exists to prevent. Caught by reading `data/spelling_levels.csv` rather than trusting the premise, and confirmed in the app: `after spending the only hint: mistakes=1 counts=true lit=dark`.

So spelling gets no special case. Hints already call `bumpMistake`, so they feed the same per-step counter as wrong taps and the same threshold applies, with the same guarantee. The cap stops being a dead end without being lifted: a hint is chosen, rationed, and *places* the chunk; the light is automatic, uncapped, and only *shows* the tile while the child still taps it. The stronger help stays rationed.

The spelling banks can't just have a class stuck on the right tile, either — which chunk is "next" moves as chunks go down and come back off, including via Backspace and Clear — so `syncSpellLight` / `syncMissingLight` relight the bank from scratch after every board change.

Every mode in the app now has a floor under failure. There is nowhere left to get stuck with no way through.

**What it does to the ladder work.** It bounds the cost of a cliff, so a too-big step becomes survivable rather than a wall, and the ladder can tolerate coarser granularity than it otherwise would. It also produces the signal the difficulty modelling wanted: "needed the reveal" is an unambiguous *couldn't do this at all*, distinct from an ordinary unclean answer — no response-time heuristics, no guessing at intent.

### Phase 68 — Tens and ones, so two-digit questions can be drawn

Visual Math could not reach the levels that most needed it. Measured: the picture support switches off exactly where the hard concept arrives. For addition it survives single-digit carrying (9+9 is 18 icons, drawable) and dies at level 4 where operands go two-digit — which is where carrying becomes *columnar* carrying. For subtraction it is worse: `visual` is already off at level 3 and borrowing does not appear until level 5, so the pictures are gone two levels before the concept that needs them.

The cause is that one icon per unit scales with **magnitude**. `add` L8 is 48 icons. Drawing a ten as one framed object scales with **digits** instead:

| worst case | icons | tens-and-ones |
|---|---|---|
| `add` L8, 29+19 | 48 | **21** |
| `add` L6, 19+19 | 38 | 20 |
| `sub` L7, 19−19 | 20 | 10 |
| `sub` L6, 15−9 | 15 | **6** |

The count is the lesser point: twenty-five identical icons must be *counted*, where "two full boxes and nine" is *read*.

**Rejected: `[icon] ×10`.** Compact, and it solved the theming question, but `×` is gated behind `add` level 7 in `math_tracks.csv` — so at `add` L4, where this first matters, he has never seen a multiplication sign. It would explain carrying with a symbol from a locked ladder, and the ten would still be a numeral. A visible box of ten can be checked rather than taken on trust.

**They are the same Pokémon, not squares.** "One box and four Pokémon" is only fourteen Pokémon if the box contains Pokémon — and when a box opens for a borrow, the ten that spill out must have been there all along. At 20px they read as texture, which is fine: the frame carries the meaning. The size is not a new low either, since the `grouped` layout already draws Pokémon at 20px for × and ÷.

Three things the screenshots caught that the numbers did not:

- **The operator was marooned.** A flex row put `+` beside the first operand while the second wrapped underneath, reading as "29 +" then a stray 19. Operands stack now, operator between them, like a column sum.
- **A box inside a box.** The ten-box and the operand container had the same blue frame, so the outer one read as a bigger ten. The operand's frame is dropped in this layout — with ten-boxes on screen a frame must mean exactly one thing.
- **Nine wrapped as eight-then-one**, which reads as "eight and one". Nine-versus-ten is the comparison the layout exists to make visible, so the loose row is sized to hold nine on one line.

Two CSS traps on the way: sizing keyed to the layout class instead of the row missed `.visual-icon-wrap`, leaving subtraction's crossed-out ones at full size; and a bare `.ones-row .visual-icon` loses on specificity to `.visual-groups.dense .visual-icon`, so the density rule silently won and the nines wrapped again.

**Deliberately incomplete.** No level pairs `visual` with two-digit operands yet, so nothing draws a box in normal play — verified, 1560 questions across every reachable level and zero ten-boxes. And the regrouping itself — a box opening for a borrow, ten closing for a carry — is not built. That is the half that actually teaches; this half only makes it drawable.

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
