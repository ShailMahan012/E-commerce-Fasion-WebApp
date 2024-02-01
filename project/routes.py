from project import app, db
from project.models import Products, Images, Orders, Cart, Sub_Emails, Users, Main_Collection_Home, Coupons, Variant
from project.paypal import create_order, capture_payment, gen_order_json
from project.get_dict import *
from project.send_mail import send_mail, sub_letter
from flask import render_template, request, session, redirect, send_file, json, Markup, flash
from werkzeug.utils import secure_filename
from functools import wraps
from base64 import b64encode

db.create_all()

TITLE = app.config['TITLE']
IMAGE_DIR = app.config['IMAGE_DIR']
PER_PAGE = app.config['PER_PAGE']['products']
paypal = app.config["paypal"]
CLIENT_ID = paypal["CLIENT_ID"]
CURRENCY = paypal["CURRENCY"]


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please login to continue!", "primary")
            return redirect(f"/user/login?redirect={b64encode(request.path.encode()).decode()}")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    main_collection = []
    product_ids = list(map(lambda prd: prd.product_id, Main_Collection_Home.query.all())) # get only product_ids from table
    for i in product_ids:
        product = db.session.get(Products, i)
        if product:
            main_collection.append(product)
    images = get_images(main_collection)
    main_collection = get_product_dict(main_collection)
    return render_template("home.html", TITLE=TITLE, main_collection=main_collection, images=images)


@app.route("/items")
def items():
    return render_template("items.html", TITLE=TITLE)


@app.route("/terms")
def terms():
    return render_template("terms.html", TITLE="Grabalty | Terms of services")


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


@app.route("/search/products")
def search_products():
    search = request.args.get('search_input')
    if search:
        search = search.strip()
        products = Products.query.filter(Products.title.like(f"%{search}%")).limit(2).all()
        images = [x[0] for x in get_images(products)]
        products = get_product_dict(products)
        for i in range(len(products)):
            products[i]['img'] = images[i]
    else:
        products = []
    return json.jsonify(products)


@app.route("/category/<string:cat>/search")
@app.route("/category/<string:cat>/search/<int:page>")
def category(cat, page=1):
    search = request.args.get('search_input')
    if not search:
        search = ""
    products = Products.query.filter(Products.title.like(f"%{search}%"), Products.category==cat.lower())
    count = products.count()

    products = products.paginate(page=page, per_page=PER_PAGE)
    images = get_images(products.items)

    return render_template("items.html", TITLE=TITLE, products=products, images=images, search=search, count=count, page_name=f"category/{cat}/search")


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
        coupon = Coupons.query.filter_by(name="Order", status=True).first()

        variants = Variant.query.with_entities(Variant.id, Variant.prd_2).filter_by(prd_1=id).all()
        variants = get_variant_dict(variants)
        var_images = []
        for i, _ in enumerate(variants):
            image = Images.query.with_entities(Images.filename).filter_by(product_id=variants[i]["id"]).order_by("order").first()
            if image:
                variants[i]["img"] = image.filename
        return render_template("product.html", TITLE=TITLE, product=product, images=images, Markup=Markup, coupon=coupon, variants=variants)
    return redirect("/")


# @app.route("/static/products/<src>")
# def product_src(src):
#     sleep(4)
#     return send_file(f"static/products/{src}")


@app.route("/cart")
def cart():
    user_id = session.get("user_id")
    if user_id:
        coupon = Coupons.query.filter_by(name="FirstOrder", status=True).first()
        order = Orders.query.filter_by(user_id=user_id, approved=True).first()
        if order:
            coupon = None
    else:
        coupon = None

    return render_template("cart.html", TITLE="YOUR CART", coupon=coupon)


@app.route("/checkout")
@login_required
def checkout():
    user_id = session.get("user_id")
    user = db.session.get(Users, user_id)
    return render_template("checkout.html", TITLE="CHECKOUT HERE", client_id=CLIENT_ID, currency=CURRENCY, user=user)


@app.route("/create-paypal-order", methods=["POST"])
def create_paypal_order():
    user_id = session.get("user_id")
    products = json.loads(request.form.get("products"))
    if products:
        email = request.form.get("email")
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        address = request.form.get("address")
        city = request.form.get("city")
        country = request.form.get("country")
        postal_code = request.form.get("postal_code")
        phone = request.form.get("phone")
        note = request.form.get("note")
        if not note:
            note = None

        order = Orders(approved=False, user_id=user_id, email=email, f_name=f_name, l_name=l_name, address=address, city=city, country=country, postal_code=postal_code, phone=phone, note=note)
        db.session.add(order)
        db.session.commit()

        products, order_response, response_code = create_order(products, invoice=order.id) # PayPal
        order_id = order_response["id"] # PayPal ID
        order.discount = products.pop().get('discount')

        # add all products to Cart table one by one
        for prd in products:
            ID = prd.get("id")
            quantity = prd.get("quantity")
            discount = prd.get("discount")
            size = prd.get("size")
            product = db.session.get(Products, ID)
            if product and quantity:
                item = Cart(order_id=order.id, product_id=ID, quantity=quantity, title=product.title, price=product.price, discount=discount, size=size)
                db.session.add(item)

        db.session.commit()
    return {'id': order_response.get("id")}, response_code


@app.route("/capture-paypal-order", methods=["POST"])
def capture_paypal_order():
    order_id = request.get_json().get("orderID")
    response, response_code = capture_payment(order_id)
    if response_code in (200, 201):
        invoice_id = response["purchase_units"][0]["payments"]["captures"][0]["invoice_id"]
        invoice_id = int(invoice_id[4:])
        order = db.session.get(Orders, invoice_id)
        order.approved = True
        db.session.commit()
    return response, response_code


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
        products = gen_order_json(products)[0]
        return json.jsonify(products)
    except ValueError:
        print("fetch_products: JSON Decode ERROR")
        return "fetch_products: JSON Decode ERROR", 501
    return 'fetch_products: This message should not be received', 501


@app.route("/subscribe")
def subscibe():
    email = request.args.get("email")
    if not Sub_Emails.query.filter_by(email=email).first():
        sub_letter(email) # send email
        email = Sub_Emails(email=email)
        db.session.add(email)
        db.session.commit()
        return "True"
    return "False"
