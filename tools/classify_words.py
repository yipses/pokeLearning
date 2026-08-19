#!/usr/bin/env python3
"""Grade every word in the item catalogue into one of the nine phonics Word Levels.

Development tool, not part of the app. Reads data/items.csv, splits every name on
spaces and hyphens, and writes data/word_levels.csv — one row per distinct word,
for review in a spreadsheet.

The classification is a first pass, not an authority. Precedence between patterns
was tuned against the 100 words that were originally graded by hand, and it
reproduces 91 of them; the rest are flagged `differs` in the output. Words that
match several patterns (Sprinkler is a blend, r-controlled AND multisyllabic) are
assigned the one a teacher would name, which is a judgement the rules approximate
rather than settle.

Needs a common-English word list to split closed compounds — "bath" and "tub" are
not themselves item names. Fetch once:
  curl -o /tmp/g10k.txt https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt

Usage:  python3 tools/classify_words.py [path-to-wordlist]   (run from the repo root)
"""
import os
WORDLIST = (__import__("sys").argv[1] if len(__import__("sys").argv) > 1
            else "/tmp/g10k.txt")

import csv, re, collections, json, sys

TOP2000 = set()
LEVELS = {1:"Short-vowel CVC",2:"Floss doubles",3:"Consonant blends",4:"Digraphs",
          5:"Silent-e",6:"Vowel teams",7:"R-controlled",8:"Compound words",9:"Multisyllabic"}

DIGRAPHS   = ["sh","ch","th","wh","ph"]          # 'ck'/'ng' deliberately excluded: the
                                                  # hand list treats Brick as a blend
BLENDS     = ["bl","br","cl","cr","dr","fl","fr","gl","gr","pl","pr","sc","sk","sl",
              "sm","sn","sp","st","sw","tr","tw","tw","qu","sq","thr","shr","spl","spr","str"]
TEAMS      = ["ai","ay","ea","ee","ie","oa","oe","oo","ue","ui","au","aw","ew","oi","oy","ou","ow","ey","igh"]
RCTRL      = ["ar","er","ir","or","ur"]
VOWELS     = "aeiouy"

def syllables(w):
    w = w.lower()
    if re.search(r"[aeiou][^aeiouy]es$", w) and w[:-1].endswith("e"): w = w[:-1]
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    # a silent final e doesn't earn its own syllable, unless it's the only vowel
    if w.endswith("e") and n > 1 and not re.search(r"[aeiou]e$", w[-3:] or ""):
        if not w.endswith(("le","ee","ye")): n -= 1
    if w.endswith("le") and len(w) > 2 and w[-3] not in VOWELS: n = max(n, 2)
    return max(1, n)

def has(w, pats): return [p for p in pats if p in w]

def silent_e(w, vocab=None):
    if re.search(r"[aeiou][^aeiouy]e$", w): return True
    if re.search(r"[aeiou][^aeiouy]es$", w) and vocab is not None:
        return w[:-1] in vocab and w[:-2] not in vocab   # vine+s, not box+es
    return False

def r_controlled(w):
    for p in RCTRL:
        for m in re.finditer(p, w):
            i = m.start()
            # "wire", "store": vowel + r + silent e is a long vowel, not r-controlled
            tail = w[i+2:]
            if tail.startswith("e") and (len(tail) == 1 or tail in ("es","e")): continue
            return True
    return False

def is_cvc(w):
    return len(w) <= 4 and syllables(w) == 1 and re.fullmatch(r"[^aeiouy]+[aeiou][^aeiouy]+", w) is not None

def floss(w): return bool(re.search(r"(ll|ff|ss|zz)$", w))

def initial_blend(w):
    return any(w.startswith(b) for b in BLENDS)

# Words a splitter can dismantle but a teacher would never call compound.
NOT_COMPOUND = {"cannon","tablet","charcoal","carpet","carrot","forest","garden","basket",
                "beacon","cabinet","candle","canvas","carbon","corner","cotton","curtain",
                "dragon","hammer","lantern","lettuce","mitten","pattern","pillow","ribbon",
                "rocket","sofa","target","tunnel","wallet","window"}

