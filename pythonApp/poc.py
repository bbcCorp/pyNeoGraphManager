from py2neo import Database, Graph, Node, Relationship

db = Database("bolt://0.0.0.0:7687")
default_db = Database()

graph = Graph(database=default_db)
graph.delete_all()

tx = graph.begin()

nicole = Node("Person", name="Nicole", age=24)
drew = Node("Person", name="Drew", age=20)

tx.create(nicole)
tx.create(drew)

mtdew = Node("Drink", name="Mountain Dew", calories=9000)
cokezero = Node("Drink", name="Coke Zero", calories=0)

tx.create(mtdew)
tx.create(cokezero)


coke = Node("Manufacturer", name="Coca Cola")
pepsi = Node("Manufacturer", name="Pepsi")

tx.create(coke)
tx.create(pepsi)

tx.commit()
print("Created nodes")

# Create Relationships
tx = graph.begin()
graph.create(Relationship(nicole, "LIKES", cokezero))
graph.create(Relationship(nicole, "LIKES", mtdew))

graph.create(Relationship(drew, "LIKES", mtdew))

graph.create(Relationship(coke, "MAKES", cokezero))
graph.create(Relationship(pepsi, "MAKES", mtdew))

tx.commit()
print("Created relationships")