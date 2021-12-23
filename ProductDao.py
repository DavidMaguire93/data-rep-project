import pymysql
import mysql.connector
import dbconfig as cfg

class ProductDao:
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
        return self.db.cursor(dictionary = True)

    # Create new product in table
    def create(self, product):
        cursor = self.getCursor() 
        # id not needed as it is auto-increment
        sql = "insert into products (name, category, price) values (%s,%s,%s)"
        values = [
            product['name'],
            product['category'],
            product['price']
                    ]
        cursor.execute(sql, values)
        self.db.commit()
        cursor.close()

        # On success, returns id of newly created product
        return cursor.lastrowid


    # View all products in database
    def getAll(self):
        cursor = self.getCursor() 
        sql = "select * from products"
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results


    # Search for a product by its id
    def findById(self, ProductID):
        cursor = self.getCursor()  
        sql = 'SELECT * from products WHERE ProductID = %s'
        values = [ ProductID ]
        cursor.execute(sql, values)
        results = cursor.fetchone()
        cursor.close()
        return results


    # Change product based on its id
    def update(self, product, ProductID):
        cursor = self.getCursor() 
        sql = "UPDATE products SET name = %s, category = %s, price = %s where ProductID = %s"
        values = [
            product['name'],
            product['category'],
            product['price'],
            ProductID
                    ]
        cursor.execute(sql, values)
        self.db.commit()
        cursor.close()
        return product


    # Delete product based on id
    def delete(self, ProductID):
        cursor = self.getCursor() 
        sql = 'DELETE from products WHERE ProductID = %s'
        values = [ ProductID ]
        cursor.execute(sql, values)
        cursor.close()
        return {}

productDao = ProductDao()