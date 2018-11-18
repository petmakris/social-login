import os
import json
import mysql.connector
from social.conf import read_file_as_json
from jinja2 import Template
from social.user import User
from social.dao import *

import logging
logger = logging.getLogger(__name__)

ROOT        = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CREDENTIALS = read_file_as_json(os.path.join(ROOT, 'credentials.json'))


class Users(MiniDAO):

    def __init__(self):
        super(Users, self).__init__(
            database='socialbuttons',
            table = 'users',
            clasz = User,
            username=CREDENTIALS['mysql-username'],
            password=CREDENTIALS['mysql-password'],
            verbose=False)


    def findById(self, user_id):
        return self.findBy('user_id', user_id, limit=1)


    def findByGoogleId(self, google_id):
        return self.findBy('google_id', google_id, limit=1)


    def findByGoogleEmail(self, google_email):
        return self.findBy('google_email', google_email, limit=1)


    def findByFacebookId(self, facebook_id):
        return self.findBy('facebook_id', facebook_id, limit=1)


    def findByFacebookEmail(self, facebook_email):
        return self.findBy('facebook_email', facebook_email, limit=1)


    def findByEmail(self, email):
        return self.findBy('email', email, limit=1)


    def findAll(self):
        return self.findBy('user_id', 0, None, oper=GT)



def app():
    logging.basicConfig(level=logging.DEBUG)

    users = Users()
    users.removeAll()

    users.create(User('A', 'AL', '1@google.com', 'pass', 'C', '101', '1@google.com', '1001', '1@facebook.com'))
    users.create(User('B', 'BL', '2@google.com', 'pass', 'C', '102', '2@google.com', '1002', '2@facebook.com'))
    users.create(User('C', 'CL', '3@google.com', 'pass', 'C', '103', '3@google.com', '1003', '3@facebook.com'))
    users.create(User('D', 'DL', '4@google.com', 'pass', 'C', '104', '4@google.com', '1004', '4@facebook.com'))
    users.create(User('E', 'EL', '5@google.com', 'pass', 'C', '105', '5@google.com', '1005', '5@facebook.com'))
    users.create(User('F', 'FL', '6@google.com', 'pass', 'C', '106', '6@google.com', '1006', '6@facebook.com'))

    assert len(users.findAll()) is 6

    u = users.findByEmail('5@google.com')
    u.google_id = 'new_google_id'
    users.update(u)

    assert users.findByGoogleId('new_google_id').user_id == u.user_id


