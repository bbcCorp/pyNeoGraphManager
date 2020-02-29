from py2neo import Database, Graph, Node, Relationship, NodeMatcher, Transaction

class NeoGraphManager:
    '''
        A class to manage Neo4j object graphs
        using py2neo library
    '''
    def __init__(self,
                 uri="bolt://localhost:7687",
                 user="neo4j",
                 password="password",
                 database=None):

        self._graph = Graph(uri=uri, auth=(user, password), database = database)

    ###########################################################################
    def createNode(self, labels: list, properties: dict, transaction=None) -> Node:

        try:
            if not labels or len(labels) < 1:
                raise ValueError("labels needs to contain at least the primary node type")

            node = Node(*labels, **properties)

            if transaction:
                transaction.create(node)
            else:
                # create node within an autocommit transaction
                self._graph.create(node)

            return node

        except Exception as ex:
            print("Error creating node", ex)
            raise


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
    def getNodes(self, 
        nodeLabel: str, 
        property: str, operator: str, value: str,
        orderByProperty: str = None,
        nlimit:int=10):
        '''
            This method will returns list of Nodes if the node property matches value.
            Returns [] if nothing matches.

            operators : = <> 	>  >= < <= 'STARTS WITH' 'ENDS WITH' 'CONTAINS'

            Refer to: https://py2neo.org/v4/matching.html?highlight=matcher#node-matching
        '''
        matcher = NodeMatcher(self._graph)

        matchQuery = f"_.{property} {operator} {value}"

        if orderByProperty:
            searchNodes = list(matcher.match(nodeLabel).where(matchQuery).order_by(f"_.{orderByProperty}").limit(nlimit))
        else:
            searchNodes = list(matcher.match(nodeLabel).where(matchQuery).limit(nlimit))

        return searchNodes
    ###########################################################################
    def getNodeCount(self, label=None, properties:dict = None):
        
        count = 0
              
        if label:
            if properties:
                count = len(self._graph.nodes.match(label, **properties))
            else:    
                count = len(self._graph.nodes.match(label))
        else:
            count = len(self._graph.nodes)
        
        return count

    ###########################################################################    
    def deleteAllNodes(self, nodeLabel=None):
        if nodeLabel:
            deleteQuery=f'MATCH (n:{nodeLabel}) DETACH DELETE n'
        else:
            deleteQuery=f'MATCH (n) DETACH DELETE n'

        return self.queryResult(query=deleteQuery)

###############################################################################
###############################################################################