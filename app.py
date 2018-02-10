import os
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from lxml import html
import urllib2
import requests
import json
import datetime
import webbrowser

path = "C:\\Users\\mikeb\\Documents\\Github\\Program Programmer"

app = Flask(__name__)

error = 'none'

@app.route('/', methods=['GET', 'POST'])
def index():
    render_template('index.html')

    # If request is posted
    if request.method == 'POST':
        # Take in the three inputs
        data=request.form['IO']
        return collect(data)

    # Render template while waiting for response
    return render_template('index.html')


def collect(data):
    i = 0
    while (i < 100000000):
        i = i + 1
    return render_template('index.html')

if __name__ == '__main__':
        app.debug = True
        port = int(os.environ.get('PORT',5000))
        app.run(host='0.0.0.0', port=port)