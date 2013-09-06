osmsna
======
extract a social network from a history openstreetmap file
http://planet.openstreetmap.org/planet/full-history/

steps
=====
1 - download a history planet file
http://planet.openstreetmap.org/planet/full-history/

2 - extract the area with osm-history-splitter

3 - import the data in postgis

4 - create the graph

 python netsosmers.py -s localhost -u dbuser -w dbpassword -d dbname -c -o graphfile 
 
 note: the "-c" calculate the interactions between user (this need time)

5 - analyze the graph with a tool like gephi
