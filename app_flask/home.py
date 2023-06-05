#!/usr/bin/python3
"""Serve flask pages"""

from flask import Flask, render_template, request, flash, redirect, url_for, abort, jsonify, jsonify
from flask_mail import Mail, Message
import time
from models import storage
from models.vendor import Vendor
from models.order import Order
from models.job import Job
from models.part import Part
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

app.config['MAIL_SERVER'] = 'smtp.njogued.tech'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "ed@njogued.tech"
app.config['MAIL_PASSWORD'] = "KZukX^*^(3"

mail = Mail(app)

@login_manager.user_loader
def load_user(id):
    if storage.find(Mechanic, "id", id):
        return storage.find(Mechanic, "id", id)
    elif storage.find(Vendor, "id", id):
        return storage.find(Vendor, "id", id)
    elif storage.find(Client, "id", id):
        return storage.find(Client, "id", id)

@app.route('/', methods=["GET", "POST"], strict_slashes=False)
def homepage():
    """Render the homepage"""
    if request.method == "POST":
        data = request.form
        client_mail = data['email']
        message = Message(data['subject'],  sender='ed@njogued.tech',  recipients=['servicemtaani@gmail.com', client_mail])
        message.body = f"User Name: {data['full_name']}. Complaint: {data['message']}"
        mail.send(message)
        flash("Email sent successfully", category="success")
        return jsonify({"Message": "Complaint lodged"})
    return render_template("landing_page.html")

@app.route('/login/<user>', methods=["GET", "POST"], strict_slashes=False)
def user_login(user=None):
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
def user_signup(user=None):
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

@app.route('/test', methods=["GET", "POST"], strict_slashes=False)
def data_post():
    if request.method == "GET":
        return render_template("test_route.html")
    if request.method == "POST":
        text = request.data
        text = text.decode('UTF-8')
        print(text)
        return text

@app.route('/vendor', strict_slashes=False)
@login_required
def vendor_orders_route():
    """Use this route to render vendor orders"""
    vendor_obj = storage.get(Vendor, current_user.id)
    order_list = []
    for part in vendor_obj.parts:
        for order in part.orders:
            if order.status == True:
                order_info = {}
                client_obj = storage.get(Client, order.client_id)
                order_info['part_name'] = part.part_name
                order_info['part_price'] = part.part_price
                order_info['part_description'] = part.part_description
                order_info['client_name'] = f"{client_obj.first_name} {client_obj.last_name}"
                order_info['client_phone_number'] = client_obj.phone_number
                order_list.append(order_info)
    return render_template("vendor_orders.html", orders=order_list, current_user=current_user)

@app.route('/vendor/delivered', strict_slashes=False)
@login_required
def vendor_delivered():
    """Use this route to render the vendor's delivered orders"""
    vendor_obj = storage.get(Vendor, current_user.id)
    order_list = []
    for part in vendor_obj.parts:
        for order in part.orders:
            if order.status == False:
                order_info = {}
                client_obj = storage.get(Client, order.client_id)
                order_info['part_name'] = part.part_name
                order_info['client_name'] = f"{client_obj.first_name} {client_obj.last_name}"
                order_info['client_phone_number'] = client_obj.phone_number
                order_info['part_price'] = part.part_price
                order_info['part_description'] = part.part_description
                order_list.append(order_info)
    return render_template("vendor_delivered.html", orders=order_list, current_user=current_user)


@app.route('/vendor/catalogue', methods=["GET", "POST", "DELETE"], strict_slashes=False)
@login_required
def vendor_catalogue():
    """This route will return the vendor's catalogue"""
    vendor_obj = storage.get(Vendor, current_user.id)
    if request.method == "GET":
        return render_template("vendor_catalogue.html", items=vendor_obj.parts, current_user=current_user)
    if request.method == "POST":
        data = request.form
        newdata = data.copy()
        newdata = {k: v for k, v in newdata.items() if v}
        part_obj = storage.get(Part, newdata['part_id'])
        del newdata['part_id']
        for k, v in newdata.items():
            setattr(part_obj, k, v)
        part_obj.save()
        vendor_obj = storage.get(Vendor, current_user.id)
        return render_template("vendor_catalogue.html", items=vendor_obj.parts, current_user=current_user)
    if request.method == "DELETE":
        data = request.get_json()
        part_obj = storage.get(Part, data['part_id'])
        part_obj.delete()
        # vendor_obj = storage.get(Vendor, current_user.id)
        # return data
        return jsonify({'message': 'Part deleted successfully'}), 200

