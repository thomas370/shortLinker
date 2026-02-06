from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from utils.shortener import generate_short_id
from utils.db import cursor, db

links_bp = Blueprint("links", __name__)

@links_bp.route("/", methods=["GET","POST"])
@login_required
def index():
    if request.method == "POST":
        short_id = generate_short_id()
        cursor.execute(
            "INSERT INTO links (user_id, short_id, long_url) VALUES (%s,%s,%s)",
            (current_user.id, short_id, request.form["long_url"])
        )
        db.commit()
        return render_template("links/index.html", short_id=short_id)

    return render_template("links/index.html")


@links_bp.route("/<short_id>")
def redirect_short(short_id):
    cursor.execute("SELECT * FROM links WHERE short_id=%s", (short_id,))
    link = cursor.fetchone()
    if not link:
        return "Not found", 404

    cursor.execute(
        "UPDATE links SET clicks = clicks + 1 WHERE id=%s",
        (link["id"],)
    )
    db.commit()
    return redirect(link["long_url"])

