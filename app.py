from flask import Flask, request, redirect, render_template
from utils.shortener import generate_short_id
from datetime import datetime

app = Flask(__name__)

# Base de données simple en mémoire
links_db = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        if long_url:
            short_id = generate_short_id()
            links_db[short_id] = {
                "long_url": long_url,
                "clicks": 0,
                "history": []
            }
            short_url = request.host_url + short_id
            return render_template("index.html", short_url=short_url)
    return render_template("index.html")

@app.route('/<short_id>')
def redirect_short(short_id):
    link_data = links_db.get(short_id)
    if link_data:
        link_data["clicks"] += 1
        click_info = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": request.remote_addr,
            "user_agent": request.headers.get("User-Agent")
        }
        link_data["history"].append(click_info)
        return redirect(link_data["long_url"])
    return "Lien non trouvé", 404

@app.route('/stats/<short_id>')
def stats(short_id):
    link_data = links_db.get(short_id)
    if not link_data:
        return "Lien non trouvé", 404
    return render_template("stats.html", short_id=short_id, link_data=link_data)

if __name__ == "__main__":
    app.run(debug=True)
