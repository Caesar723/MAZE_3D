from substance import *
from display import display_t

import numpy


class Block(Substance):
    
    def __init__(self,x,y,z) -> None:
        super().__init__(x,y,z)
        
        self.direct_vec=numpy.array([
            [0],
            [0],
            [-1]
        ],dtype=float)# toward backward

        self.create_points()
        self.initinal_surface()
        self.color=(255,255,255)
        

    def create_points(self):
        points=[(-1,1,-1),(-1,1,1),(1,1,-1),(1,1,1),#x,y,z top four points
                (-1,-1,-1),(-1,-1,1),(1,-1,-1),(1,-1,1)]# bottom four points
        
        x,y,z=[],[],[]
        for point in points:
            
            get_point=self.pos+numpy.resize(numpy.array(point),(3,1))*self.length
            x.append(get_point[0,0])
            y.append(get_point[1,0])
            z.append(get_point[2,0])
            
        self.points=numpy.array([x,y,z])
        
       
    def initinal_surface(self):
        self.four_sur=[[(0,1,5,4)],
                        [(0,2,6,4)],
                        [(1,3,7,5)],
                        [(2,3,7,6)]
                        ]#(index,...)four index of points , which create a surface, direction vector

        for surface in self.four_sur:
            
            direction=(self.points[:,surface[0][0]]+self.points[:,surface[0][2]])/2-numpy.reshape(self.pos,(1,3))[0]# calculate vector
            surface.append(direction)

        #print(self.four_sur)
    def __repr__(self) -> str:
        return str(self.pos_in_map)

   
    def display(self,camera:Camera,screen:pygame.surface,map,transparent_degree):
        display_t(camera,self,screen,map,transparent_degree) 
    
       
        


if __name__=="__main__":
    Block(1,0,1)