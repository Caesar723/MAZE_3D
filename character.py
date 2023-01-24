from substance import *
from rotate import *


import random
import os 


ORGPATH=os.path.dirname(os.path.abspath(__file__))
PATH_P=f"{ORGPATH}/photo/"
PATH_S=f"{ORGPATH}/music/"


class Node:
    next=None
    def __init__(self,pos,last,score) -> None:
        
        self.last=last
        self.pos=pos
        self.score=score


    def __repr__(self) -> str:
        return str(self.pos)+" "+str(self.score)


class Leo(Substance):

    def __init__(self, x, y, z) -> None:
        super().__init__(x, y, z)
        self.size=160
        self.image=pygame.image.load(f"{PATH_P}leo2.png")
        self.activate=False
        self.moving=False
        self.step_counter=0

        self.sound_shout=pygame.mixer.Sound(f"{PATH_S}foul1.mp3")

        self.sound_normal=[pygame.mixer.Sound(f"{PATH_S}foul2.mp3"),pygame.mixer.Sound(f"{PATH_S}foul3.mp3")]
        self.sound_find=[self.sound_shout,pygame.mixer.Sound(f"{PATH_S}ll.mp3")]
        
        self.sound_count=0
        
        self.open=True


    def display(self,camera:Camera,screen,map,transparent_degree):

        displacement=self.pos-camera.pos
        rotate_y_v=Ry(camera.turning_hori)
        rotate_x_v=Rx(camera.turning_vert)
        displacement=rotate_x_v*rotate_y_v*displacement

        
        orig_p=(displacement[:,0])
        
        distance=((self.pos[2][0]-camera.pos[2][0])**2+(self.pos[0][0]-camera.pos[0][0])**2)**0.5
        if orig_p[2,0]<0 or distance>45:
            return

        final_p=[725+orig_p[0,0]*camera.dis_to_scree/(abs(orig_p[2,0]+2)+0.001),
                400+orig_p[1,0]*camera.dis_to_scree/(abs(orig_p[2,0]+2)+0.001)]#x,y
        
        size=self.size*100/(abs(orig_p[2,0]+2)+0.001)

        newImg=pygame.transform.scale(self.image,(1*size,1.2*size))
        newImg.set_alpha(255*transparent_degree()*1/(1+2.71**(distance/10-2)))
        screen.blit(newImg,[final_p[0]-size/2,final_p[1]-size/2])

    def whether_act(self,map,camera:Camera):# it will check whether in vision 
        leo_x=self.pos[0][0]/10
        leo_z=self.pos[2][0]/10

        cam_x=camera.pos[0][0]/10
        cam_z=camera.pos[2][0]/10

        k=(cam_z-leo_z)/(cam_x-leo_x+0.0001)
        
        if abs(k)<1:
            b=leo_z-k*leo_x

            start_x=round(min(leo_x,cam_x))
            end_x=round(max(leo_x,cam_x))
            for x in range(start_x,end_x):
                z=round(k*x+b)
                if map[z][x]:
                    return False
            return True
        else:
            
            k=(cam_x-leo_x)/(cam_z-leo_z+0.0001)
            b=leo_x-k*leo_z
            start_z=round(min(leo_z,cam_z))
            end_z=round(max(leo_z,cam_z))
            for z in range(start_z,end_z):
                x=round(k*z+b)
                if map[z][x]:
                    return False
            return True

    def whole_steps(self,map,camera:Camera):
        if self.open:
            if self.activate:
                if self.moving:

                    self.pos[0][0]+=self.move_x
                    self.pos[2][0]+=self.move_z
                    if ((self.pos[0][0]/10-self.get_node.pos[0])**2+(self.pos[2][0]/10-self.get_node.pos[1])**2)**0.5<0.1:
                        self.moving=False
                        self.step_counter+=1
                        if self.step_counter>=5:
                            self.activate=False
                else:
                    self.get_node=(self.A_star(camera,map))
                    if self.get_node:
                        self.move_x,self.move_z=(self.get_node.pos[0]-self.pos[0][0]/10)/3,(self.get_node.pos[1]-self.pos[2][0]/10)/3
                        
                        self.moving=True

            else:
                
                if self.whether_act(map,camera) :
                    self.activate=True
                    self.play_sound_find(camera)
                    self.step_counter=0

    def A_star(self,camera:Camera,map):
        cam_x=round(camera.pos[0][0]/10)
        cam_z=round(camera.pos[2][0]/10)

        leo_x=round(self.pos[0][0]/10)
        leo_z=round(self.pos[2][0]/10)

        start_node=Node((leo_x,leo_z),None,0)
        open_set=[start_node]
        close_set=[]

        neighbours=[(1,0),(-1,0),(0,1),(0,-1)]
        while open_set:
            
            min_node=(open_set[0],open_set[0].score)
            for node in open_set:
                if node.score<min_node[1]:
                    min_node=(node,node.score)


            if min_node[0].pos[0]==cam_x and min_node[0].pos[1]==cam_z:
                new_node=min_node[0]
                next_node=new_node
                while new_node.last!=None:
                    next_node=new_node
                    new_node=new_node.last
                    
                return next_node

            open_set.remove(min_node[0])
            close_set.append(min_node[0])


            for neighbour in neighbours:
                new_pos=(neighbour[0]+min_node[0].pos[0],neighbour[1]+min_node[0].pos[1])
                check=False
                if map[new_pos[1]][new_pos[0]]==0 :
                    for close in close_set:
                        if close.pos[0]==new_pos[0] and new_pos[1]==close.pos[1]:
                            check=True
                            break
                    for open in open_set:
                        if open.pos[0]==new_pos[0] and new_pos[1]==open.pos[1]:
                            check=True
                            break
                    if check==False:

                        score=min_node[1]+1+((cam_x-new_pos[0])**2+(cam_z-new_pos[1])**2)**0.5
                        open_set.append(Node(new_pos,min_node[0],score))
            
    def play_sound_normal(self,camera):
        self.sound_count+=1
        if self.sound_count>=100 and self.open:
            self.sound_count=0

            strength=self.cal_strength(camera)-3

            sound=self.sound_normal[random.randint(0,1)]
            sound.set_volume(1/(1+2.71**strength))
            sound.play()


    def play_sound_find(self,camera):# when find people call this fun
        strength=self.cal_strength(camera)-3
        sound=self.sound_find[random.randint(0,1)]
        sound.set_volume(1/(1+2.71**strength))
        sound.play()

    def play_sound_finish(self,camera):# when catch people
        strength=self.cal_strength(camera)-3
        self.sound_shout.set_volume(1/(1+2.71**strength))
        self.sound_shout.play()


    def cal_strength(self,camera,theta=1):
        leo_x=self.pos[0][0]/10
        leo_z=self.pos[2][0]/10

        cam_x=camera.pos[0][0]/10
        cam_z=camera.pos[2][0]/10

        return (((cam_x-leo_x)**2+(cam_z-leo_z)**2)**0.5)/theta

            
    
            




