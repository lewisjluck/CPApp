#Flask libraries
from flask import Flask, render_template, request, redirect
from static.helpers import Form, Client, Product

#Standard libraries
import os
import json

#Coreplus API keys
COREPLUS_API_CONSUMER_ID = "44f2f611-0842-4845-8731-adedfe0a7ef4"
COREPLUS_API_SECRET = "7JmH8WdxQxGgduaR538bQ7euoWDBtXp7NEWMpUWcYk3PVAg2YrDdUg=="
COREPLUS_ACCESS_KEY = "c20f18ff-e535-4c0f-b811-c13503bf35c5"

#Google Maps API Key
GOOGLE_MAPS_API_KEY = "AIzaSyCSk58iSStU1iZCRWAlvXmmhArg0HOAYdA"

# *** TESTING ***
client = Client("Angelina", "Barbieri", "123456", "80 McIlwraith Avenue", "Norman Park", "QLD", "4170", "0467226317")
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
