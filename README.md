# NeoGraphManager

NeoGraphManager is a module to do the most common operations using Neo4j graph db.

Refer to the file [simple Graph example](simpleGraph.py) or the [unit tests](neoGraphManager/neoGraphManagerTests.py) on how to use the [NeoGraphManager](neoGraphManager/neoGraphManager.py) apis.

-------------------------------------------------------------------------------

## Prerequisite

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
## Cipher Query Language(CQL)

Neo4j [Cipher Query Language](https://neo4j.com/developer/cypher-query-language/) is a query language for Neo4j Graph Database.

Here's a short intro to using CQL:

The following Cypher commands are used on the `system` database to manage multiple databases:

* SHOW DATABASES              : Show the name and status of all the databases.
* SHOW DEFAULT DATABASE       : Show the name and status of the default database.

-------------
Select the default database and run the following commands in neo4j browser

* Delete any pre-existing nodes if required
```cypher
MATCH (n) DETACH DELETE n
```

* Creating a few nodes of type `Person`
```cypher
create (bbc:Person {name: 'BBC'})
```

* Read the node
```cypher
MATCH (bbc:Person {name: 'BBC'}) RETURN bbc
```

* We can create a relationship between two Person nodes using the following command
```cypher
CREATE (granddad:Person {name: 'Grand Dad', age:60})-[r:PARENT_OF]->(dad:Person {name: 'Dad', age:40})-[r2:PARENT_OF]->(son:Person {name: 'Son', age:5})
```

* Next, we will add two additional nodes `Grand Mom` and `Mom` and link it to the existing `Dad` and `Son` nodes

```cypher

CREATE (grandmom:Person {name: 'Grand Mom', age:55})
CREATE (mom:Person {name: 'Mom', age:38})

MERGE (gm:Person {name: 'Grand Mom'})
MERGE (d:Person {name: 'Dad'})
CREATE (gm)-[:PARENT_OF]->(d)

MERGE (m:Person {name: 'Mom'})
MERGE (s:Person {name: 'Son'})
CREATE (m)-[:PARENT_OF]->(s)
```
That should establish the relationship.

* Get a list of person and their relationships
```cypher
MATCH (p:Person)-[r:PARENT_OF]->(c:Person) RETURN p, c LIMIT 25
```

```cypher
MATCH (n) WHERE EXISTS(n.name) RETURN DISTINCT "node" as entity, n.name AS name LIMIT 25 UNION ALL MATCH ()-[r]-() WHERE EXISTS(r.name) RETURN DISTINCT "relationship" AS entity, r.name AS name LIMIT 25
```

-------------------------------------------------------------------------------
## References

* [Medium: Py2neo v4: The Next Generation](https://medium.com/neo4j/py2neo-v4-2bedc8afef2)
* [Graph Databases for Python Users](https://youtu.be/3JMhX1sT98U)
* [Neo4j Browser](https://neo4j.com/developer/neo4j-browser/)
* [The Py2neo v4 Handbook](https://py2neo.org/v4/index.html)
* [Neo4j Cipher Query Language](https://neo4j.com/developer/cypher-query-language/)