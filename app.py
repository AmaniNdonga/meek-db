from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productTitle = db.Column(db.String(100), unique=False)
    productPrice = db.Column(db.String(100), unique=False)

    def __init__(self, productTitle, productPrice):
        self.productTitle = productTitle
        self.productPrice = productPrice

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('productTitle', 'productPrice')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Endpoint to create a new product
@app.route('/product', methods=["POST"])
def add_product():
    productTitle = request.json['productTitle']
    productPrice = request.json['productPrice']

    new_product = Product(productTitle, productPrice)

    db.session.add(new_product)
    db.session.commit()

    product = Product.query.get(new_product.id)

    return product_schema.jsonify(product)

# Endpoint to query all products
@app.route('/products', methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Endpoint for querying a single guide
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Endpoint for updating a guide
@app.route("/product/<id>", methods=["PUT"])
def product_update(id):
    product = Product.query.get(id)
    productTitle = request.json['productTitle']
    productPrice = request.json['productPrice']

    product.productTitle = productTitle
    product.productPrice = productPrice

    db.session.commit()
    return product_schema.jsonify(product)

# Endpoint for deleting a record
@app.route('/product/<id>', methods=["DELETE"])
def product_delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return "product_schema.jsonify(product)"

if __name__ == '__main__':
    app.run(debug=True)