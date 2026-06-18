from pathlib import Path

from config import GREETING_TYPES

GIF_DIR = Path(__file__).resolve().parent.parent / "frontend" / "static" / "gifs"
DEFAULT_GIF = "default.gif"

GREETING_TYPE_TO_GIF = {
    "שבת שלום": "shabbat_shalom.gif",
    "מזל טוב": "mazal_tov.gif",
    "חג שמח": "chag_sameach.gif",
    "מתגעגעת אליכם": "miss_you.gif",
    "ברכות": "brachot.gif",
}


def get_gif_filename(greeting_type):
    if greeting_type not in GREETING_TYPES:
        raise ValueError(f"סוג ברכה לא תקין: {greeting_type}")

    filename = GREETING_TYPE_TO_GIF.get(greeting_type, DEFAULT_GIF)
    if not (GIF_DIR / filename).exists():
        return DEFAULT_GIF
    return filename


def get_gif_path(greeting_type):
    return f"gifs/{get_gif_filename(greeting_type)}"
