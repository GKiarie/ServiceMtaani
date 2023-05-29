#!/usr/bin/python3
"""Serve flask pages"""

from flask import Flask, render_template, request, flash, redirect, url_for
import time
from models import storage
from models.vendor import Vendor
from models.order import Order
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config.update(SECRET_KEY='osd(99092=36&462134kjKDhuIS_d23')



@app.route('/', strict_slashes=False)
def homepage():
    """Render the homepage"""
    return render_template("home.html")

@app.route('/vendor/login', methods=["GET", "POST"], strict_slashes=False)
def signup():
    """Render the homepage"""
    if request.method == "POST":
        data = request.form
        newdata = data.copy()
        # hashed_pass = generate_password_hash(newdata["password"], method='sha256')
        # newdata['password'] = hashed_pass
        vendor_obj = storage.find(Vendor, "email", newdata.get("email"))
        if not vendor_obj:
            flash("No user found with provided email.", category='error')
        elif vendor_obj and check_password_hash(vendor_obj.password, newdata.get("password")):
            flash('Login Successful', category='success')
            return redirect('/vendor')
        else:
            flash('Wrong password. Try again', category="error")
    return render_template("login.html")

@app.route('/vendor/sign_up', methods=["GET", "POST"], strict_slashes=False)
def vendor_signup():
    """Render the homepage"""
    if request.method == "POST":
        data = request.form
        newdata = data.copy()
        newdata["phone_number"] = int(newdata["phone_number"])
        
        if newdata.get("password") != newdata.get("password2"):
            flash('Passwords do not match', category='error')
        elif storage.find(Vendor, "email", newdata.get("email")):
            flash('Vendor email already exists', category='error')
        else:
            flash('Creating account...', category='success')
            newdata["password"] = generate_password_hash(newdata["password"], method='sha256')
            del newdata["password2"]
            vendor_obj = Vendor(**newdata)
            vendor_obj.save()
            # if storage.find(Vendor, 'id', vendor1.id):
            #     flash('Account created successfully. Log in.', category='success')
            #     # return render_template("signup.html")
            #     # return redirect(url_for('app.vendor.login'))
            return redirect('/vendor/login')
    return render_template("signup.html")

@app.route('/test', strict_slashes=False)
def vendor():
    """Use this route to test new pages before integrating them"""
    return render_template("test_route.html")

@app.route('/vendor/orders', strict_slashes=False)
def vendor_orders_route():
    """Use this route to render vendor orders"""
    items = [
    {
        'order_name': 'Order 1',
        'client_name': 'Foo',
        'client_phone': '1234567890',
        'parts': 'Tyres, Headlights'
    },
    {
        'order_name': 'Order 2',
        'client_name': 'Bar',
        'client_phone': '9876543210',
        'parts': 'Headlights'
    }
    ]
    return render_template("vendor_orders.html", items=items)

@app.route('/vendor/delivered', strict_slashes=False)
def vendor_delivered():
    """Use this route to render the vendor's delivered orders"""
    items = [
    {
        'order_name': 'Order 1',
        'client_name': 'Foo',
        'client_phone': '1234567890',
        'parts': 'Tyres, Headlights'
    },
    {
        'order_name': 'Order 2',
        'client_name': 'Bar',
        'client_phone': '9876543210',
        'parts': 'Headlights'
    }
    ]
    return render_template("vendor_delivered.html", items=items)

@app.route('/vendor/catalogue', strict_slashes=False)
def vendor_catalogue():
    """This route will return the vendor's catalogue"""
    items = [
    {
        'part_name': 'Headlights',
        'part_description': 'Very bright',
        'part_price': 20000
    },
    {
        'part_name': 'Tyres',
        'part_price': 20000
    }
    ]
    return render_template("vendor_catalogue.html", items=items)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)