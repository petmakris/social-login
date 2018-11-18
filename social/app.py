import os
import cherrypy
import simplejson
import base64
import requests
import urllib
import time

from social.conf import session, update_session
from social.conf import render
from social.conf import read_file_as_json
from social.conf import start_server
from social.conf import colorize

from social.auth_tools import googleTokenToAuthObject
from social.auth_tools import facebookTokenToAuthObject

from social.user import User
from social.users import Users

import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

ROOT          = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATES     = os.path.join(ROOT, 'templates')
CREDENTIALS   = read_file_as_json(os.path.join(ROOT, 'credentials.json'))
VENDORS       = ['google', 'facebook']

google_client_id   = CREDENTIALS['google-client-id']
google_secret      = CREDENTIALS['google-secrect']

facebook_client_id = CREDENTIALS['facebook-cliend-id']
facebook_secret    = CREDENTIALS['facebook-secrect']


def config():
    return {
        'google-client-id': google_client_id,
        'facebook-client-id': facebook_client_id
    }


# if 'sessionid' not in cherrypy.session:
#     cherrypy.session['sessionid'] = uuid.uuid4()

# return cherrypy.session['sessionid']

class SocialButtons(object):

    def __init__(self):
        self.users = Users()


    def isConnected(self):
        return session('connected') == True


    def currentUserId(self):
        user_id = session('user_id')
        if user_id is None:
            return None
        else:
            return user_id


    def currentUser(self):
        user_id = self.currentUserId()
        if user_id is None:
            return {}
        
        return self.users.findById(user_id).asDict()


    def model(self, model_data={}):
        m = {
            'config': config(),
            'version': int(time.time() * 10.0),
            'connected': self.isConnected(),
            'user': self.currentUser(),
            'data': model_data
        }
        return m


    def render(self, template, model={}):
        return render(TEMPLATES, template, self.model(model))


    @cherrypy.expose
    def index(self):
        return self.render('index.html')


    @cherrypy.expose
    def login(self):
        return self.render('login.html')


    @cherrypy.expose
    def register(self, **url_params):
        return self.render('register.html', url_params)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def token(self, vendor, token):
        if vendor == 'google':
            return self.handleAuth(googleTokenToAuthObject(token))

        elif vendor == 'facebook':
            return self.handleAuth(facebookTokenToAuthObject(token))

        else:
            return { 'error': 'Unknown Vendor [%s]' % vendor }


    def handleAuth(self, auth):
        """
        return the auth object to complete registration in case the user does not exist,
        or if the users exists login user and return { 'connected': True } 
        """

        if auth['vendor'] in VENDORS:
            if auth['vendor'] == 'google':
                u = self.users.findByGoogleId(auth['vid'])
                if u is not None:
                    u.google_email = auth['email']
                    self.users.update(u)
                    return self.loginUser(u)
                    
            if auth['vendor'] == 'facebook':
                u = self.users.findByFacebookId(auth['vid'])
                if u is not None:
                    u.facebook_email = auth['email']
                    self.users.update(u)
                    return self.loginUser(u)

            u = self.users.findByEmail(auth['email']) 
            if u is not None:
                if auth['vendor'] == 'google':
                    u.google_id = auth['vid']
                    u.google_email = auth['email']
                    self.users.update(u)
                    return self.loginUser(u)
                    
                
                if auth['vendor'] == 'facebook':
                    u.facebook_id = auth['vid']
                    u.facebook_email = auth['email']
                    self.users.update(u)
                    return self.loginUser(u)

        u = self.users.findByEmail(auth['email'])
        if u is not None:
            if u.password == auth['password']:
                if auth['vendor'] == 'google':
                    u.google_id = auth['vid']
                    u.google_email = auth['email']
                    self.users.update(u)
                    return self.loginUser(u)

                if auth['vendor'] == 'facebook':
                    u.facebook_id = auth['vid']
                    u.facebook_email = auth['email']
                    self.users.update(u)
                    return self.loginUser(u)

            else:
                return {
                    'connected': False,
                    'error': 'Incorrect password'
                    } 

        return auth


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def createUser(self, **auth):
        user = User.getUserFromAuthObject(auth)
        user_id = self.users.create(user) # check status
        return self.loginUser(self.users.findById(user_id))


    def loginUser(self, user):
        update_session('connected', True)
        update_session('user_id', user.user_id)
        return { 'connected': True }


    @cherrypy.expose
    def logout(self):
        update_session('connected', False)
        update_session('user_id', None)
        return { 'connected': False }


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getUsers(self):
        return [v.__dict__ for v in self.users.findAll()]


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getSession(self):
        return {
            'connected': self.isConnected(),
            'user_id': self.currentUserId()
        }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getModel(self):
        return self.model()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def deleteCurrentUser(self):
        if self.isConnected():
            user_id = self.currentUserId()
            self.logout()
            self.users.deleteById(user_id)
            return { 'deleted': True }
        
        return { 'error': 'Unexpected error' }



def app():
    logging.basicConfig(level=logging.DEBUG)
    Users().removeAll()
    start_server(ROOT, SocialButtons())

