import os
import cherrypy
import pickledb 
import jinja2
import json
import base64
import requests

from social.conf import get_session_id
from social.conf import render
from social.conf import read_file_as_json
from social.conf import start_server

from social.auth_tools import google_jwt_to_auth_object
from social.auth_tools import facebook_token_to_auth_object

import urllib

ROOT          = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATES     = os.path.join(ROOT, 'templates')
DB            = pickledb.load(os.path.join(ROOT, 'social.db'), False)
CREDENTIALS   = read_file_as_json(os.path.join(ROOT, 'credentials.json'))

google_secret   = CREDENTIALS['google']
facebook_secret = CREDENTIALS['facebook']

class SocialButtons(object):

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
    def createUser(self, **url_params):
        return 'done'

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def google(self, id_token):
        return google_jwt_to_auth_object(id_token)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def facebook(self, access_token):
        return facebook_token_to_auth_object(access_token)

    @cherrypy.expose
    def logout(self):
        return ''


def app():
    start_server(ROOT, SocialButtons())
