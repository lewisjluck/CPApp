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

#Work address
WORK_ADDRESS = secret[3]

#Google maps API key
GOOGLE_MAPS_API_KEY = secret[4]

# *** TESTING ***
client = Client("Angelina", "Barbieri", "123456", "6 Chrystal Street", "Paddington", "QLD", "4064", "0467226317")
options = {
    "report":True,
    "visit":True,
    "delivery":True,
    "setup":False
}
form = Form(client, [Product("1", "1", "1", "Example Product"), Product("2", "2", "1", "Example Product"), Product("3", "3", "1", "Example Product")], options, True)
form.make_pdf(GOOGLE_MAPS_API_KEY, WORK_ADDRESS)
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
