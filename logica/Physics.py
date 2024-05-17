from Object import Object

class PhysicsObject(Object):

    def __init__(self, coordinates:tuple[int]=(0,0), shape:tuple[int] = (0,0), color:tuple[int] = (0, 0), mass:int = 0):
        Object.__init__(self, coordinates, shape, color)
        self.maxSpeed:tuple[int] = (0, 0)
        self.acceleration:tuple[int] = (0, 0)
        self.massCenter:tuple[int] = self.bounds.center
        self.torque:tuple[int] = (0, 0)
        self.mass:int = mass

    def setSpeed(self, speed:tuple[int]):
        self.maxSpeed = speed

    def setAcceleration(self, acceleration:tuple[int]):
        self.acceleration = acceleration

    def setTorque(self, torque:tuple[int]):
        self.torque = torque
    