# NeoGraphManager

NeoGraphManager is a module to do the most common operations using Neo4j graph db.

Refer to the `simpleGraph.py` or the unit tests on how to use the module.

-------------------------------------------------------------------------------
## Installation

### Install Neo4j Server on Ubuntu

Use the following commands to install neo4j community edition on Ubuntu based distro.
```
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j
```

If you want to set default database to something other than `neo4j`, you can edit the file `/etc/neo4j/neo4j.conf` and change the following lines
```
# The name of the default database
dbms.default_database=neo4j
```

To start the service, use the command
```
$ sudo service neo4j start
```

### Use Neo4j Docker container
Pull the latest Neo4j 4.0 Docker image
```
$ docker pull neo4j 
```

Start the Neo4j container
```
$ docker-compose up -d neo4j
```

### Install dependencies
```
pip install -r ./requirements.txt
```

Browse the database manager
```
http://127.0.0.1:7474/browser/
```
Use the credentials username `neo4j` and password:`password`

Try connecting with bolt settings `bolt://0.0.0.0:7687` and `bolt://localhost:7687`

-------------------------------------------------------------------------------
## Drivers

* Python : `py2neo`

-------------------------------------------------------------------------------
## Query

Get a list of person and their drinks
```
MATCH (p:Person)-[r:LIKES]->(d:Drink) RETURN p, d LIMIT 25
```

To get a list with both the relationships
```
MATCH (p:Person)-[r1:LIKES]->(d:Drink),(m:Manufacturer)-[r2:MAKES]->(d:Drink) RETURN p,d,m LIMIT 25
```

```
MATCH (n) WHERE EXISTS(n.name) RETURN DISTINCT "node" as entity, n.name AS name LIMIT 25 UNION ALL MATCH ()-[r]-() WHERE EXISTS(r.name) RETURN DISTINCT "relationship" AS entity, r.name AS name LIMIT 25
```

-------------------------------------------------------------------------------
## References

* [Medium: Py2neo v4: The Next Generation](https://medium.com/neo4j/py2neo-v4-2bedc8afef2)
* [Graph Databases for Python Users](https://youtu.be/3JMhX1sT98U)
* [Neo4j Browser](https://neo4j.com/developer/neo4j-browser/)
