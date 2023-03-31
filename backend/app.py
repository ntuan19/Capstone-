
import base64, functools, json, os
import subprocess as sp
from cgitb import html
from functools import wraps

from flask import (Flask, abort, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_wtf import FlaskForm
from pymongo import MongoClient
from dotenv import load_dotenv


import google_auth
import stripe


# Database configuration
MONGO_PASS = "mongodb+srv://capstone1:capstone1@database1.l32rjl2.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_PASS)
db = client.clientinfo
clientCollection = db.clientCollection
investmentCollection = db.investment

# Flask app configuration
app = Flask(__name__, static_url_path='/static')
app.debug = True
app.config['SECRET_KEY'] = 'Slay!12fsf34_sfsfsf'
app.config['WTF_CSRF_ENABLED'] = True

load_dotenv()
from authentication_helper import check_sign_up,check_email_duplicates
from dao.crud import Crud
from dataform import InvestmentForm
from flask_wtf.csrf import CSRFProtect, validate_csrf, generate_csrf
csrf = CSRFProtect(app)
app.secret_key = "Slay13353" 
import uuid
res = uuid.uuid4().hex
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="investment_post",
    user="postgres",
    password="Elespolacoyovn19"
)


@app.route('/')
def home():
    date = sp.getoutput("date /t")
    return render_template("hello.html",data=date)

@app.route('/home')
def account_creation():
    return render_template("home_inf.html")


@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method =="GET":
        return render_template("signup.html")
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        retype_password= request.form["retype-password"]
        check_signup  =  check_sign_up(password,retype_password)
        check_duplicates = check_email_duplicates(email)
        if check_signup == True and check_duplicates == True:
            client_infor = {"email":email,"password":password}
            insertion = clientCollection.insert_one(client_infor)
            return redirect(url_for("signin"))
        else:
            return render_template("signup.html")

@app.route("/signin", methods=["POST","GET"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    elif request.method == "POST":
        print(request.form.get("csrf_token"))
        if not validate_csrf(request.form.get('csrf_token')):
            print("Yes")
            email = request.form["email"]
            password = request.form["password"]
            dic_info = {"email": email, "password": password}
            crud = Crud(dic_info)
            if crud.find():
                session["email"] = email
                session["password"] = password
                return redirect(url_for("account_crud"))
        return redirect(url_for("signin"))


@app.route("/accountinfor",methods=["POST","GET","UPDATE","DELETE"])
def account_crud():
    if request.method == "GET":
            if session["email"] and session["password"]:
                crud = Crud({"email":session["email"],"password":session["password"]})
                result = crud.find()
                dic_account_info = {"first_name":"N/A","last_name":"N/A","address":"N/A","phone_number":"N/A","date_of_birth":"N/A"}
                for key in dic_account_info:
                    if key in result:
                        dic_account_info[key] = result[key]
                return render_template("profile.html",dic=dic_account_info)
            return redirect(url_for("signin"))
    if request.method =="POST":
        if session["email"] and session["password"]:
            dic_account_info = {}
            dic_account_info["first_name"] = request.form["fname"]
            dic_account_info["last_name"] = request.form["lname"]
            dic_account_info["address"] = request.form["address"]
            dic_account_info["phone_number"] = request.form["phonenumber"]
            dic_account_info["date_of_birth"] = request.form["dateofbirth"]
            crud = Crud({"email":session["email"],"password":session["password"]})
            crud.update(dic_account_info)
        return render_template("profile.html", dic=dic_account_info)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session or "password" not in session:
            return redirect(url_for("signin"))
        return f(*args, **kwargs)
    return decorated_function

import binascii,json
from base64 import b64encode


@app.route("/news_feed",methods=["POST","GET","UPDATE"])
@login_required
def news_feed():
    results = investmentCollection.find({}, {'_id': 0})
    investments = []
    for investment in results:
        # Convert the binary image data to a base64-encoded string
        image_data = b64encode(investment['pictures']).decode('utf-8')
        # Create a data URI for the image
        investment['image_uri'] = f"data:image/jpeg;base64,{image_data}"
        investments.append(investment)
    return render_template("viewinvestment.html",investments=investments)

@app.route('/investment_registration', methods=['GET', 'POST'])
@login_required
def investment_registration():
    form = InvestmentForm()
    if request.method == 'GET':
        return render_template('investment.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            token = request.form.get("csrf_token")
            business_registration = form.business_registration.data
            business_address = form.business_address.data
            company_name = form.company_name.data
            current_rounds = form.current_rounds.data
            total_funding_wanted = form.total_funding_wanted.data
            currency = form.currency.data
            pictures = form.pictures.data
            financial_situation = form.financial_situation.data
            approved = False
            link_documents = form.link_documents.data
            # Create a new document with the extracted data
            investment = {
                'business_registration': business_registration,
                'business_address': business_address,
                'company_name': company_name,
                'current_rounds': current_rounds,
                'total_funding_wanted': float(total_funding_wanted),
                'currency': currency,
                'pictures': pictures.read(),
                "approved":approved,
                'financial_situation': financial_situation,
                'link_documents': link_documents
            }
            # Insert the new document into a MongoDB collection
            investment_infor = Crud(investment)
            result = investment_infor.insert_investment()
            if result != False:
                return jsonify({"Success":200})
            return redirect(url_for("investment_registration"))

#create news feeds api to retrieve all data.
        else:
            # Return a 400 Bad Request status code and the validation errors
            errors = form.errors
            response = jsonify(errors)
            response.status_code = 400
            return response          
@app.route("/get_csrf_token",methods=["GET"])
def get_csrf_token():
    token = generate_csrf()
    return jsonify({"csrf_token": token})

@app.route("/accountinfo/v/paymentinfo",methods = ["POST"])
#@login_required
def account_payment_infor():
    name = request.form["user_name"]
    card_number = request.form["card_number"]
    csv_code = request.form["csv_code"]
    exp_month = request.form["epx_month"]
    exp_year = request.form["epx_year"]
    # dic_info = {"email": session["email"], "password": session["password"]}
    #crud = Crud(dic_info).find()
    return "Success"


    # try:
    #     token = stripe.Token.create(
    #         card={
    #             "number": card_number,
    #             "exp_month": exp_month,
    #             "exp_year": exp_year,
    #             "cvc": csv_code,
    #         },
    #     )
    #     # if card information is correct, save data to PostgreSQL table
    #     conn = connect_postgres()
    #     cur = conn.cursor()
    #     cur.execute(
    #         "INSERT INTO your_table (name, card_number, csv_code, exp_month, exp_year) VALUES (%s, %s, %s, %s, %s)",
    #         (name, card_number, csv_code, exp_month, exp_year),
    #     )
    #     conn.commit()
    #     cur.close()
    #     conn.close()
    #     return "Card information saved successfully"
    # except stripe.error.CardError as e:
    #     # handle error
    #     return str(e)



@app.route("/payment",methods = ["POST"])
@login_required
def create_payment():
    pass 
    #firstly check if the users have entered the account yet 

    #if they already entered the account -> then if their account is valid ( charging 0.1USD)
    #if they have not entered account -> ask to put new account 
    #if the account is successfully verified and put in -> proceed to payment
    #payment: if payment successful -> save the data into the table, increase the total amount of money raised for specific investment
    #if it failed -> understand why it failed -> redirect customers to the new payment. 

@app.route("/logout", methods=["POST"])
def api_logout():
    if "logout" in request.json and request.json["logout"]:
        # Clear session
        session.pop("email", None)
        session.pop("password", None)
        return jsonify(success=True)
    else:
        return jsonify(success=False, error="Invalid request")

