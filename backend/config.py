import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///local.db")

GREETING_TYPES = [
    "Shabbat Shalom",
    "Happy Birthday",
    "Holiday Greeting",
    "Missing You",
    "Congratulations",
]

RECIPIENTS = [
    "Grandchildren",
    "Grandson",
    "Granddaughter",
    "Family",
    "Son",
    "Daughter",
]

GRANDMA_STYLES = [
    "Polish Grandma",
    "Moroccan Grandma",
    "Iraqi Grandma",
    "Russian Grandma",
]
