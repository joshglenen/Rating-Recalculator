import sys
from flask import Flask, render_template, json, request
import HTML_IMDB

app = Flask(__name__)


@app.route('/')
def display():
    return render_template('index.html')


@app.route('/<url>', methods=['POST'])
def execute(url):
    return HTML_IMDB.findID(url,0)  # TODO: implement dropdown menu with index

if __name__ == '__main__':
    app.run()
