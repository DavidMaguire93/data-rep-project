from flask import Flask, url_for, request, redirect, abort, jsonify, session
from pymysql import NULL
from werkzeug.urls import url_quote_plus
from ProductDao import productDao
from OrderDao import orderDao

app = Flask(__name__, static_url_path='', static_folder='staticpages')
app.secret_key = 'SomeSecretKey'

@app.route('/')
def home():
    if not 'username' in session:
        return redirect(url_for('login'))

    return 'Welcome ' + session['username'] +\
        '<br><br><a href = "'+url_for('logout')+'"><button>Logout</button></a>' +\
        '<br><br><a href = "index.html"><button>Shop Index</button>'

@app.route('/login')
def login():
    return 'Please enter your username (Check Readme)'+\
        '<br><br><input type="text" placeholder="Enter Username" name="uname" required>' +\
        '<button>'+\
            '<a href="'+url_for('process_login')+'">' +\
                'login' +\
            '</a>' +\
        '</button>'

@app.route('/processlogin')
def process_login():
    # Insert check for credentials
    # Redirect to login page if not valid

    #else
    session['username']="sampleUser"
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


# Get all products
@app.route('/products')
def getAll():

    if not 'username' in session:
        abort(401)
    
    return jsonify(productDao.getAll())

# Get all orders
@app.route('/orders')
def getAllOrders():

    if not 'username' in session:
        abort(401)
    
    return jsonify(orderDao.getAllOrders())


# Get all orders joined with products
@app.route('/ordersjoin')
def getAllOrdersJoin():

    if not 'username' in session:
        abort(401)
    
    return jsonify(orderDao.getAllOrdersJoin())


# Search for product by ID
@app.route('/products/<int:ProductID>')
def findByID(ProductID):

    if not 'username' in session:
        abort(401)

    return jsonify(productDao.findById(ProductID))

# Search for order by ID
@app.route('/orders/<int:orderID>')
def findByorderID(orderID):

    if not 'username' in session:
        abort(401)

    return jsonify(orderDao.findByOrderId(orderID))


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

    if not 'username' in session:
        abort(401)

    return jsonify(productDao.create(product))

# Create order (id not needed)
@app.route('/orders', methods=['POST'])
def createOrder():
    if not request.json:
        abort(400)

    order = {
        "customerID":request.json["customerID"],
        "productID":request.json["productID"],
        "quantity":request.json["quantity"]
    }

    if not 'username' in session:
        abort(401)

    return jsonify(orderDao.createOrder(order))


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

    if not 'username' in session:
        abort(401)

    return jsonify(currentProduct)

# Update order
@app.route('/orders/<int:orderID>', methods=['PUT'])
def updateOrder(orderID):
    foundOrder=orderDao.findByOrderId(orderID)
    if foundOrder == None:
        return jsonify({}), 404
    currentOrder = foundOrder
    if 'customerID' in request.json:
        currentOrder['customerID'] = request.json['customerID']
    if 'productID' in request.json:
        currentOrder['productID'] = request.json['productID']
    if 'quantity' in request.json:
        currentOrder['quantity'] = request.json['quantity']
    orderDao.updateOrder(currentOrder, orderID)

    if not 'username' in session:
        abort(401)

    return jsonify(currentOrder)


# Delete product
@app.route('/products/<int:ProductID>', methods=['DELETE'])
def delete(ProductID):
    foundProduct=productDao.findById(ProductID)
    if foundProduct == None:
        return "Product not Present", 404
    productDao.delete(ProductID)
    
    if not 'username' in session:
        abort(401)


    return jsonify({"done":True})

# Delete order
@app.route('/orders/<int:orderID>', methods=['DELETE'])
def deleteOrder(orderID):
    foundOrder=orderDao.findByOrderId(orderID)
    if foundOrder == None:
        return "Order not Present", 404
    orderDao.deleteOrder(orderID)
    
    if not 'username' in session:
        abort(401)


    return jsonify({"done":True})


# Run app
if __name__ == "__main__":
    app.run(debug=True)