#Flask libraries
from flask import Flask, render_template, request, redirect
from static.helpers import Form, Client, Product

#Standard libraries
import os
import json

#Open file for secret
secret = open("secret.txt", "r").readlines()

#Coreplus API keys
COREPLUS_API_CONSUMER_ID = secret[0]
COREPLUS_API_SECRET = secret[1]
COREPLUS_ACCESS_KEY = secret[2]

# *** TESTING ***
client = Client("Lewis", "Luck", "123456", "6 Chrystal Street", "Paddington", "QLD", "4064", "0467226317")
options = {
    "report":True,
    "visit":True,
    "delivery":True,
    "setup":False,
    "urgent":False
}
form = Form(client, [Product("1", "1", "1", "Example Product 1"), Product("2", "2", "1", "Example Product 2"), Product("3", "3", "1", "Example Product 3")], options, True)
form.make_pdf()

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
