from pybricks.hubs import EV3Brick
from pybricks.ev3devices import UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait
''' Este programa lee la distancia en mm de un 
 sensor de ultrasonido
'''
def main():
 # Inicializar el EV3
 ev3 = EV3Brick()
 
 # Inicializar el sensor de ultrasonido en el puerto 2
 sensor_ultrasonido = UltrasonicSensor(Port.S2)
 # Imprimir la distancia en mm
 ev3.screen.print(sensor_ultrasonido.distance())
 
 # Esperar 5 segundos
 wait(5000)
#-----------------------------------------------------------
if __name__ == "__main__":
 main()