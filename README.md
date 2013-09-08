# osmsna
extract a social network from a history openstreetmap file
http://planet.openstreetmap.org/planet/full-history/

## how use
1 - download a history planet file
http://planet.openstreetmap.org/planet/full-history/

2 - extract the area with osm-history-splitter

3 - create the file osmsna.style with this informations
```
node,way  osm_user       text
node,way  osm_uid        int8
node,way  osm_version    int8
node,way  osm_timestamp  text
```

4 - import the data in postgis
```bash
osm2pgsql -P 5433 -U dbuser -d dbname -m -x -k -S /path/of/osmsna.style file_history.osh
```

5 - create the graph
```bash
 python netsosmers.py -s localhost -u dbuser -w dbpassword -d dbname -i -o graphfile -g gexf
```
 note: the "-i" calculate the interactions between user (this need time)

6 - analyze the graph with a tool like gephi

## some example outputs
gefx file of the openstreetmap network of Trento - Italy

https://github.com/napo/osmsna/raw/master/examples/trento.gexf

viewer of the network in Trento - Italy

http://napo.github.io/osmsna/


image of the network in Trento - Italy

![trento osm network](https://raw.github.com/napo/osmsna/master/examples/trento_network.png)

