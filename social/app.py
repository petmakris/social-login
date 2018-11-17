import os
import cherrypy
import json
import base64
import requests
import urllib

from social.conf import get_session_id
from social.conf import render
from social.conf import read_file_as_json
from social.conf import start_server
from social.conf import colorize

from social.auth_tools import google_jwt_to_auth_object
from social.auth_tools import facebook_token_to_auth_object

from social.users import Users

import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

ROOT          = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATES     = os.path.join(ROOT, 'templates')
CREDENTIALS   = read_file_as_json(os.path.join(ROOT, 'credentials.json'))

google_secret   = CREDENTIALS['google']
facebook_secret = CREDENTIALS['facebook']


def error(msg):
    return { 'error': msg }


class SocialButtons(object):

    def __init__(self):
        self.users = Users()


    @cherrypy.expose
    def index(self):
        return render(TEMPLATES, 'index.html')


    @cherrypy.expose
    def login(self):
        return render(TEMPLATES, 'login.html')


    @cherrypy.expose
    def register(self, **url_params):
        return render(TEMPLATES, 'register.html', url_params)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def google(self, id_token):
        auth = google_jwt_to_auth_object(id_token)
        # verify token?
        return self.handleAuth(auth)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def facebook(self, access_token):
        auth = facebook_token_to_auth_object(access_token)

        # verify token? nope for facebook
        return self.handleAuth(auth)


    def handleAuth(self, auth):
        # case should be covered: 
        # user exists but with other vendor or email/passwd
        # so update database information for user?

        # first check vendor id, if exists then we simply login the user
        # secondly 


        pass

        # if user is not None:
        #     self.loginUser(auth['email'])
        #     auth['status'] = 'connected'
        # return auth


    @cherrypy.expose
    def logout(self):
        return ''


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def createUser(self, **form):
        if len(form['vendor']):
            return self.registerWithVendor(form)
        else:
            return self.registerWithEmailAndPassword(form)


    @cherrypy.expose
    def loginUser(self, email):
        logger.info('Logged in user [%s]' % email)


    def registerWithVendor(self, params):

        user = ''

        # validate form data
        if user is None:
            return self.registerWithEmailAndPassword(params)
        else:
            logger.info('User [%s] already exists, merged')
            return {}


    def registerWithEmailAndPassword(self, params):
        email = params['email']



        # if users.get(email) is None:
        #     users[email] = params
        #     logger.info('Registered user [%s]' % params['email'])
        #     return {}
        # else:
        #     return error('User [%s] already exists' % email)



def app():
    print(Users())
    # start_server(ROOT, SocialButtons())

