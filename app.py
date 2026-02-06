from flask import Flask
from flask_login import LoginManager
from utils.db import db
from auth.routes import auth_bp
from links.routes import links_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

app.register_blueprint(auth_bp)
app.register_blueprint(links_bp)

if __name__ == "__main__":
    app.run(debug=True)
