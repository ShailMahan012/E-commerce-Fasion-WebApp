from flask import render_template, request, session, redirect, send_file
from functools import wraps
from project import app, db
from project.models import Users
from time import sleep

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


@app.route("/items")
def items():
       return render_template("items.html", TITLE=TITLE)


@app.route("/product/<int:id>")
def product(id):
        # print(f"PRODUCT: {id}")
        return render_template("product.html", TITLE=TITLE)

# @app.route("/static/products/<src>")
# def product_src(src):
#         sleep(4)
#         return send_file(f"static/products/{src}")


@app.route("/cart")
def cart():
       return render_template("cart.html", TITLE="YOUR CART")


@app.route("/checkout")
def checkout():
       return render_template("checkout.html", TITLE="CHECKOUT HERE")
