import json
import base64
import requests
import urllib

def google_jwt_to_auth_object(id_token):

    body = id_token.split('.')[1]
    body += '=' * ((4- len(body) % 4) % 4)

    auth_response = json.loads(base64.b64decode(body))
    
    return {
        'vid': auth_response['sub'],
        'vendor': 'google',
        'first_name': auth_response['given_name'],
        'last_name': auth_response['family_name'],
        'email': auth_response['email'],
        'token': id_token
    }

def facebook_token_to_auth_object(access_token):
    me_url = 'https://graph.facebook.com/me?' + urllib.parse.urlencode({
        'fields': 'email,name,first_name,last_name',
        'access_token': access_token
    })

    req = requests.get(me_url)

    if req.status_code is 200:
        auth_response = req.json()
        return {
            'vid': auth_response['id'],
            'vendor': 'facebook',
            'first_name': auth_response['first_name'],
            'last_name': auth_response['last_name'],
            'email': auth_response['email'],
            'token': access_token
        }
    else:
        print('error')
        return {}