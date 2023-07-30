from flask import render_template, request, session, redirect, send_file, json, Markup
from functools import wraps
from project import app, db
from project.models import Users, Products, Images, Orders, Cart
from werkzeug.utils import secure_filename
import os
from time import time

db.create_all()

TITLE = "Fashion"
IMAGE_DIR = 'project/static/product_images'
PER_PAGE = 15

# take a list and return list of unique items
def unique(lst):
    unique_lst = []
    for i in lst:
        if i not in unique_lst:
            unique_lst.append(i)
    return unique_lst


# take products as list and return list of images in 2d list with first two indexes of primary and secondary images for each product
def get_images(products):
    images_list = [] # 2d array to store images of all products
    for i in products:
        product_id = i.id
        images = Images.query.with_entities(Images.filename).filter_by(product_id=product_id).order_by("order").all()
        images = [i[0] for i in images] # save only first item of each row since we only need filename of images
        if not images:
            images.append(None)
        images_list.append(images)
    return images_list


def get_images_data(products):
    images_dict = {}
    for prd in products:
        product_id = prd.id
        images = Images.query.filter_by(product_id=product_id).order_by("order").all()
        images_list = []
        for img in images:
            image = {
                'id': img.id,
                'filename': img.filename
            }
            images_list.append(image)
        images_dict[product_id] = images_list
    return images_dict


def get_product_dict(products):
    products_dict = []
    for prd in products:
        product = {
            'id': prd.id,
            'title': prd.title,
            'category': prd.category,
            'price': prd.price,
            'details': prd.details,
            'core_collection': prd.core_collection,
        }
        products_dict.append(product)
    return products_dict


# just get products as dictionary but not as array
def get_product_dict_id(products):
    products_dict = {}
    for prd in products:
        product = {
            'title': prd.title,
            'price': prd.price,
            'category': prd.category,
        }
        products_dict[prd.id] = product
    return products_dict


def get_images_dict(images):
    images_dict = []
    for img in images:
        image = {
            'id': img.id,
            'title': img.title,
            'filename': img.filename,
        }
        images_dict.append(image)
    return images_dict


def get_orders_dict(orders):
    orders_dict = {}
    for o in orders:
        order = {
            'f_name': o.f_name,
            'l_name': o.l_name,
            'address': o.address,
            'city': o.city,
            'postal_code': o.postal_code,
            'phone': o.phone,
            'note': o.note,
            'status': o.status
        }
        orders_dict[o.id] = order
    return orders_dict


def get_cart_dict(cart):
    cart_dict = {}
    for i in cart:
        if not cart_dict.get(i.order_id):
            cart_dict[i.order_id] = []
        item = {
            'product': i.product_id,
            'quantity': i.quantity
        }
        cart_dict[i.order_id].append(item)
    return cart_dict


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    core_collection = Products.query.filter_by(core_collection=True).limit(13)
    images = get_images(core_collection)
    return render_template("home.html", TITLE=TITLE, core_collection=core_collection, images=images)


@app.route("/items")
def items():
    return render_template("items.html", TITLE=TITLE)


@app.route("/search")
@app.route("/search/<int:page>")
def search(page=1):
    search = request.args.get('search_input')
    if not search:
        search = ""
    products = Products.query.filter(Products.title.like(f"%{search}%"))
    count = products.count()

    products = products.paginate(page=page, per_page=PER_PAGE)
    images = get_images(products.items)

    return render_template("items.html", TITLE=TITLE, products=products, images=images, search=search, count=count, page_name="search")


@app.route("/core_collection")
@app.route("/core_collection/<int:page>", methods=["GET"])
def core_collection(page=1):
    products = Products.query.filter_by(core_collection=True)
    count = products.count()

    products = products.paginate(page=page, per_page=PER_PAGE)
    images = get_images(products.items)
    return render_template("items.html", TITLE=TITLE, products=products, images=images, count=count, page_name="core_collection")


@app.route("/product/<int:id>")
def product(id):
    product = Products.query.get(id)
    if product:
        images = get_images([product]) # get_images accept list of prodoucts
        if images: images = images[0] # save only first item because we only gave one product (2d list to 1d list)
        return render_template("product.html", TITLE=TITLE, product=product, images=images, Markup=Markup)
    return redirect("/")