def compound_split(w, vocab):
    if w in NOT_COMPOUND: return None
    """Both halves must be real words of >=3 letters. Longest-first on the left
    part avoids junk splits ("sandbox" as "san"+"dbox"), and a plural "s" on the
    whole word is peeled first so "pinwheels" reads as pin+wheel."""
    if len(w) < 6: return None
    cands = [w]
    if w.endswith("s") and len(w) > 7: cands.append(w[:-1])
    for word in cands:
        for i in range(len(word)-3, 2, -1):
            a, b = word[:i], word[i:]
            if len(b) < 3: continue
            # Two three-letter halves are usually a junk split ("asp"+"ear"),
            # unless both are very common words in their own right ("lap"+"top").
            if max(len(a), len(b)) < 4 and not (a in TOP2000 and b in TOP2000): continue
            if a in vocab and b in vocab: return (a, b)
    return None

def classify(w, vocab):
    w = w.lower()
    matched = []
    if has(w, DIGRAPHS): matched.append("digraph")
    if silent_e(w, vocab): matched.append("silent-e")
    if r_controlled(w): matched.append("r-controlled")
    if has(w, TEAMS): matched.append("vowel-team")
    if initial_blend(w): matched.append("blend")
    if floss(w): matched.append("floss")
    syl = syllables(w)
    comp = compound_split(w, vocab)
    if comp: matched.append(f"compound({comp[0]}+{comp[1]})")

    # Precedence, tuned against the 100 hand-graded words. Structure beats
    # pattern; among patterns, the one a teacher would actually name.
    if comp:                                  lvl = 8
    elif "digraph" in matched:                lvl = 4
    elif "silent-e" in matched and syl == 1:  lvl = 5
    elif syl >= 3:                            lvl = 9
    elif "r-controlled" in matched:           lvl = 7
    elif "vowel-team" in matched:             lvl = 6
    elif "blend" in matched and syl <= 2:     lvl = 3
    elif floss(w):                            lvl = 2
    elif is_cvc(w):                           lvl = 1
    else:                                     lvl = 9
    return lvl, matched, syl

# ---------------- build vocabulary ----------------
items = [r["name"] for r in csv.DictReader(open("data/items.csv"))]
plain = [n for n in items if re.fullmatch(r"[A-Za-z]+([ -][A-Za-z]+)*", n)]
uses = collections.Counter()
for n in plain:
    for part in re.split(r"[ -]", n): uses[part.lower()] += 1
vocab = set(uses)
# A common-English list makes compound splitting possible at all: "bath"+"tub"
# are not themselves item names. Restricted to the top ~10k so the splitter
# can't reach for obscure fragments.
ranked = [l.strip() for l in open(WORDLIST)]
TOP2000.update(ranked[:2000])
common = {l.strip() for l in open(WORDLIST) if len(l.strip()) >= 3}
common |= {"tub","pit","cork","drift","weed","rail","pad","post","dust","bench","wheel","shell",
           "sand","bags","spot","sky","hay","mat","rug","ore","orb","kit","log","cot","fin","fir"}
vocab |= common

# Pokémon names that turn up as item words ("Hoppip water bottle", "Pikachu
# doll"). They carry a phonics level like anything else, but it is fiction: they
# are invented proper nouns learned by memory, not decoded by pattern. Flagged
# here so the Spelling trail can leave them alone — they are already reachable as
# Pokémon names proper, gated by generation.
POKE_NAMES = {r["name"].lower() for r in csv.DictReader(open("data/pokemon.csv"))}

HAND = {
 1:["Fan","Mug","Sink"], 2:["Bell","Moss"], 3:["Brick","Fluff","Glass","Gravel"],
 4:["Shutter","Torch","Perch","Wheat","Charcoal","Sandwiches"],
 5:["Bike","Rope","Slide","Wire","Frame","Plate","Twine","Stone","Ice","Vines"],
 6:["Balloons","Bean","Book","Canoe","Clay","Honey","Leaf","Levee","Toilet"],
 7:["Barrel","Cart","Counter","Fern","Lantern","Letter","Lumber","Marble","Paper","Planter","Printer","Speaker"],
 8:["Bathtub","Bookcase","Campfire","Corkboard","Driftwood","Duckweed","Firepit","Gravestone","Handcar","Handrail","Laptop","Leftovers","Limestone","Mailbox","Notepad","Pinwheels","Sandbags","Sandbox","Sandstone","Seashell","Seaweed","Signpost","Skylight","Spaceship","Spacesuit","Spotlight","Stardust","Walkway","Wildflower","Workbench"],
 9:["Bonfire","Cannon","Computer","Concrete","Diploma","Foundation","Humidifier","Icicles","Microscope","Newspaper","Nugget","Potato","Pulley","Refrigerator","Repel","Sprinkler","Stalactites","Stalagmites","Tablet","Television","Tomato","Treasure","Wastepaper","Wheelbarrow"],
}
hand = {w.lower(): lv for lv, ws in HAND.items() for w in ws}

