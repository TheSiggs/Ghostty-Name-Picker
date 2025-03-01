import flask
import securescaffold


app = securescaffold.create_app(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Demonstration of using CSRF to protect a form."""
    context = {
        "page_title": "CSRF protection",
        "message": "",
    }

    if flask.request.method == "POST":
        first_name = flask.request.form.get("first-name")

        if first_name:
            context["message"] = f"Hello {first_name}!"

    return flask.render_template("index.html", **context)
