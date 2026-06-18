from pathlib import Path

from config import GRANDMA_STYLES, GREETING_TYPES

GIF_DIR = Path(__file__).resolve().parent.parent / "frontend" / "static" / "gifs"
DEFAULT_GIF = "default.gif"

GRANDMA_STYLE_SLUG = {
    "סבתא פולניה": "polish",
    "סבתא מרוקאית": "moroccan",
    "סבתא עיראקית": "iraqi",
    "סבתא רוסיה": "russian",
}

GREETING_TYPE_SLUG = {
    "שבת שלום": "shabbat",
    "מזל טוב": "birthday",
    "חג שמח": "holiday",
    "מתגעגעת אליכם": "miss_you",
    "ברכות": "blessings",
}


def get_gif_filename(greeting_type, grandma_style):
    style_slug = GRANDMA_STYLE_SLUG.get(grandma_style)
    type_slug = GREETING_TYPE_SLUG.get(greeting_type)
    if not style_slug or not type_slug:
        return DEFAULT_GIF

    filename = f"{style_slug}_{type_slug}.gif"
    if not (GIF_DIR / filename).exists():
        return DEFAULT_GIF
    return filename


def get_gif_path(greeting_type, grandma_style):
    return f"gifs/{get_gif_filename(greeting_type, grandma_style)}"
