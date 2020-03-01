from py2neo import Database, Graph, Node, Relationship, NodeMatcher, Transaction
import logging

class NeoGraphManager:
    '''
        A simple class to manage Neo4j object graphs
        using py2neo library
    '''

    def __init__(self,
                 uri: str = "bolt://localhost:7687",
                 user: str = "neo4j",
                 password: str = "password",
                 logger=None):

        self._graph = Graph(uri=uri, auth=(user, password))

        if logger:
            self._logger = logger
        else:

            formatter = logging.Formatter(
                '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)

            self._logger = logging.getLogger('NeoGraphManager')
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.ERROR)

    ###########################################################################
    def createNode(self, labels: list, properties: dict, transaction=None) -> Node:

        try:
            if not labels or len(labels) < 1:
                raise ValueError(
                    "labels needs to contain at least the primary node type")

            node = Node(*labels, **properties)

            if transaction:
                transaction.create(node)
            else:
                # create node within an autocommit transaction
                self._graph.create(node)

            self._logger.info(f"Created node {labels[0]}:{properties}")
            return node

        except Exception as ex:
            self._logger.exception(f"\nError creating node:", ex)
            raise

    ###########################################################################
    def createRelationship(self,
                           sourceNode: Node,
                           relationship: str, targetNode: Node, transaction=None) -> Relationship:

        rel = None
        self._logger.debug(f"Creating relationship:{relationship} ")
        try:
            if transaction:
                rel = transaction.create(Relationship(
                    sourceNode, relationship, targetNode))
            else:
                # create relationship within an autocommit transaction
                rel = self._graph.create(Relationship(
                    sourceNode, relationship, targetNode))

            self._logger.info(
                f"Created relationship:{relationship} between node#{sourceNode.identity} and node#{targetNode.identity}")
            return rel

        except Exception as ex:
            self._logger.exception(
                f"\nError creating relationship:{relationship} Error:", ex)
            raise
    ###########################################################################
    def createIndex(self, nodeLabel: str, field: str):

        self._logger.debug(f"Creating index on {nodeLabel}:{field}")
        try:
            query = f"CREATE INDEX ON :{nodeLabel}({field})"
            self._graph.run(query)

            self._logger.info(f"Created index on {nodeLabel}:{field}")
        except Exception as ex:
            self._logger.exception(f"\nError creating index:", ex)
            raise
    ###########################################################################
    def dropIndex(self, nodeLabel: str, field: str):

        self._logger.debug(f"Dropping index for {nodeLabel}:{field}")
        try:
            query = f"DROP INDEX ON :{nodeLabel}({field})"
            self._graph.run(query)

            self._logger.info(f"Dropped index for {nodeLabel}:{field}")
        except Exception as ex:
            self._logger.exception(f"\nError dropping index:", ex)
            raise
    ###########################################################################

    def createUniqueConstraint(self, nodeLabel: str, field: str):
        self._logger.debug(
            f"Creating unique constraint on {nodeLabel}:{field}")
        try:
            query = f"CREATE CONSTRAINT ON (n:{nodeLabel}) ASSERT n.{field} IS UNIQUE"
            self._graph.run(query)
            self._logger.info(
                f"Created unique constraint for {nodeLabel}:{field}")

        except Exception as ex:
            self._logger.exception(
                f"\nError creating unique constraint on {nodeLabel}:{field}:", ex)
            raise
    ###########################################################################

    def startTransaction(self) -> Transaction:
        tx = self._graph.begin()
        return tx

    ###########################################################################
    def queryResult(self, query):

        # example query: "MATCH (a:Person) RETURN a.name, a.born LIMIT 4"

        self._logger.debug(f"Executing query: {query}")

        result = self._graph.run(query).data()

        self._logger.debug(f"Result of query: {query} : {result}")
        return result

    ###########################################################################
    def getNodes(self,
                 nodeLabel: str,
                 property: str, operator: str, value: str,
                 orderByProperty: str = None,
                 nlimit: int = 10):
        '''
            This method will returns list of Nodes if the node property matches value.
            Returns [] if nothing matches.

            operators : = <> 	>  >= < <= 'STARTS WITH' 'ENDS WITH' 'CONTAINS'

            Refer to: https://py2neo.org/v4/matching.html?highlight=matcher#node-matching
        '''
        matcher = NodeMatcher(self._graph)

        matchQuery = f"_.{property} {operator} {value}"

        if orderByProperty:
            searchNodes = list(matcher.match(nodeLabel).where(
                matchQuery).order_by(f"_.{orderByProperty}").limit(nlimit))
        else:
            searchNodes = list(matcher.match(
                nodeLabel).where(matchQuery).limit(nlimit))

        self._logger.info(f"{len(searchNodes)} nodes matched search criteria")
        return searchNodes
    ###########################################################################
    def getNodeCount(self, label=None, properties: dict = None):

        count = 0

        if label:
            if properties:
                count = len(self._graph.nodes.match(label, **properties))
            else:
                count = len(self._graph.nodes.match(label))
        else:
            count = len(self._graph.nodes)

        self._logger.info(
            f"{count} nodes of type:{label} matched search criteria")
        return count

    ###########################################################################
    def deleteAllNodes(self, nodeLabel=None):
        if nodeLabel:
            self._logger.debug(f"Deleting all nodes of type:{nodeLabel}")
            deleteQuery = f'MATCH (n:{nodeLabel}) DETACH DELETE n'
            self._logger.debug(f"Deleted all nodes of type:{nodeLabel}")
        else:
            self._logger.debug(f"Deleting all nodes")
            deleteQuery = f'MATCH (n) DETACH DELETE n'
            self._logger.info(f"Deleted all nodes")

        return self.queryResult(query=deleteQuery)

###############################################################################
#                           FINISH                                            #
###############################################################################