agree = dis = 0
misses = []
for w, want in hand.items():
    got, matched, syl = classify(w, vocab)
    if got == want: agree += 1
    else:
        dis += 1
        misses.append((w, want, got, ",".join(matched), syl))
print(f"agreement with the 100 hand-graded words: {agree}/{agree+dis} ({round(agree/(agree+dis)*100)}%)")
for m in sorted(misses, key=lambda x: x[1]):
    print(f"   {m[0]:<14} hand {m[1]} -> got {m[2]}   [{m[3]}] {m[4]} syl")

# ---------------- emit data/word_levels.csv ----------------
rows = []
for w in sorted(uses):
    lvl, matched, syl = classify(w, vocab)
    comp = [m for m in matched if m.startswith("compound(")]
    rows.append({
        "word": w,
        "level": lvl,
        "pattern": LEVELS[lvl],
        "letters": len(w),
        "syllables": syl,
        "compound_parts": comp[0][9:-1].replace("+"," + ") if comp else "",
        "also_matches": ", ".join(m for m in matched if not m.startswith("compound(")),
        "proper_noun": "yes" if w in POKE_NAMES else "",
        "used_in_items": uses[w],
        "previous_level": hand.get(w, ""),
        "review": "differs" if (w in hand and hand[w] != lvl) else "",
    })
with open("data/word_levels.csv","w",newline="") as f:
    wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    wtr.writeheader(); wtr.writerows(rows)

print()
dist = collections.Counter(r["level"] for r in rows)
print(f"{'level':<6}{'pattern':<20}{'words':>7}   sample")
for lv in range(1,10):
    ws = [r["word"] for r in rows if r["level"]==lv]
    print(f"{lv:<6}{LEVELS[lv]:<20}{len(ws):>7}   {', '.join(ws[:6])}")
print(f"\ntotal {len(rows)} words -> data/word_levels.csv")

# ---------------- emit data/item_levels.csv ----------------
# The per-item view: every catalogue name with the level it lands on. Derived
# from word_levels.csv, so correcting a word there re-grades every item using it.
word_level = {r["word"]: r["level"] for r in rows}
proper = {r["word"] for r in rows if r["proper_noun"]}
out = []
for name in items:
    spellable = bool(re.fullmatch(r"[A-Za-z]+([ -][A-Za-z]+)*", name))
    parts = [p.lower() for p in re.split(r"[ -]", name)] if spellable else []
    lvls = [word_level[p] for p in parts if p in word_level]
    out.append({
        "item": name,
        "level": max(lvls) if lvls else "",
        "kind": "" if not spellable else ("compound" if len(parts) > 1 else "single"),
        "words": len(parts) if spellable else "",
        "components": " + ".join(parts) if len(parts) > 1 else "",
        "component_levels": " + ".join(str(l) for l in lvls) if len(parts) > 1 else "",
        "proper_noun": "yes" if any(p in proper for p in parts) else "",
        "letters": len(re.sub(r"[^A-Za-z]", "", name)),
        "longest_word": max((len(p) for p in parts), default=""),
        "spellable": "yes" if spellable else "no",
    })
out.sort(key=lambda r: (r["level"] == "", r["level"], r["item"]))
with open("data/item_levels.csv", "w", newline="") as f:
    wtr = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    wtr.writeheader(); wtr.writerows(out)

byl = collections.Counter(r["level"] for r in out if r["level"] != "")
print(f"   proper-noun items (excluded from Spelling): {sum(1 for r in out if r['proper_noun'])}")
print(f"\ndata/item_levels.csv: {len(out)} items ({sum(1 for r in out if r['spellable']=='no')} unspellable, kept with a blank level)")
print("items per level:", {k: byl[k] for k in sorted(byl)})
for probe in ["Sea glass fragments", "Charcoal", "Copper ore", "Log bed"]:
    r = next((x for x in out if x["item"] == probe), None)
    if r: print(f"   {r['item']:<22} L{r['level']}  {r['kind']:<9} {r['components'] or '-':<34} {r['component_levels']}")
