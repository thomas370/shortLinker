from flask import Flask, request, redirect, render_template
from utils.shortener import generate_short_id
from utils.db import db, cursor
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        if long_url:
            short_id = generate_short_id()
            # Insérer le lien dans MySQL
            cursor.execute("INSERT INTO links (short_id, long_url) VALUES (%s, %s)", (short_id, long_url))
            db.commit()
            short_url = request.host_url + short_id
            return render_template("index.html", short_url=short_url)
    return render_template("index.html")

@app.route('/<short_id>')
def redirect_short(short_id):
    cursor.execute("SELECT * FROM links WHERE short_id=%s", (short_id,))
    link_data = cursor.fetchone()
    if link_data:
        # Ajouter un clic
        cursor.execute(
            "INSERT INTO clicks (link_id, ip, user_agent) VALUES (%s,%s,%s)",
            (link_data['id'], request.remote_addr, request.headers.get("User-Agent"))
        )
        cursor.execute("UPDATE links SET clicks = clicks + 1 WHERE id=%s", (link_data['id'],))
        db.commit()
        return redirect(link_data['long_url'])
    return "Lien non trouvé", 404

@app.route('/stats/<short_id>')
def stats(short_id):
    cursor.execute("SELECT * FROM links WHERE short_id=%s", (short_id,))
    link_data = cursor.fetchone()
    if not link_data:
        return "Lien non trouvé", 404
    cursor.execute("SELECT * FROM clicks WHERE link_id=%s ORDER BY click_time DESC", (link_data['id'],))
    clicks = cursor.fetchall()
    return render_template("stats.html", short_id=short_id, link_data=link_data, clicks=clicks)

if __name__ == "__main__":
    app.run(debug=True)
