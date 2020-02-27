# graphDbPoc
Testing out Neo4j Graph DB performance for large datasets


## Steps
Pull the latest Neo4j 4.0 Docker image

Start the Neo4j container
```
$ docker-compose up neo4j
```

Browse the database manager
```
http://127.0.0.1:17474/browser/
```
Login with username `neo4j` and password:`password`

## Drivers

* Python
```
$ pip install neo4j
```

* Dotnet
```
$ dotnet add package Neo4j.Driver --version 4.0.0
```

References

* []()
* [Neo4j Browser](https://neo4j.com/developer/neo4j-browser/)