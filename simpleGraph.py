from neoGraphManager import NeoGraphManager

###############################################################################
def createNodesAndRelationships(gm: NeoGraphManager):
    
    # Delete all previous nodes
    gm.deleteAllNodes()

    print("Creating nodes ... ")
    # Create person nodes
    nicole = gm.createNode(
        labels=["Person"], 
        properties={ "name": "Nicole", "age": 24})
    assert nicole != None
    assert nicole['name'] == 'Nicole'    

    # Drew has additional label of student
    drew = gm.createNode(
        labels=["Person", "Student"], 
        properties={ "name": "Drew", "age": 20})
    assert drew != None
    assert drew['name'] == 'Drew'

    nCount = gm.queryResult(
        query='MATCH (n:Person) return count(distinct n)')
    print(f"Count of Person nodes in db: {nCount}")

    assert  gm.getNodeCount(label='Person') == 2

    # Create drink nodes
    mtdew = gm.createNode(
        labels=["Drink"], 
        properties={"name": "Mountain Dew", "calories": 9000})
    assert mtdew != None
    assert mtdew['name'] == 'Mountain Dew'

    cokezero = gm.createNode(
        labels=["Drink"], 
        properties={"name": "Coke Zero", "calories": 0})
    assert cokezero != None
    assert cokezero['name'] == 'Coke Zero'

    nCount = gm.queryResult(query='MATCH (n:Drink) return count(distinct n)')
    print(f"Count of Drink nodes in db: {nCount}")

    assert  gm.getNodeCount(label='Drink') == 2

    # Create manufacturer nodes
    coke = gm.createNode(
        labels=["Manufacturer"], 
        properties={ "name": "Coca Cola"})
    assert coke != None
    assert coke['name'] == 'Coca Cola'


    pepsi = gm.createNode(
        labels=["Manufacturer"], 
        properties={"name": "Pepsi"})
    assert pepsi != None
    assert pepsi['name'] == 'Pepsi'


    assert  gm.getNodeCount(label='Manufacturer') == 2
    
    nCount = gm.queryResult(
        query='MATCH (n:Manufacturer) return count(distinct n)')
    print(f"Count of Manufacturer nodes in db: {nCount}")

    assert  gm.getNodeCount() == 6

    # Create Relationships
    print("Creating relationships ...")

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

###############################################################################
def fetchNodes(gm: NeoGraphManager):

    n = gm.getNodes(nodeLabel="Person", property="name", operator='=', value="'Nicole'")
    assert len(n) > 0
    assert n[0]['name'] == 'Nicole'

    n = gm.getNodes(nodeLabel="Student", property="age", operator='=', value=20)
    assert len(n) > 0
    assert n[0]['name'] == 'Drew'
    assert n[0]['age'] == 20

    n = gm.getNodes(nodeLabel="Person", 
        property="age", operator='>=', value=20, orderByProperty='age')
    assert len(n) == 2
    assert n[0]['name'] == 'Drew'   
    assert n[0]['age'] == 20

    assert n[1]['name'] == 'Nicole' 
    assert n[1]['age'] == 24

###############################################################################
if __name__ == "__main__":
    gm = NeoGraphManager(
        uri="bolt://127.0.0.1:7687",
        user="neo4j",
        password="password")

    createNodesAndRelationships(gm)
    fetchNodes(gm)

###############################################################################