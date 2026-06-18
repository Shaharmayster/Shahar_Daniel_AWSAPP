import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///local.db")

GREETING_TYPES = [
    "שבת שלום",
    "מזל טוב",
    "חג שמח",
    "מתגעגעת אליכם",
    "ברכות",
]

RECIPIENTS = [
    "נכדים",
    "נכד",
    "נכדה",
    "משפחה",
    "בן",
    "בת",
]

GRANDMA_STYLES = [
    "סבתא פולניה",
    "סבתא מרוקאית",
    "סבתא עיראקית",
    "סבתא רוסיה",
]
