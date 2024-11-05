

class Graph:
    # An array of connections outgoing from the given node.
    def __init__(self):
        self.vectorGrafo = []

    def insertarNodo(self,nodo):
        self.vectorGrafo.append(nodo)

    def crearArista(self,n1,n2,costo):
        self.vectorGrafo[n1].crearConexion(self.vectorGrafo[n2],costo)

    # Solo es dar las aristas del nodo pasado como parametro
    def getConnections(self,fromNode): # -> Connection[]   fromNode es un Node
        return fromNode.conexiones

class Connection:
    def __init__(self,fromNode,toNode,cost):   
        # The node that this connection came from.
        self.fromNode = fromNode # Node
        # The node that this connection leads to.
        self.toNode = toNode # Node
        # The non-negative cost of this connection.
        self.cost = cost #float
    def getCost(self): # -> float
       return self.cost

    def getFromNode(self):# -> Node
      return self.fromNode

    def getToNode(self):# -> Node
      return self.toNode

class Node:
    def __init__(self,nombre,vectorPosicion,tipo):
        self.nombre = nombre
        self.conexiones = []
        self.vectorPosicion = vectorPosicion
        # Para saber si es una pared o no
        self.tipo = tipo
    def crearConexion(self,nodo,costo):
        conexion = Connection(self,nodo,costo)
        self.conexiones.append(conexion)

