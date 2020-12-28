#Flask libraries
from flask import Flask, render_template, request, redirect
from static.helpers import Form, Client, Product

#Standard libraries
import os
import json

#Coreplus API keys
COREPLUS_API_CONSUMER_ID = os.environ["COREPLUS_API_CONSUMER_ID"]
COREPLUS_API_SECRET = os.environ["COREPLUS_API_SECRET"]
COREPLUS_ACCESS_KEY = os.environ["COREPLUS_ACCESS_KEY"]

# *** TESTING ***
client = Client("Angelina", "Barbieri", "123456", "6 Chrystal Street", "Paddington", "QLD", "4064", "0467226317")
options = {
    "report":True,
    "visit":True,
    "delivery":True,
    "setup":False
}
form = Form(client, [Product("123", "123", "1", "Example Product")], options, True)
form.make_pdf()
#print(form.find_distance(GOOGLE_MAPS_API_KEY))

#Flask setup
app = Flask(__name__)
app.secret_key = os.urandom(24)

#Main Page
@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("homepage.html")

#Contracts
@app.route("/contracts", methods = ["GET", "POST"])
def contracts():
    if request.method == "GET":
        return render_template("contracts.html")

"""
if __name__ == "__main__":
    app.run(debug=True)
"""
