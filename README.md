# מחולל ברכות סבתא / Grandma Greeting Generator

אפליקציית ווב ליצירת ברכות מצחיקות ואישיות בסגנונות סבתא שונים, עם גיף תואם. פרויקט גמר לקורס **מחשוב ושירותי ענן מנוהלים**.

האפליקציה פשוטה בכוונה — המטרה העיקרית היא להדגים מיומנויות תשתית ענן (AWS, Terraform, זמינות גבוהה), לא מורכבות אפליקטיבית.

## סטטוס פרויקט

| שלב | סטטוס |
|-----|--------|
| **Phase 1** — פיתוח מקומי (Flask + SQLite) | **הושלם** (יוני 2026) |
| **Phase 2** — הכנת תשתית Terraform (קוד בלבד) | **הושלם** (יוני 2026) |
| **Phase 3** — יצירת RDS ואינטגרציה | **נדחה** (כמה ימים לפני ההגשה) |
| **פריסה סופית** — `terraform apply` + EC2 + הדגמת HA | **ממתין** |

אין משאבי AWS פעילים כרגע — לא הורץ `terraform apply`, לא נוצר RDS, ואין עלויות AWS.

**ריפו:** https://github.com/Shaharmayster/Shahar_Daniel_AWSAPP

לדרישות מלאות, ראו [PROJECT.md](PROJECT.md). להנחיות Terraform, ראו [terraform/README.md](terraform/README.md).

---

## מה האפליקציה עושה

1. המשתמשת בוחרת **סוג ברכה**, **נמען** ו**סגנון סבתא**
2. המערכת מייצרת ברכה בעברית מתבניות Python מוגדרות מראש
3. המערכת מציגה גיף סטטי עם איור סבתא וכיתוב בעברית
4. הברכה נשמרת במסד הנתונים (SQLite מקומית, RDS בפרודקשן)

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
└── terraform/              # Phase 2 — קוד Terraform מוכן
    ├── provider.tf
    ├── variables.tf
    ├── networking.tf
    ├── security.tf
    ├── alb.tf
    ├── launch_template.tf
    ├── asg.tf
    ├── outputs.tf
    ├── terraform.tfvars.example
    └── README.md
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

## טכנולוגיות

| שכבה | טכנולוגיה |
|------|-----------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, Jinja (RTL, עברית) |
| Database (Phase 1 — מקומי) | SQLite |
| Database (Phase 3+ — פרודקשן) | RDS MySQL (ידני, דרך `DATABASE_URL`) |
| תשתית | Terraform (קוד מוכן ב-`terraform/`, לא נפרס עדיין) |

---

## הגדרות

| משתנה | ברירת מחדל | תיאור |
|--------|------------|--------|
| `DATABASE_URL` | `sqlite:///local.db` | מחרוזת חיבור למסד נתונים |

### מעבר ל-RDS (Phase 3)

הקוד ב-`backend/database.py` כבר תומך ב-MySQL. ב-Phase 3:

```bash
cp .env.example .env
# ערכי .env:
# DATABASE_URL=mysql://USER:PASSWORD@RDS_ENDPOINT:3306/DATABASE_NAME
./RUN.SH
```

מעבר חזרה ל-SQLite: `DATABASE_URL=sqlite:///local.db`

---

## שלבים הבאים

- **Phase 3:** יצירת RDS ידנית, חיבור `DATABASE_URL`, בדיקת read/write
- **שבוע ההגשה:** `terraform apply`, פריסת Flask על EC2, הדגמת HA (כיבוי instance)
- פירוט מלא: [terraform/README.md](terraform/README.md) ו-[PROJECT.md](PROJECT.md)

---

## קורס

**מחשוב ושירותי ענן מנוהלים**

ארכיטקטורת יעד (פריסה סופית):

```
Browser → ELB → ASG → EC2 (×2) → RDS
```

---

## סיכום מהיר

| שאלה | תשובה |
|------|--------|
| משהו רץ ועולה כסף? | לא — רק קוד מקומי |
| Terraform — מה צריך? | AWS account + Access Key + Secret Key + `aws configure` + Terraform |
| RDS — מה צריך? | יצירה ידנית + endpoint / user / password / db name + `DATABASE_URL` על EC2 |
| מתי מתחילים לשלם? | אחרי `terraform apply` (~$30–35/חודש) + RDS (~$15–20/חודש נוסף) |

---

## Checklist ליום ההגשה

1. `terraform init` → `plan` → `apply`
2. יצירת/חיבור RDS + הגדרת `DATABASE_URL` על EC2
3. פריסת Flask על שני ה-instances (פורט 5000)
4. גישה לאפליקציה דרך DNS של ה-ALB
5. יצירת ברכה — אימות כתיבה ל-RDS
6. כיבוי EC2 instance אחד — אימות שהאפליקציה ממשיכה לעבוד
7. `terraform destroy` אחרי סיום (לחיסכון בעלויות)
