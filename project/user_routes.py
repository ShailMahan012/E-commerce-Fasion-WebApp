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
    user_id = session.get("user_id")
    user = db.session.get(Users, user_id)
    if user:
        return render_template("user.html", TITLE="Grabalty | User", user=user)
    flash("User not found!", "danger")
    return redirect("/user/logout")


@user.route("/update_info", methods=["POST"])
@login_required
def update_info():
    user_id = session.get("user_id")
    user = db.session.get(Users, user_id)
    if user:
        email = request.form.get("email")
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        
        address = request.form.get("address")

        city = request.form.get("city")
        country = request.form.get("country")
        postal_code = request.form.get("postal_code")
        phone = request.form.get("phone")

        user.email = email
        user.f_name = f_name
        user.l_name = l_name
        user.address = address
        user.city = city
        user.country = country
        user.postal_code = postal_code
        user.phone = phone
        db.session.commit()
        flash("User Information has been updated!", "primary")
        return redirect("/user")
    flash("User not found!", "danger")
    return redirect("/user/logout")


@user.route("/track_order", methods=["GET", "POST"])
@login_required
def track_order():
    if request.method == "POST":
        email = request.form["email"]
        invoice = request.form["invoice"]
        if len(invoice) > 4:
            invoice = invoice[4:]
            flash("Order not found", "danger")
        else:
            flash("Invalid invoice number", "danger")
    return render_template("track_order.html", TITLE="Grabalty | Track Order")


@user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        redirect_path = request.args.get("redirect")
        if not redirect_path:
            redirect_path = "/user"
        else:
            redirect_path = b64decode(redirect_path).decode()
        email = request.form.get("email")
        password = request.form.get("password")
        user = Users.query.filter_by(email=email).first()
        if user and user.verify(password):
            session["user_id"] = user.id
            return redirect(redirect_path)
        flash("Incorrect Information!", "danger")
    return render_template("login_user.html", PAGE="Grabalty | LOGIN")


@user.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        
        address = request.form.get("address")

        city = request.form.get("city")
        country = request.form.get("country")
        postal_code = request.form.get("postal_code")
        phone = request.form.get("phone")
        password = request.form.get("password")
        if not Users.query.filter_by(email=email).first():
            user = Users(email=email, f_name=f_name, l_name=l_name, address=address, city=city, country=country, postal_code=postal_code, phone=phone)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account has been created!", "primary")
            return redirect("/user/login")

        flash("Account with this email already exist!", "warning")
    return render_template("login_user.html", PAGE="Grabalty | SIGNUP")


@user.route("/logout")
def logout():
    session.pop("user_id")
    return redirect("/user/login")
