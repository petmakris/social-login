import os
import cherrypy

from os.path import join, abspath, dirname
from social.conf import cherry_conf

import pickledb 

from jinja2 import Template, Environment, FileSystemLoader

ROOT          = abspath(join(dirname(__file__), '..'))
TEMPLATE_ROOT = join(ROOT, 'templates')
JINJA_LOADER  = FileSystemLoader(TEMPLATE_ROOT)
JINJA_ENV     = Environment(loader=JINJA_LOADER)
DB_FILEPATH   = join(ROOT, 'social.db')

DB            = pickledb.load(DB_FILEPATH, False)


def get_template(template_name):
    with open(join(TEMPLATE_ROOT, template_name)) as f:
        return JINJA_ENV.from_string(f.read())


class SocialButtons(object):

    @cherrypy.expose
    def index(self):
        return get_template('index.html').render()

    @cherrypy.expose
    def login(self):
        return get_template('login.html').render()

    @cherrypy.expose
    def register(self):
        return get_template('register.html').render()


def app():
    cherrypy.quickstart(SocialButtons(), '/', cherry_conf(ROOT))
