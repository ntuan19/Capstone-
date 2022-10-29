from flask import Flask, request, redirect, url_for,session
import google.oauth2.credentials
import google_auth_oauthlib.flow
import flask 
# from auth import login
app = Flask(__name__)
#app.secret_key = "capstone"


@app.route("/",methods=['GET'])
def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        '/Users/ntuan_195/Personal Projects/Capstone-/clientsecrets.json',
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"])

    flow.redirect_uri = "http://127.0.0.1:5000"
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    #code = input('Enter the authorization code: ')
    #flow.fetch_token(code=code)
    return flask.redirect(authorization_url)


@app.route("/signup",methods=['GET','POST'])
def signup():
    return "Hello there"
app.run(debug=True)
