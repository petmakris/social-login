import mysql.connector
from jinja2 import Template

import logging
logger = logging.getLogger(__name__)

__all__ = [ 'EQ', 'NEQ', 'GT', 'LT', 'MiniDAO', 'render' ]

EQ   = '='
NEQ  = '<>'
GT   = '>'
LT   = '<'

def render(query, **params):
    return Template(query).render(**params)


class MiniDAO(object):

    def __init__(self, database, table, clasz, username='root', password='', hostname='localhost', verbose=False):
        self.database = database
        self.table = table
        self.clasz = clasz
        self.verbose = verbose

        self.all = ', '.join(clasz.columns())

        self.con = mysql.connector.connect(
            host=hostname,
            user=username,
            passwd=password,
            database=self.database)


    def render(self, q, **args):
        return render(q, all=self.all, table=self.table, **args)


    def execute(self, cursor, operation, params=None, multi=False):
        if self.verbose:
            logger.debug(operation)
        return cursor.execute(operation, params, multi)


    def findBy(self, column, arg, limit, oper=EQ):
        cur = self.con.cursor()

        q = self.render('SELECT {{all}} FROM {{table}} WHERE {{column}} {{oper}} %s',
            column=column,
            oper=oper)

        if limit:
            q += self.render(' LIMIT {{limit}}', limit=int(limit))
        v = (arg, )
        
        self.execute(cur, q, v)
        if limit == 1:
            res = cur.fetchone()
            if res is None:
                return None

            return self.clasz(*res)
        else:
            return [self.clasz(*values) for values in cur.fetchall()]

    
    def delete(self, user):
        self.deleteById(user.user_id)


    def deleteById(self, user_id):
        cur = self.con.cursor()
        q = self.render('DELETE FROM {{table}} WHERE user_id = %s')
        v = (user_id,)
        self.execute(cur, q, v)
        self.con.commit()


    def removeAll(self):
        cur = self.con.cursor()
        self.execute(cur, 'SET sql_safe_updates = 0')
        self.execute(cur, self.render('DELETE from {{table}}'))
        self.execute(cur, 'SET sql_safe_updates = 1')
        self.con.commit()


    def create(self, entity):
        cur = self.con.cursor()

        valueables = [entity.__getattribute__(name) for name in self.clasz.columns()]

        q = self.render(
            'INSERT INTO {{table}} ({{all}}) VALUES ({{values}})',
            values=', '.join(['%s' for j in valueables]))

        v = tuple(valueables)
        
        self.execute(cur, q, v)
        self.con.commit()
        return cur.lastrowid


    def update(self, entity):
        cur = self.con.cursor()

        columns = self.clasz.columns()
        values = [entity.__getattribute__(name) for name in self.clasz.columns()]

        update_values = ', '.join([ "%s='%s'" % (c, v) for (c, v) in zip(columns, values) ])

        q = self.render(
            "UPDATE {{table}} SET {{values}} WHERE user_id={{user_id}}",
            values=update_values,
            user_id=entity.user_id)

        self.execute(cur, q)
        self.con.commit()
        return cur.lastrowid
