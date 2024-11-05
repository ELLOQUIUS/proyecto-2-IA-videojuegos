from .SteeringOutput import SteeringOutput
from .funciones import newOrientation
import numpy as np

class Seek: # And flee
    def __init__(self,character,target,maxAcceleration): 
        self.character = character # Kinematic
        self.target = target   # Kinematic
        self.maxAcceleration = maxAcceleration # float

    def getSteering(self): # -> SteeringOutput:
        result = SteeringOutput([0,0],0)
        # Get the direction to the target.
        # Change to character.position - target.position
        # for flee
        # Seek
        result.linear[0] = self.target.position[0] - self.character.position[0]
        result.linear[1] = self.target.position[1] - self.character.position[1]
        # Flee
        #result.linear[0] = self.character.position[0] - self.target.position[0]
        #result.linear[1] = self.character.position[1] - self.target.position[1]

        # Give full acceleration along this direction.
        temp = np.array(result.linear)
        # Calcular la norma del vector
        norma = np.linalg.norm(temp)
        if temp[0] == 0 and temp[1] == 0:
            vector_normalizado = np.array([0,0])
        else:
            vector_normalizado = temp / norma

        result.linear = vector_normalizado * self.maxAcceleration
        
        # Esta linea no esta en el algoritmo original, si quiero que cambie la orientacion la descomento
        self.character.orientation = newOrientation(self.character.orientation,result.linear)
        
        result.angular = 0 #si lo dejo asi, no rota, y en ningun momento se cambia la aceleracion angular

        return result