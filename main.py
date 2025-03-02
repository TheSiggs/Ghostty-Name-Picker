from flask import request, url_for, redirect, session, jsonify
import flask
import securescaffold
from google.cloud import ndb
from models.Ghost import Ghost
from models.User import User
import csv
import random
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from authlib.integrations.flask_client import OAuth
import secrets
from starlette.responses import RedirectResponse


app = securescaffold.create_app(__name__)
client = ndb.Client()

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v2/",
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)
users = {}


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


@app.route("/login")
def login():
    nonce = secrets.token_urlsafe(16)
    session["nonce"] = nonce
    return google.authorize_redirect(
        url_for("authorize", _external=True),
        nonce=nonce
    )


@app.route("/authorize")
def authorize():
    nonce = session.pop("nonce", None)
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token, nonce)
    if not nonce:
        return "Nonce missing", 400  # Ensure nonce exists

    if user_info:
        user = User(user_info["sub"], user_info["name"], user_info["email"])
        users[user.id] = user
        login_user(user)
        return redirect(url_for("ghost_form"))

    return "Authorization Failed", 401


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/", methods=["GET"])
def index():
    with client.context():
        ghosts = Ghost.query().fetch()
        if current_user.is_authenticated:
            has_ghost = Ghost.query(Ghost.email == current_user.email).get()
        else:
            has_ghost = False

    context = {
        "ghosts": ghosts,
        "user": current_user if current_user.is_authenticated else None,
        "has_ghost": has_ghost,
    }
    return flask.render_template("index.html", **context)


@app.route("/ghostpicker", methods=["GET", "POST"])
@login_required
def ghost_form():
    with client.context():
        has_ghost = Ghost.query(Ghost.email == current_user.email).get()

    context = {
        "user": current_user.name if current_user.is_authenticated else None,
        "has_ghost": has_ghost,
    }
    return flask.render_template("ghost_form.html", **context)


@app.route("/generate_names", methods=["POST"])
def generate_names():
    with client.context():
        ghosts = Ghost.query(ndb.OR(Ghost.email == None, Ghost.email == "")).fetch()

        random_ghosts = random.sample(ghosts, min(3, len(ghosts)))
        context = {
            "ghosts": random_ghosts,
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "user": current_user.name if current_user.is_authenticated else None
        }
        print(random_ghosts)
        return flask.render_template("ghost_name_picker.html", **context)


@app.route("/confirm_name", methods=["POST"])
@login_required
def confirm_name():
    email = current_user.email
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    ghost_id = request.form.get("ghost_id")

    if not ghost_id:
        return "Invalid request: Missing ghost ID", 400

    with client.context():
        existing_ghost = Ghost.query(Ghost.email == email).get()
        if existing_ghost and existing_ghost.key.id() != int(ghost_id):
            existing_ghost.email = None
            existing_ghost.first_name = None
            existing_ghost.last_name = None
            existing_ghost.put()

        ghost_key = ndb.Key(Ghost, int(ghost_id))
        ghost = ghost_key.get()
        if ghost:
            ghost.first_name = first_name
            ghost.last_name = last_name
            ghost.email = email
            ghost.put()
            return redirect(url_for("index"))
        else:
            return "Couldn't find ghost", 404


def import_csv(filename):
    """Reads a CSV file and imports data into Google Cloud Datastore."""
    with client.context():
        keys = Ghost.query().fetch(keys_only=True)
        ndb.delete_multi(keys)
        with open(filename, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                email = None
                first_name = None
                last_name = None
                ghost_name = row.get("ghost_name", "").strip() or "Unknown"
                ghost_description = row.get("description", "").strip() or "Unknown"
                ghost = Ghost(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    ghost_name=ghost_name,
                    description=ghost_description,
                )
                ghost.put()
                print(f"Inserted: {ghost_name}")


if __name__ == "__main__":
    # import_csv("ghost_names.csv")
    app.run(debug=True)
