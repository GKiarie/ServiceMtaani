#!/usr/bin/python3
"""Serve flask pages"""

from flask import Flask, render_template, request, flash, redirect, url_for
import time
from models import storage
from models.vendor import Vendor
from models.order import Order
from models.job import Job
from models.bid import Bid
from models.mechanic import Mechanic
from models.client import Client
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config.update(SECRET_KEY='osd(99092=36&462134kjKDhuIS_d23')



@app.route('/', strict_slashes=False)
def homepage():
    """Render the homepage"""
    return render_template("home.html")

@app.route('/login/<user>', methods=["GET", "POST"], strict_slashes=False)
def login(user=None):
    """Render the homepage"""
    if request.method == "POST":
        data = request.form
        newdata = data.copy()
        # hashed_pass = generate_password_hash(newdata["password"], method='sha256')
        # newdata['password'] = hashed_pass
        if user == "vendor":
            user_obj = storage.find(Vendor, "email", newdata.get("email"))
            if not user_obj:
                flash("No user found with provided email.", category='error')
            elif user_obj and check_password_hash(user_obj.password, newdata.get("password")):
                flash('Login Successful', category='success')
                return render_template("vendor_orders.html")
            else:
                flash('Wrong password. Try again', category="error")

        if user == "mechanic":
            user_obj = storage.find(Mechanic, "email", newdata.get("email"))
            if not user_obj:
                flash("No user found with provided email.", category='error')
            elif user_obj and check_password_hash(user_obj.password, newdata.get("password")):
                flash('Login Successful', category='success')
                all_jobs = storage.openjobs()
                return render_template("mechanic_homepage.html", all_jobs=all_jobs, user_id=user_obj.id)
            else:
                flash('Wrong password. Try again', category="error")
        
        if user == "client":
            user_obj = storage.find(Client, "email", newdata.get("email"))
            if not user_obj:
                flash("No user found with provided email.", category='error')
            elif user_obj and check_password_hash(user_obj.password, newdata.get("password")):
                flash('Login Successful', category='success')
                all_jobs = storage.openjobs()
                return render_template("client_homepage.html", all_jobs=all_jobs)
            else:
                flash('Wrong password. Try again', category="error")
    return render_template("login.html")

@app.route('/sign_up/<user>', methods=["GET", "POST"], strict_slashes=False)
def vendor_signup(user=None):
    """Render the homepage"""
    if request.method == "POST":
        data = request.form
        newdata = data.copy()
        newdata["phone_number"] = int(newdata["phone_number"])
        if newdata.get("password") != newdata.get("password2"):
            flash('Passwords do not match', category='error')
            return redirect(f'/sign_up/{user}')
        if user == "vendor":
            if storage.find(Vendor, "email", newdata.get("email")):
                flash('Email already exists', category='error')
            else:
                flash('Creating account...', category='success')
                newdata["password"] = generate_password_hash(newdata["password"], method='sha256')
                del newdata["password2"]
                user_obj = Vendor(**newdata)
                user_obj.save()
                # if storage.find(Vendor, 'id', vendor1.id):
                #     flash('Account created successfully. Log in.', category='success')
                #     # return render_template("signup.html")
                #     # return redirect(url_for('app.vendor.login'))
                return redirect('/login/vendor')
        if user == "client":
            if storage.find(Client, "email", newdata.get("email")):
                flash('Email already exists', category='error')
            else:
                flash('Creating account...', category='success')
                newdata["password"] = generate_password_hash(newdata["password"], method='sha256')
                del newdata["password2"]
                user_obj = Client(**newdata)
                user_obj.save()
                # if storage.find(Vendor, 'id', vendor1.id):
                #     flash('Account created successfully. Log in.', category='success')
                #     # return render_template("signup.html")
                #     # return redirect(url_for('app.vendor.login'))
                return redirect('/login/client')

        if user == "mechanic":
            if storage.find(Mechanic, "email", newdata.get("email")):
                flash('Email already exists', category='error')
            else:
                flash('Creating account...', category='success')
                newdata["password"] = generate_password_hash(newdata["password"], method='sha256')
                del newdata["password2"]
                user_obj = Mechanic(**newdata)
                user_obj.save()
                # if storage.find(Vendor, 'id', vendor1.id):
                #     flash('Account created successfully. Log in.', category='success')
                #     # return render_template("signup.html")
                #     # return redirect(url_for('app.vendor.login'))
                return redirect('/login/mechanic')
    return render_template("signup.html")

@app.route('/test', strict_slashes=False)
def test_route():
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

@app.route('/mechanic/', methods=['GET', 'POST'], strict_slashes=False)
def mechanic_jobs():
    """This route will render the mechanic home page"""
    all_jobs = storage.openjobs()
    if request.method == "GET":
        all_jobs = storage.openjobs()
        return render_template("mechanic_homepage.html", all_jobs=all_jobs)
    if request.method == "POST":
        # bid1 = Bid()
        # flash()
        return render_template("mechanic_homepage.html", all_jobs=all_jobs)
    
@app.route('/mechanic/place_bid', methods=['POST'], strict_slashes=False)
def place_bid():
    """Route to place bid"""
    if request.method == "POST":
        data = request.form
        new_bid = Bid(**data)
        new_bid.save()
        return redirect('/mechanic')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)