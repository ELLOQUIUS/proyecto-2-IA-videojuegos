import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import random
from Clases.funciones import pintar_mapa,movimiento_asig_vetadas,crearGrafo,rotate_polygon,dibujar_linea
from Clases.Kinematic import Kinematic
from Grafo import Graph
from PathfindingAStar import pathfindAStar,Heuristic
from Clases.Seek import Seek
from Clases.Kinematic import Kinematic
from DecisionTree import DecisionTreeNodeP1,ActionP1

base = 15      # Parametro modificable
altura = 20    # Parametro modificable
arrow = [
    pygame.Vector2(0, -altura),  # Vértice superior
    pygame.Vector2(-base / 2, 0),  # Vértice inferior izquierdo
    pygame.Vector2(base / 2, 0)  # Vértice inferior derecho
]

tamaño_cuadricula = 40  # Parametro modificable

ancho = 0
alto = 0
pygame.init()
temp1 = int(input("Elije el ancho del mapa: "))
temp2 = int(input("Elije el alto del mapa: "))

radio_de_aceptacion = 20.5  # Parametro modificable. Aumentarlo si se aumenta la velocidad
nodos_bloqueados = [3,7,13,23,27,33,43,47,48,49,50,53,56,60,62,63,70,73,76,90,91,93,96,97,98,99,105,125,140,
                    141,142,145,146,147,148,150,151,153,156,157,158,162,176,182,185,186,187,188,190,191,192,
                    193,196,205,210,216,225,230,233,236,242,245,248,249,250,253,256,262,265,270,271,272,273,
                    276,277,278,285,305,306,307,320,321,322,327,330,334,336,337,338,339,347,350,354]

columnas = 0
filas = 0
while ancho < temp1:
    ancho += tamaño_cuadricula
    columnas += 1
while alto < temp2:
    alto += tamaño_cuadricula
    filas += 1

ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Mapa")
fuente = pygame.font.Font(None, 20)

# Eleccion de las posiciones iniciales del target, el personaje y la recarga. Cada una es diferente

numero_aleatorio_1 = random.randint(0, filas*columnas-1)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_1 == nodos_bloqueados[i]:
        numero_aleatorio_1 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_2 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_1)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_2 == nodos_bloqueados[i]:
        numero_aleatorio_2 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_3 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_2)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_3 == nodos_bloqueados[i]:
        numero_aleatorio_3 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

nodos_bloqueados.pop()
nodos_bloqueados.pop()     

nodo_objetivo = numero_aleatorio_1    # Parametro modificable
nodo_inicial = numero_aleatorio_2    # Parametro modificable
nodo_recarga = numero_aleatorio_3    # Parametro modificable'''

'''nodo_objetivo = 21    
nodo_inicial = 121    
nodo_recarga = 61 '''

temp = 0
pos_i_personaje = 0
pos_j_personaje = 0
pos_i_objetivo = 0
pos_j_objetivo = 0
pos_i_recarga = 0
pos_j_recarga = 0
# Busco automaticamente la posicion i,j del personaje
pos_j_personaje = nodo_inicial % columnas;
while temp + pos_j_personaje != nodo_inicial:
    temp += columnas
    pos_i_personaje += 1

# Busco automaticamente la posicion i,j del objetivo
temp = 0
pos_j_objetivo = nodo_objetivo % columnas;
while temp + pos_j_objetivo != nodo_objetivo:
    temp += columnas
    pos_i_objetivo += 1

# Busco automaticamente la posicion i,j de la recarga
temp = 0
pos_j_recarga = nodo_recarga % columnas;
while temp + pos_j_recarga != nodo_recarga:
    temp += columnas
    pos_i_recarga += 1

posicion_x_objetivo = pos_j_objetivo
posicion_y_objetivo = pos_i_objetivo
posicion_x_personaje = pos_j_personaje
posicion_y_personaje = pos_i_personaje
posicion_x_recarga = pos_j_recarga
posicion_y_recarga = pos_i_recarga

personaje1 = Kinematic([(tamaño_cuadricula*posicion_x_personaje)+tamaño_cuadricula/2,(tamaño_cuadricula*posicion_y_personaje)+tamaño_cuadricula/2],[0,0],0,0) # Personaje (Seek) 
target = Kinematic([(tamaño_cuadricula*posicion_x_objetivo)+tamaño_cuadricula/2,(tamaño_cuadricula*posicion_y_objetivo)+tamaño_cuadricula/2],[0,0],0,0) # Target (Seek)
target_aux = Kinematic([0,0],[0,0],0,0) # Target (Seek)
targetRecarga = Kinematic([(tamaño_cuadricula*posicion_x_recarga)+tamaño_cuadricula/2,(tamaño_cuadricula*posicion_y_recarga)+tamaño_cuadricula/2],[0,0],0,0)

