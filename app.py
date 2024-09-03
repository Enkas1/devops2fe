from flask import Flask, request, render_template, url_for, session, redirect, jsonify
import os
import re
import psycopg2
from datetime import datetime
from functions import *


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def render_index():
    return render_template("index.html")

@app.route("/loginindex.html", methods=["GET"])
def render_loginindex():
    return render_template("loginindex.html")

    
if __name__ == "__main__":
    app.run(debug=True)   