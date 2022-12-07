from cgitb import html
from flask import Flask, render_template, request, redirect, url_for,session,flash
# import google.oauth2.credentials
# import google_auth_oauthlib.flow
# import flask 
# import functools
# import os 
#https://ankush-chavan.medium.com/creating-flask-application-with-mongodb-database-77ec45b5b995 
import google.oauth2.credentials
from authlib.integrations.requests_client import OAuth2Session
import json
from pymongo import MongoClient 
import os 
import functools
import google_auth
import subprocess as sp 
#from db.connect import mongopass
mongopass ="mongodb+srv://capstone1:capstone1@database1.l32rjl2.mongodb.net/?retryWrites=true&w=majority"
app = Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)
client = MongoClient(mongopass)
db = client.clientinfo
clientCollection = db.clientCollection 
app.debug = True 

from authentication_helper import check_sign_up,check_email_duplicates
from dao.crud import Crud

#app.register_blueprint(google_auth.app)

# @app.route('/login')
# def index():
#     if google_auth.is_logged_in():
#         user_info = google_auth.get_user_info()
#         return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info, indent=4) + "</pre>"

#     return 'You are not currently logged in.'

@app.route('/')
def home():
    date = sp.getoutput("date /t")
    return render_template("home.html",data=date)

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
    print(check_duplicates)
    if check_signup == True and check_duplicates == True:
             client_infor = {"email":email,"password":password}
             insertion = clientCollection.insert_one(client_infor)
             return redirect(url_for("signin"))
    if check_duplicates== False or check_signup == False:
            #  return redirect(url_for("signup"))
            return render_template("signup.html")
            
@app.route("/signin",methods=["POST","GET"])
def signin():
    if request.method =="GET":
        return render_template("signin.html")
    elif request.method == "POST":
       email = request.form["email"]
       password = request.form["password"]
       dic_info = {"email":email,"password":password}
    #    flash(dic_info)
       crud = Crud(dic_info)
       #print(crud.dic_data)
       if crud.find_one():
          return "Success"
    

    













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
