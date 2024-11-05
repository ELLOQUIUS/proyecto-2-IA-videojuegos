import math
import numpy as np
import random
import pygame
from .Kinematic import Kinematic
from Archivos_principales.Grafo import Node,Graph

def newOrientation(current, velocity): # -> float
    # Make sure we have a velocity.
    vector_velocidad = np.array(velocity)
    rapidez = np.linalg.norm(vector_velocidad)
    if rapidez > 0:
        # Calculate orientation from the velocity.
        #return math.atan2(-velocity[0], velocity[1])
        return math.degrees(math.atan2(velocity[1], velocity[0]))

    # Otherwise use the current orientation.
    else:
        return current

def randomBinomial():
    return 2 * random.random() - 1

def mapToRange(angle):# -> float:
	return (angle + math.pi) % (2 * math.pi) - math.pi

def grados_a_radianes(grados):
    return grados * math.pi / 180

def radianes_a_grados(radianes):
    return radianes * (180 / math.pi)

def rotate_polygon(polygon, angle):
    return [point.rotate(angle) for point in polygon]

def calculate_angle(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    angle = math.degrees(math.atan2(dy, dx))
    return angle

def movimiento_teclado(keys,target,velocityT,rot):
    if keys[pygame.K_a]: # Escribo "pygame.K_(tecla)" para capturar la tecla que quiero
        target.position[0] -= velocityT
        if rot:
            target.orientation = 180
    if keys[pygame.K_d]:
        target.position[0] += velocityT
        if rot:
            target.orientation = 0
    if keys[pygame.K_w]:
        target.position[1] -= velocityT
        if rot:
            target.orientation = -90
    if keys[pygame.K_s]:
        target.position[1] += velocityT
        if rot:
            target.orientation = 90
    if keys[pygame.K_a] and keys[pygame.K_w] and rot:
        target.orientation = -135
    if keys[pygame.K_a] and keys[pygame.K_s] and rot:
        target.orientation = 135
    if keys[pygame.K_w] and keys[pygame.K_d] and rot:
        target.orientation = -45
    if keys[pygame.K_s] and keys[pygame.K_d] and rot:
        target.orientation = 45

def movimiento_teclado_borde(keys,target,velocityT,rot,teclas_vetadas):
    if keys[pygame.K_a] and not teclas_vetadas[0]: # Escribo "pygame.K_(tecla)" para capturar la tecla que quiero
        target.position[0] -= velocityT
        if rot:
            target.orientation = 180
    if keys[pygame.K_d] and not teclas_vetadas[2]:
        target.position[0] += velocityT
        if rot:
            target.orientation = 0
    if keys[pygame.K_w] and not teclas_vetadas[1]:
        target.position[1] -= velocityT
        if rot:
            target.orientation = -90
    if keys[pygame.K_s] and not teclas_vetadas[3]:
        target.position[1] += velocityT
        if rot:
            target.orientation = 90
    if keys[pygame.K_a] and not teclas_vetadas[0] and keys[pygame.K_w] and not teclas_vetadas[2] and rot:
        target.orientation = -135
    if keys[pygame.K_a] and not teclas_vetadas[0] and keys[pygame.K_s] and not teclas_vetadas[3] and rot:
        target.orientation = 135
    if keys[pygame.K_w] and not teclas_vetadas[1] and keys[pygame.K_d] and not teclas_vetadas[2] and rot:
        target.orientation = -45
    if keys[pygame.K_s] and not teclas_vetadas[3] and keys[pygame.K_d] and not teclas_vetadas[2]and rot:
        target.orientation = 45

def movimiento_asig_vetadas(keys,vetadas,ancho,alto,t4,velocity):
    if t4.position[0] >= ancho-2 and t4.position[1] < alto and t4.position[1] > 30:
        vetadas[2] = True
        movimiento_teclado_borde(keys,t4,velocity,False,vetadas)
    elif t4.position[0] >= ancho-2 and t4.position[1] >= alto:
        vetadas[2] = True
        vetadas[3] = True
        movimiento_teclado_borde(keys,t4,velocity,False,vetadas)
    elif t4.position[0] < ancho-2 and t4.position[0] > 30 and t4.position[1] >= alto:
        vetadas[3] = True
        movimiento_teclado_borde(keys,t4,velocity,False,vetadas)
    elif t4.position[0] <= 30 and t4.position[1] >= alto:
        vetadas[0] = True
        vetadas[3] = True
        movimiento_teclado_borde(keys,t4,velocity,False,vetadas)
    elif t4.position[0] <= 30 and t4.position[1] < alto and t4.position[1] > 30:
        vetadas[0] = True
        movimiento_teclado_borde(keys,t4,velocity,False,vetadas)
    elif t4.position[0] <= 30 and t4.position[1] <= 30:
        vetadas[0] = True
        vetadas[1] = True
        movimiento_teclado_borde(keys,t4,velocity,False,vetadas)
    elif t4.position[0] > 30 and t4.position[0] < ancho-2 and t4.position[1] <= 30:
        vetadas[1] = True
        movimiento_teclado_borde(keys,t4,velocity,False,vetadas)
    elif t4.position[0] >= ancho-2 and t4.position[1] <= 30:
        vetadas[1] = True
        vetadas[2] = True
        movimiento_teclado_borde(keys,t4,velocity,False,vetadas)
    else:
        movimiento_teclado_borde(keys,t4,velocity,False,vetadas)

def movimiento_teclado_cambio_velocity(keys,target,velocityT,rot):
    banda = False
    bandw = False
    bands = False
    bandd = False
    if keys[pygame.K_a]: # Escribo "pygame.K_(tecla)" para capturar la tecla que quiero
        banda = True
        target.velocity[0] = -velocityT;
        if rot:
            target.orientation = 180
    if keys[pygame.K_d]:
        bandd = True
        target.velocity[0] = velocityT;
        if rot:
            target.orientation = 0
    if keys[pygame.K_w]:
        bandw = True
        target.velocity[1] = -velocityT;
        if rot:
            target.orientation = -90
    if keys[pygame.K_s]:
        bands = True
        target.velocity[1] = velocityT;
        if rot:
            target.orientation = 90

    if keys[pygame.K_a] and keys[pygame.K_w] and rot:
        target.orientation = -135
    if keys[pygame.K_a] and keys[pygame.K_s] and rot:
        target.orientation = 135
    if keys[pygame.K_w] and keys[pygame.K_d] and rot:
        target.orientation = -45
    if keys[pygame.K_s] and keys[pygame.K_d] and rot:
        target.orientation = 45

    if not banda and not bandd:
        target.velocity[0] = 0
    if not bandw and not bands:
        target.velocity[1] = 0

def desacelerar(personaje, factor_desaceleracion):
    result = Kinematic([personaje.position[0],personaje.position[1]],[personaje.velocity[0],personaje.velocity[1]],personaje.orientation,personaje.rotation)
    
    if result.velocity[0] > 0:
        result.velocity[0] -= factor_desaceleracion
        if result.velocity[0] < 0:
            result.velocity[0] = 0
    if result.velocity[0] < 0:
        result.velocity[0] += factor_desaceleracion
        if result.velocity[0] > 0:
            result.velocity[0] = 0
    if result.velocity[1] > 0:
        result.velocity[1] -= factor_desaceleracion
        if result.velocity[1] < 0:
            result.velocity[1] = 0
    if result.velocity[1] < 0:
        result.velocity[1] += factor_desaceleracion
        if result.velocity[1] > 0:
            result.velocity[1] = 0

    return result
       
def pintar_mapa(ventana,ancho,alto,tamaño_c,nodos_bloqueados):
    tam_actual_x = 0
    tam_actual_y = 0
    numero_nodos_fila = 0
    numero_nodos_col = 0
    cont = 0
    fuente = pygame.font.Font(None, 12)
    cont_nod_bloq = 0
    i = 0
    while tam_actual_y < alto:
        numero_nodos_fila += 1
        i+=1
        while tam_actual_x < ancho:
            if i == 1:
                numero_nodos_col += 1
            
            if cont_nod_bloq < len(nodos_bloqueados):
                if cont == nodos_bloqueados[cont_nod_bloq]:                
                    pygame.draw.rect(ventana, (0, 0, 0), (tam_actual_x,tam_actual_y,tamaño_c,tamaño_c))
                    cont_nod_bloq += 1
                else:
                    pygame.draw.rect(ventana, (0, 0, 0), (tam_actual_x,tam_actual_y,tamaño_c,tamaño_c))
                    pygame.draw.rect(ventana, (211, 211, 211), (tam_actual_x+1,tam_actual_y+1,tamaño_c-1.5,tamaño_c-1.5))
                    pygame.draw.circle(ventana, (0,0,0), (tam_actual_x+tamaño_c/2, tam_actual_y+tamaño_c/2), tamaño_c-32)
                    pygame.draw.circle(ventana, (211, 211, 211), (tam_actual_x+tamaño_c/2, tam_actual_y+tamaño_c/2), tamaño_c-33)
                    Nombre_nodo = fuente.render(str(cont), True, (0, 0, 0))
                    ventana.blit(Nombre_nodo, (tam_actual_x+tamaño_c/2-4, tam_actual_y+tamaño_c/2-4))
            else:
                pygame.draw.rect(ventana, (0, 0, 0), (tam_actual_x,tam_actual_y,tamaño_c,tamaño_c))
                pygame.draw.rect(ventana, (211, 211, 211), (tam_actual_x+1,tam_actual_y+1,tamaño_c-1.5,tamaño_c-1.5))
                pygame.draw.circle(ventana, (0,0,0), (tam_actual_x+tamaño_c/2, tam_actual_y+tamaño_c/2), tamaño_c-32)
                pygame.draw.circle(ventana, (211, 211, 211), (tam_actual_x+tamaño_c/2, tam_actual_y+tamaño_c/2), tamaño_c-33)
                Nombre_nodo = fuente.render(str(cont), True, (0, 0, 0))
                ventana.blit(Nombre_nodo, (tam_actual_x+tamaño_c/2-4, tam_actual_y+tamaño_c/2-4))
            tam_actual_x += tamaño_c
            cont += 1
        tam_actual_x = 0
        tam_actual_y += tamaño_c
    return [numero_nodos_fila,numero_nodos_col]

def dibujar_linea(ventana,camino,actual,tamaño_cuadricula,columnas):
    # Busco automaticamente la posicion i,j de la posicion
    for i in range(actual,len(camino)):
        pos_x = camino[i].toNode.vectorPosicion[1]
        pos_y = camino[i].toNode.vectorPosicion[0]
        # Dibujo las lineas de tal forma que esten unidas y se conecten
        if camino[i].fromNode.vectorPosicion[0] == pos_y and camino[i].fromNode.vectorPosicion[1] < camino[i].toNode.vectorPosicion[1]:
            pygame.draw.line(ventana, (0,0,255), (pos_x * tamaño_cuadricula - tamaño_cuadricula/2 , pos_y * tamaño_cuadricula + tamaño_cuadricula/2), (pos_x * tamaño_cuadricula + tamaño_cuadricula - tamaño_cuadricula / 2,pos_y * tamaño_cuadricula + tamaño_cuadricula/2), 2)  
        elif camino[i].fromNode.vectorPosicion[0] == pos_y and camino[i].fromNode.vectorPosicion[1] > camino[i].toNode.vectorPosicion[1]:
            pygame.draw.line(ventana, (0,0,255), (pos_x * tamaño_cuadricula + tamaño_cuadricula/2 , pos_y * tamaño_cuadricula + tamaño_cuadricula/2), (pos_x * tamaño_cuadricula + tamaño_cuadricula + tamaño_cuadricula / 2,pos_y * tamaño_cuadricula + tamaño_cuadricula/2), 2)            
        elif camino[i].fromNode.vectorPosicion[1] == pos_x and camino[i].fromNode.vectorPosicion[0] > camino[i].toNode.vectorPosicion[0]:
            pygame.draw.line(ventana, (0,0,255), (pos_x * tamaño_cuadricula + tamaño_cuadricula/2 , pos_y * tamaño_cuadricula + tamaño_cuadricula/2), (pos_x * tamaño_cuadricula + tamaño_cuadricula/2 , pos_y * tamaño_cuadricula + tamaño_cuadricula + tamaño_cuadricula/2), 2)
        elif camino[i].fromNode.vectorPosicion[1] == pos_x and camino[i].fromNode.vectorPosicion[0] < camino[i].toNode.vectorPosicion[0]:
            pygame.draw.line(ventana, (0,0,255), (pos_x * tamaño_cuadricula + tamaño_cuadricula/2 , pos_y * tamaño_cuadricula - tamaño_cuadricula/2), (pos_x * tamaño_cuadricula + tamaño_cuadricula/2 , pos_y * tamaño_cuadricula + tamaño_cuadricula - tamaño_cuadricula/2), 2)
              
      
def crearGrafo(grafo,num_filas,num_col,nodos_bloqueados):
    tam = 0
    cont_nod_bloq = 0
    for i in range(num_filas):
        for j in range(num_col):
            if cont_nod_bloq < len(nodos_bloqueados):
                if j+tam == nodos_bloqueados[cont_nod_bloq]:                             
                    nodo = Node(j+tam,[i,j],1)
                    cont_nod_bloq += 1
                else:
                    nodo = Node(j+tam,[i,j],0)
            else:
                nodo = Node(j+tam,[i,j],0)
            grafo.insertarNodo(nodo)
        tam += num_col 

    for i in range(len(grafo.vectorGrafo)):
        if grafo.vectorGrafo[i].tipo == 0:
            if (i % num_col)-1 >= 0:
                if grafo.vectorGrafo[i-1].tipo == 0:
                    grafo.crearArista(i,i-1,1)
            if i-num_col > 0:
                if grafo.vectorGrafo[i-num_col].tipo == 0:
                    grafo.crearArista(i,i-num_col,1)
            if (i % num_col) + 1 < num_col:
                if grafo.vectorGrafo[i+1].tipo == 0:
                    grafo.crearArista(i,i+1,1)
            if i+num_col < len(grafo.vectorGrafo):
                if grafo.vectorGrafo[i+num_col].tipo == 0:
                    grafo.crearArista(i,i+num_col,1)
     
    return grafo
    