@app.route('/add_new_part', methods=['GET', 'POST'])
def vendor_parts():
    """Take in new part and add to db"""
    data = request.form
    newdata = data.copy()
    newdata = {k: v for k, v in newdata.items() if v}
    newdata['vendor_id'] = current_user.id
    part_obj = Part(**newdata)
    part_obj.save()
    return redirect(url_for('vendor_catalogue'))


@app.route('/mechanic/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def mechanic_jobs():
    """This route will render the mechanic home page"""
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

@app.route('/mechanic/openbids', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@login_required
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
            bid_dict['client_name'] = f'{job_obj.client.first_name} {job_obj.client.last_name}'
            bids_dict.append(bid_dict)
    if request.method == "GET":
        # return bids_dict
        return render_template("mechanic_bids.html", bids = bids_dict, current_user=current_user)
    if request.method == "POST":
        data = request.form
        newdata = data.copy()
        newdata['bid_amount'] = int(newdata['bid_amount'])
        bid_obj = storage.get(Bid, newdata['id'])
        bid_obj.bid_amount = newdata['bid_amount']
        bid_obj.save()
        return bids_dict
    if request.method == "DELETE":
        data = request.get_json()
        bid_obj = storage.get(Bid, data['bid_id'])
        bid_obj.delete()
        storage.save()

        return jsonify({"Message": "Bid deleted successfully"}), 200
        # return redirect("mechanic/openbids")
        # return render_template("mechanic_bids.html", bids = bids_dict, current_user=current_user)


@app.route('/mechanic/activejobs', strict_slashes=False)
@login_required
def active_jobs():
    mech_obj = storage.get(Mechanic, current_user.id)
    bids = mech_obj.bids
    bids_dict = []
    for bid in bids:
        if bid.bid_status == 1:
            job_obj = storage.get(Job, bid.job_id)
            if job_obj.job_status == 2:
                bid_dict = {}
                bid_dict['id'] = bid.id
                bid_dict['client_name'] = f'{job_obj.client.first_name} {job_obj.client.first_name}'
                bid_dict['client_phone_number'] = job_obj.client.phone_number
                bid_dict['client_id'] = job_obj.client.id
                bid_dict['bid_amount'] = bid.bid_amount
                bid_dict['job_title'] = job_obj.job_title
                bid_dict['job_description'] = job_obj.job_description
                bids_dict.append(bid_dict)
    return render_template("mechanic_active_jobs.html", jobs=bids_dict, current_user=current_user)

@app.route('/mechanic/completedjobs', strict_slashes=False)
@login_required
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
                bid_dict['client_name'] = f'{job_obj.client.first_name} {job_obj.client.last_name}'
                bids_dict.append(bid_dict)
    return render_template("mechanic_completed_jobs.html", jobs=bids_dict, current_user=current_user)

@app.route('/mechanic/reviews', strict_slashes=False)
@login_required
def mechanic_reviews():
    mech_obj = storage.get(Mechanic, current_user.id)
    reviews = mech_obj.reviews
    return reviews

@app.route('/client', methods=["GET", "POST", "PUT", "DELETE"], strict_slashes=False)
@login_required
def client_home():
    """Render the client homepage"""
    client_obj = storage.get(Client, current_user.id)
    if request.method == "GET":
        jobs = {}
        for job in client_obj.jobs:
            bids_list = []
            bids = storage.query_bids(current_user.id, job.id)
            count = 0
            if bids:
                for bid in bids:
                    count += 1
                    bid_info = {}
                    bid_info['job_title'] = job.job_title
                    bid_info['job_id'] = bid.job_id
                    bid_info['job_description'] = job.job_description
                    bid_info['bid_amount'] = bid.bid_amount
                    bid_info['bid_id'] = bid.id
                    bid_info['mechanic_phone'] = bid.mechanic.phone_number
                    bid_info['mechanic_name'] = f"{bid.mechanic.first_name} {bid.mechanic.last_name}"
                    bid_info['mechanic_rating'] = bid.mechanic.rating
                    bid_info['bid_count'] = count
                    bids_list.append(bid_info)
            if not bids:
                job_info = {}
                job_info['job_title'] = job.job_title
                job_info['job_description'] = job.job_description
                job_info['job_id'] = job.id
                bids_list.append(job_info)
            if job.job_status == 1:
                jobs[f'Job.{job.id}'] = bids_list
        # return jobs
        return render_template("client_homepage.html", title="Client Home", jobs=jobs, current_user=current_user)

    if request.method == "DELETE":
        my_dict = request.get_json()
        job_obj = storage.get(Job, my_dict['job_id'])
        job_obj.delete()
        storage.save()

        return jsonify({"Message": "Deleted and gone"})

    if request.method == "PUT":
        my_dict = request.get_json()

        bid_obj = storage.get(Bid, my_dict['bid_id'])
        bid_obj.bid_status = 1
        bid_obj.job.job_status = 2

        bid_obj.save()
        bid_obj.job.save()

        jobs = {}
        for job in client_obj.jobs:
            bids_list = []
            bids = storage.query_bids(current_user.id, job.id)
            count = 0
            if bids:
                for bid in bids:
                    count += 1
                    bid_info = {}
                    bid_info['job_title'] = job.job_title
                    bid_info['job_description'] = job.job_description
                    bid_info['bid_amount'] = bid.bid_amount
                    bid_info['bid_id'] = bid.id
                    bid_info['mechanic_phone'] = bid.mechanic.phone_number
                    bid_info['mechanic_name'] = f"{bid.mechanic.first_name} {bid.mechanic.last_name}"
                    bid_info['mechanic_rating'] = bid.mechanic.rating
                    bid_info['bid_count'] = count
                    bids_list.append(bid_info)
            if not bids:
                job_info = {}
                job_info['job_title'] = job.job_title
                job_info['job_description'] = job.job_description
                bids_list.append(job_info)
            if job.job_status == 1:
                jobs[f'Job.{job.id}'] = bids_list

        return render_template("client_homepage.html", title="Client Home", jobs=jobs, current_user=current_user)

    if request.method == "POST":
        my_dict = request.get_json()
        my_dict['client_id'] = current_user.id

        if not my_dict:
            abort(400, "Invalid input")

        else:
            job_obj = Job(**my_dict)
            job_obj.save()

        return job_obj.to_dict()


@app.route('/client/activejobs', methods=["GET", "POST"], strict_slashes=False)
@login_required
def client_active_jobs():
    active_jobs = storage.query_active_jobs(current_user.id)
    if request.method == "GET":
        jobs = {}
        for job in active_jobs:
            job_info = []
            bids = storage.query_winning_bid(job.id)
            for bid in bids:
                bid_info = {}
                bid_info['job_title'] = job.job_title
                bid_info['job_description'] = job.job_description
                bid_info['bid_amount'] = bid.bid_amount
                bid_info['bid_id'] = bid.id
                bid_info['mechanic_phone'] = bid.mechanic.phone_number
                bid_info['mechanic_name'] = f"{bid.mechanic.first_name} {bid.mechanic.last_name}"
                bid_info['mechanic_rating'] = bid.mechanic.rating
                job_info.append(bid_info)
            jobs[f'Job.{job.id}'] = job_info
        return render_template("client_active_jobs.html", title="Client Home", jobs=jobs, current_user=current_user)


@app.route('/client/completedjobs', methods=["GET", "POST"], strict_slashes=False)
@login_required
def client_completed_jobs():
    if request.method == "GET":
        completed_jobs = storage.query_completed_jobs(current_user.id)
        jobs = {}
        for job in completed_jobs:
            job_info = []
            bids = storage.query_winning_bid(job.id)
            for bid in bids:
                bid_info = {}
                bid_info['job_title'] = job.job_title
                bid_info['job_description'] = job.job_description
                bid_info['bid_amount'] = bid.bid_amount
                bid_info['bid_id'] = bid.id
                bid_info['mechanic_phone'] = bid.mechanic.phone_number
                bid_info['mechanic_name'] = f"{bid.mechanic.first_name} {bid.mechanic.last_name}"
                bid_info['mechanic_rating'] = bid.mechanic.rating
                job_info.append(bid_info)
            jobs[f'Job.{job.id}'] = job_info
        # return jobs
        return render_template("client_completed_jobs.html", title="Client Home", jobs=jobs, current_user=current_user)


@app.route('/client/myorders', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def client_orders():
    client_obj = storage.get(Client, current_user.id)
    order_list = []
    for order in client_obj.orders:
        order_info = {}
        order_info['order_id'] = order.id
        order_info['order_part_name'] = order.parts[0].part_name
        order_info['order_part_description'] = order.parts[0].part_description
        order_info['vendor_name'] = f'{order.parts[0].vendor.first_name} {order.parts[0].vendor.last_name}'
        order_info['vendor_phone_number'] = order.parts[0].vendor.phone_number
        order_info['part_price'] = order.parts[0].part_price
        order_list.append(order_info)
    # print(order_list)
    # return order_list
    if request.method == 'GET':
        return render_template("client_orders.html", title="Client Home", orders=order_list, current_user=current_user)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)