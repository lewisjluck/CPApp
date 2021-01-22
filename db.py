#Standard libraries
import sqlite3
import csv
from static.helpers import Form, Client, Product

#Dynamic pathing
from os import path
ROOT = path.dirname(path.realpath(__file__))

#Open database
def open_db():
    db = sqlite3.connect(path.join(ROOT, "products.db"))
    db.commit()
    return db

#Close database
def close_db(db):
    if db is not None:
        db.close()

#Input products from csv to db
def input_products(file_name):
    db = open_db()
    with open(file_name) as products:
        reader = csv.reader(products, delimiter=",")
        for row in reader:
            db.execute("INSERT INTO products (ref, description) VALUES (?,?)", (row[0], row[1]))
            if len(row) > 2:
                if row[2]:
                    db.execute("INSERT INTO lots (ref, lot) VALUES (?,?)", (row[0], row[2]))
            db.commit()
    close_db(db)

#Search for product
def search_product(query):
    db = open_db()
    matches = []
    products =  db.execute("SELECT * FROM products WHERE description LIKE ?", ("%" + query + "%",)).fetchall()
    if products == []:
        products = db.execute("SELECT * FROM products WHERE ref LIKE ?", ("%" + query + "%",)).fetchall()
    for product in products:
        sql_lots = db.execute("SELECT lot FROM lots WHERE ref=?", (product[0],)).fetchall()
        lots = [lot[0] for lot in sql_lots]
        matches.append({
        "ref":product[0],
        "lot":lots,
        "description":product[1]
        })
    return matches

#Add product lot
def add_lot(product):
    db = open_db()
    db.execute("INSERT INTO lots (ref, lot) VALUES (?, ?)", (product.reference, product.lot))
    db.commit()
    close_db(db)