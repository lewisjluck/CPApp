#Flask libraries
from flask import Flask, render_template, request, redirect, jsonify, Response
from static.helpers import Form, Client, Product
import requests
from werkzeug.datastructures import ImmutableMultiDict

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
client = Client("Lewis", "Luck", "123456", "6 Chrystal Street", "Paddington", "QLD", "4064", "0467226317")
options = {
    "report":True,
    "visit":True,
    "delivery":True,
    "setup":False,
    "urgent":False
}
form = Form(client, [Product("1", "1", "1", "Example Product 1")], options, True)
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

#Back end method for autocomplete clients
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
        return render_template("error.html", message="Something went wrong! Sorry! Let's try that again.", address="/contracts")

#Back end method to call print and pdf generation
@app.route("/make_file", methods= ["GET", "POST"])
def make_file():
    data = request.get_json(force=True)
    if data:
        client_list_query = COREPLUS_BASE_URL + "/Client/" + data["id"]
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
        json_data = response.json()
        suburb = json_data['addressResidential']["suburb"][:-3]
        if not json_data['addressResidential']["state"] == "":
            state = json_data['addressResidential']["state"]
        else:
            state = json_data['addressResidential']["suburb"][-3:]
        if json_data["phoneNumberMobile"]:
            number = json_data["phoneNumberMobile"]
        else:
            number = json_data["phoneNumberHome"]
        client = Client(json_data['firstName'], json_data["lastName"], "123456", json_data['addressResidential']["streetAddress"], suburb, state, json_data['addressResidential']["postcode"], number)
        options = data["options"]
        products = []
        for i in range(len(data["products"][0]) - 1):
            products.append(Product(data["products"][0][i], data["products"][1][i], data["products"][2][i], data["products"][3][i]))
        form = Form(client, products, data["options"], data["new"])
        form.make_pdf()
        return "/print_file"
    else:
        return "/print_error"

@app.route("/print_file", methods=["GET", "POST"])
def print_file():
    return render_template("error.html", message="This page is not implemented yet.", address="/")

@app.route("/print_error", methods=["GET", "POST"])
def print_error():
    return render_template("error.html", message="Something went wrong! Sorry! Let's try that again.", address="/contracts")

@app.route("/deliveries", methods = ["GET", "POST"])
def deliveries():
    return render_template("error.html", message="This page is not implemented yet.", address="/")

@app.route("/reports", methods = ["GET", "POST"])
def reports():
    return render_template("error.html", message="This page is not implemented yet.", address="/")

@app.route("/login", methods = ["GET", "POST"])
def login():
    return render_template("error.html", message="This page is not implemented yet.", address="/")

"""
if __name__ == "__main__":
    app.run(debug=True)
"""
