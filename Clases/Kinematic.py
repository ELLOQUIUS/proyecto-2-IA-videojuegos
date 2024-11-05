import math
import numpy as np

class Kinematic:
    def __init__(self,position, velocity, orientation, rotation):
        self.position = position        # vector
        self.orientation = orientation  # float
        self.velocity = velocity        # vector
        self.rotation = rotation        # float
    
    def asVector(self):
        radian = math.radians(self.orientation)
        x = math.cos(radian)
        y = math.sin(radian)
        return [x, y]

    def update(self,steering,maxSpeed,time): # steering es steeringoutput
        self.position[0] += self.velocity[0] * time
        self.position[1] += self.velocity[1] * time
        self.orientation += self.rotation * time

        # and the velocity and rotation.
        self.velocity[0] += steering.linear[0] * time
        self.velocity[1] += steering.linear[1] * time
        self.rotation += steering.angular * time

        # Check for speeding and clip.
        vector_velocidad = np.array(self.velocity)
        rapidez = np.linalg.norm(vector_velocidad)
        if rapidez > maxSpeed:

            temp = np.array(self.velocity)
            # Calcular la norma del vector
            norma = np.linalg.norm(temp)
            # Normalizar el vector
            vector_normalizado = temp / norma
            self.velocity = vector_normalizado * maxSpeed
