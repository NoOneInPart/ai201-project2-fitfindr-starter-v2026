# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr is a command-line thrift shopping and styling assistant. Users enter what they are looking for in plain English, optionally specifying a preferred size or price limit (such as `'vintage graphic tee under $30'`). The assistant searches secondhand listings to find the best match and suggests styled outfit combinations by pairing the find with items the user already owns in their wardrobe. Finally, it writes a short social media caption (a "fit card") highlighting the piece, its price, where to buy it, and its overall aesthetic vibe.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Look for listings with a matching description/size/max_price and return them as a list.
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
               description (str), size (str or None), max_price (float or None)
- **Returns:** list (dict) of matching items (id, title, description, category, style_tags [list], size,
        condition, price [float], colors [list], brand [str or None], platform), best match first
- **When it has nothing:** BRANCHING POINT: search_listings returns an empty list, the agent places an error in the session. otherwise call suggest_outfit

### `suggest_outfit`

- **What it does:** Suggest an outfit (or two) based on a considered item and the user's wardrobe
- **Inputs:** new_item (dict) (id, title, description, category, style_tags [list], size,
        condition, price [float], colors [list], brand [str or None], platform), wardrobe (dict) (id, name, category, colors [list], style_tags [list], notes)
- **Returns:** string with outfit suggestions
- **When it has nothing:** return string with general styling advice if no wardrobe

### `create_fit_card`

- **What it does:** write a caption about the find like how a social media influencer would write about some random thing they got from a thrift store to hype it up and drive ebay prices up
- **Inputs:** outfit (str), new_item (dict) (id, title, description, category, style_tags [list], size, condition, price [float], colors [list], brand [str or None], platform)
- **Returns:** 2-4 sentence string
- **When it has nothing:** return descriptive message string

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a helpful message in `session["error"]` explaining what the user could adjust (raising the price ceiling, checking different sizes, or broadening search terms) and stop without calling `suggest_outfit`. Otherwise, assign the first match (`search_results[0]`) to `session["selected_item"]` and proceed to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
Regex. Regular expressions extract price ceilings (e.g., `under $30`, `max $50`) into `max_price: float` and size specifications (e.g., `size M`, `in size M`, `size 8`) into `size: str`. Conversational filler phrases (e.g., `looking for a`, `find me`) and the matched price/size clauses are stripped, leaving the core item keywords in `description: str`.

**What moves through the session:** <!-- which fields, in what order -->
1. `query` and `wardrobe` (initialized by `new_session`)
2. `parsed` (stores extracted `description`, `size`, and `max_price`)
3. `search_results` (stores list of matching listing dicts from `search_listings`)
4. `error` (set with actionable guidance if `search_results` is empty, ending the run)
5. `selected_item` (stores the top match `search_results[0]` for styling)
6. `outfit_suggestion` (stores output string from `suggest_outfit`)
7. `fit_card` (stores final social media caption string from `create_fit_card`)

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'
$ python app.py ask 'jeans'

  Found:    Baggy Carpenter Jeans — Dark Wash — $36.0 on depop

  Outfit:   Hey! As your FitFindr stylist, I am *so* on board with you thrifting these baggy carpenter jeans. 90s workwear is having a massive moment, and that hammer loop detail adds instant street-cred. 

Since you already have an incredible foundation of streetwear basics and grunge staples in your closet, you can style these right away. Here are two distinct outfit combinations using pieces you already own:

### Look 1: The 90s Off-Duty Model (Casual Streetwear)
*   **Top:** White ribbed tank top
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** 
*   **Silhouette Balance:** The baggy, low-to-mid waist fit of the carpenter jeans creates a classic skater/90s silhouette. Pairing them with a fitted, ribbed white tank top creates an effortless high-contrast balance between tight and loose. 
*   **Aesthetic & Color:** Throwing on the vintage black denim jacket over top leans into the double-denim trend without being matchy-matchy (indigo blue meets washed black). The chunky white sneakers tie in with the crisp white tank, grounding the whole streetwear vibe.

