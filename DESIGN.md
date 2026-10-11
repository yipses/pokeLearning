# Design rules

The rules every screen follows. They were settled one screen at a time
(progress.md Phases 80–90 record how), and each exists because breaking it
looked wrong on a real device. **Read this before any UI change; a change that
breaks a rule changes this file first.** Sizes are phone CSS px; a screen that
zooms the question scales everything together.

## Who it's for

- **The child often can't read.** Words on a child's screen are names and
  numbers. No instructions, no captions; a picture, an icon or a spoken name
  does that job. Grown-up screens (Settings, My progress) may use sentences.
- **One thing to look at.** Each screen has one question, one focus and one
  forward action. If two things compete, one of them steps back.

## Colour means one thing each

- **Green = correct**, and nothing else. Answer tiles, choices and letter tiles
  are **neutral** (white, `paper-line` edge, `#958b75` press edge) until chosen.
- **Amber = you are here** (the open slot, row or gap).
- **Orange = the answer revealed** (the help light) in Maths and Reading;
  Spelling, Alphabet and Pattern light green instead, because amber is already
  their cursor.
- **Trail colours** live only on the trail's icon, bar and mode tag.
- **Done steps back.** Finished rows fade (pale `#b3aa97` text, pictures at
  40%, the green answer at 70%) so the open one is the only thing at full
  strength.

## Type: four roles

| Role | Size | Used for |
|---|---|---|
| label | 14 / 800 | mode tag, counters, card headings, names under pictures |
| word | 20 / 800 | word answers, the home Pokémon name, "Level 8" |
| answer | 28 / 900 | any letter or number the child places or chooses |
| prompt | 32 / 900 | what is being asked (28 under 860px tall, 26 under 700) |

Nothing on a screen is bigger than its prompt except the forward button, and a
decorative label never outranks the child's own progress. Long words shrink to
fit one line rather than wrap (floor 16px for a spelled word, 26 for a prompt);
a two-word name breaks only between words.

## Controls

- **Fixed sizes, never percentages of their container.** A control is the same
  object on every screen and every device.
- **Tap targets are at least 44px.** What you see is what you tap — with one
  sanctioned exception: the speaker is drawn at 40px and reaches 44 with 2px
  of invisible margin.
- **One speaker**: 40px `sun-500` circle, `sun-800` mark, `sun-700` edge, on the
  **bottom-right** of the picture it names — centred on a round frame's edge at
  45°, inside a tile's corner. Same size and place on every screen. A word tile
  that needs hearing carries its own, inside its right end, with the tile made
  wide enough that the word never sits under it.
- **Icons are judged by their ink, not their box.** A mark is centred to within
  half a pixel and fills about half its button. Check at 4× zoom.
- **Only tappable things have a press edge.** A label with an edge reads as a
  button; if it does nothing, it can't look pressable (that killed the "Caught!"
  ribbon and the logo Pokéball).
- **Scenery never wears a control's shape.** A white pill is a counter or a
  button here, so the clouds are puffs, a little see-through, and sit below the
  HUD row rather than behind it.
- **The way out stays on screen.** On a screen that scrolls, the ✕ row is
  pinned to the top (a cream bar that casts a shadow once something scrolls
  under it); the counters above it scroll away. What you'd navigate with goes in
  the bar too — the Pokédex's generation tabs.

## Pictures

- **Size by what is drawn.** Artwork is a padded square shaped however the
  Pokémon is; scale it so its visible area matches the median (√(w×h) = 0.81 of
  the box), capped at 1.5×, and never past 2× an image's own pixels.
- **Centre what is drawn, not the canvas.** In a tile, dead centre. In a scene,
  standing on the ground by its lowest drawn pixel, with a soft shadow as wide
  as the Pokémon.
- **Nothing sits under a speaker.** Test the drawing's pixels against the
  speaker's circle; shrink only the pictures that collide, only as far as needed.
- **No frame inside a frame.** A tile is the picture's frame; don't add a disc
  or box inside it.
- **The ground meets the Pokémon.** In a tall scene, seat the subject where it
  balances and bring the ground up to its feet; don't pin it to the bottom
  under empty sky.
- **A badge that is always on says nothing.** Show a marker only where it
  distinguishes (NEW in the Pokédex, not on a screen of new catches).
- **Fewer things get more room.** 1–4 catches stand large in the meadow, sized
  by how many there are, not as chips in a grid built for many.

## Layout

- **The layout gives way, the controls don't.** When space runs out, change the
  arrangement (columns are chosen per question: every balanced count is tried,
  the biggest tiles that fit both width and height win), then shrink text, then
  pictures — never tap targets.
- **Tiles have fixed shapes**: 5:4, flattening to 3:2 only if that fits; at
  most 200px wide. A short last row is centred.
- **A box means one thing.** In Visual Maths a blue box is always five (or ten)
  places, empty ones drawn as faint solid Pokémon; nothing else may wear that
  frame.
- **Scenes above, words on paper.** Pictures stand in the meadow; headings, the
  name card and buttons sit on paper or a white card. Nothing floats on the
  hill line.
- **Highlights never touch.** Two coloured shapes (a ring and a highlight)
  keep at least ~10px apart, or they merge into one.
- **Spacing is a 4px scale** (gaps of 4, 8, 12, 16, 20, 24).
- **Fit or it isn't done.** No vertical or horizontal scroll at 360×640,
  390×844, 470×830, 820×1180, 1024×768, 1280×800 and 1440×900, with the longest
  content (12-letter names, two-word names, five options, four catches).

## How to work

1. **Measure before designing** — sizes, ink, counts, the real data's extremes.
2. **Mock in the browser first** (inject CSS/JS with Playwright); the repo
   stays untouched until the owner says go.
3. **Look at screenshots at true scale.** Never compare devices on a sheet
   scaled to equal height — it makes a small screen's controls look huge.
4. **Fix the system, not the screen.** If a control is wrong in one place, find
   every place it appears and apply one rule.
