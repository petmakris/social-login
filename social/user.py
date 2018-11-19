import json

__all__ = [ 'User' ]

class User(object):

    def __init__(self, first_name=None, last_name=None, email=None,
                       password=None, devlang=None,
                       google_id=None, google_email=None,
                       facebook_id=None, facebook_email=None,
                       user_id=None):

        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.devlang = devlang
        self.google_id = google_id
        self.google_email = google_email
        self.facebook_id = facebook_id
        self.facebook_email = facebook_email

    
    
    @classmethod
    def getUserFromAuthObject(cls, auth):

        fn = auth['first_name']
        ln = auth['last_name']
        em = auth['email']
        pw = auth['password']
        dl = auth['devlang']
        gid, gem, fid, fem = ('', '', '', '')

        if auth['vendor'] == 'google':
            gid = auth['vid']
            gem = auth['email']
            em  = gem

        elif auth['vendor'] == 'facebook':
            fid = auth['vid']
            fem = auth['email']
            em  = fem

        return User(fn, ln, em, pw, dl, gid, gem, fid, fem)


    def asDict(self):
        return self.__dict__


    def __str__(self):
        return json.dumps(self.__dict__)


    def __json__(self):
        return self.__str__()


    @classmethod
    def columns(cls):
        return [
            'first_name', 'last_name', 'email', 'password', 'devlang',
            'google_id', 'google_email', 'facebook_id', 'facebook_email',
            'user_id',
        ]