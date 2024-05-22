from pygame import Rect
from pygame import Surface
class Object:
    def __init__(self, coordinates:tuple[int]=(0,0), shape:tuple[int] = (0,0), color:tuple[int] = (0, 0)):
        self.bounds:Rect = Rect(coordinates, shape)
        self.angle = 0
        self.color = color
        self.image = Surface(shape)
        self.image.fill(color)

    
    def setPosition(self, coordinates:tuple[int]):
        self.bounds.x, self.bounds.y = coordinates

    def draw(self, matriz:list[bool], surface:Surface):
        surface.blit(self.image, self.bounds)

    def getImage(self):
        return self.image

    def logic(self):
        pass