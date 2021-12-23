import pymysql
import mysql.connector
import dbconfig as cfg

class OrderDao:
    db = ""

    def connectToDB(self):
        # Takes input from python config file
        self.db = mysql.connector.connect(
            host = cfg.mysql['host'], 
            user = cfg.mysql['user'], 
            password = cfg.mysql['password'], 
            database = cfg.mysql['database'],
        )
            # this cursorclass allows to get outputs from select statements etc as dicts without having to convert

            

    def __init__(self):
        self.connectToDB()

    def getCursor(self):
        if not self.db.is_connected():
            self.connectToDB()

        # Gets queries as dicts
        return self.db.cursor(dictionary = True)

    # Create new order in table
    def createOrder(self, order):
        cursor = self.getCursor() 
        # id not needed as it is auto-increment
        sql = "insert into orders (customerID, productID, quantity) values (%s,%s,%s)"
        values = [
            order['customerID'],
            order['productID'],
            order['quantity']
                    ]
        cursor.execute(sql, values)
        self.db.commit()
        cursor.close()

        # On success, returns id of newly created order
        return cursor.lastrowid


    # View all orders in database
    def getAllOrders(self):
        cursor = self.getCursor() 
        sql = "select orderID, customerID, productID, quantity from orders;"
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results


       # View all orders in database with products and prices
    def getAllOrdersJoin(self):
        cursor = self.getCursor() 
        sql = "select orderID, customerID, name as productName, category, quantity, price as productPrice, round(quantity*price,2) AS orderCost from orders left join products on orders.productID = products.ProductID;"
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results


    # Search for a order by its id
    def findByOrderId(self, OrderID):
        cursor = self.getCursor()  
        sql = 'select orderID, customerID, productID, quantity from orders WHERE OrderID = %s'
        values = [ OrderID ]
        cursor.execute(sql, values)
        results = cursor.fetchone()
        cursor.close()
        return results


    # Change order based on its id
    def updateOrder(self, order, OrderID):
        cursor = self.getCursor() 
        sql = "UPDATE orders SET customerID = %s, productID = %s, quantity = %s where OrderID = %s"
        values = [
            order['customerID'],
            order['productID'],
            order['quantity'],
            OrderID
                    ]
        cursor.execute(sql, values)
        self.db.commit()
        cursor.close()
        return order


    # Delete order based on id
    def deleteOrder(self, OrderID):
        cursor = self.getCursor() 
        sql = 'DELETE from orders WHERE OrderID = %s'
        values = [ OrderID ]
        cursor.execute(sql, values)
        cursor.close()
        return {}

orderDao = OrderDao()