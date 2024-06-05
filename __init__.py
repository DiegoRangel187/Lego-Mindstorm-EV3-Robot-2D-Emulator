from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait
def main():
 # Inicializar el EV3
 ev3 = EV3Brick()
 # Inicializar un motor en el puerto A
 test_motor = Motor(Port.A)
 test_motor2 = Motor(Port.B)
 # Mueve el motor a una velocidad rotacional de 
 # 500 grados por segundo, durante 5 segundos 
 test_motor.run(10)
 test_motor2.run(10)
 wait (5000)
 # Detiene el motor
 test_motor.stop()
 test_motor2.stop()
#-----------------------------------------------------------
if __name__ == "__main__":
 main()