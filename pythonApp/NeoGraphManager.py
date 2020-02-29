from py2neo import Database, Graph, Node, Relationship, NodeMatcher, Transaction


class NeoGraphManager:
    def __init__(self,
                 uri="bolt://localhost:7687",
                 user="neo4j",
                 password="password",
                 defaultDb=None):

        if not defaultDb:
            defaultDb = Database()

        self._graph = Graph(uri=uri, auth=(user, password))

    ###########################################################################
    def createNode(self, nodeLabel, node: dict, transaction=None) -> Node:

        node = Node(nodeLabel, **node)

        if transaction:
            transaction.create(node)
        else:
            # create node within an autocommit transaction
            self._graph.create(node)

        return node

    ###########################################################################
    def createRelationship(self,
                           sourceNode: Node,
                           relationship: str, targetNode: Node, transaction=None) -> Relationship:

        rel = None
        if transaction:
            rel = transaction.create(Relationship(
                sourceNode, relationship, targetNode))
        else:
            # create relationship within an autocommit transaction
            rel = self._graph.create(Relationship(
                sourceNode, relationship, targetNode))

        return rel

    ###########################################################################
    def startTransaction(self) -> Transaction:
        tx = self._graph.begin()
        return tx

    ###########################################################################
    def commitTransaction(self, transaction: Transaction):
        transaction.commit()

    ###########################################################################
    def queryResult(self, query):

        # example query: "MATCH (a:Person) RETURN a.name, a.born LIMIT 4"
        result = self._graph.run(query).data()
        return result

    ###########################################################################
    def getNode(self, nodeLabel: str, property: str, value: str):
        '''
            This method will returns nodes if the node property matches value.
            Returns None if nothing matches.
        '''
        matcher = NodeMatcher(self._graph)
        searchNodes = matcher.match(nodeLabel).where(
            f"_.{property} = {value}")
        return searchNodes
    ###########################################################################

###############################################################################
if __name__ == "__main__":

    gm = NeoGraphManager(
        uri="bolt://127.0.0.1:7687",
        user="neo4j",
        password="password")

    # Delete all previous nodes
    gm.queryResult(query='MATCH (n) DETACH DELETE n')

    print("Creating nodes ... ")
    # Create person nodes
    nicole = gm.createNode(nodeLabel="Person", node={"name": "Nicole", "age": 24})
    drew = gm.createNode(nodeLabel="Person", node={"name": "Drew", "age": 20})

    nCount = gm.queryResult(
        query='MATCH (n:Person) return count(distinct n)')
    print(f"Count of Person nodes in db: {nCount}")

    # Create drink nodes
    mtdew = gm.createNode(nodeLabel="Drink", node={"name": "Mountain Dew", "calories": 9000})
    cokezero = gm.createNode(nodeLabel="Drink", node={"name": "Coke Zero", "calories": 0})

    nCount = gm.queryResult(query='MATCH (n:Drink) return count(distinct n)')
    print(f"Count of Drink nodes in db: {nCount}")

    # Create manufacturer nodes
    coke = gm.createNode(nodeLabel="Manufacturer", node={"name": "Coca Cola"})
    pepsi = gm.createNode(nodeLabel="Manufacturer", node={"name": "Pepsi"})

    nCount = gm.queryResult(
        query='MATCH (n:Manufacturer) return count(distinct n)')
    print(f"Count of Manufacturer nodes in db: {nCount}")

    # Create Relationships
    print("\n\n Creating relationships ...")

    gm.createRelationship(
        sourceNode=nicole, relationship="LIKES", targetNode=cokezero)
    gm.createRelationship(
        sourceNode=nicole, relationship="LIKES", targetNode=mtdew)

    gm.createRelationship(
        sourceNode=drew, relationship="LIKES", targetNode=mtdew)

    gm.createRelationship(
        sourceNode=coke, relationship="MAKES", targetNode=cokezero)
    gm.createRelationship(
        sourceNode=pepsi, relationship="MAKES", targetNode=mtdew)


    n = gm.getNode("PERSON", "name", "'Nicole'")
    print("Read node: ", n.first())
###############################################################################
###############################################################################