from flask import Flask, render_template, request, redirect, session
from flask import send_file, make_response, send_from_directory
from functions import get_json
import os


# Sets CWD to whatever directory app.py is located in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, template_folder="templates", static_url_path='/static')

# app.secret_key = SECRET_KEY
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/map")
def map():
    map = get_json()
    print(map)
    return render_template("map.html", map=map)


app.run(debug=True)