ite = 0
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    ventana.fill((211, 211, 211))

    velocity = 7

    # Descomentar estas tres lineas si se quiere mover el cuadrado 
    #keys = pygame.key.get_pressed() # Para agarrar las teclas del teclado y mover el objetivo
    #vetadas = [False,False,False,False] # Vector auxiliar para cuando choque con un borde
    #movimiento_asig_vetadas(keys,vetadas,ancho,alto,target,velocity)

    num = pintar_mapa(ventana,ancho,alto,tamaño_cuadricula,nodos_bloqueados)
    ite += 1
    # Creo el grafo asociado:
    if ite == 1:
        grafo = Graph()
        grafo = crearGrafo(grafo,num[0],num[1],nodos_bloqueados)
        heuristica = Heuristic(grafo.vectorGrafo[nodo_objetivo])
        result = pathfindAStar(grafo,grafo.vectorGrafo[nodo_inicial],grafo.vectorGrafo[nodo_objetivo],heuristica)

        if len(result) > 0:
            target_aux.position[0] = (result[0].toNode.vectorPosicion[1] * tamaño_cuadricula) + tamaño_cuadricula/2
            target_aux.position[1] = (result[0].toNode.vectorPosicion[0] * tamaño_cuadricula) + tamaño_cuadricula/2
        k4 = Seek(personaje1,target_aux,0.03) # Busqueda del personaje al target (Seek)

        # Arbol de desicion de p1
        ener = 40 
        energia = [ener]
        ir_a_recargar = [False]
        camino_actual = [0]
        nodo_inicial_vec = [nodo_inicial]
        arbolDeP1 = DecisionTreeNodeP1(personaje1,target,nodo_inicial_vec,k4,target_aux,energia,radio_de_aceptacion,tamaño_cuadricula,result,camino_actual,grafo.vectorGrafo,ener,ir_a_recargar)        
        accion = arbolDeP1.makeDecision()
        if accion.opcion == 0:
            nodo_inicial = accion.nodo_inicial[0]
            accion.camino_actual[0] = 0
            result = pathfindAStar(grafo,grafo.vectorGrafo[nodo_inicial],grafo.vectorGrafo[nodo_objetivo],heuristica)
            arbolDeP1.path_result = result

    # Evaluo que decision debo tomar
    accion = arbolDeP1.makeDecision()

    # Si estoy en el objetivo, me tepeo
    if accion.opcion == 0:
        nodo_inicial = accion.nodo_inicial[0]
        heuristica = heuristica = Heuristic(grafo.vectorGrafo[nodo_objetivo])
        result = pathfindAStar(grafo,grafo.vectorGrafo[nodo_inicial],grafo.vectorGrafo[nodo_objetivo],heuristica)
        target_aux.position[0] = (result[0].toNode.vectorPosicion[1] * tamaño_cuadricula) + tamaño_cuadricula/2
        target_aux.position[1] = (result[0].toNode.vectorPosicion[0] * tamaño_cuadricula) + tamaño_cuadricula/2
        camino_actual = [0]
        nodo_inicial_vec = [nodo_inicial]
        # Creo otro arbol para p1, ahora con otro pathfinding
        arbolDeP1 = DecisionTreeNodeP1(personaje1,target,nodo_inicial_vec,k4,target_aux,energia,radio_de_aceptacion,tamaño_cuadricula,result,camino_actual,grafo.vectorGrafo,ener,ir_a_recargar)
    # Si no estoy en el objetivo, haggo path al objetivo
    
    # Si no tengo energia, mi objetivo sera el nodo de recarga y voy a recargar la energia.
    elif accion.opcion == 2:
        # Calculo el nodo actual donde p1 se quedó sin energia
        posicion_i_p1_s_e = round((personaje1.position[1] - tamaño_cuadricula/2) / tamaño_cuadricula)
        posicion_j_p1_s_e = round((personaje1.position[0] - tamaño_cuadricula/2) / tamaño_cuadricula)
        nodo_actual_p1 = (columnas * posicion_i_p1_s_e) + posicion_j_p1_s_e
        # Calculo el pathfinding entre el nodo actual de p1 y el nodo de recarga
        heuristica = heuristica = Heuristic(grafo.vectorGrafo[nodo_recarga]) 
        result = pathfindAStar(grafo,grafo.vectorGrafo[nodo_actual_p1],grafo.vectorGrafo[nodo_recarga],heuristica)

        # En caso de que justo pase que se me acabe la energia cuando estoy en el nodo de recargar energia
        if len(result) > 0:
            target_aux.position[0] = (result[0].toNode.vectorPosicion[1] * tamaño_cuadricula) + tamaño_cuadricula/2
            target_aux.position[1] = (result[0].toNode.vectorPosicion[0] * tamaño_cuadricula) + tamaño_cuadricula/2
            k4 = Seek(personaje1,target_aux,0.03) # Busqueda del personaje al target (Seek)
        camino_actual = [0]
        nodo_inicial_vec = [nodo_actual_p1]
        arbolDeP1 = DecisionTreeNodeP1(personaje1,targetRecarga,nodo_inicial_vec,k4,target_aux,energia,radio_de_aceptacion,tamaño_cuadricula,result,camino_actual,grafo.vectorGrafo,ener,ir_a_recargar)        

    rotated_arrow4 = rotate_polygon(arrow, k4.character.orientation + 90) # Seek '''   
    arrow_points4 = [([personaje1.position[0],personaje1.position[1]] + point) for point in rotated_arrow4] # Seek'''    
    pygame.draw.polygon(ventana, (0, 0, 255), arrow_points4) # Seek '''
    
    pygame.draw.rect(ventana, (255, 100, 10), (target.position[0]-15, target.position[1]-15, 30, 30)) # Seek '''
    pygame.draw.rect(ventana, (0, 150, 205), (targetRecarga.position[0]-15, targetRecarga.position[1]-15, 30, 30)) # Seek '''

    # Para cambiar el color de la energia
    if accion.energia[0] < ener/3:
        energiaText = fuente.render(str(accion.energia[0]), True, (255, 0, 0))
    elif accion.energia[0] > ener/3 and accion.energia[0] < ener/3 + ener/3:
        energiaText = fuente.render(str(accion.energia[0]), True, (255, 165, 0))
    else:
        energiaText = fuente.render(str(accion.energia[0]), True, (0, 255, 0))
    ventana.blit(energiaText, (personaje1.position[0]-15, personaje1.position[1]-25))

    dibujar_linea(ventana,result,camino_actual[0],tamaño_cuadricula,columnas)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

