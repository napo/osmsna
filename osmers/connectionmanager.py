#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import psycopg2
import logging
import urlparse

logger = logging.getLogger('osmsna.connectionmanager')


class ConnectionManager(object):
   
   def __init__(self, engine):
      self.engine = engine
   
   def connection_setup(self):
      self.con = psycopg2.connect(self.engine)
      logger.debug("Connecting to DB")
      return self.con
   
   def connection_close(self):
      logger.debug("Closing connection to DB")
      return self.con.close()
   
   
   def __call__(self, f):
      def wrapped(*args,**kwargs):
         self.connection_setup()
         self.cur=self.con.cursor()
         kwargs['con']=self.con
         kwargs['cur']=self.cur
         res=self.f(*args,**kwargs)
         self.connection_close()
         return res
      return wrapped


class Cursor(object):
    def __init__(self, engine):
        self.engine = engine
	result = urlparse.urlparse(engine)
	username = result.username
	password = result.password
	database = result.path[1:]
	hostname = result.hostname
	dbport = result.port
	self.connection = psycopg2.connect(
    		database = database,
    		user = username,
   		password = password,
    		host = hostname,
		port = dbport
	)
        self.cursor = self.connection.cursor()

    def __iter__(self):
        for item in self.cursor:
            yield item

    def __enter__(self):
        return self.cursor

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()


# ----- main -----
if __name__ == '__main__':
   pass
