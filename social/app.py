import os
import cherrypy
import pickledb 
import jinja2
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

import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


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

    @cherrypy.expose
    def create_user(self, **url_params):

        users = DB.get('users')
        
        if url_params['vendor'] is 'google':
            pass
            # {
            #     "devlang": "Java",
            #     "email": "petmakris@gmail.com",
            #     "first_name": "Petros",
            #     "last_name": "Makris",
            #     "password": "",
            #     "token": "",
            #     "vendor": "google",
            #     "vid": "109011938596560303242"
            # }

        elif url_params['vendor'] is 'facebook':
            pass

            # {
            #     "devlang": "Python",
            #     "email": "petmakris@gmail.com",
            #     "first_name": "Petros",
            #     "last_name": "Makris",
            #     "password": "",
            #     "token": "",
            #     "vendor": "facebook",
            #     "vid": "2290465577856262"
            # }

        else:
            logger.error('Uknown vendor')

        # check if user exists in database 

        logger.info(colorize(url_params))
        return 'done'


def app():
    try:
        if DB.get('users') is False:
            logger.info('Initializing users')
            DB.set('users', [])

        start_server(ROOT, SocialButtons())
    finally:
        DB.dump()