# @app.route("/static/products/<src>")
# def product_src(src):
#     sleep(4)
#     return send_file(f"static/products/{src}")


@app.route("/cart")
def cart():
    return render_template("cart.html", TITLE="YOUR CART")


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        email = request.form.get("email")
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        
        address = request.form.get("address")

        city = request.form.get("city")
        postal_code = request.form.get("postal_code")
        phone = request.form.get("phone")

        products = json.loads(request.form.get("products"))

        if products:
            order = Orders(email=email, f_name=f_name, l_name=l_name, address=address, city=city, postal_code=postal_code, phone=phone)
            db.session.add(order)

            for prd in products:
                ID = prd.get("id")
                quantity = prd.get("quantity")
                if Products.query.get(ID) and quantity:
                    item = Cart(order_id=order.id, product_id=ID, quantity=quantity)
                    db.session.add(item)

            db.session.commit()
            return "True"

        return "False"
    return render_template("checkout.html", TITLE="CHECKOUT HERE")


@app.route("/admin")
def admin():
    return render_template("admin/index.html")


@app.route("/admin/products")
@app.route("/admin/products/<int:page>")
def get_products(page=1):
    products = Products.query.paginate(page=page, per_page=PER_PAGE)

    images = get_images(products.items)
    images = [i[0] for i in images]

    return render_template("admin/products.html", TITLE="ADMIN", products=products, images=images)


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


@app.route("/admin/new_product", methods=["GET", "POST"])
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

    return render_template("admin/new_product.html", time=time)


@app.route("/admin/delete/product/<int:ID>")
def delete_product(ID):
    product = Products.query.get(ID)
    if product:
        db.session.delete(product)
        images = Images.query.filter_by(product_id=ID).all()
        for img in images:
            img.product_id = None
    db.session.commit()
    return redirect("/admin/products")


@app.route("/admin/update/product/<int:ID>", methods=["GET", "POST"])
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
    return render_template("admin/update_product.html", product=product, images=images)


@app.route("/fetch/products", methods=["POST"])
def fetch_products():
    products_id = request.form.get("id")
    try:
        products_id = json.loads(products_id)
        products = Products.query.filter(Products.id.in_((products_id))).all()
        images = [x[0] for x in get_images(products)]
        products = get_product_dict(products)
        for i in range(len(products)):
            products[i]['img'] = images[i]
        return json.jsonify(products)
    except ValueError:
        print("fetch_products: JSON Decode ERROR")
        return "fetch_products: JSON Decode ERROR", 501
    return 'fetch_products: This message should not be received', 501


@app.route("/admin/images")
@app.route("/admin/images/<int:page>")
def images(page=1):
    images = Images.query.paginate(page=page, per_page=PER_PAGE)
    return render_template("admin/images.html", images=images)


@app.route("/admin/delete/image/<int:ID>")
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


@app.route("/admin/fetch/images", methods=["POST"])
def admin_images_fetch():
    search = request.form.get("search")
    images = Images.query.filter(Images.title.like(f"%{search}%"), Images.product_id==None).all()
    images = get_images_dict(images)
    return json.jsonify(images)


@app.route("/admin/orders")
@app.route("/admin/orders/<int:page>")
def orders(page=1):
    orders = Orders.query.paginate(page=page, per_page=6)
    orders_dict = get_orders_dict(orders.items)
    cart = Cart.query.filter(Cart.order_id.in_((list(orders_dict.keys())))).all()

    cart_dict = get_cart_dict(cart)
    for i in orders_dict:
        items = [] if not cart_dict.get(i) else cart_dict.get(i)
        orders_dict[i]['items'] = items

    products_id = []
    for prd in cart:
        products_id.append(prd.product_id)
    
    products = Products.query.filter(Products.id.in_((products_id))).all()
    images = get_images_data(products)
    products = get_product_dict_id(products)
    for i in products:
        products[i]["images"] = images[i]
    return render_template("admin/orders.html", orders=orders, products_json=products, orders_json=orders_dict)


@app.route("/admin/order/mark/<int:ID>/<int:page>")
def mark_order(ID, page):
    order = Orders.query.get(ID)
    if order:
        order.status = not order.status
        db.session.commit()
    return redirect(f"/admin/orders/{page}")


@app.route("/logout")
def logout():
    return redirect("/admin")

