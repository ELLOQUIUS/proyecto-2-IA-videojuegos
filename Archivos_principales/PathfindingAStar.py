from Grafo import Graph,Connection,Node
import queue
import math

# This structure is used to keep track of the 
# information we need for each node.
class NodeRecord:
    def __init__(self,node,connection,costSoFar,estimatedTotalCost,padre):
        self.node = node # Node
        self.connection = connection # Connection
        self.costSoFar = costSoFar # float
        self.estimatedTotalCost = estimatedTotalCost # float
        self.padre = padre # NodeRecord
    def __lt__(self, other): return self.estimatedTotalCost < other.estimatedTotalCost

class Heuristic:
    def __init__(self,goalNode) -> None:
        # Stores the goal node that this heuristic is estimating for.
        self.goalNode = goalNode # Node

    # Estimated cost to reach the stored goal from the given node.
               # Node
    def estimate(self,fromNode): # -> float
        return self.estimateToNode(fromNode, self.goalNode)

    # Estimated cost to move between any two nodes.
                    # Node     Node
    def estimateToNode(self,fromNode, toNode): #-> float
        # Aqui uso la distancia euclidiana de momento
        x1 = fromNode.vectorPosicion[0]
        y1 = fromNode.vectorPosicion[1]
        x2 = toNode.vectorPosicion[0]
        y2 = toNode.vectorPosicion[1]
        return math.sqrt(pow(x2-x1,2)+pow(y2-y1,2))

class PathfindingList:

    def __init__(self):
        self.cola_prioridad = queue.PriorityQueue()

    # returns the NodeRecord structure in the list with the lowest estimatedTotalCost value.
    def smallestElement(self):# -> NodeRecord
        result = self.cola_prioridad.queue[0]
        return result

    # returns true only if the list contains a NodeRecord structure 
    # whose node member is equal to the given parameter.
                # Node
    def contains(self,node):# -> bool
        for i in range(len(self.cola_prioridad.queue)):
            #  NodeRecord actual                   Nodo a revisar
            nodeRecordActual = self.cola_prioridad.queue[i][1].node.nombre 
            if nodeRecordActual == node.nombre:
                return True
        return False

    # returns the NodeRecord structure from the list whose node member
    # is equal to the given parameter.
            # Node
    def find(self,node):# -> NodeRecord
        for i in range(len(self.cola_prioridad.queue)):
            #  NodeRecord actual                   Nodo a revisar
            nodeRecordActual = self.cola_prioridad.queue[i][1].node.nombre 
            if nodeRecordActual == node.nombre:
                return self.cola_prioridad.queue[i][1]

                
def nada():
    return
                # Graph  Node   Node Heuristic
def pathfindAStar(graph, start, end, heuristic):# -> Connection[]:

    # Initialize the record for the start node.
    nodeNull = Node(-1,[-1,-1],0)
    connectionNull = Connection(nodeNull,nodeNull,0)
    nodeRecordNull = NodeRecord(nodeNull,connectionNull,-1,-1,None)

    startRecord = NodeRecord(start,connectionNull,0,heuristic.estimate(start),nodeRecordNull)

    # Initialize the open_ and closed lists.
    open_ = PathfindingList()
    open_.cola_prioridad.put((startRecord.estimatedTotalCost,startRecord))
    closed = PathfindingList()

    # Iterate through processing each node.
    while not open_.cola_prioridad.empty():
        # Find the smallest element in the open_ list (using the estimatedTotalCost).
        current = open_.smallestElement()

        # If it is the goal node, then terminate.
        if current[1].node.nombre == end.nombre:
            break

        # Otherwise get its outgoing connections.
        connections = graph.getConnections(current[1].node)

        # Loop through each connection in turn.
        for connection in connections:
            # Get the cost estimate for the end node.
            endNode = connection.getToNode()
            endNodeCost = current[1].costSoFar + connection.getCost()
            # If the node is closed we may have to skip, or 
            # remove it from the closed list.
            if closed.contains(endNode):
                # Here we find the record in the closed list 
                # corresponding to the endNode.
                endNodeRecord = closed.find(endNode)

                # If we didn’t find a shorter route, skip.
                if endNodeRecord.costSoFar <= endNodeCost:
                    continue

                # Otherwise remove it from the closed list.
                try:
                    closed.cola_prioridad.queue.remove(endNodeRecord)  
                except:
                    nada()

                # We can use the node’s old cost values to 
                # calculate its heuristic without calling the 
                # possibly expensive heuristic function.
                endNodeHeuristic = endNodeRecord.estimatedTotalCost - endNodeRecord.costSoFar

            # Skip if the node is open_ and we’ve not 
            # found a better route.
            elif open_.contains(endNode):
                # Here we find the record in the open_ list 
                # corresponding to the endNode.
                endNodeRecord = open_.find(endNode)
                # If our route is no better, then skip.
                if endNodeRecord.costSoFar <= endNodeCost:
                    continue

                # Again, we can calculate its heuristic.
                endNodeHeuristic = endNodeRecord.estimatedTotalCost - endNodeRecord.costSoFar

            # Otherwise we know we’ve got an unvisited 
            # node, so make a record for it.
            else:
                endNodeRecord = NodeRecord(endNode,connectionNull,0,0,current[1])
                #endNodeRecord.node = endNode
                
                # We’ll need to calculate the heuristic 
                # value using the function, since we don’t 
                # have an existing record to use.
                endNodeHeuristic = heuristic.estimate(endNode)

            # We’re here if we need to update the node. Update the 
            # cost, estimate and connection.
            endNodeRecord.costSoFar = endNodeCost # -> endNodeRecord.cost = endNodeCost
            endNodeRecord.connection = connection                   
            # Esta linea la agregue yo 
            #endNodeRecord.padre = connection.fromNode
            # (mierda) endNodeRecord.padre = NodeRecord(connection.fromNode,connectionNull,0,0,nodeRecordNull)   
            endNodeRecord.padre = current[1]               
            endNodeRecord.estimatedTotalCost = endNodeCost + endNodeHeuristic

            # And add it to the open_ list.
            if not open_.contains(endNode):
                open_.cola_prioridad.put((endNodeRecord.estimatedTotalCost,endNodeRecord))

        # We’ve finished looking at the connections for the 
        # current node, so add it to the closed list and remove 
        # it from the open_ list.
        open_.cola_prioridad.queue.remove(current) # open_ -= current
        closed.cola_prioridad.put((current[1].estimatedTotalCost,current[1])) # closed -= current

    # We’re here if we’ve either found the goal, or if we’ve no 
    # more nodes to search, find which.
    if current[1].node.nombre != end.nombre:
        # We’ve run out of nodes without finding the goal, so 
        # there’s no solution.
        return []

    # Compile the list of connections in the path.
    path = []

    # Work back along the path, accumulating 
    # connections.
    tempCurrent = current[1]
    while tempCurrent.node.nombre != start.nombre:
        path.append(tempCurrent.connection) # path += current.connection
        tempCurrent = tempCurrent.padre

    # Reverse the path, and return it.
    #return reverse(path)
    return path[::-1]