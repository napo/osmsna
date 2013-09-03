#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
from osmers.settings import set_connection
from optparse import OptionParser
import sys
from osmers.graph import OSMNetGraph
# *** settings ***

# *** end settings ***

# ***** logging module objects and definition *****
LOGFORMAT_STDOUT = { logging.DEBUG: '%(module)s:%(funcName)s:%(lineno)s - %(levelname)-8s: %(message)s',
           logging.INFO: '%(levelname)-8s: %(message)s',
           logging.WARNING: '%(levelname)-8s: %(message)s',
           logging.ERROR: '%(levelname)-8s: %(message)s',
           logging.CRITICAL: '%(levelname)-8s: %(message)s'
         }

LOGFORMAT_FILE = { logging.DEBUG: "%(module)s:%(funcName)s:%(lineno)s - ***%(levelname)s***: %(message)s",
         logging.INFO: "%(asctime)s ***%(levelname)s***: %(message)s",
         logging.WARNING: "%(asctime)s ***%(levelname)s***: [%(module)s:%(funcName)s] %(message)s",
         logging.ERROR: "%(asctime)s *****%(levelname)s*****: ***[%(module)s:%(funcName)s:%(lineno)s]*** ***%(message)s***",
         logging.CRITICAL: "%(asctime)s *****%(levelname)s*****: ***[%(module)s:%(funcName)s:%(lineno)s]*** ***%(message)s***"
       }

LOGDATEFMT = '%Y-%m-%d %H:%M:%S'

class NullHandler(logging.Handler):
   def emit(self, record):
      pass
# ***** END logging module *****

# *** utilities ***

def netosmsers(cmd):
    dbserver = 'localhost'
    dbname = ''
    dbuser = ''
    dbpasswd = ''
    dbport = 5432
    graphfile = ''
    graphformat = 'gefx'
    interactions = False
    if (cmd.dbserver):
        dbserver = cmd.dbserver
    if (cmd.dbuser):
        dbuser = cmd.dbuser
    if (cmd.dbpasswd):
        dbpasswd = cmd.dbpasswd
    if (cmd.dbname):
        dbname = cmd.dbname
    if (cmd.dbport):
        dbport = cmd.dbport
    if (cmd.graphfile):
        graphfile = cmd.graphfile
    if (cmd.graphformat):
        graphformat = cmd.graphformat
    if (cmd.interactions):
        interactions = cmd.interactions    
    engine = set_connection(dbname=dbname,user=dbuser,password=dbpasswd,host=dbserver,port=dbport)
    osmnetgraph = OSMNetGraph(engine)
    if (interactions):
        osmnetgraph.generate_interactions()
    if (graphfile != ''):
        osmnetgraph.create_graph(graphfile,graphformat)
        
        
    
def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-s", "--dbserver", action="store", dest="dbserver", help="postgresql hostname (default=localhost)",default='localhost')
    parser.add_option("-u", "--dbuser", action="store", dest="dbuser", help="postgresql user")
    parser.add_option("-w", "--dbpassword", action="store", dest="dbpasswd", help="postgresql password")
    parser.add_option("-d", "--dbname", action="store", dest="dbname", help="postgresql password")
    parser.add_option("-p", "--dbport", action="store", dest="dbport", help="postgresql port (default=5432)",default=5432)
    parser.add_option("-o", "--graphfile", action="store", dest="graphfile", help="social network output file (without extension)")
    parser.add_option("-g","--graphformat",action="store",dest="graphformat",help="social network graph format: gexf (default),gml,pajek,graphml)",default='gexf')
    parser.add_option("-i", "--interactions", action="store_true", dest="interactions", help="calculate the users interactions",default=False) 
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="display status messages on the std output",default=False)    

    (options,args) = parser.parse_args()
    if (options.dbname == None) and ((options.graphfile == None) | (options.interactions == None)):
        parser.print_help()
        sys.exit(0)
    else:
        netosmsers(options)        
            
        
if __name__ == "__main__":
    main()




#if __name__ == '__main__':
#    rootlogger = logging.getLogger()
#    rootlogger.setLevel(logging.DEBUG)
#
#    lvl_config_logger = logging.DEBUG
#
#    console = logging.StreamHandler()
#    console.setLevel(lvl_config_logger)
#
#    formatter = logging.Formatter(LOGFORMAT_STDOUT[lvl_config_logger])
#    console.setFormatter(formatter)
#
#    rootlogger.addHandler(console)
#
#    logger = logging.getLogger(__name__)

 
