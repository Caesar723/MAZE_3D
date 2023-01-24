import numpy


class Camera:
    
    __turning_hori=0 #0~360
    __turning_vert=0 #0~360

    dis_to_scree=2000
    LIMIT=(0,2*numpy.pi)
    VISION_RANGE_R=2*numpy.pi*134/360 # 124 degree
    VISION_RANGE_A=134 # 124 degree

    VERT_MIN=10
    VERT_MAX=350

    def __init__(self,x=10,y=0,z=10) -> None:
        self.pos=numpy.array([[x],#x
                    [y],#y
                    [z]],dtype=float)#z


    @property
    def turning_hori(self):
        return self.__turning_hori%360
    
    @turning_hori.setter
    def turning_hori(self,val):
       
        self.__turning_hori=val

    @property
    def turning_vert(self):
        return self.__turning_vert%360
    
    @turning_vert.setter
    def turning_vert(self,val):
        
        if val<self.VERT_MAX and val>180:
            self.__turning_vert=self.VERT_MAX
        elif val>self.VERT_MIN and val<180:
            self.__turning_vert=self.VERT_MIN
        else:
            self.__turning_vert=val

    @property
    def direct_vec(self):
        angle=2*numpy.pi*self.turning_hori/360
        return -numpy.array([[numpy.sin(angle),0,numpy.cos(angle)]],dtype=float)

    def move(self,angle,step=0.5):
        x,z=numpy.sin((2*numpy.pi)*angle/360)*step,numpy.cos((2*numpy.pi)*angle/360)*step
        self.pos[0,0]+=x
        self.pos[2,0]+=z

    def forward(self):
        self.move(self.turning_hori)

    def backward(self):
        self.move(self.turning_hori-180)

    def left(self):
        self.move(self.turning_hori-90)

    def right(self):
        self.move(self.turning_hori+90)

