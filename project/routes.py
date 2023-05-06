from flask import render_template, request, session, redirect
from functools import wraps
from project import app, db
from project.models import Users

# db.create_all()

TITLE = "Fashion"

def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
                if session.get("id") is None:
                        return redirect("/login")
                return f(*args, **kwargs)
        return decorated_function


@app.route("/")
def index():
    return render_template("home.html", TITLE=TITLE)
