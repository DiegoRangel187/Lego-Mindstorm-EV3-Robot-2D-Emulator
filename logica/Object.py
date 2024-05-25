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

    def draw(self, surface:Surface):
        surface.blit(self.image, self.bounds)

    def getImage(self):
        return self.image

    def logic(self):
        pass

    def onDelete(self):
        pass

class ObjectColletion:

    def __init__(self, objects:list[Object]):
        self.__objects:list[Object] = objects

    def logic(self):
        for i in self.__objects:
            i.logic()

    def draw(self, screen:Surface):
        for i in self.__objects:
            i.draw(screen)

    def onDelete(self):
        for i in self.__objects:
            i.onDelete()

    def append(self, object:Object):
        self.__objects.append(object)

    def delete(self, object:Object):
        pass

    def getObjects(self):
        return self.__objects