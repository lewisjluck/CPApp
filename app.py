#Flask libraries
from flask import Flask, render_template, request, redirect, jsonify, Response
from static.helpers import Form, Client, Product
import requests

#Standard libraries
import os
import json
import jwt
import datetime


#Open file for secret
secret = open("secret.txt", "r").read().splitlines()

#Coreplus API keys
COREPLUS_API_CONSUMER_ID = secret[0]
COREPLUS_API_SECRET = secret[1]
COREPLUS_ACCESS_KEY = secret[2]

#Coreplus base url
COREPLUS_BASE_URL = "https://sandbox.coreplus.com.au/api/core/v2.1"

# *** TESTING ***
"""
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
"""

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
        return render_template("contracts.html", secret=secret)
    else:
        if request.form:
            print("hello")

@app.route("/get_clients", methods= ["GET", "POST"])
def get_clients():
    name_fragment = request.args.get('name')
    if name_fragment:
        client_list_query = COREPLUS_BASE_URL + "/Client/?name=" + name_fragment
        claims = {
              "iss": "http://127.0.0.1:5000/",
              "aud": "https://coreplus.com.au",
              "nbf": datetime.datetime.utcnow(),
              "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=60),
              "consumerId": COREPLUS_API_CONSUMER_ID,
              "accessToken": COREPLUS_ACCESS_KEY,
              "url": client_list_query,
              "httpMethod": "GET"
          };
        encoded_jwt_byte = jwt.encode(claims, COREPLUS_API_SECRET, algorithm='HS256')
        headers = {"Authorization": "JwToken" + " " + str(encoded_jwt_byte), "content-type": "application/json"}
        response = requests.get(url=client_list_query, verify=True, headers=headers, timeout=45);
        if response.json():
            return jsonify(response.json()["clients"])
        else:
            return jsonify([])
    else:
        return render_template("error.html", message="Something went wrong accessing Coreplus!", address="/contracts")


@app.route("/deliveries", methods = ["GET", "POST"])
def deliveries():
    return render_template("error.html", message="This page is not implemented yet.", address="/")

@app.route("/reports", methods = ["GET", "POST"])
def reports():
    return render_template("error.html", message="This page is not implemented yet.", address="/")

@app.route("/login", methods = ["GET", "POST"])
def login():
    return render_template("error.html", message="This page is not implemented yet.", address="/")

if __name__ == "__main__":
    app.run(debug=True)
