#!/usr/bin/env python3 

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('home.html')


@app.route("/debug")
def debugg():
    return "DEBUGGER!!"


if __name__ == "__main__":
    app.run(debug=True)
