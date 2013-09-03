#! /usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import logging

logger = logging.getLogger('osmsna_rewrite.global')

# ***** application (meta)data *****
APPNAME = 'osmsna_rewrite'

VERSION = '0.1'

BASE_DIR = os.path.dirname(os.path.normpath(os.path.realpath(sys.argv[0])))

CURR_DIR = os.path.abspath(os.path.normpath(os.getcwd()))

DESCRIPTION="""Description"""

EPILOG = """Copyright 2013 - Fondazione Bruno Kessler 
Author: Cristian Consonni.
This program is free software; you may redistribute it under the terms of
the GNU General Public License version 3 or (at your option) any later version. 
This program has absolutely no warranty."""
# ***** END application (meta)data *****

DBMS = 'postgresql'

HOST = "localhost"

PORT = 5432


def set_connection(dbname, 
                   user, 
                   password,
                   dbms=DBMS,
                   host=HOST,
                   port=PORT):

    engine = '{dbms}://{user}:{password}@{host}:{port}/{dbname}'.format(
                dbms=dbms,
                user=user,
                password=password,
                host=host,
                port=port,
                dbname=dbname
                )

    return engine






