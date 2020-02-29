import unittest
from NeoGraphManager import NeoGraphManager
import uuid

class NeoGraphManagerTests(unittest.TestCase):
    
    def setUp(self):
        self.gm = NeoGraphManager(
        uri="bolt://127.0.0.1:7687",
        user="neo4j",
        password="password")

        self.testRunId = str(uuid.uuid4().hex)
        self.primaryTestLabel = f'UnitTest_{self.testRunId}'

    def tearDown(self):
        self.gm.deleteAllNodes(nodeLabel=self.primaryTestLabel)
        self.gm = None

    ###########################################################################
    def test_Node_crud_1(self):

        # create 
        test1label = f"UnitTest_{self.testRunId}_T1"
        n = self.gm.createNode(
            labels=[self.primaryTestLabel, test1label], 
            properties={ "name": "ParentNode1", "age": 60})
        assert n != None
        assert n['name'] == 'ParentNode1'
        assert n.identity > -1

        # read
        assert self.gm.getNodeCount(label=test1label) == 1
        readNode = self.gm.getNodes(
            nodeLabel=self.primaryTestLabel, property="name", operator='=', value="'ParentNode1'")
        assert readNode != None
        assert readNode[0]['name'] == 'ParentNode1'

        readNode = self.gm.getNodes(
            nodeLabel=test1label, property="name", operator='=', value="'ParentNode1'")
        assert readNode != None
        assert readNode[0]['name'] == 'ParentNode1'

        # delete
        self.gm.deleteAllNodes(nodeLabel=test1label)
        assert self.gm.getNodeCount(label=test1label) == 0

###########################################################################
    def test_Node_crud_2(self):

        test2label = f"UnitTest_{self.testRunId}_T2"

        tx = self.gm.startTransaction()

        # create         
        parentnode = self.gm.createNode(transaction=tx,
            labels=[self.primaryTestLabel, test2label], 
            properties={ "name": "ParentNode2", "age": 60})
        assert parentnode != None
        assert parentnode['name'] == 'ParentNode2'

        childnode = self.gm.createNode(
            labels=[self.primaryTestLabel, test2label], 
            properties={ "name": "ChildOfParentNode2", "age": 20})

        self.gm.createRelationship(sourceNode=parentnode, relationship="ParentOf", targetNode=childnode, transaction=tx)

        self.gm.commitTransaction(tx)

        # read
        assert self.gm.getNodeCount(label=test2label) == 2

        # delete
        self.gm.deleteAllNodes(nodeLabel=test2label)
        assert self.gm.getNodeCount(label=test2label) == 0

    ###########################################################################

if __name__ == '__main__':
    unittest.main()