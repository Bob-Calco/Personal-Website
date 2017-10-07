from urllib.parse import quote, urlencode
from django.conf import settings
import base64
import json
import time
import requests
import uuid


### MANAGING AUTHORIZATION ###

# Client ID and secret
client_id = settings.OUTLOOK_CLIENT_ID
client_secret = settings.OUTLOOK_CLIENT_SECRET

# Constant strings for OAuth2 flow
# The OAuth authority
authority = 'https://login.microsoftonline.com'

# The authorize URL that initiates the OAuth2 client credential flow for admin consent
authorize_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/authorize?{0}')

# The token issuing endpoint
token_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/token')

# The scopes required by the app
scopes = [
    'openid',
    'User.Read',
    'Calendars.Read',
    'offline_access',
]

def get_signin_url(redirect_uri):
    # Build the query parameters for the signin url
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': ' '.join(str(i) for i in scopes)
    }

    signin_url = authorize_url.format(urlencode(params))

    return signin_url

def get_token_from_code(auth_code, redirect_uri):
    # Build the post from for the token request
    post_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'scope': ' '.join(str(i) for i in scopes),
        'client_id': client_id,
        'client_secret': client_secret
    }
    r = requests.post(token_url, data=post_data)

    try:
        return r.json()
    except:
        return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)

def get_token_from_refresh_token(refresh_token, redirect_uri):
  # Build the post form for the token request
  post_data = { 'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'redirect_uri': redirect_uri,
                'scope': ' '.join(str(i) for i in scopes),
                'client_id': client_id,
                'client_secret': client_secret
              }

  r = requests.post(token_url, data = post_data)

  try:
    return r.json()
  except:
    return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)

def get_access_token(request, redirect_uri):
    current_token = request.session['access_token']
    expiration = request.session['token_expires']
    now = int(time.time())
    if (current_token and now < expiration):
    # Token still valid
        return current_token
    else:
        # Token expired
        refresh_token = request.session['refresh_token']
        new_tokens = get_token_from_refresh_token(refresh_token, redirect_uri)

        # Update session
        # expires_in is in seconds
        # Get current timestamp (seconds since Unix Epoch) and
        # add expires_in to get expiration time
        # Subtract 5 minutes to allow for clock differences
        expiration = int(time.time()) + new_tokens['expires_in'] - 300

        # Save the token in the session
        request.session['access_token'] = new_tokens['access_token']
        request.session['refresh_token'] = new_tokens['refresh_token']
        request.session['token_expires'] = expiration

        return new_tokens['access_token']

### API CALLS ###

graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'

# Generic API Sending
def make_api_call(method, url, token, user_email, payload=None, parameters=None):
    # Send these headers with all API calls
    headers = {
        'User-Agent': 'Python_overtime_tracker/1.0',
        'Authorization': 'Bearer {0}'.format(token),
        'Accept': 'application/json',
        'X-AnchorMailbox': user_email
    }

    # Use these headers to instrument calls. Makes it easier
    # to correlate requests and responses in case of problems
    # and is a recommended best practice.
    request_id = str(uuid.uuid4())
    instrumentation = { 'client-request-id' : request_id,
                      'return-client-request-id' : 'true' }

    headers.update(instrumentation)

    response = None

    if (method.upper() == 'GET'):
        response = requests.get(url, headers = headers, params = parameters)
    elif (method.upper() == 'DELETE'):
        response = requests.delete(url, headers = headers, params = parameters)
    elif (method.upper() == 'PATCH'):
        headers.update({ 'Content-Type' : 'application/json' })
        response = requests.patch(url, headers = headers, data = json.dumps(payload), params = parameters)
    elif (method.upper() == 'POST'):
        headers.update({ 'Content-Type' : 'application/json' })
        response = requests.post(url, headers = headers, data = json.dumps(payload), params = parameters)
    return response

def get_me(access_token):
    get_me_url = graph_endpoint.format('/me')

    # Use OData query parameters to control the results
    #  - Only return the displayName and mail fields
    query_parameters = {'$select': 'displayName,mail'}

    r = make_api_call('GET', get_me_url, access_token, "", parameters = query_parameters)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)

def get_my_events(access_token, user_email, start_date, end_date):
    get_events_url = graph_endpoint.format('/me/events')

    query_parameters = {
        '$select': 'subject,start,end',
        '$top': 50, # default is 10
        '$filter': "end/dateTime gt '{0}' and start/dateTime lt '{1}'".format(start_date.strftime('%Y-%m-%dT%H:%M:%S'), end_date.strftime('%Y-%m-%dT%H:%M:%S')),
    }

    r = make_api_call('GET', get_events_url, access_token, user_email, parameters = query_parameters)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)
