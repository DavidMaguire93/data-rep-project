from flask import Flask, url_for, request, redirect, abort, jsonify
from pymysql import NULL
from ProductDao import productDao

app = Flask(__name__, static_url_path='', static_folder='staticpages')

@app.route('/')
def index():
    return "hello"


# Get all products
@app.route('/products')
def getAll():
    return jsonify(productDao.getAll())


# Search for product by ID
@app.route('/products/<int:ProductID>')
def findByID(ProductID):
    return jsonify(productDao.findById(ProductID))


# Create product (id not needed)
@app.route('/products', methods=['POST'])
def create():
    if not request.json:
        abort(400)

    product = {
        "name":request.json["name"],
        "category":request.json["category"],
        "price":request.json["price"]
    }

    return jsonify(productDao.create(product))


# Update product
@app.route('/products/<int:ProductID>', methods=['PUT'])
def update(ProductID):
    foundProduct=productDao.findById(ProductID)
    if foundProduct == None:
        return jsonify({}), 404
    currentProduct = foundProduct
    if 'name' in request.json:
        currentProduct['name'] = request.json['name']
    if 'category' in request.json:
        currentProduct['category'] = request.json['category']
    if 'price' in request.json:
        currentProduct['price'] = request.json['price']
    productDao.update(currentProduct, ProductID)

    return jsonify(currentProduct)


# Delete product
@app.route('/products/<int:ProductID>', methods=['DELETE'])
def delete(ProductID):
    foundProduct=productDao.findById(ProductID)
    if foundProduct == None:
        return "Product not Present", 404
    productDao.delete(ProductID)
    

    return jsonify({"done":True})


# Run app
if __name__ == "__main__":
    app.run(debug=True)