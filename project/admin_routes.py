# Routes for admin
from project import app, admin, db
from project.models import Products, Images, Orders, Cart, Admin
from project.get_dict import *
from flask import render_template, request, session, redirect, json, flash
from werkzeug.utils import secure_filename
from functools import wraps
from base64 import b64encode, b64decode
import os
from time import time


IMAGE_DIR = app.config['IMAGE_DIR']
PER_PAGE = app.config['PER_PAGE']


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin_id") is None:
            return redirect(f"/admin/login?redirect={b64encode(request.path.encode()).decode()}")
        return f(*args, **kwargs)
    return decorated_function


@admin.route("/admin")
@login_required
def index():
    return render_template("index.html")


@admin.route("/admin/products")
@admin.route("/admin/products/<int:page>")
@login_required
def get_products(page=1):
    products = Products.query.paginate(page=page, per_page=PER_PAGE)

    images = get_images(products.items)
    images = [i[0] for i in images]

    return render_template("products.html", TITLE="ADMIN", products=products, images=images)


def set_images(product_id, form, primary, secondary):
    img_ids = []
    for i in range(4):
        img_name = f"img_id{i}"
        img_id = form.get(img_name)
        if img_id:
            image = Images.query.get(img_id)
            if image:
                image.product_id = product_id
                image.order = None
                img_ids.append(image)

    if img_ids:
        primary = 0 if primary > len(img_ids)-1 else primary
        secondary = 0 if secondary > len(img_ids)-1 else secondary

        img_ids[primary].order = 0
        img_ids[secondary].order = 1

        x = 2
        for img in img_ids:
            if img.order is None:
                img.order = x
                x += 1

        db.session.commit()


@admin.route("/admin/new_product", methods=["GET", "POST"])
@login_required
def new_product():
    if request.method == "POST":
        title = request.form.get("title")
        category = request.form.get("category")
        details = request.form.get("details")
        price = request.form.get("price")
        primary = 0 if not request.form.get("primary") else request.form.get("primary")
        secondary = 0 if not request.form.get("secondary") else request.form.get("secondary")
        core_collection = True if request.form.get("core_collection") else False

        product = Products(title=title, category=category, details=details, price=price, core_collection=core_collection)
        db.session.add(product)
        db.session.commit()

        set_images(product.id, request.form, int(primary), int(secondary))

    return render_template("new_product.html", time=time)


@admin.route("/admin/delete/product/<int:ID>")
@login_required
def delete_product(ID):
    product = Products.query.get(ID)
    if product:
        db.session.delete(product)
        images = Images.query.filter_by(product_id=ID).all()
        for img in images:
            img.product_id = None
    db.session.commit()
    return redirect("/admin/products")


@admin.route("/admin/update/product/<int:ID>", methods=["GET", "POST"])
@login_required
def update_product(ID):
    product = Products.query.get(ID)
    images = Images.query.filter_by(product_id=ID)
    if request.method == "POST":
        title = request.form.get("title")
        category = request.form.get("category")
        details = request.form.get("details")
        price = request.form.get("price")
        primary = 0 if not request.form.get("primary") else request.form.get("primary")
        secondary = 0 if not request.form.get("secondary") else request.form.get("secondary")
        core_collection = True if request.form.get("core_collection") else False

        product.title = title
        product.category = category
        product.details = details
        product.price = price
        product.core_collection = core_collection

        for i in images:
            i.product_id = None
        db.session.commit()

        set_images(ID, request.form, int(primary), int(secondary))

    images = Images.query.filter_by(product_id=ID)
    images = get_images_dict(images)
    return render_template("update_product.html", product=product, images=images)


@admin.route("/admin/images")
@admin.route("/admin/images/<int:page>")
@login_required
def images(page=1):
    images = Images.query.paginate(page=page, per_page=PER_PAGE)
    return render_template("images.html", images=images)


@admin.route("/admin/delete/image/<int:ID>")
@login_required
def delete_image(ID):
    image = Images.query.get(ID)
    if image:
        file = os.path.join(IMAGE_DIR, image.filename)
        if os.path.isfile(file):
            os.remove(file)
        else:
            print(file, "IMG NOT FOUND DEL")
        db.session.delete(image)
        db.session.commit()
    return redirect("/admin/images")


@admin.route("/admin/new_image", methods=["GET", "POST"])
@login_required
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

    return render_template("new_image.html", time=time)


@admin.route("/admin/fetch/images", methods=["POST"])
@login_required
def admin_images_fetch():
    search = request.form.get("search")
    images = Images.query.filter(Images.title.like(f"%{search}%"), Images.product_id==None).all()
    images = get_images_dict(images)
    return json.jsonify(images)


@admin.route("/admin/orders")
@admin.route("/admin/orders/<int:page>")
@login_required
def orders(page=1):
    orders = Orders.query.paginate(page=page, per_page=PER_PAGE)
    orders_dict = get_orders_dict(orders.items)
    cart = Cart.query.filter(Cart.order_id.in_((list(orders_dict.keys())))).all()

    cart_dict = get_cart_dict(cart)
    for i in orders_dict:
        items = [] if not cart_dict.get(i) else cart_dict.get(i) # use empty list if cart does not have any item of currect order
        orders_dict[i]['items'] = items

    products_id = []
    for prd in cart:
        products_id.append(prd.product_id)
    
    images = get_cart_images(cart)
    return render_template("orders.html", orders=orders, images_json=images, orders_json=orders_dict, TITLE="ORDERS")


@admin.route("/admin/order/mark/<int:ID>/<int:page>")
@login_required
def mark_order(ID, page):
    order = Orders.query.get(ID)
    if order:
        order.status = not order.status
        db.session.commit()
    return redirect(f"/admin/orders/{page}")


@admin.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        redirect_path = request.args.get("redirect")
        if not redirect_path:
            redirect_path = "/admin"
        else:
            redirect_path = b64decode(redirect_path).decode()
        uname = request.form["uname"]
        password = request.form["password"]
        user = Admin.query.filter_by(username=uname).first()
        if user and user.verify(password):
            session['admin_id'] = user.id
            session['admin_uname'] = user.username
            return redirect(redirect_path)
        flash("Incorrect information", "danger")
    return render_template("login.html")


@admin.route("/admin/logout")
@login_required
def logout():
    session.pop('admin_id')
    session.pop('admin_uname')
    return redirect("/admin/login")