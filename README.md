# graphDbPoc
Testing out Neo4j Graph DB performance for large datasets

-------------------------------------------------------------------------------
## Steps

### Install Neo4j 
Pull the latest Neo4j 4.0 Docker image

Start the Neo4j container
```
$ docker-compose up -d neo4j
```

### Install dependencies
```
pip install -r ./pythonApp/requirements.txt
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
* Dotnet : `Neo4j.Driver`
-------------------------------------------------------------------------------
## Query

Get a list of person and their drinks
```
MATCH (p:Person)-[r:LIKES]->(d:Drink) RETURN p, d LIMIT 25
```



## References

* [Graph Databases for Python Users](https://youtu.be/3JMhX1sT98U)
* [Neo4j Browser](https://neo4j.com/developer/neo4j-browser/)