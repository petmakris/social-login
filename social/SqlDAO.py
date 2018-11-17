import mysql.connector
from jinja2 import Template

import logging
logger = logging.getLogger(__name__)

__all__ = [ 'EQ', 'NEQ', 'GT', 'LT', 'SqlDAO', 'render' ]

EQ   = '='
NEQ  = '<>'
GT   = '>'
LT   = '<'

def render(query, **params):
    return Template(query).render(**params)


class SqlDAO(object):

    def __init__(self, database, table, columns=[], username='root', password='', hostname='localhost'):
        self.database = database
        self.table = table
        self.columns = columns

        self.all = ', '.join(self.columns)

        self.con = mysql.connector.connect(
            host=hostname,
            user=username,
            passwd=password,
            database=self.database)


    def render(self, q, **args):
        return render(q, all=self.all, table=self.table, **args)


    def execute(self, cursor, operation, params=None, multi=False):
        logger.debug(operation)
        return cursor.execute(operation, params, multi)


    def findBy(self, column, arg, limit, oper):
        cur = self.con.cursor()

        q = self.render('SELECT {{all}} FROM {{table}} WHERE {{column}} {{oper}} %s',
            column=column,
            oper=oper)

        if limit:
            q += self.render(' LIMIT {{limit}}', limit=int(limit))

        v = (arg, )
        
        self.execute(cur, q, v)
        return cur.fetchall()


    def removeAll(self):
        cur = self.con.cursor()
        self.execute(cur, 'SET sql_safe_updates = 0')
        self.execute(cur, self.render('DELETE from {{table}}'))
        self.execute(cur, 'SET sql_safe_updates = 1')
        self.con.commit()
