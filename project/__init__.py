from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask(__name__)
admin = Blueprint("admin", __name__, template_folder="templates/admin", url_prefix="/admin")
user = Blueprint("user", __name__, template_folder="templates/user", url_prefix="/user")


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.app_context().push()


app.config['paypal'] = {
    # "BASE_URL": "https://api-m.paypal.com",
    # "CLIENT_ID": "AV6qiggsr5K-Bf-ZtuFdyaCk_cQC3mvEh0LUwAqZXcGvY_WhGp1OxLplyK6Hk61V4womA9yaXFiysuIz",
    # "APP_SECRET": "EGt1FVt_xxFJXI7G0OmF3SGCXVgyhjnOImt5SzhYw421BeCJnb5tZ41ZKecZZU8SMRHK3cMPUmtVgDoV",
    "BASE_URL": "https://api-m.sandbox.paypal.com",
    # "CLIENT_ID": "ATXfygBnUHBmBMPTjmfwlhgqVqtVoSgov3d5eStEpAi1Vxq_ZSVNFyhE-PvsdIUIesvpbOQOiJudzd-B",
    # "APP_SECRET": "EIh57RP1iOqkLQ5jc8SK6mq2uo1ZPB3Ow7_TSoRm_xxGpP7qFjLDKtHO3qzSVEuRla3oFn9Q3CTdY_KT",
    "CLIENT_ID": "AaYITUxB_0he79pMHBsHSgs2c6IGRjkbbRJJ5H47mh4GcYbkeiJ60uzXRtgt4-YmmLmiC33yhJ4rrXQm",
    "APP_SECRET": "EAe0WivXOobHvPhrsVS9ObDaEaaR9pWgPXnRg5UO57m3caAqNWZd_kQf1QvgSDefqW7zurVWYtYZ8Dc-",
    "CURRENCY": "CAD"
}
app.config['IMAGE_DIR'] =  'project/static/product_images'
app.config['TITLE'] = "Grabalty® Official Site : Athleisure Lifestyle & Fashion Brand"
app.config['PER_PAGE'] = {
    "admin": 15,
    "products": 6
}

from project import routes, admin_routes, user_routes
app.register_blueprint(admin)
app.register_blueprint(user)

