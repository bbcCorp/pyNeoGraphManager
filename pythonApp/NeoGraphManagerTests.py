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
    def test_1_Node(self):

        # create 
        testlabel = f"UnitTest_{self.testRunId}_T1"
        n = self.gm.createNode(
            labels=[self.primaryTestLabel, testlabel], 
            properties={ "name": "ParentNode1", "age": 60})
        assert n != None
        assert n['name'] == 'ParentNode1'
        assert n.identity > -1

        # read
        assert self.gm.getNodeCount(label=testlabel) == 1
        readNode = self.gm.getNodes(
            nodeLabel=self.primaryTestLabel, property="name", operator='=', value="'ParentNode1'")
        assert readNode != None
        assert readNode[0]['name'] == 'ParentNode1'

        readNode = self.gm.getNodes(
            nodeLabel=testlabel, property="name", operator='=', value="'ParentNode1'")
        assert readNode != None
        assert readNode[0]['name'] == 'ParentNode1'

        # delete
        self.gm.deleteAllNodes(nodeLabel=testlabel)
        assert self.gm.getNodeCount(label=testlabel) == 0

###########################################################################
    def test_2_NodeAndRelationship(self):

        testlabel = f"UnitTest_{self.testRunId}_T2"

        tx = self.gm.startTransaction()

        # create         
        parentNode = self.gm.createNode(transaction=tx,
            labels=[self.primaryTestLabel, testlabel], 
            properties={ "name": "ParentNode2", "age": 60})
        assert parentNode != None
        assert parentNode['name'] == 'ParentNode2'

        childNode = self.gm.createNode(
            labels=[self.primaryTestLabel, testlabel], 
            properties={ "name": "ChildOfParentNode2", "age": 20})

        self.gm.createRelationship(sourceNode=parentNode, relationship="ParentOf", targetNode=childNode, transaction=tx)

        self.gm.commitTransaction(tx)

        # read
        assert self.gm.getNodeCount(label=testlabel) == 2

        _nodes = self.gm.getNodes(nodeLabel=testlabel, 
            property="age", operator='>=', value=20, orderByProperty='age')
        assert len(_nodes) == 2
        assert _nodes[0]['age'] == 20
        assert _nodes[1]['age'] == 60

        # delete
        self.gm.deleteAllNodes(nodeLabel=testlabel)
        assert self.gm.getNodeCount(label=testlabel) == 0

###########################################################################
    def test_3_NodeAndRelationship_DeepGraph(self):

        testlabel = f"UnitTest_{self.testRunId}_T3"

        tx = self.gm.startTransaction()

        # create         
        parentNode = self.gm.createNode(transaction=tx,
            labels=[self.primaryTestLabel, testlabel], 
            properties={ "name": "grandParentNode", "age": 60})
        assert parentNode != None
        assert parentNode['name'] == 'grandParentNode'
        
        grandParentNode = parentNode

        for i in range(5):
            parentNode = self.gm.createNode(
                labels=[self.primaryTestLabel, testlabel], 
                properties={ "name": f"ParentNode{i+1}", "age": 20+i})
            assert parentNode != None

            self.gm.createRelationship(
                sourceNode=grandParentNode, relationship="ParentOf", targetNode=parentNode, transaction=tx)
            

            childNode = self.gm.createNode(
                labels=[self.primaryTestLabel, testlabel], 
                properties={ "name": f"ChildNode{i+1}", "age": 2+i})

            self.gm.createRelationship(
                sourceNode=parentNode, relationship="ParentOf", targetNode=childNode, transaction=tx)

            grandParentNode = parentNode

        self.gm.commitTransaction(tx)

        # read
        assert self.gm.getNodeCount(label=testlabel) == 11

        # test order-by query
        _nodes = self.gm.getNodes(nodeLabel=testlabel, 
            property="age", operator='>=', value=20, orderByProperty='age')
        assert len(_nodes) == 6
        assert _nodes[0]['age'] == 20
        assert _nodes[1]['age'] == 21
        assert _nodes[2]['age'] == 22
        assert _nodes[3]['age'] == 23
        assert _nodes[4]['age'] == 24
        assert _nodes[5]['age'] == 60

        # delete
        self.gm.deleteAllNodes(nodeLabel=testlabel)
        assert self.gm.getNodeCount(label=testlabel) == 0

    ###########################################################################

if __name__ == '__main__':
    unittest.main()