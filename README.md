# מחולל ברכות סבתא / Grandma Greeting Generator

אפליקציית ווב ליצירת ברכות מצחיקות ואישיות בסגנונות סבתא שונים, עם גיף תואם. פרויקט גמר לקורס **מחשוב ושירותי ענן מנוהלים**.

האפליקציה פשוטה בכוונה — המטרה העיקרית היא להדגים מיומנויות תשתית ענן (AWS, Terraform, זמינות גבוהה), לא מורכבות אפליקטיבית.

## סטטוס פרויקט

| שלב | סטטוס |
|-----|--------|
| **Phase 1** — פיתוח מקומי | **הושלם** (יוני 2026) |
| **Phase 2** — מעבר ל-RDS | **הושלם** (קוד מוכן — ממתין לפרטי RDS מהמרצה) |
| Phase 3 — פריסה ב-AWS | לא התחיל |

**ריפו:** https://github.com/Shaharmayster/Shahar_Daniel_AWSAPP

לדרישות מלאות, ראו [PROJECT.md](PROJECT.md).

---

## מה האפליקציה עושה

1. המשתמשת בוחרת **סוג ברכה**, **נמען** ו**סגנון סבתא**
2. המערכת מייצרת ברכה בעברית מתבניות Python מוגדרות מראש
3. המערכת מציגה גיף סטטי עם איור סבתא וכיתוב בעברית
4. הברכה נשמרת במסד הנתונים (SQLite או RDS)

### דוגמה

| שדה | ערך |
|-----|-----|
| סוג ברכה | שבת שלום |
| נמען | נכדים |
| סגנון סבתא | סבתא פולניה |

**פלט:**

> שבת שלום נכדים שלי היקרים ❤️
>
> אכלתם היום משהו? אתם נראים רזים מדי בתמונה האחרונה.

+ גיף `polish_shabbat.gif` (סבתא פולנית + כיתוב "שבת שלום")

---

## הרצה מקומית

### דרישות

- Python 3

### הרצה מהירה

משורש הפרויקט:

```bash
./RUN.SH
```

ואז לפתוח [http://127.0.0.1:5000](http://127.0.0.1:5000)

### הרצה ידנית

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

---

## מבנה הפרויקט

```
├── PROJECT.md              # מפרט מלא (source of truth)
├── .env.example            # תבנית DATABASE_URL ל-RDS
├── README.md
├── RUN.SH                  # סקריפט הרצה מקומית
├── backend/                # Flask + Python
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── greeting_generator.py
│   ├── gif_selector.py
│   └── requirements.txt
├── frontend/               # HTML, CSS, Jinja
│   ├── templates/
│   └── static/
│       ├── css/
│       └── gifs/           # 21 גיפים סטטיים
├── scripts/
│   └── generate_gifs.py    # יצירת גיפים (dev only)
└── terraform/              # Phase 3 — לא מומש
```

---

## גיפים

20 גיפים סטטיים (4 סגנונות סבתא × 5 סוגי ברכה) + `default.gif`:

| סגנון סבתא | סוג ברכה | קובץ |
|------------|----------|------|
| סבתא פולניה | שבת שלום | `polish_shabbat.gif` |
| סבתא מרוקאית | מזל טוב | `moroccan_birthday.gif` |
| סבתא עיראקית | חג שמח | `iraqi_holiday.gif` |
| סבתא רוסיה | מתגעגעת אליכם | `russian_miss_you.gif` |

הגיף נבחר לפי **סגנון סבתא + סוג ברכה**. לא נשמר במסד הנתונים.

---

## טכנולוגיות (Phase 1)

| שכבה | טכנולוגיה |
|------|-----------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, Jinja (RTL, עברית) |
| Database (Phase 1) | SQLite (ברירת מחדל) |
| Database (Phase 2+) | RDS MySQL (דרך `DATABASE_URL`) |

---

## הגדרות

| משתנה | ברירת מחדל | תיאור |
|--------|------------|--------|
| `DATABASE_URL` | `sqlite:///local.db` | מחרוזת חיבור למסד נתונים |

### מעבר ל-RDS (Phase 2)

```bash
cp .env.example .env
# ערכי .env:
# DATABASE_URL=mysql://USER:PASSWORD@RDS_ENDPOINT:3306/DATABASE_NAME
./RUN.SH
```

מעבר חזרה ל-SQLite: `DATABASE_URL=sqlite:///local.db`

---

## שלבים הבאים

- **Phase 3:** פריסה ב-AWS עם Terraform (VPC, EC2, ELB, ASG)
- **RDS:** כשיתקבלו פרטים מהמרצה — הגדר `DATABASE_URL` ב-`.env` ובדוק חיבור

---

## קורס

**מחשוב ושירותי ענן מנוהלים**

ארכיטקטורת יעד (Phase 3):

```
Browser → ELB → ASG → EC2 (×2) → RDS
```
