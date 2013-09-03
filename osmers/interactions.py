# -*- coding: utf-8 -*-

from connectionmanager import Cursor
class DBUsers():
    engine = None
    def __init__(self,engine):
        self.engine = engine
    
    def get_osm_ids(self):
       with Cursor(self.engine) as cur:
       		query="SELECT DISTINCT osm_id FROM planet_osm_point"
       		cur.execute(query)
       		res=cur.fetchall()
       		oids=frozenset([res[i][0] for i in range(len(res))])
       return oids
    
    def _create_tmp_interactions_table(self):
       with Cursor(self.engine) as cur:
       		query="""CREATE TABLE tmp_interactions(uid1 INT4, 
                                             uid2 INT4,
                                             weight INT4)"""
       		cur.execute(query)
    
    def _fill_tmp_interactions_table(self,oids):
       interactions=[]
       totoids=len(oids)
       i=0
       
       for oid in oids:
          i=i+1
          
          try:
              with Cursor(self.engine) as cur:
                  query="""SELECT osm_id, osm_uid, osm_version 
                     FROM planet_osm_point WHERE osm_id={oid} 
                     ORDER BY osm_version DESC""".format(oid=oid)
                  cur.execute(query)
                  interactions.append(cur.fetchall())
          except Exception as e:
             msg="Error: {err}".format(err=e)
             logger.error(msg)
             continue
    
       totints=len(interactions)
       i=0
       for it in interactions:
          i=i+1
    
          try:
             for k in reversed(range(2,len(it))):
                uid1=it[k][1]
                uid2=it[k-1][1]
                with Cursor(self.engine) as cur:
                    query="""INSERT INTO tmp_interactions(uid1,uid2,weight) 
                   	     VALUES({uid1},{uid2},1);
                   	     """.format(uid1=uid1,uid2=uid2)
                    cur.execute(query)
          except Exception as e:
             msg="Error: {err}".format(err=e)
             logger.error(msg)
             continue
       
       return interactions
    
    def _drop_tmp_interactions_table(self):
       try:
    	 with Cursor(self.engine) as cur:
          		query="DROP TABLE tmp_interactions;"
          		cur.execute(query)
          #con.commit()
       except Exception as e:
          msg="Error: {err}".format(err=e)
          print msg
          	#con.rollback()
          return None
    
    
    
    def create_interaction_table(self,oids):
    
       self._create_tmp_interactions_table()
    
       interactions=self._fill_tmp_interactions_table(oids)
       
       
       with Cursor(self.engine) as cur:
    		query="""CREATE TABLE interactions(id SERIAL, 
                                          uid1 INT4, 
                                          uid2 INT4,
                                          weight INT4)"""
       		cur.execute(query)
       		#con.commit()
    
       		query="""INSERT INTO interactions(uid1,uid2,weight)
            	    SELECT DISTINCT uid1,uid2,SUM(weight) AS weight
            	    FROM tmp_interactions
            	    GROUP BY uid1, uid2"""
       		cur.execute(query)
       #con.commit()
       
       self._drop_tmp_interactions_table()
    
       return interactions
    
    
    def drop_interaction_tables(self):
       
       logger.debug("Dropping interaction tables")
       try:
          tabledrop=[]
          with Cursor(self.engine) as cur:
          	query="""SELECT table_name 
          	         FROM information_schema.tables 
          	         WHERE table_name like '%interaction%';
          	      """
          	cur.execute(query)
          	res=cur.fetchall()
          	tabledrop=[r[0] for r in res]
       except Exception as e:
          msg="Error: {err}".format(err=e)
          print msg
          return None
    
       logger.debug("interaction tables to drop:")
       logger.debug(tabledrop)
       
       for t in tabledrop:
          try:
             query="DROP TABLE {table}".format(table=t)
             cur.execute(query)
             #con.commit()
          except Exception as e:
             msg="Error: {err}".format(err=e)
             print msg
             #con.rollback()
             return None
    
       logger.debug("Dropped interaction tables")
       
       return tabledrop
    
    def get_interactions(self):
        with Cursor(self.engine) as cur:
            query = """SELECT uid1, uid2, SUM(weight)
                        FROM interactions
                        GROUP BY uid1,uid2
                    """
    
            cur.execute(query)
            edges=cur.fetchall()
        
        return edges
    
    def get_users(self):
        with Cursor(self.engine) as cur:
            users=dict()
            query=""" SELECT osm_uid, osm_user 
                     FROM planet_osm_point 
                  """
            cur.execute(query)
            res=cur.fetchall()
    
        for i in range(len(res)):
            users[res[i][0]]=res[i][1]
    
        return users

if __name__ == '__main__':
   pass
