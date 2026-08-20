# Working agreement

**Do not build, commit, or push until we have aligned.** This is the rule, not a
preference, and it has been broken more than once.

- **Investigating is not permission to fix.** "Can you check X?" means check X
  and report. It does not mean check X, change it, document it, and push it.
- **Answer my questions first.** If a proposal raises open questions, ask them
  and stop. Do not start work on the parts that seem settled while the rest is
  still open.
- **Wait for an explicit go.** "Build it", "ship it", "do it" — an actual
  instruction. Agreement with a diagnosis is not an instruction to act on it.
- **This covers everything in the repo**, not just app code: docs, CSVs,
  tooling. While a design is being worked out, the working tree stays as it is
  unless I have asked for a change.
- **Uncommitted work is fine.** A stop hook may complain about uncommitted or
  untracked files. It is wrong to act on that during a design discussion — leave
  the work in place and say so.
- **What is always welcome:** measuring, modelling, reading code, running the
  app to reproduce something, and reporting what was found. Do as much of that
  as is useful. Then stop and report.

# Where things live

- `Overview.md` — what the app does today. No history, no status, no plans.
- `progress.md` — how it got here, and what's still open.
- `LessonTrails.md` — curriculum design rationale.
- `data/README.md` — every CSV column, and the editing traps that aren't obvious.
- `data/*.csv` — the game's content **and** all ten lesson ladders: spelling,
  reading, and eight maths tracks. `index.html` holds no copy of any of them;
  the CSVs are authored from a design spreadsheet.

# One file, one namespace

`index.html` holds all the CSS and JS. There is no module scope and no tooling to
warn you, so **before naming a new class or top-level function — or deleting one —
grep for the name.** Every collision this project has hit was silent:

- a `.tiles` rule reflowed the spelling letter bank into three columns;
- a second `placeChunk` meant every tap in one mode reached the other mode's
  function and returned with no sound, no error and nothing on screen;
- `.count-badge` was nearly deleted as dead when it was still the Battle
  screen's win/loss record.

`grep -o "^function [a-zA-Z0-9_]*" index.html | sort | uniq -d` catches the
second kind in a second, and has since caught a bad splice that duplicated 160
lines including a whole second `renderReading`.

# Running it

The app fetches its CSVs, so it must be **served**, not opened from `file://`.
Node, Playwright and Chromium are preinstalled — serve the folder and drive it:

```js
// The preinstalled build is older than a fresh `npm i playwright` expects, so
// launch with an explicit path and do NOT run `npx playwright install`.
chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' })
```

Check screenshots, not just assertions, and zoom in when something is reported
as looking wrong. Several bugs here passed every structural assertion while being
visibly broken. The reverse happens too: misaligned HUD icons measured *correct*
on every number available, and the cause was obvious the moment the row was
rendered at 4×.

# Measure before designing

The habit that has paid off most. The pity timer was settled by simulation, not
reasoning; six answer choices only worked once the answer *space* per level was
counted; and sorting those choices was checked by measuring where the answer
landed, which exposed an exploit the change itself could never have shown.
Reported numbers in `progress.md` are worth trusting — they were generated, not
estimated.
