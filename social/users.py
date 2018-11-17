import os
import mysql.connector
from social.conf import read_file_as_json
from jinja2 import Template
from social.SqlDAO import *

import logging
logger = logging.getLogger(__name__)

ROOT        = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CREDENTIALS = read_file_as_json(os.path.join(ROOT, 'credentials.json'))

COLUMNS = [
    'first_name',
    'last_name',
    'email',
    'password',
    'devlang',
    'google_id',
    'google_email',
    'facebook_id',
    'facebook_email'
]

class Users(SqlDAO):

    def __init__(self):
        super(Users, self).__init__(
            database='socialbuttons',
            table = 'users',
            columns=COLUMNS,
            username=CREDENTIALS['mysql-username'],
            password=CREDENTIALS['mysql-password'])


    def create(self, *values):
        cur = self.con.cursor()
        
        valuables = ', '.join(['%s' for j in values])

        q = self.render(
            'INSERT INTO {{table}} ({{all}}) VALUES ({{values}})',
            values=valuables)

        v = values

        self.execute(cur, q, v)
        self.con.commit()
        return cur.lastrowid


    def findById(self, user_id, limit=None, oper=EQ):
        return self.findBy('user_id', user_id, limit, oper)


    def findByGoogleId(self, google_id, limit=None, oper=EQ):
        return self.findBy('google_id', google_id, limit, oper)


    def findByFacebookId(self, facebook_id, limit=None, oper=EQ):
        return self.findBy('facebook_id', facebook_id, limit, oper)


    def findByEmail(self, email, limit=None, oper=EQ):
        return self.findBy('email', email, limit, oper)


    def findAll(self):
        return self.findBy('user_id', 0, None, oper=GT)


    def update(self, user_id, ):
        pass



def app():
    logging.basicConfig(level=logging.DEBUG)

    users = Users()
    users.removeAll()

    n = users.create('petros', 'makris', 
        'petmakris@gmail.com', 'pass', 'devlang',
        'google_id', 'google_email', 'facebook_id', 'facebook_email')

    r = users.findAll()
    print(r)

