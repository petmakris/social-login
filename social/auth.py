import json
import base64
import requests
import urllib
import logging

import hmac
import simplejson as json
from base64 import urlsafe_b64decode
from hashlib import sha256

logger = logging.getLogger(__name__)

from social.conf import colorize
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests



def base64_url_decode(input):
    input += '=' * (4 - (len(input) % 4))
    return urlsafe_b64decode(input.encode('utf-8'))



def isGoogleValidReq(token, google_client_id, google_secret):
    r = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?' + urllib.parse.urlencode({
        'id_token': token,
    }))

    if r.status_code is not 200:
        logger.error('Invalid Token')
        return False

    d = r.json()

    return all([
        d['iss'] in ['accounts.google.com', 'https://accounts.google.com'],
        d['aud'] == google_client_id,
    ])


def isGoogleValidSig(token, google_client_id, google_secret):
    try:
        request = google_requests.Request()
        idinfo = id_token.verify_oauth2_token(token, request, google_client_id)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError()

        return True

    except:
        logger.info('Error validating token')
        return False


def isGoogleValid(*args, **kwargs):
    return isGoogleValidReq(*args, **kwargs)


def googleTokenToAuthObject(id_token, google_client_id, google_secret):

    body = id_token.split('.')[1]

    auth_response = json.loads(base64_url_decode(body))
    
    if isGoogleValid(id_token, google_client_id, google_secret):
        return {
            'connected': False,
            'vid': auth_response['sub'],
            'vendor': 'google',
            'first_name': auth_response['given_name'],
            'last_name': auth_response['family_name'],
            'email': auth_response['email'],
            'token': id_token
        }
    else:
        raise ValueError('Invalid Token')


def isFacebookValid(*args, **kwargs):
    return isFacebookValidReq(*args, **kwargs)


def parseFacebookSignedRequest(signed_request, facebook_secret):
    [encoded_signature, encoded_payload] = signed_request.split('.')
    
    signature = base64_url_decode(encoded_signature)

    payload = json.loads(base64_url_decode(encoded_payload))
    
    if payload['algorithm'].upper() != 'HMAC-SHA256':
        raise ValueError('Unknown algorithm [%s]. Expected HMAC-SHA256' % payload['algorithm'].upper())
    
    expected_signature = hmac.new(
        facebook_secret.encode('utf-8'),
        encoded_payload.encode('utf-8'), sha256).digest()

    if signature != expected_signature:
        raise ValueError('Bad Signed JSON signature!')
    
    return payload


def isFacebookValidReq(token, facebook_client_id, facebook_secret):
    try:
        r = requests.get('https://graph.facebook.com/debug_token?' + urllib.parse.urlencode({
            'input_token': token,
            'access_token': '%s|%s' % (facebook_client_id, facebook_secret)
        }))

        if r.status_code is not 200:
            raise ValueError()
       
        return r.json()['data']['is_valid']
        
    except:
        logger.error('Error validating token')
        return False


def facebookTokenToAuthObject(access_token, facebook_client_id, facebook_secret):
    me_url = 'https://graph.facebook.com/me?' + urllib.parse.urlencode({
        'fields': 'email,name,first_name,last_name',
        'access_token': access_token
    })

    req = requests.get(me_url)

    if req.status_code is 200:
        auth_response = req.json()

        if isFacebookValid(access_token, facebook_client_id, facebook_secret):
            return {
                'connected': False,
                'vid': auth_response['id'],
                'vendor': 'facebook',
                'first_name': auth_response['first_name'],
                'last_name': auth_response['last_name'],
                'email': auth_response['email'],
                'token': access_token
            }
        else:
            raise ValueError('Invalid Token')

    else:
        raise Exception('Invalid State')

