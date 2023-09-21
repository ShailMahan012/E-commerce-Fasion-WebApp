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


def create_order(products):
    url = f"{BASE_URL}/v2/checkout/orders"
    access_token = generate_access_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    data = gen_order_json(products)

    response = requests.post(url, headers=headers, json=data)
    return jsonify(response.json()), response.status_code


def capture_payment(order_id):
    url = f"{BASE_URL}/v2/checkout/orders/{order_id}/capture"
    access_token = generate_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    
    response = requests.post(url, headers=headers)
    data = response.json()
    
    return jsonify(data), response.status_code


def gen_order_json(products):
    total_price = get_total_price(products)
    paypal_json = {"intent": "CAPTURE", "purchase_units": [{"amount": {"currency_code": CURRENCY, "value": total_price}}]}

    return paypal_json


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
