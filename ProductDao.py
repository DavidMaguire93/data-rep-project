import pymysql
import dbconfig as cfg

class ProductDao:
    db = ""
    def __init__(self):

        # Takes input from python config file
        self.db = pymysql.connect(
            host = cfg.mysql['host'], 
            user = cfg.mysql['user'], 
            password = cfg.mysql['password'], 
            database = cfg.mysql['database'],
            
            # this cursorclass allows to get outputs from select statements etc as dicts without having to convert
            cursorclass=pymysql.cursors.DictCursor
            )



    # Create new product in table
    def create(self, product):
        cursor = self.db.cursor() 
        # id not needed as it is auto-increment
        sql = "insert into products (name, category, price) values (%s,%s,%s)"
        values = [
            product['name'],
            product['category'],
            product['price']
                    ]
        cursor.execute(sql, values)
        self.db.commit()

        # On success, returns id of newly created product
        return cursor.lastrowid


    # View all products in database
    def getAll(self):
        cursor = self.db.cursor() 
        sql = "select * from products"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results


    # Search for a product by its id
    def findById(self, ProductID):
        cursor = self.db.cursor() 
        sql = 'SELECT * from products WHERE ProductID = %s'
        values = [ ProductID ]
        cursor.execute(sql, values)
        results = cursor.fetchone()
        return results


    # Change product based on its id
    def update(self, product, ProductID):
        cursor = self.db.cursor() 
        sql = "UPDATE products SET name = %s, category = %s, price = %s where ProductID = %s"
        values = [
            product['name'],
            product['category'],
            product['price'],
            ProductID
                    ]
        cursor.execute(sql, values)
        self.db.commit()
        return product


    # Delete product based on id
    def delete(self, ProductID):
        cursor = self.db.cursor() 
        sql = 'DELETE from products WHERE ProductID = %s'
        values = [ ProductID ]
        cursor.execute(sql, values)
        return {}

productDao = ProductDao()