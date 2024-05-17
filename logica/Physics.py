from Object import Object

class PhysicsObject(Object):

    def __init__(self, coordinates:tuple[int]=(0,0), shape:tuple[int] = (0,0), color:tuple[int] = (0, 0), mass:int = 0):
        Object.__init__(self, coordinates, shape, color)
        self.maxSpeed:tuple[int] = (0, 0)
        self.acceleration:tuple[int] = (0, 0)
        self.massCenter:tuple[int] = self.bounds.center
        self.torque:tuple[int] = (0, 0)
        self.mass:int = mass
        self.speed = (0, 0)

    def setSpeed(self, speed:tuple[int]):
        self.maxSpeed = speed

    def setAcceleration(self, acceleration:tuple[int]):
        self.acceleration = acceleration

    def setTorque(self, torque:tuple[int]):
        self.torque = torque

    def onCollition(self, collided):
        momentum1 = PhysicsObject.momentum(self.speed)
        momentum2 = PhysicsObject
    @staticmethod
    def momentum(speed:tuple[int], mass:int):
        return (speed[0]*mass, speed[1]*mass)

    @staticmethod
    def torque(ratio:tuple[int], force:tuple[int]):
        return (ratio[0]*force[0], ratio[1]*force[1])

    @staticmethod
    def force(acceleration:tuple[int], mass:int):
        return (acceleration[0]*mass, acceleration[1]*mass)

    