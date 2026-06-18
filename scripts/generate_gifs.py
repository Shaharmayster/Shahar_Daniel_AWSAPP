#!/usr/bin/env python3
"""Generate static grandma greeting GIFs (one per style + greeting type)."""

from pathlib import Path

from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

GIF_DIR = Path(__file__).resolve().parent.parent / "frontend" / "static" / "gifs"
WIDTH, HEIGHT = 360, 280

GRANDMA_STYLES = {
    "polish": {
        "title": "סבתא פולניה",
        "skin": (255, 220, 190),
        "hair": (210, 210, 210),
        "scarf": (70, 100, 160),
        "apron": (240, 240, 245),
        "bg": (255, 248, 230),
    },
    "moroccan": {
        "title": "סבתא מרוקאית",
        "skin": (210, 170, 130),
        "hair": (50, 35, 25),
        "scarf": (200, 50, 60),
        "apron": (255, 200, 80),
        "bg": (255, 240, 220),
    },
    "iraqi": {
        "title": "סבתא עיראקית",
        "skin": (200, 160, 120),
        "hair": (30, 25, 20),
        "scarf": (140, 100, 60),
        "apron": (255, 230, 200),
        "bg": (255, 245, 235),
    },
    "russian": {
        "title": "סבתא רוסיה",
        "skin": (245, 215, 195),
        "hair": (120, 90, 70),
        "scarf": (180, 30, 40),
        "apron": (200, 220, 240),
        "bg": (245, 248, 255),
    },
}

GREETING_TYPES = {
    "shabbat": {
        "label": "שבת שלום",
        "subtitle": "שבת שלום ומנוחה לכל המשפחה",
    },
    "birthday": {
        "label": "מזל טוב",
        "subtitle": "שתזכו לרוב שנים של אושר ובריאות",
    },
    "holiday": {
        "label": "חג שמח",
        "subtitle": "חג שמח ושמח מהלב",
    },
    "miss_you": {
        "label": "מתגעגעת אליכם",
        "subtitle": "מתגעגעת אליכם כל יום מחדש",
    },
    "blessings": {
        "label": "ברכות",
        "subtitle": "ברכות חמות ואוהבות מהלב",
    },
}

STYLE_KEY_TO_HEBREW = {
    "polish": "סבתא פולניה",
    "moroccan": "סבתא מרוקאית",
    "iraqi": "סבתא עיראקית",
    "russian": "סבתא רוסיה",
}

TYPE_KEY_TO_HEBREW = {
    "shabbat": "שבת שלום",
    "birthday": "מזל טוב",
    "holiday": "חג שמח",
    "miss_you": "מתגעגעת אליכם",
    "blessings": "ברכות",
}

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Hebrew.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_grandma(draw, style, cx, cy):
    skin = style["skin"]
    hair = style["hair"]
    scarf = style["scarf"]
    apron = style["apron"]

    draw.ellipse([cx - 70, cy - 20, cx + 70, cy + 110], fill=apron)
    draw.ellipse([cx - 55, cy - 80, cx + 55, cy + 30], fill=skin)
    draw.ellipse([cx - 58, cy - 95, cx + 58, cy - 10], fill=hair)
    draw.polygon(
        [(cx - 60, cy - 30), (cx + 60, cy - 30), (cx + 45, cy + 10), (cx - 45, cy + 10)],
        fill=scarf,
    )
    draw.arc([cx - 55, cy - 95, cx + 55, cy - 10], 190, 350, fill=hair, width=8)
    draw.ellipse([cx - 22, cy - 25, cx - 8, cy - 12], fill=(60, 40, 30))
    draw.ellipse([cx + 8, cy - 25, cx + 22, cy - 12], fill=(60, 40, 30))
    draw.arc([cx - 18, cy - 5, cx + 18, cy + 18], 10, 170, fill=(180, 80, 90), width=3)
    draw.ellipse([cx - 48, cy + 2, cx - 32, cy + 18], fill=(255, 180, 180))
    draw.ellipse([cx + 32, cy + 2, cx + 48, cy + 18], fill=(255, 180, 180))


def rtl(text):
    return get_display(text)


def draw_centered_text(draw, text, y, font, fill, width):
    display_text = rtl(text)
    bbox = draw.textbbox((0, 0), display_text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, y), display_text, font=font, fill=fill)


def create_gif(style_key, type_key):
    style = GRANDMA_STYLES[style_key]
    greeting = GREETING_TYPES[type_key]

    img = Image.new("RGB", (WIDTH, HEIGHT), style["bg"])
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([10, 10, WIDTH - 10, HEIGHT - 10], radius=18, outline=(80, 80, 100), width=3)

    title_font = load_font(34)
    subtitle_font = load_font(20)
    style_font = load_font(18)

    draw_centered_text(draw, greeting["label"], 24, title_font, (40, 40, 60), WIDTH)
    draw_grandma(draw, style, WIDTH // 2, 120)
    draw_centered_text(draw, style["title"], 200, style_font, (90, 70, 50), WIDTH)
    draw_centered_text(draw, greeting["subtitle"], 232, subtitle_font, (70, 90, 120), WIDTH)

    return img


def main():
    GIF_DIR.mkdir(parents=True, exist_ok=True)

    for old in GIF_DIR.glob("*.gif"):
        old.unlink()

    for style_key in GRANDMA_STYLES:
        for type_key in GREETING_TYPES:
            filename = f"{style_key}_{type_key}.gif"
            img = create_gif(style_key, type_key)
            img.save(GIF_DIR / filename, format="GIF")
            print(f"Created {filename}")

    img = create_gif("polish", "shabbat")
    img.save(GIF_DIR / "default.gif", format="GIF")
    print("Created default.gif")


if __name__ == "__main__":
    main()
