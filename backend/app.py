from cgitb import html
from flask import Flask, render_template, request, redirect, url_for,session,flash, abort
from functools import wraps
# import google.oauth2.credentials
# import google_auth_oauthlib.flow
# import flask 
# import functools
# import os 
#https://ankush-chavan.medium.com/creating-flask-application-with-mongodb-database-77ec45b5b995 
# import google.oauth2.credentials
# from authlib.integrations.requests_client import OAuth2Session
import json
from pymongo import MongoClient 
import os 
import functools
import google_auth
import subprocess as sp 
#from db.connect import mongopass
mongopass ="mongodb+srv://capstone1:capstone1@database1.l32rjl2.mongodb.net/?retryWrites=true&w=majority"
app = Flask(__name__)
app.debug = True
client = MongoClient(mongopass)
app.config['SECRET_KEY'] = 'Slay!12fsf34_sfsfsf'
app.config['WTF_CSRF_ENABLED'] = True
db = client.clientinfo

clientCollection = db.clientCollection 
from flask_wtf import FlaskForm
app = Flask(__name__, static_url_path='/static')
from investmentapi import connect_to_database, check_database, create_database
invesment_conn = connect_to_database()
create_database(invesment_conn)
print(check_database(invesment_conn))



from authentication_helper import check_sign_up,check_email_duplicates
from dao.crud import Crud
from dataform import InvestmentForm
from flask_wtf.csrf import CSRFProtect, validate_csrf, generate_csrf
csrf = CSRFProtect(app)
app.secret_key = "Slay13353"

import uuid
res = uuid.uuid4().hex
print(res)


@app.route('/')
def home():
    date = sp.getoutput("date /t")
    return render_template("hello.html",data=date)

@app.route('/home')
def account_creation():
    return render_template("home_inf.html")


@app.route("/signup",methods=["GET","POST"])
def signup_view():
    if request.method =="GET":
        return render_template("signup.html")
    # if request.method == "POST:
    #     return render_template("signup.html")

@app.route("/create_account")
def create_account():
    email = request.args.get("email")
    password = request.args.get("password")
    retype_password= request.args.get("retype")
    check_signup  =  check_sign_up(password,retype_password)
    check_duplicates = check_email_duplicates(email)
    if check_signup == True and check_duplicates == True:
             client_infor = {"email":email,"password":password}
             insertion = clientCollection.insert_one(client_infor)
             return redirect(url_for("signin"))
    if check_duplicates== False or check_signup == False:
            #  return redirect(url_for("signup"))
            return render_template("signup.html")
            
# @app.route("/signin",methods=["POST","GET"])
# def signin():
#     if request.method =="GET":
#         return render_template("signin.html")
#     elif request.method == "POST":
#        email = request.form["email"]
#        password = request.form["password"]
#        dic_info = {"email":email,"password":password}
#     #    flash(dic_info)
#        crud = Crud(dic_info)
#        #print(crud.dic_data)
#        if crud.find():
#             session["email"] = email
#             session["password"]= password
#             return redirect(url_for("account_crud"))
#        return redirect(url_for("signin"))

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

@app.route("/news_feed",methods=["POST","GET","UPDATE","DELETE"])
def news_feed():
    pass 

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session or "password" not in session:
            return redirect(url_for("signin"))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/investment_registration', methods=['GET', 'POST'])
@login_required
def investment_registration():
    form = InvestmentForm()
    if request.method == 'GET':
        return render_template('investment.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            token = request.form.get("csrf_token")
            #get the or unique user id 
            email = session["email"]
            password = session["password"]
            dic_info = {"email": email, "password": password}
            crud = Crud(dic_info)
            result = crud.find()
            unique_id = result["_id"]
            # process the form data
            # if validate_csrf(token):
            #     flash('CSRF validation not failed')
            #     sql = "INSERT INTO investments (investment_id, investment_poster_id, business_registration, business_address, company_name, current_round, presentation, pictures, financial_situation, approved) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            #     return 'Form submitted successfully!'
            # else:
            #     return "Invalid CSRF"
            investment_id = uuid.uuid4().hex
            # sql = "INSERT INTO investments (investment_id, investment_poster_id, business_registration, business_address, company_name, current_round, presentation, pictures, financial_situation, approved) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql = "INSERT INTO investments (investment_id, investment_poster_id, business_registration, business_address, company_name, current_round) VALUES (%s, %s, %s, %s, %s, %s)"
            investment_data = (
                investment_id,  
                unique_id, 
                form.business_registration.data,
                form.business_address.data,
                form.company_name.data,
                form.current_rounds.data)
                # form.presentation.data,
                # form.pictures.data,
                # form.financial_situation.data,
                # form.approved.data)
            cursor = invesment_conn.cursor()
            cursor.execute(sql, investment_data)
            invesment_conn.commit()

            sql_2 = "SELECT * FROM investments"
            cursor.execute(sql)

            # Fetch all the rows
            rows = cursor.fetchall()

            # Print the rows
            for row in rows:
                print(row)
            print(cursor.fetchall())
            
            cursor.close()
            print("Data")
            flash('Investment posted successfully!')
            return redirect(url_for('investment_registration'))

        else:
            # handle form validation errors
            return render_template('investment.html', form=form)
        
         
if __name__ == '__main__':
    app.debug = True
    app.run()









# # from auth import login
# app = Flask(__name__)
# #app.secret_key = "capstone"


# @app.route("/",methods=['GET'])
# def login():
#     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#         '/Users/ntuan_195/Personal Projects/Capstone-/clientsecrets.json',
#         scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"])

#     flow.redirect_uri = "http://127.0.0.1:5000"
#     authorization_url, state = flow.authorization_url(
#         # Enable offline access so that you can refresh an access token without
#         # re-prompting the user for permission. Recommended for web server apps.
#         access_type='offline',
#         # Enable incremental authorization. Recommended as a best practice.
#         include_granted_scopes='true')
#     #code = input('Enter the authorization code: ')
#     #flow.fetch_token(code=code)
#     return flask.redirect(authorization_url)


# @app.route("/signup",methods=['GET','POST'])
# def signup():
#     return "Hello there"
# app.run(debug=True)
