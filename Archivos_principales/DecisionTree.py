
import random
    
class ActionP1:
    def __init__(self,personaje,objetivo,nodo_inicial,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,camino_actual,vectorGrafo,recarga,ir_a_recargar,opcion):
        self.personaje = personaje
        self.objetivo = objetivo
        self.nodo_inicial = nodo_inicial
        self.kin = kin
        self.objetivoAUX = objetivoAUX
        self.energia = energia
        self.radio_de_aceptacion = radio_de_aceptacion
        self.tamaño_cuadricula = tamaño_cuadricula
        self.path_result = path_result
        self.camino_actual = camino_actual
        self.vectorGrafo = vectorGrafo
        self.recarga = recarga # Entero
        self.ir_a_recargar = ir_a_recargar
        self.opcion = opcion
        # Si ya llegue al nodo objetivo, cambio la posicion del personaje de manera aleatoria
        if opcion == 0:
            numero_aleatorio = random.randint(0, len(self.vectorGrafo)-1)
            while self.vectorGrafo[numero_aleatorio].tipo == 1:
                numero_aleatorio = random.randint(0, len(self.vectorGrafo)-1)
            self.personaje.position[0] = (self.tamaño_cuadricula * self.vectorGrafo[numero_aleatorio].vectorPosicion[1]) + self.tamaño_cuadricula/2
            self.personaje.position[1] = (self.tamaño_cuadricula * self.vectorGrafo[numero_aleatorio].vectorPosicion[0]) + self.tamaño_cuadricula/2 
            self.nodo_inicial[0] = numero_aleatorio
            self.camino_actual[0] = 0
            # Si ya estoy en el nodo para recargar y tengo que recargar, recargo la energia
            if self.ir_a_recargar[0] == True:
                self.energia[0] = recarga
                self.ir_a_recargar[0] = False

        # Si aun no llegue al nodo objetivo y aun tengo energia, hago el pathfinding a el nodo objetivo
        elif opcion == 1:
            if (self.personaje.position[0] <= self.objetivoAUX.position[0] + self.radio_de_aceptacion and self.personaje.position[0] >= self.objetivoAUX.position[0] - self.radio_de_aceptacion) and (self.personaje.position[1] >= self.objetivoAUX.position[1] - self.radio_de_aceptacion and self.personaje.position[1] <= self.objetivoAUX.position[1] + self.radio_de_aceptacion):
                self.objetivoAUX.position[0] = (self.tamaño_cuadricula * self.path_result[self.camino_actual[0]].toNode.vectorPosicion[1]) + self.tamaño_cuadricula/2
                self.objetivoAUX.position[1] = (self.tamaño_cuadricula * self.path_result[self.camino_actual[0]].toNode.vectorPosicion[0]) + self.tamaño_cuadricula/2
                self.kin.target = objetivoAUX
                self.camino_actual[0] += 1
                if self.energia[0] > 0:    
                    self.energia[0] -= 1       
            seek = self.kin.getSteering() # Me da un SteeringOutput. Realiza la busqueda (Seek) del personaje al target
            self.personaje.update(seek,0.5,2)
        else:
            self.ir_a_recargar[0] = True

    def makeDecision(self): # -> DecisionTreeNode:
        return self
    
class P1_decision:
    def __init__(self,personaje,objetivo,nodo_inicial,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,camino_actual,vectorGrafo,recarga,ir_a_recargar):
        self.personaje = personaje # Personaje
        self.objetivo = objetivo # Objetivo
        self.nodo_inicial = nodo_inicial # entero
        self.kin = kin # SteringOutput  
        self.objetivoAUX = objetivoAUX # Objetivo
        self.energia = energia # Entero 
        self.radio_de_aceptacion = radio_de_aceptacion # float
        self.tamaño_cuadricula = tamaño_cuadricula # entero
        self.path_result = path_result # Vector de posiciones
        self.camino_actual = camino_actual # numero de la posicion actual de result
        self.vectorGrafo = vectorGrafo # Vector de Nodos
        self.recarga = recarga # Entero
        self.ir_a_recargar = ir_a_recargar # Vector de bool
    # Defined in subclasses, with the appropriate type.
    def testValue(self):# -> any
        return
    
    # Perform the test.
    def getBranch(self):# -> DecisionTreeNode
        # Si ya llegue al nodo objetivo, cambio la posicion del personaje de manera aleatoria
        #print(self.personaje.position[0],self.personaje.position[1],"  ",self.objetivo.position[0] + self.radio_de_aceptacion,self.objetivo.position[0] - self.radio_de_aceptacion,self.objetivo.position[1] - self.radio_de_aceptacion,self.objetivo.position[1] + self.radio_de_aceptacion)
        if (self.personaje.position[0] <= self.objetivo.position[0] + self.radio_de_aceptacion and self.personaje.position[0] >= self.objetivo.position[0] - self.radio_de_aceptacion) and (self.personaje.position[1] >= self.objetivo.position[1] - self.radio_de_aceptacion and self.personaje.position[1] <= self.objetivo.position[1] + self.radio_de_aceptacion):
            action1 = ActionP1(self.personaje,self.objetivo,self.nodo_inicial,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.camino_actual,self.vectorGrafo,self.recarga,self.ir_a_recargar,0) 
            return action1.makeDecision()
        else:
            # Si aun no llegue al nodo objetivo y aun tengo energia, hago el pathfinding a el nodo objetivo
            if self.energia[0] > 0:
                action2 = ActionP1(self.personaje,self.objetivo,self.nodo_inicial,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.camino_actual,self.vectorGrafo,self.recarga,self.ir_a_recargar,1) 
                return action2.makeDecision()
            else:
                if self.ir_a_recargar[0]:
                    action2 = ActionP1(self.personaje,self.objetivo,self.nodo_inicial,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.camino_actual,self.vectorGrafo,self.recarga,self.ir_a_recargar,1) 
                    return action2.makeDecision()
                else:
                    action3 = ActionP1(self.personaje,self.objetivo,self.nodo_inicial,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.camino_actual,self.vectorGrafo,self.recarga,self.ir_a_recargar,2) 
                    return action3.makeDecision() 

    # Recursively walk through the tree.
    def makeDecision(self):# -> DecisionTreeNode
        # Make the decision and recurse based on the result.
        branch = self.getBranch() # DecisionTreeNode o Accion
        if str(type(branch)) == "<class 'DecisionTree.ActionP1'>":
            return branch
        else:
            return branch.makeDecision()
    
class DecisionTreeNodeP1:
    def __init__(self,personaje,objetivo,nodo_inicial,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,camino_actual,vectorGrafo,recarga,ir_a_recargar):
        self.personaje = personaje
        self.objetivo = objetivo
        self.kin = kin
        self.nodo_inicial = nodo_inicial
        self.objetivoAUX = objetivoAUX
        self.energia = energia
        self.radio_de_aceptacion = radio_de_aceptacion
        self.tamaño_cuadricula = tamaño_cuadricula
        self.path_result = path_result
        self.camino_actual = camino_actual
        self.vectorGrafo = vectorGrafo
        self.recarga = recarga # Entero
        self.ir_a_recargar = ir_a_recargar # Vector de bool
        self.decision = P1_decision(personaje,objetivo,nodo_inicial,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,camino_actual,vectorGrafo,recarga,ir_a_recargar)
        
    # Recursively walk through the tree.
    def makeDecision(self):
        return self.decision.makeDecision() # -> DecisionTreeNode
