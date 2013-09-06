#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
from interactions import DBUsers
from areas import HDYC
from datetime import date
logger = logging.getLogger('osmers.graph')

import networkx as nx

class OSMNetGraph():
    engine = None
    dbuserdata = None
    FORMATS = {
        'gml': nx.write_gml,
        'gexf': nx.write_gexf,
        'net': nx.write_pajek,
        'graphml': nx.write_graphml
        }
    def __init__(self,engine):
        self.engine = engine
        self.dbuserdata = DBUsers(engine)

        
    def generate_interactions(self):
        oids = self.dbuserdata.get_osm_ids()
        self.dbuserdata.create_interaction_table(oids)
    
    def write_graph(self,gr, graphname, grtype='gml', **kwargs):
        nx_write = self.FORMATS[grtype.lower()]
        nx_write(gr,graphname,**kwargs)
        
    def create_graph(self,graphname,graphformat):
        g =  nx.DiGraph()
        hdyc = HDYC()
        YEAR = date.today().year
        users = self.dbuserdata.get_users()

        for uid, uname in users.iteritems():
            if uid is None:
                continue
            if uname is None:
                logger.warning('username is None, uid: {uid}'.format(uid=uid))
                continue

            uname=uname.decode('utf-8','ignore')

            logger.debug("uid: %s, name: %s" %(uid,uname))

            g.add_node(uid,label=uname)
            userdata = hdyc.user_data(uname)
            x = -999
            y = -999
            if userdata.has_key('activtyarea'):
                todecript = userdata['activtyarea']
                polygon =  hdyc.decode(todecript,5)
                centroid =  hdyc.center(polygon)
                ux, uy = centroid[0], centroid[1]
                x=ux
                y=uy
            else:
                if (userdata.has_key('node')):
                    x = userdata['node']['f_lon']                     
                    y = userdata['node']['f_lat']
                if (x != ""):
                    x = float(x)
                else:
    		    x = -999
                if (y != None):
                    y = float(y)
                else:
                    y = -999
            g.node[uid]['x'] = x
            g.node[uid]['y'] = y
            
            if (userdata.has_key('node')):
                first_changeset = userdata['node']['f_tstamp']
                g.node[uid]['first_changeset']=first_changeset	
                last_changeset = userdata['node']['l_tstamp']
                g.node[uid]['last_changeset']=last_changeset
    
            if (userdata.has_key('contributor')):	
                registered = userdata['contributor']['since']
                g.node[uid]['registered']=registered	
                img = userdata['contributor']['img']
                g.node[uid]['img']=img
                days_years = {}
                for yd in range(2004,YEAR+1):
                    days_years[str(yd)] = 0
    
            if userdata.has_key('changesets'):
                mapping_days = userdata['changesets']['mapping_days']
                years = mapping_days.split(";")
                tmp_years = {}
                for year in years:
                    y,d = year.split("=")
                    tmp_years[y]=d
                    for yd in range(2004,YEAR+1):
                         try:
                            days_years[str(yd)]=tmp_years[str(yd)]
                         except Exception:
                            pass
            for yd in range(2004,YEAR+1):
                    g.node[uid][str(yd)]=days_years[str(yd)]
        
        edges = self.dbuserdata.get_interactions()

    
        for e in edges:
            uid1, uid2, weight = e[0], e[1], e[2]
    
            logger.debug("Adding edge: <Edge(uid1 = {uid1}, uid2 = {uid2},weight = {weight})>".format(uid1=uid1,uid2=uid2,weight= weight))
            g.add_edge(uid1,uid2,weight=weight)

        self.write_graph(g,graphname+'.' + graphformat,graphformat)

if __name__ == '__main__':
    from settings import set_connection
    engine = set_connection(dbname='brunico',user='gis',password='gis',host='localhost',port=5432)
    ogn = OSMNetGraph(engine)
    ogn.create_graph('brunico','net')

