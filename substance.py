from camera import Camera


import numpy
import pygame



class Substance:

    ratio=10
    length=5

    def __init__(self,x,y,z) -> None:
        self.pos_in_map=[x,z]
        self.pos=numpy.array([[x*self.ratio],#x
                    [y*self.ratio],#y
                    [z*self.ratio]],dtype=float)#z

    def display(self,camera:Camera,screen:pygame.surface,map,transparent_degree):
        pass