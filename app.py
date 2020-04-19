from flask import Flask, render_template, request, redirect, session, url_for
from flask import send_file, make_response, send_from_directory
from functions import json_to_list, remove_from_list, add_to_list, text_info, set_session_keys
from keys import MAPBOX_TOKEN
import os


# Sets CWD to whatever directory app.py is located in
os.chdir(os.path.dirname(os.path.abspath(__file__)))


app = Flask(__name__, template_folder="templates", static_url_path='/static')

app.secret_key = 'abcd'
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True



@app.route("/")
def home():
    if 'visited' in request.cookies:
        return render_template("index.html", list_new=json_to_list(), mbat=MAPBOX_TOKEN, show_faq=False)
    response = make_response(render_template("index.html", list_new=json_to_list(), mbat=MAPBOX_TOKEN, show_faq=True))
    response.set_cookie('visited', 'visited', max_age=60 * 60 * 24 * 365)
    return response

@app.route("/map/")
def map(): 
    return render_template("map.html", list_new=json_to_list(), mbat=MAPBOX_TOKEN)

@app.route('/remove/<identifier>/', methods=['POST'])
def remove(identifier: str):
    if request.method == 'POST':
        text_info(str(identifier), request.form['phone_number'])
        remove_from_list(str(identifier))
        return redirect('/')

@app.route('/add/', methods=['POST'])
def add():
    if request.method == 'POST':
        add_to_list(request)
        return redirect('/')

@app.route('/setaddress/', methods=['POST'])
def setaddress():
    if request.method == 'POST':
        set_session_keys(request)
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

