#!/usr/bin/python3
"""Serve flask pages"""

from flask import Flask, render_template
app = Flask(__name__)

app.route('/', strict_slashes=False)
def homepage():
    """Render the homepage"""
    return render_template("homepage.html")

if __name__ == "__main__":
    app.route(host='0.0.0.0', port=5000)