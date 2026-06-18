from config import GRANDMA_STYLES, GREETING_TYPES, RECIPIENTS

TEMPLATES = {
    ("Shabbat Shalom", "Polish Grandma"): (
        "Shabbat Shalom {recipient} ❤️\n\n"
        "Did you eat today? You look too skinny in the last picture. "
        "I made too much cholent — come eat before it gets cold."
    ),
    ("Shabbat Shalom", "Moroccan Grandma"): (
        "Shabbat Shalom {recipient} 🌙\n\n"
        "The house smells like cumin and love. I set your place at the table — "
        "don't make me call you three times to come eat."
    ),
    ("Shabbat Shalom", "Iraqi Grandma"): (
        "Shabbat Shalom {recipient} ✨\n\n"
        "May this Shabbat bring peace to your heart. I lit the candles and "
        "prayed for you by name. Eat well and rest — family is everything."
    ),
    ("Shabbat Shalom", "Russian Grandma"): (
        "Shabbat Shalom {recipient}.\n\n"
        "Sit down. Eat. Rest. You work too hard. "
        "On Shabbat we stop — even the world can wait one day."
    ),
    ("Happy Birthday", "Polish Grandma"): (
        "Happy Birthday {recipient}! 🎂\n\n"
        "Another year older and still not eating enough. "
        "I baked your favorite cake — three layers, just like you deserve."
    ),
    ("Happy Birthday", "Moroccan Grandma"): (
        "Happy Birthday {recipient}! 🎉\n\n"
        "Today we celebrate YOU with music, sweets, and enough couscous "
        "to feed the whole neighborhood. Mazal tov, my treasure!"
    ),
    ("Happy Birthday", "Iraqi Grandma"): (
        "Happy Birthday {recipient}! 🎂\n\n"
        "May God bless your new year with health, joy, and a home full of laughter. "
        "I made baklava — your favorite — don't share it with anyone."
    ),
    ("Happy Birthday", "Russian Grandma"): (
        "Happy Birthday {recipient}.\n\n"
        "Strong year ahead of you. I made borscht and a cake big enough "
        "for the whole family. Come celebrate — no excuses."
    ),
    ("Holiday Greeting", "Polish Grandma"): (
        "Happy Holiday {recipient}! 🕯️\n\n"
        "The table is set, the house is warm, and there's enough food "
        "for an army. Bring your appetite — I already started worrying you won't come."
    ),
    ("Holiday Greeting", "Moroccan Grandma"): (
        "Happy Holiday {recipient}! ✨\n\n"
        "The house is full of light, spices, and music. "
        "Holidays are for family — come dance, eat, and stay until morning."
    ),
    ("Holiday Greeting", "Iraqi Grandma"): (
        "Happy Holiday {recipient}! 🕯️\n\n"
        "May this season bring blessings to your home. "
        "I prepared all the traditional dishes — your seat is waiting."
    ),
    ("Holiday Greeting", "Russian Grandma"): (
        "Happy Holiday {recipient}.\n\n"
        "Winter is cold but the house is warm. I cooked for two days straight. "
        "Come eat. Then eat more. That's what holidays are for."
    ),
    ("Missing You", "Polish Grandma"): (
        "I miss you {recipient} 💛\n\n"
        "The house is too quiet without you. I keep cooking portions for one extra person. "
        "When are you visiting? I already froze your favorite food."
    ),
    ("Missing You", "Moroccan Grandma"): (
        "I miss you {recipient} 💛\n\n"
        "Every day I think — my {recipient_short} should be here for tea and stories. "
        "Come home soon. The mint is fresh and my arms are empty."
    ),
    ("Missing You", "Iraqi Grandma"): (
        "I miss you {recipient} 💛\n\n"
        "Distance is hard on an old heart. I pray for you every morning. "
        "Remember — no matter how far, you always have a home with me."
    ),
    ("Missing You", "Russian Grandma"): (
        "I miss you {recipient}.\n\n"
        "Come visit. I made your favorite food and saved your blanket. "
        "Don't make an old woman wait — time doesn't wait for anyone."
    ),
    ("Congratulations", "Polish Grandma"): (
        "Congratulations {recipient}! 🎉\n\n"
        "I'm so proud I could burst! But also — did you eat something to celebrate? "
        "Success means nothing on an empty stomach. Come, I'll make you a feast."
    ),
    ("Congratulations", "Moroccan Grandma"): (
        "Congratulations {recipient}! 🎊\n\n"
        "Mabrouk! I knew you could do it — you have fire in your soul. "
        "Tonight we celebrate with music, sweets, and the whole family!"
    ),
    ("Congratulations", "Iraqi Grandma"): (
        "Congratulations {recipient}! 🎉\n\n"
        "Baruch Hashem! My heart is overflowing with pride. "
        "You honor our family with every achievement. May God bless what's ahead."
    ),
    ("Congratulations", "Russian Grandma"): (
        "Congratulations {recipient}.\n\n"
        "I always knew you were capable. Hard work pays off — "
        "now come celebrate properly. I made enough food for everyone."
    ),
}


def format_recipient(recipient):
    mapping = {
        "Grandchildren": "my dear grandchildren",
        "Grandson": "my dear grandson",
        "Granddaughter": "my dear granddaughter",
        "Family": "my dear family",
        "Son": "my dear son",
        "Daughter": "my dear daughter",
    }
    return mapping.get(recipient, f"my dear {recipient.lower()}")


def format_recipient_short(recipient):
    mapping = {
        "Grandchildren": "grandchildren",
        "Grandson": "grandson",
        "Granddaughter": "granddaughter",
        "Family": "family",
        "Son": "son",
        "Daughter": "daughter",
    }
    return mapping.get(recipient, recipient.lower())


def generate_greeting(greeting_type, recipient, grandma_style):
    if greeting_type not in GREETING_TYPES:
        raise ValueError(f"Invalid greeting type: {greeting_type}")
    if recipient not in RECIPIENTS:
        raise ValueError(f"Invalid recipient: {recipient}")
    if grandma_style not in GRANDMA_STYLES:
        raise ValueError(f"Invalid grandma style: {grandma_style}")

    template = TEMPLATES.get((greeting_type, grandma_style))
    if template is None:
        raise ValueError(
            f"No template for {greeting_type} + {grandma_style}"
        )

    return template.format(
        recipient=format_recipient(recipient),
        recipient_short=format_recipient_short(recipient),
    )
