import os
import cherrypy

from os.path import join, abspath, dirname
from social.conf import cherry_conf

root = abspath(join(dirname(__file__), '..'))

class SocialButtons(object):

    @cherrypy.expose
    def index(self):
        return open(join(root, join('templates', 'index.html')))

    @cherrypy.expose
    def login(self):
        return open(join(root, join('templates', 'login.html')))

    @cherrypy.expose
    def register(self):
        return open(join(root, join('templates', 'register.html')))


def app():
    cherrypy.quickstart(SocialButtons(), '/', cherry_conf(root))
