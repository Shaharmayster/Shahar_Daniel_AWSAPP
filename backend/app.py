from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

from config import GRANDMA_STYLES, GREETING_TYPES, RECIPIENTS
from database import get_recent_greetings, init_db, save_greeting
from gif_selector import get_gif_path
from greeting_generator import generate_greeting

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = Flask(
    __name__,
    template_folder=str(FRONTEND_DIR / "templates"),
    static_folder=str(FRONTEND_DIR / "static"),
)
app.secret_key = "dev-only-change-in-production"


@app.route("/")
def index():
    return render_template(
        "index.html",
        greeting_types=GREETING_TYPES,
        recipients=RECIPIENTS,
        grandma_styles=GRANDMA_STYLES,
        greetings=get_recent_greetings(),
        get_gif_path=get_gif_path,
    )


@app.route("/generate", methods=["POST"])
def generate():
    greeting_type = request.form.get("greeting_type", "")
    recipient = request.form.get("recipient", "")
    grandma_style = request.form.get("grandma_style", "")

    if (
        greeting_type not in GREETING_TYPES
        or recipient not in RECIPIENTS
        or grandma_style not in GRANDMA_STYLES
    ):
        flash("יש לבחור סוג ברכה, נמען וסגנון סבתא תקינים.")
        return redirect(url_for("index"))

    try:
        generated_text = generate_greeting(greeting_type, recipient, grandma_style)
        save_greeting(greeting_type, recipient, grandma_style, generated_text)
        flash(generated_text, "greeting")
        flash(get_gif_path(greeting_type), "gif")
    except ValueError as exc:
        flash(str(exc))

    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
