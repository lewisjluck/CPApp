#Flask libraries
from flask import Flask, render_template, request, redirect

#Standard libraries
import os
import json

#Flask setup
app = Flask(__name__)
app.secret_key = os.urandom(24)

#Main Page
@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template("homepage.html")

if __name__ == "__main__":
    app.run(debug=True)
