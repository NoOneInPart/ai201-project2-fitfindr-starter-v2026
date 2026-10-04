"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re
import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings

_STOP_WORDS = {
    "a", "an", "the", "in", "on", "at", "for", "with", "of", "and", "or",
    "to", "is", "it", "i", "me", "my", "under", "size", "looking"
}


def _matches_size(target_size: str, item_size: str) -> bool:
    """
    Check whether an item size matches the target size string.
    Avoids false positives like 's' in 'us 9' or 'l' in 'xl'.
    """
    if not item_size or not target_size:
        return False
    t = target_size.strip().lower()
    s = item_size.strip().lower()
    if t == s:
        return True

    # Check parts of slash sizes (e.g. 'M' matches 'S/M' or 'M/L')
    slash_parts = [p.strip() for p in s.split("/")]
    if t in slash_parts:
        return True

    # Word boundary check on alphanumeric tokens
    pattern = rf"(?<![a-zA-Z0-9.]){re.escape(t)}(?![a-zA-Z0-9.])"
    if re.search(pattern, s):
        return True

    # Match numeric waist sizes with 'W' prefix in data (e.g. '30' matches 'W30')
    if t.isdigit() and re.search(rf"(?<![a-zA-Z0-9.])w{re.escape(t)}(?![a-zA-Z0-9.])", s):
        return True

    return False


def _score_listing(listing: dict, description: str) -> float:
    """Score listing by keyword overlap and phrase matching against description."""
    desc_lower = description.lower()
    raw_tokens = re.findall(r"[a-zA-Z0-9]+", desc_lower)
    tokens = [t for t in raw_tokens if t not in _STOP_WORDS]
    if not tokens:
        tokens = raw_tokens
    if not tokens:
        return 0.0

    score = 0.0
    title = listing.get("title", "")
    item_desc = listing.get("description", "")
    style_tags = listing.get("style_tags", [])
    category = listing.get("category", "")
    brand = listing.get("brand") or ""
    colors = listing.get("colors", [])

    title_words = set(re.findall(r"[a-zA-Z0-9]+", title.lower()))
    desc_words = set(re.findall(r"[a-zA-Z0-9]+", item_desc.lower()))
    cat_words = set(re.findall(r"[a-zA-Z0-9]+", category.lower()))
    brand_words = set(re.findall(r"[a-zA-Z0-9]+", brand.lower()))
    tag_words = set(re.findall(r"[a-zA-Z0-9]+", " ".join(style_tags).lower()))
    color_words = set(re.findall(r"[a-zA-Z0-9]+", " ".join(colors).lower()))

    # Bonus for exact full phrase match
    if desc_lower in title.lower():
        score += 5.0
    if any(desc_lower == tag.lower() for tag in style_tags):
        score += 5.0

    # Overlap per keyword token
    for token in tokens:
        if token in title_words:
            score += 3.0
        if token in tag_words:
            score += 3.0
        if token in cat_words:
            score += 2.0
        if token in brand_words:
            score += 2.0
        if token in desc_words:
            score += 1.0
        if token in color_words:
            score += 1.0

    return score


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    # 1. Load every listing with load_listings().
    listings = load_listings()

    # 2. Filter by max_price and by size, when each is provided.
    filtered = []
    for item in listings:
        if max_price is not None and item.get("price", float("inf")) > max_price:
            continue
        if size is not None and not _matches_size(size, item.get("size", "")):
            continue
        filtered.append(item)

    # 3. Score what's left by keyword overlap with `description`.
    # 4. Drop anything scoring zero.
    scored = []
    for item in filtered:
        score = _score_listing(item, description)
        if score > 0:
            scored.append((score, item))

    # 5. Sort by score, highest first, and return the listing dicts —
    #    at most config.SEARCH_RESULT_LIMIT of them.
    scored.sort(key=lambda x: x[0], reverse=True)
    limit = getattr(config, "SEARCH_RESULT_LIMIT", 10)
    return [item for _, item in scored[:limit]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    # 1. Check whether wardrobe['items'] is empty.
    if not new_item:
        return "No item provided for outfit suggestions."

    wardrobe_items = wardrobe.get("items", []) if isinstance(wardrobe, dict) else []

    title = new_item.get("title", "thrifted item")
    category = new_item.get("category", "")
    colors = ", ".join(new_item.get("colors", []))
    style_tags = ", ".join(new_item.get("style_tags", []))
    description = new_item.get("description", "")
    brand = new_item.get("brand") or "unbranded"

    item_summary = (
        f"- Item: {title}\n"
        f"- Category: {category}\n"
        f"- Brand: {brand}\n"
        f"- Colors: {colors}\n"
        f"- Style tags: {style_tags}\n"
        f"- Description: {description}"
    )

    if not wardrobe_items:
        # 2. If it is, ask the model for general styling ideas for this item.
        prompt = (
            "You are a creative personal fashion stylist for FitFindr.\n\n"
            f"The user is considering thrifting this piece:\n{item_summary}\n\n"
            "The user currently has an empty wardrobe with no saved pieces.\n"
            "Provide 1 or 2 versatile outfit suggestions and styling advice for how to wear "
            "this piece with common wardrobe staples (e.g., neutral basics, classic denim, "
            "or everyday footwear). Keep it concise, practical, and stylish."
        )
    else:
        # 3. If it isn't, format the wardrobe items into the prompt and ask for
        #    specific combinations naming pieces the user already owns.
        formatted_wardrobe = "\n".join(
            f"- {item.get('name', 'Piece')} ({item.get('category', '')}, "
            f"colors: {', '.join(item.get('colors', []))}, "
            f"tags: {', '.join(item.get('style_tags', []))})"
            for item in wardrobe_items
        )
        prompt = (
            "You are a creative personal fashion stylist for FitFindr.\n\n"
            f"The user is considering thrifting this piece:\n{item_summary}\n\n"
            f"The user's wardrobe contains the following pieces:\n{formatted_wardrobe}\n\n"
            "Suggest 1 or 2 specific outfit combinations incorporating this thrifted item with specific pieces "
            "the user already owns. Explicitly name the pieces they own, and briefly explain why the outfit works "
            "(color harmony, silhouette, or aesthetic vibe)."
        )

    # 4. Return the model's response.
    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    # 1. Guard against an empty or whitespace-only `outfit`.
    if not outfit or not outfit.strip():
        return "No outfit suggestions provided to create a fit card caption."

    if not new_item:
        return "No item provided to create a fit card caption."

    # 2. Build a prompt with the item details and the outfit.
    title = new_item.get("title", "thrift find")
    price = new_item.get("price")
    platform = new_item.get("platform", "thrift store")
    price_str = f"${price:.2f}" if price is not None else "thrift price"

    prompt = (
        "Write a short, authentic social media caption (2 to 4 sentences) showcasing a thrift find.\n\n"
        f"Item: {title}\n"
        f"Price: {price_str}\n"
        f"Platform: {platform}\n\n"
        f"Outfit and styling:\n{outfit.strip()}\n\n"
        "Requirements:\n"
        "- Write exactly 2 to 4 sentences in a natural, conversational voice (like someone posting on Instagram or TikTok, not a dry sales description).\n"
        f"- Explicitly mention the item ('{title}'), its price ('{price_str}'), and the platform ('{platform}') once each.\n"
        "- Be specific about the aesthetic vibe and how the pieces come together.\n"
        "- Return only the caption text."
    )

    # 3. Call generate() and return the response.
    return generate(prompt)
