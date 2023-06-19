from flask import render_template, request, session, redirect, send_file
from functools import wraps
from project import app, db
from project.models import Users, Products, Images
from werkzeug.utils import secure_filename
import os
from time import time

db.create_all()

TITLE = "Fashion"
IMAGE_DIR = 'project/static/product_images'

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
    products = Products.query.all()
    images = []
    for prd in products:
        product_id = prd.id
        primary = prd.primary
        prd_images = Images.query.filter_by(product_id=product_id).all()
        if (len(prd_images) <= 0) or len(prd_images) - 1 < primary:
            images.append("None")
        else:
            images.append(prd_images[primary].filename)
    return render_template("admin/products.html", products=products, images=images)


@app.route("/admin/new_image", methods=["GET", "POST"])
def new_image():
    if request.method == "POST":
        title = request.form.get("title")
        for i in request.files:
            file = request.files.get(i)
            filename = file.filename
            if filename:
                filename = str(time()) + secure_filename(filename)
                path = os.path.join(IMAGE_DIR, filename)
                file.save(path)

                image = Images(title=title, filename=filename)
                db.session.add(image)
        db.session.commit()


    return render_template("admin/new_image.html", time=time)


@app.route("/admin/new_product", methods=["GET", "POST"])
def new_product():
    if request.method == "POST":
        title = request.form.get("title")
        details = request.form.get("details")
        price = request.form.get("price")
        primary = 0 if not request.form.get("primary") else request.form.get("primary")
        secondary = 0 if not request.form.get("secondary") else request.form.get("secondary")
        core_collection = True if request.form.get("core_collection") else False

        product = Products(title=title, details=details, price=price, primary=primary, secondary=secondary, core_collection=core_collection)
        db.session.add(product)
        db.session.commit()

        for i in request.files:
            file = request.files.get(i)
            filename = file.filename
            if filename:
                filename = str(time()) + secure_filename(filename)
                path = os.path.join(IMAGE_DIR, filename)
                file.save(path)

                image = Images(product_id=product.id, filename=filename)
                db.session.add(image)

        db.session.commit()
    return render_template("admin/new_product.html", time=time)


@app.route("/admin/delete/product/<int:ID>")
def delete_product(ID):
    product = Products.query.get(ID)
    if product:
        db.session.delete(product)
        images = Images.query.filter_by(product_id=ID).all()
        for img in images:
            file = os.path.join(IMAGE_DIR, img.filename)
            if os.path.isfile(file):
                os.remove(file)
            else:
                print(file, "IMG NOT FOUND DEL")
            db.session.delete(img)
    db.session.commit()
    return redirect("/admin")


@app.route("/admin/update/product/<int:ID>", methods=["GET", "POST"])
def update_product(ID):
    product = Products.query.get(ID)
    return render_template("admin/update_product.html", product=product)


@app.route("/logout")
def logout():
    return redirect("/new_product")

