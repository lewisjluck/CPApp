#Flask libraries
from flask import Flask, render_template, request, redirect, jsonify, Response, send_from_directory, send_file, json
from static.helpers import Form, Client, Product, make_doc, get_text
import requests
from db import search_product, add_lot, update_product

#SMS Library - Twilio
import twilio.rest

#Standard libraries
import os
import json
import jwt
import datetime
import csv

#Open file for secret
secret = open("secret.txt", "r").read().splitlines()

#Coreplus API keys
COREPLUS_API_CONSUMER_ID = secret[0]
COREPLUS_API_SECRET = secret[1]
COREPLUS_ACCESS_KEY = secret[2]
TWILIO_SID = secret[5]
TWILIO_TOKEN = secret[6]

#Coreplus base url
COREPLUS_BASE_URL = "https://sandbox.coreplus.com.au/api/core/v2.1"

#Deliveries clients
deliveries_clients = []

#Numbers
numbers = []

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
form = Form(client, [Product("1", "1", "1", "Example Product 1")], options, True)
form.make_pdf()
"""



#Flask setup
app = Flask(__name__)
app.secret_key = os.urandom(24)

#Helper function to parse json data to Form Object
def parse_form(json_data, data):
    suburb = json_data['addressResidential']["suburb"][:-3]
    if not json_data['addressResidential']["state"] == "":
        state = json_data['addressResidential']["state"]
    else:
        state = json_data['addressResidential']["suburb"][-3:]

    client = Client(json_data['firstName'], json_data["lastName"], "123456", json_data['addressResidential']["streetAddress"], suburb, state, json_data['addressResidential']["postcode"], json_data["phoneNumberMobile"], json_data["phoneNumberHome"])
    if data["id"] not in deliveries_clients:
        client.update_doc()
        deliveries_clients.append(data["id"])
    options = data["options"]
    products = []
    responses = []
    for i in range(len(data["products"][0])):
        if not data["products"][0][i] == "":
            products.append(Product(data["products"][0][i], data["products"][1][i], data["products"][2][i], data["products"][3][i]))
    for product in products:
        match = search_product(product.reference)
        try:
            if not product.lot in [lot[0] for lot in match[0]["lot"]]:
                add_lot(product)
        except:
            responses.append(update_product(product))
    return (Form(client, products, data["options"], data["new"], data["page-options"]), responses)

#Helper function to generate coreplus API claims
def claims(url):
    claims = {
          "iss": "http://127.0.0.1:5000/",
          "aud": "https://coreplus.com.au",
          "nbf": datetime.datetime.utcnow(),
          "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=60),
          "consumerId": COREPLUS_API_CONSUMER_ID,
          "accessToken": COREPLUS_ACCESS_KEY,
          "url": url,
          "httpMethod": "GET"
    };
    encoded_jwt_byte = jwt.encode(claims, COREPLUS_API_SECRET, algorithm='HS256')
    headers = {"Authorization": "JwToken" + " " + str(encoded_jwt_byte)[2:-1], "content-type": "application/json"}
    return headers

#Default error response
def error(message="Something went wrong! Let's try that again.", address="contracts"):
    return render_template("error.html", message=message, address="/" + address)

#Default not implemented response
def unimplemented(address=""):
    return render_template("error.html", message="This page is not implemented yet.", address="/" + address)





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
        response = requests.get(url=client_list_query, verify=True, headers=claims(client_list_query), timeout=45);
        try:
            return jsonify(response.json()["clients"])
        except Exception as e:
            print("ERROR ACCESSING COREPLUS, Error:", e)
            return jsonify([])
    else:
        return error()

#Back end method for autocomplete products
@app.route("/get_products", methods= ["GET", "POST"])
def get_products():
    query = request.args.get('query')
    if query:
        try:
            return jsonify(search_product(query))
        except error:
            return error()
    else:
        return error()

#Back end method to call print and pdf generation
@app.route("/make_file", methods= ["GET", "POST"])
def make_file():
    data = request.get_json(force=True)
    if data:
        client_data_query = COREPLUS_BASE_URL + "/Client/" + data["id"]
        api_response = requests.get(url=client_data_query, verify=True, headers=claims(client_data_query), timeout=45);
        json_data = api_response.json()
        parse = parse_form(json_data, data)
        text = f"The contract for " + json_data["firstName"] + " " + json_data["lastName"] + " has been printed."
        for info in parse[1]:
            text += f"The product with reference " + str(response["reference"]) + " has been added."
        form = parse[0]
        form.make_pdf()
        return jsonify(form.text, text)

#Display file
@app.route("/Contract", methods = ["GET", "POST"])
def get_file():
    return send_file("./static/print.pdf", mimetype="application/pdf", cache_timeout=0)

#Print error page
@app.route("/print_error", methods=["GET", "POST"])
def print_error():
    return error()

#Page to record delivery client details
@app.route("/deliveries", methods = ["GET", "POST"])
def deliveries():
    if request.method == "POST":
        if "download" in request.form:
            return send_file("./static/deliveries.docx", cache_timeout=0)
        elif "clear" in request.form:
            try:
                os.remove("./static/deliveries.docx")
            except:
                print("FILE DOES NOT EXIST")
            make_doc()
            deliveries_clients = []
            return render_template("deliveries.html", message=f"Client details cleared.")
        elif "send" in request.form:
            number = request.form.get("number")
            client = twilio.rest.Client(TWILIO_SID, TWILIO_TOKEN)
            try:
                message = client.messages.create(to=number, from_="+16622658077", body=get_text())
                print(numbers)
                return render_template("deliveries.html", message=f"Your message was sent to {number}.")
            except Exception as e:
                return render_template("deliveries.html", message=f"Your message failed. This is likely due to the number you entered.")
    else:
        print(numbers)
        return render_template("deliveries.html", message="")

#Page to update or add products to the database
@app.route("/products", methods = ["GET", "POST"])
def products():
    if request.method == "POST":
        if not request.form.get("ref"):
            return error("You must enter a reference number for your product!", "product")
        response = update_product(Product(str(request.form.get("ref")), str(request.form.get("lot")), "", str(request.form.get("description"))))
        message = f"The product with reference: " + str(response["reference"]) + (" has been added" if response["new"] else " has been updated")
        message += " and its lot has been changed." if response["lot_changed"] and not response["new"] else "."
        return render_template("products.html", message=message)
    else:
        return render_template("products.html")

#Login page for security (may not be implemented)
@app.route("/help", methods = ["GET", "POST"])
def help():
    import markdown
    with open("static/user_guide.md", 'r') as file:
        text = file.read()
        html = markdown.markdown(text)
    return render_template("help.html", content = html)

"""
if __name__ == "__main__":
    app.run(debug=True)
"""
