from flask import Blueprint, request, jsonify
from config import db
from models import Product

product_bp = Blueprint('product_bp', __name__)

# Helper function
def check_restock(product):
    product.need_restock = product.available_quantity < (0.2 * product.total_quantity)
    db.session.commit()

# Add product
@product_bp.route('/product', methods=['POST'])
def add_product():
    data = request.get_json()
    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        # price=data['price'],
        price=float(data['price']),
        total_quantity=int(data['total_quantity']),
        available_quantity=int(data['available_quantity'])


        # total_quantity=data['total_quantity'],
        # available_quantity=data['available_quantity']
    )
    check_restock(product)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

# Get all products
@product_bp.route('/product', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200

# Get product by ID
@product_bp.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict()), 200

# Update product
@product_bp.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    # product.price = data.get('price', product.price)
    # product.total_quantity = data.get('total_quantity', product.total_quantity)
    # product.available_quantity = data.get('available_quantity', product.available_quantity)
    product.price = float(data.get('price', product.price))
    product.total_quantity = int(data.get('total_quantity', product.total_quantity))
    product.available_quantity = int(data.get('available_quantity', product.available_quantity))

    check_restock(product)
    db.session.commit()
    return jsonify(product.to_dict()), 200

# Delete product
@product_bp.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200

# Restock check
@product_bp.route('/restock/<int:id>', methods=['GET'])
def restock_status(id):
    product = Product.query.get_or_404(id)
    check_restock(product)
    return jsonify({"need_restock": product.need_restock}), 200

# Update restock manually
@product_bp.route('/restock/update/<int:id>', methods=['PUT'])
def update_restock_status(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.need_restock = data.get('need_restock', product.need_restock)
    db.session.commit()
    return jsonify(product.to_dict()), 200

# List products needing restock
@product_bp.route('/restock/list', methods=['GET'])
def get_restock_list():
    products = Product.query.filter_by(need_restock=True).all()
    return jsonify([p.to_dict() for p in products]), 200
