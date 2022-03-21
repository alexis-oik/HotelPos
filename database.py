import mysql.connector
import os


class Database:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database="pos_orders"
        )
        self.cursor = self.mydb.cursor()

        self.customers = []
        self.get_customers()

        self.products = {
            "beers": [],
            "soft drinks": [],
            "wine": [],
            "water": []
        }
        self.get_products()

    def get_customers(self):
        sql = "SELECT * FROM customers"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            r = {
                "id": row[0],
                "name": row[1],
                "room": row[2],
                "guests": row[3]
            }
            self.customers.append(r)

    def get_products(self):
        sql = "SELECT * FROM products"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            r = {
                "id": row[0],
                "title": row[2],
                "price": row[3],
            }
            self.products[row[1].lower()].append(r)

    def send_invoice(self, values):
        sql = "INSERT INTO `invoice`(`customer_id`, `date`, `time`, `table`, `total_price`) VALUES (%s, " \
              "%s, %s, %s, %s) "
        self.cursor.execute(sql, values)
        self.mydb.commit()

    def send_order(self, values):
        sql = "INSERT INTO `order`(`customer_id`, `product_id`, `invoice_id`, `date`, `quantity`, " \
              "`total_price`) VALUES (" \
              "%s, %s, %s, %s, %s, %s) "
        self.cursor.execute(sql, values)
        self.mydb.commit()

    def find_customer_id(self, customer_name):
        return [customer['id'] for customer in self.customers if customer['name'] == customer_name][0]

    def find_product_id(self, product_name):
        sql = "SELECT product_id FROM products WHERE products.name = %s"
        val = ([product_name])
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        return result[0][0]

    def get_last_invoice_id(self):
        return self.cursor.lastrowid

    def get_all_orders(self):
        sql = "SELECT date, time, invoice.table, customers.name, invoice.invoice_id, total_price FROM invoice INNER " \
              "JOIN customers ON " \
              "invoice.customer_id = customers.customer_id ORDER BY date DESC "
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_selected_order_items(self, invoice_id):
        sql = "SELECT products.name, pos_orders.order.quantity, pos_orders.order.total_price FROM products INNER JOIN " \
              "pos_orders.order ON " \
              "pos_orders.order.product_id = pos_orders.products.product_id WHERE pos_orders.order.invoice_id = %s"
        val = ([invoice_id])
        self.cursor.execute(sql, val)
        return self.cursor.fetchall()
