from flask import redirect, request
import flask
import securescaffold
from google.cloud import ndb
from models.Ghost import Ghost
import csv
import random


app = securescaffold.create_app(__name__)
client = ndb.Client()


@app.route("/", methods=["GET"])
def index():
    with client.context():
        ghosts = Ghost.query().fetch()
    return flask.render_template("index.html", ghosts=ghosts)


@app.route("/ghostpicker", methods=["GET", "POST"])
def ghost_form():
    context = {"page_title": "CSRF protection", "message": ""}
    if flask.request.method == "POST":
        first_name = flask.request.form.get("first-name")
        if first_name:
            context["message"] = f"Hello {first_name}!"
    return flask.render_template("ghost_form.html", **context)


@app.route("/generate_names", methods=["POST"])
def generate_names():
    with client.context():
        ghosts = Ghost.query(ndb.OR(Ghost.email == None, Ghost.email == "")).fetch()

    random_ghosts = random.sample(ghosts, min(3, len(ghosts)))
    ghost_names = [ghost.ghost_name for ghost in random_ghosts]
    print(request.form)
    context = {
        "ghost_names": ghost_names,
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
    }
    return flask.render_template("ghost_name_picker.html", **context)


@app.route("/confirm_name", methods=["POST"])
def confirm_name():
    email = ""
    first_name = request.form.get("first_name"),
    last_name = request.form.get("last_name"),
    ghost_name = request.form.get("ghost_name")
    return index()


def import_csv(filename):
    """Reads a CSV file and imports data into Google Cloud Datastore."""
    with client.context():
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
    app.run(debug=True)
