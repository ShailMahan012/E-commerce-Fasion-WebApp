from flask import render_template, request, session, redirect, send_file
from functools import wraps
from project import app, db
from project.models import Users, Products, Images
from werkzeug.utils import secure_filename
from time import time

db.create_all()

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


@app.route("/items")
def items():
    return render_template("items.html", TITLE=TITLE)


@app.route("/product/<int:id>")
def product(id):
    # print(f"PRODUCT: {id}")
    return render_template("product.html", TITLE=TITLE)


# @app.route("/static/products/<src>")
# def product_src(src):
#     sleep(4)
#     return send_file(f"static/products/{src}")


@app.route("/cart")
def cart():
    return render_template("cart.html", TITLE="YOUR CART")


@app.route("/checkout")
def checkout():
    return render_template("checkout.html", TITLE="CHECKOUT HERE")


@app.route("/admin")
def admin():
    return render_template("admin/products.html")


@app.route("/new_product", methods=["GET", "POST"])
def new_product():
    if request.method == "POST":
        title = request.form.get("title")
        details = request.form.get("details")
        primary = 0 if not request.form.get("primary") else request.form.get("primary")
        secondary = 0 if not request.form.get("secondary") else request.form.get("secondary")
        core_collection = True if request.form.get("core_collection") else False

        product = Products(title=title, details=details, primary=primary, secondary=secondary, core_collection=core_collection)
        db.session.add(product)
        db.session.commit()

        # images = []
        # for i in request.files:
        #     file = request.files.get(i)
        #     if file.filename:
        #         images.append(file)

    # Images(product_id=product.id)
    return render_template("admin/new_product.html", time=time)


@app.route("/logout")
def logout():
    return redirect("/new_product")

