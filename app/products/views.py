from flask import Blueprint, render_template

products_bp = Blueprint("products", __name__, template_folder="templates")

@products_bp.route("/list")
def list_products():
    products = [
        {"name": "Ноутбук", "price": 35000},
        {"name": "Мишка", "price": 500},
        {"name": "Клавіатура", "price": 1200}
    ]
    return render_template("products/list.html", products=products)
