# Routes for user
from project import app, user, db
from project.models import Users
from flask import render_template, request, session, redirect, json, flash
# from werkzeug.utils import secure_filename
from functools import wraps
from base64 import b64encode, b64decode


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(f"/user/login?redirect={b64encode(request.path.encode()).decode()}")
        return f(*args, **kwargs)
    return decorated_function


@user.route("/")
@login_required
def user_page():
    return render_template("user.html")


@user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        redirect_path = request.args.get("redirect")
        if not redirect_path:
            redirect_path = "/admin"
        else:
            redirect_path = b64decode(redirect_path).decode()
        email = request.form.get("email")
        password = request.form.get("password")
        user = Users.query.filter_by(email=email).first()
        if user and user.verify(password):
            session["user_id"] = user.id
            return redirect("/user")
        flash("Incorrect Information!", "danger")
    return render_template("login_user.html", PAGE="LOGIN")


@user.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        
        address = request.form.get("address")

        city = request.form.get("city")
        postal_code = request.form.get("postal_code")
        phone = request.form.get("phone")
        password = request.form.get("password")
        if not Users.query.filter_by(email=email).first():
            user = Users(email=email, f_name=f_name, l_name=l_name, address=address, city=city, postal_code=postal_code, phone=phone)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account has been created!", "primary")
            return redirect("/user/login")

        flash("Account with this email already exist!", "warning")
    return render_template("login_user.html", PAGE="SIGNUP")


@user.route("/logout")
def logout():
    session.pop("user_id")
    return redirect("/")
