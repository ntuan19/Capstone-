import google.oauth2.credentials
import google_auth_oauthlib.flow


# def login():
#     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#         '/Users/ntuan_195/Personal Projects/Capstone-/clientsecrets.json',
#         scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'])

#     flow.redirect_uri = "http://127.0.0.1:5000"
#     authorization_url, state = flow.authorization_url(
#         # Enable offline access so that you can refresh an access token without
#         # re-prompting the user for permission. Recommended for web server apps.
#         access_type='offline',
#         # Enable incremental authorization. Recommended as a best practice.
#         include_granted_scopes='true')
    
