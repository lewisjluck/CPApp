#Standard libraries
import sqlite3
import csv
from static.helpers import Form, Client, Product
from datetime import date

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
                    db.execute("INSERT INTO lots (ref, lot, info) VALUES (?,?,?)", (row[0], row[2], ""))
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
        lots = db.execute("SELECT lot, info FROM lots WHERE ref=?", (product[0],)).fetchall()
        matches.append({
        "ref":product[0],
        "lot":lots,
        "description":product[1]
        })
    return matches

#Add product lot
def add_lot(product):
    db = open_db()
    db.execute("INSERT INTO lots (ref, lot, info) VALUES (?, ?, ?)", (product.reference, product.lot, date.today().strftime("%d/%m/%Y")))
    db.commit()
    close_db(db)

#Update databse information depending on input data
def update_product(product):
    db = open_db()
    response = {"new":False, "lot_changed":False, "reference":product.reference}
    search_product = db.execute("SELECT * FROM products WHERE ref=?", (product.reference,)).fetchone()
    if search_product:
        db.execute("UPDATE products SET description = ? WHERE ref=?", (product.description, product.reference))
    else:
        db.execute("INSERT INTO products (ref, description) VALUES (?, ?)", (product.reference, product.description))
        response["new"] = True
    sql_lots = db.execute("SELECT * FROM lots WHERE ref=?", (product.reference,)).fetchall()
    lots = [lot[0] for lot in sql_lots]
    if not product.lot in lots and not product.lot == "":
        db.execute("INSERT INTO lots (ref, lot, info) VALUES (?, ?, ?)", (product.reference, product.lot, date.today().strftime("%d/%m/%Y")))
        response["lot_changed"] = True
    db.commit()
    close_db(db)
    return response
