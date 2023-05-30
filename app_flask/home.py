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
import os
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager.login_view = 'homepage'
login_manager.init_app(app)
# app.config.update(SECRET_KEY='osd(99092=36&462134kjKDhuIS_d23')

@login_manager.user_loader
def load_user(id):
    if storage.find(Mechanic, "id", id):
        return storage.find(Mechanic, "id", id)
    elif storage.find(Vendor, "id", id):
        return storage.find(Vendor, "id", id)
    elif storage.find(Client, "id", id):
        return storage.find(Client, "id", id)

@app.route('/', strict_slashes=False)
def homepage():
    """Render the homepage"""
    return render_template("index.html")

@app.route('/login/<user>', methods=["GET", "POST"], strict_slashes=False)
def login(user=None):
    """Render the homepage"""
    if request.method == "POST":
        data = request.form
        newdata = data.copy()
        if user == "vendor":
            user_obj = storage.find(Vendor, "email", newdata.get("email"))
            if not user_obj:
                flash("No user found with provided email.", category='error')
            elif user_obj and check_password_hash(user_obj.password, newdata.get("password")):
                flash('Login Successful', category='success')
                login_user(user_obj, remember=True)
                return redirect("/vendor")
            else:
                flash('Wrong password. Try again', category="error")

        if user == "mechanic":
            user_obj = storage.find(Mechanic, "email", newdata.get("email"))
            if not user_obj:
                flash("No user found with provided email.", category='error')
            elif user_obj and check_password_hash(user_obj.password, newdata.get("password")):
                flash('Login Successful', category='success')
                all_jobs = storage.openjobs()
                login_user(user_obj, remember=True)
                return redirect("/mechanic")
            else:
                flash('Wrong password. Try again', category="error")        
        
        if user == "client":
            user_obj = storage.find(Client, "email", newdata.get("email"))
            if not user_obj:
                flash("No user found with provided email.", category='error')
            elif user_obj and check_password_hash(user_obj.password, newdata.get("password")):
                flash('Login Successful', category='success')
                login_user(user_obj, remember=True)
                return redirect("/client")
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
                return redirect('/login/mechanic')
    return render_template("signup.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/test', strict_slashes=False)
def test_route():
    """Use this route to test new pages before integrating them"""
    return render_template("test_route.html")

@app.route('/vendor', strict_slashes=False)
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
    return render_template("vendor_orders.html", items=items, current_user=current_user)

@app.route('/vendor/delivered', strict_slashes=False)
@login_required
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
    # all_jobs = storage.openjobs()
    # mech_obj = storage.get(Mechanic, current_user.id)
    # for bid in mech_obj.bids:
    #     if bid.job in all_jobs:
    #         all_jobs.remove(bid.job)
    # mech_bids = storage.get(Mechanic, current_user.id).bids
    if request.method == "GET":
        all_jobs = storage.openjobs()
        mech_obj = storage.get(Mechanic, current_user.id)
        for bid in mech_obj.bids:
            if bid.job in all_jobs:
                all_jobs.remove(bid.job)
        return render_template("mechanic_homepage.html", all_jobs=all_jobs, current_user=current_user)
    if request.method == "POST":
        data = request.form
        newdata = data.copy()
        newdata['bid_amount'] = int(newdata['bid_amount'])
        bid_obj = Bid(**newdata)
        bid_obj.save()
        all_jobs = storage.openjobs()
        mech_obj = storage.get(Mechanic, current_user.id)
        for bid in mech_obj.bids:
            if bid.job in all_jobs:
                all_jobs.remove(bid.job)
        return render_template("mechanic_homepage.html", all_jobs=all_jobs, current_user=current_user)
    
@app.route('/mechanic/openbids', methods=['GET', 'POST'], strict_slashes=False)
def mechanic_openbids():
    """The route will show the open jobs"""
    mech_obj = storage.get(Mechanic, current_user.id)
    bids = mech_obj.bids
    bids_dict = []
    for bid in bids:
        bid_dict = {}
        job_obj = storage.get(Job, bid.job_id)
        if job_obj.job_status == 1:
            bid_dict['id'] = bid.id
            bid_dict['bid_amount'] = bid.bid_amount
            bid_dict['job_title'] = job_obj.job_title
            bid_dict['job_description'] = job_obj.job_description
            bids_dict.append(bid_dict)
    if request.method == "GET":
        return bids_dict
    if request.method == "POST":
        data = request.form
        newdata = data.copy()
        newdata['bid_amount'] = int(newdata['bid_amount'])
        bid_obj = storage.get(Bid, newdata['id'])
        bid_obj.bid_amount = newdata['bid_amount']
        bid_obj.save()
        return bids_dict
    
@app.route('/mechanic/activejos', strict_slashes=False)
def active_jobs():
    mech_obj = storage.get(Mechanic, current_user.id)
    bids = mech_obj.bids
    bids_dict = []
    for bid in bids:
        if bid.bid_status == 1:
            job_obj = storage.get(Job, bid.job_id)
            if job_obj.job_status != 0:
                bid_dict = {}
                bid_dict['id'] = bid.id
                bid_dict['bid_amount'] = bid.bid_amount
                bid_dict['job_title'] = job_obj.job_title
                bid_dict['job_description'] = job_obj.job_description
                bids_dict.append(bid_dict)
    return bids_dict

@app.route('/mechanic/completedjobs', strict_slashes=False)
def completed_jobs():
    mech_obj = storage.get(Mechanic, current_user.id)
    bids = mech_obj.bids
    bids_dict = []
    for bid in bids:
        if bid.bid_status == 1:
            job_obj = storage.get(Job, bid.job_id)
            if job_obj.job_status == 0:
                bid_dict = {}
                bid_dict['id'] = bid.id
                bid_dict['bid_amount'] = bid.bid_amount
                bid_dict['job_title'] = job_obj.job_title
                bid_dict['job_description'] = job_obj.job_description
                bids_dict.append(bid_dict)
    return bids_dict

@app.route('/mechanic/reviews', strict_slashes=False)
def mechanic_reviews():
    mech_obj = storage.get(Mechanic, current_user.id)
    reviews = mech_obj.reviews
    return reviews
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)