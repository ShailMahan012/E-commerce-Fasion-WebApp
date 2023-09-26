import base64
from project.models import Products, Orders, Coupons
from flask import jsonify, session
from project import app
import requests

paypal = app.config["paypal"]
BASE_URL = paypal["BASE_URL"]
CLIENT_ID = paypal["CLIENT_ID"]
APP_SECRET = paypal["APP_SECRET"]
CURRENCY = paypal["CURRENCY"]


def create_order(products, invoice):
    data, products = gen_paypal_json(products, invoice)
    response = paypal_request("/v2/checkout/orders", json_data=data)
    data = response.json()
    return products, data, response.status_code


def capture_payment(order_id):
    # response = paypal_request(f"/v2/checkout/orders/{order_id}/capture", json_data={})
    url = BASE_URL + f"/v2/checkout/orders/{order_id}/capture"
    access_token = generate_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)

    data = response.json()
    return data, response.status_code


def gen_paypal_json(products, invoice):
    products, total_price = gen_order_json(products)
    invoice = f"ORD_{invoice:0>10}"
    paypal_json = {"intent": "CAPTURE", "purchase_units": [{"amount": {"currency_code": CURRENCY, "value": total_price}, "invoice_id": invoice}]}
    return paypal_json, products


def generate_access_token():
    url = f"{BASE_URL}/v1/oauth2/token"
    auth = base64.b64encode(f"{CLIENT_ID}:{APP_SECRET}".encode("utf-8")).decode("utf-8")


    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth}",
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)

    json_data = response.json()
    access_token = json_data.get("access_token")

    return access_token


def paypal_request(url, json_data=None, request_method="POST"):
    url = BASE_URL + url
    access_token = generate_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    if json_data:
        headers["Content-Type"] = "application/json"
    
    if request_method =="GET":
        response = requests.get(url, headers=headers)
    elif json_data:
        response = requests.post(url, headers=headers, json=json_data)
    else:
        response = requests.post(url, headers=headers)
    return response


def paypal_order_detail(order_id):
    response = paypal_request(f'/v2/checkout/orders/{order_id}', request_method="GET")
    return response.json(), response.status_code


def get_total_price(products):
    user_id = session.get("user_id")
    first_order = Orders.query.filter_by(user_id=user_id).first()

    total_price = 0
    if products:
        for prd in products:
            ID = prd.get("id")
            quantity = prd.get("quantity")
            product = Products.query.get(ID)
            if product and quantity:
                coupon = Coupons.query.filter_by(name="OneProductAmount", status=True).first() # only one coupon
                discount = True
                if coupon:
                    if coupon.min_amount:
                        if product.price < coupon.min_amount:
                            discount = False
                if coupon and discount:
                    price = product.price * (100-coupon.amount) * quantity / 100 # giving discount of coupon.amount percent
                else:
                    price = product.price * quantity
                total_price += price
    coupon = Coupons.query.filter_by(name="FirstOrder", status=True).first()
    if coupon:
        total_price = total_price * (100-coupon.amount) / 100
    return total_price


def gen_order_json(products):
    user_id = session.get("user_id")
    first_order = Orders.query.filter_by(user_id=user_id).first()

    total_price = 0
    if products:
        for i, prd in enumerate(products):
            ID = prd.get("id")
            quantity = prd.get("quantity")
            if not quantity:
                quantity = 0
            product = Products.query.get(ID)
            if product:
                coupon = Coupons.query.filter_by(name="OneProductAmount", status=True).first() # only one coupon
                discount = True
                if coupon:
                    if coupon.min_amount:
                        if product.price < coupon.min_amount:
                            discount = False
                if coupon and discount:
                    price = product.price * (100-coupon.amount) * quantity / 100 # giving discount of coupon.amount percent
                    products[i]["discount"] = coupon.amount
                else:
                    price = product.price * quantity
                total_price += price

    coupon = Coupons.query.filter_by(name="FirstOrder", status=True).first()
    order = Orders.query.filter_by(user_id=user_id, approved=True).first()
    if coupon and not order:
        total_price = total_price * (100-coupon.amount) / 100
        products.append({"discount": coupon.amount})
    else:
        products.append({"discount": None})
    return products, total_price