---

### Look 2: Grungy Utilitarian (Cozy & Edgy)
*   **Top:** Oversized grey crewneck sweatshirt
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt, Black crossbody bag

**Why it works:**
*   **Proportions & Vibe:** This leans heavily into the workwear and grunge aesthetic. Tucking a corner of the oversized grey crewneck into the waistband (and letting the brown leather belt peek out) defines your waist while keeping the top comfortably slouchy to match the volume of the pants.
*   **Color Harmony:** The cool charcoal grey of the sweatshirt complements the deep indigo dark wash of the carpenter jeans, while the black combat boots add a tough, grounded finish that plays offthe utilitarian hammer loop on the pants. 

**Stylist Verdict:** *Buy them!* They’ll easily integrate into your current rotation and give you that effortless, slouchy aesthetic.

  Fit card: Scored these vintage Baggy Carpenter Jeans — Dark Wash on Depop for just $36.00, and I am officially obsessed with the 90s workwear energy! Whether I'm pairing them with a sleek ribbed tank and chunky sneakers for that off-duty model look or leaning into grunge with an oversized crewneck and combat boots, that hammer loop detail adds instant street-cred. 🛠️✨

2 model calls this session, 1007 prompt + 552 output tokens

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}]
```

```
$ python -c "from tools import suggest_outfit; ..."
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Hey there! As your FitFindr stylist, I am *so* on board with you grabbing these vintage Levi’s 501s. A good medium-wash 501 is the ultimate wardrobe holy grail—they truly go with everything. 

```
Since you already have a killer mix of streetwear basics, minimal pieces, and edgy footwear, here are two effortless outfit combinations you can build using your current wardrobe:

### Look 1: The 90s Off-Duty Streetwear Vibe
* **The Recipe:** Vintage Levi’s 501 Jeans + White ribbed tank top + Black cropped zip hoodie + Chunky white sneakers + Black crossbody bag.
* **Why it works:** 
  * **Silhouette:** The fitted white tank balances out the straight-leg cut of the 501s, while layering the black cropped zip hoodie on top creates a cool, dimensional streetwear proportion. 
  * **Color Harmony:** Classic blue denim, crisp white, and black is a timeless, foolproof color palette. The chunky white sneakers tie back to the white tank for a cohesive, intentional finish.

### Look 2: Edgy Grunge-Classic
* **The Recipe:** Vintage Levi’s 501 Jeans + Oversized grey crewneck sweatshirt + Brown leather belt + Black combat boots + Vintage black denim jacket.
* **Why it works:**
  * **Aesthetic Vibe:** This leans into a textured, effortlessly cool grunge-meets-vintage aesthetic. Tucking the oversized grey crewneck into the 501s and cinching it with the brown leather belt adds a touch of structure.
  * **Silhouette & Contrast:** Pairing the structured medium-wash denim with the heavier black combat boots grounds the look, and throwing on the black denim jacket creates an awesome "denim-on-denim" moment with the black-and-blue contrast. 

**Stylist Verdict:** Definitely add these to your cart! They’re going to slot right into your rotation and give you so much styling versatility.
```
$ python -c "from tools import create_fit_card; ..."

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Nothing beats the effortless 90s off-duty model vibe of these Vintage Levi's 501 Jeans in a perfect medium wash. I love pairing them with crisp white sneakers for that ultimate casual, everyday look that just works. Snag this holy grail piece over on my depop for just $38.00 before someone else grabs them!
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* Help writing the agent loop
- *What came back:* A surprisingly well-documented agent loop
- *What I changed:* I changed the suggestion for if there are no results since "raising your budget" isn't always going to get you more results.

**Moment 2**

- *What I asked for:* Help with writing my criteria to be measureable
- *What came back:* A highly technical sounding version of my criteria that is more measureable
- *What I changed:* I rewrote it in my own words

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
