from camera import Camera
from display import *
from find_current_block import find_block
from check_cam_round import check_cam,check_cam_planB,check_limit
from character import *



import pygame
import threading
import time
import os



ORGPATH=os.path.dirname(os.path.abspath(__file__))
FONT_PATH=f"{ORGPATH}/maze_word/"

class Game:
    MOVE_LIMIT=1000
    def __init__(self,map,maps:list,camera:Camera,gaming_state) -> None:
        self.screen=pygame.display.set_mode((1450, 800))
        self.small_map=pygame.Surface((200,200))#5x5
        self.small_map_r=4

        self.TRANSPARENT=0# 0~8
        self.transparent_degree=lambda :1/(1+(2.718281**(self.TRANSPARENT-5)))
        self.background_color=30
        self.map_color=230

        self.step_counter=0# counte moving step
        self.changing_map=False

        self.cam=camera

        self.leo=map[1]#Leo(1,0,6)#
        
        self.map=map[0]
        self.maps=maps
        self.map_change_index=-1

        self.press={
            pygame.K_w:self.forward_press,
            pygame.K_s:self.backward_press,
            pygame.K_a:self.left_press,
            pygame.K_d:self.right_press,
            pygame.K_p:self.start_changing_map
            }
        self.release={
            pygame.K_w:self.forward_relea,
            pygame.K_s:self.backward_relea,
            pygame.K_a:self.left_relea,
            pygame.K_d:self.right_relea
        }
        self.gaming_state=gaming_state
        # self.run=True
        # self.gaming=True

        self.check_list=[
            [False,self.cam.forward],#False :unpress True:press
            [False,self.cam.backward],
            [False,self.cam.left],
            [False,self.cam.right]
            ]
        
        self.move_dir=False


        self.win,self.fail=False,False

        self.font= pygame.font.Font(f'{FONT_PATH}Kaiti.ttc', 180)
        self.text_created=0
        self.text_color=[255,0,0]

    def event_process(self,moving):
        for eve in pygame.event.get():
            if eve.type==pygame.QUIT:
                self.gaming_state[0]=False

            if moving:
                if eve.type == pygame.KEYDOWN:
                    if eve.key in self.press:
                        self.press[eve.key]()

                if eve.type == pygame.KEYUP:
                    if eve.key in self.release:
                        self.release[eve.key]()

            if eve.type==pygame.MOUSEBUTTONDOWN:
                if self.win or self.fail:
                    self.gaming_state[1]=False
                else:
                    self.mouse_press(pygame.mouse.get_pos())

            if eve.type==pygame.MOUSEBUTTONUP:
                self.mouse_release()

    def update(self):
        

        self.screen.fill([self.background_color*self.transparent_degree()]*3)
        self.small_map.fill([self.map_color*self.transparent_degree()]*3)


        moving=self.check_whether_move()
        
        
        self.event_process(moving)



        
        #check_cam(self.cam,self.map)
        check_cam_planB(self.cam,self.map)

        if self.step_counter>=self.MOVE_LIMIT:# if counter over the limit the map will be changed
            self.start_changing_map()
       
        blocks,sort_fun=find_block(self.map,self.cam)
        blocks.append(self.leo)
        blocks.sort(key=sort_fun,reverse=True)
        for block in blocks:
            block.display(self.cam,self.screen,self.map,self.transparent_degree)
            

        for move in self.check_list:
            if  move[0]:
                move[1]()
                self.step_counter+=1

        if self.move_dir:
            self.change_direction(pygame.mouse.get_pos())

        self.build_small_map()
        self.screen.blit(self.small_map,(1200,50))

        self.check_win()
        self.check_fail()
        self.leo.whole_steps(self.map,self.cam)
        self.leo.play_sound_normal(self.cam)

        if (self.win or self.fail) and self.text_created:
            self.screen.blit(self.text_created,(600,300))
    

    
            
    def start_changing_map(self):# find the map that match the position
        c_x,c_z=self.cam.pos[0][0],self.cam.pos[2][0]#wall
        change_x,change_z=round(c_x/10),round(c_z/10)

        find=False
        for i in range(len(self.maps)):
            if not self.maps[i][0][change_z][change_x]:
                find=True
                self.map_change_index=i
        if find:
            self.step_counter=0
            self.changing_map=True
            for move in self.check_list:
                move[0]=False
            self.leo.open=False

    def check_whether_move(self)->bool:
        moving=False
        if self.win==False and self.fail==False:
            if self.changing_map:
                if self.TRANSPARENT<8:
                    self.TRANSPARENT+=0.1
                else:
                    self.change_map()
                    self.changing_map=False
            else:
                if self.TRANSPARENT>0:
                    self.TRANSPARENT-=0.1
                else:
                    moving=True
        return moving

    def change_map(self):# change the map
        newmap=self.maps.pop(self.map_change_index)
        self.maps.append((self.map,self.leo))
        self.map=newmap[0]
        self.leo=newmap[1]
        self.leo.open=True
        


    def build_small_map(self):
        c_x,c_z=self.cam.pos[0][0],self.cam.pos[2][0]#wall
        change_x,change_z=round(c_x/10),round(c_z/10)
        len_x,len_z=len(self.map[0]),len(self.map)
        for z in range(change_z-self.small_map_r,change_z+self.small_map_r):
            for x in range(change_x-self.small_map_r,change_x+self.small_map_r):
                if check_limit(x,z,len_x,len_z) and self.map[z][x]:
                    
                    pygame.draw.circle(self.small_map,(0,0,0),[(x-change_x)*(200/(self.small_map_r*2+1))+100,
                    (z-change_z)*(200/(self.small_map_r*2+1))+100],10)
        
        c_m_x=((c_x/10)-change_x)*(200/(self.small_map_r*2+1))+100#camera
        c_m_z=((c_z/10)-change_z)*(200/(self.small_map_r*2+1))+100
        direction=(self.cam.turning_hori)
        next_pos_x=c_m_x+self.small_map_r*2*numpy.sin(2*numpy.pi*direction/360)
        next_pos_z=c_m_z+self.small_map_r*2*numpy.cos(2*numpy.pi*direction/360)
        pygame.draw.circle(self.small_map,[100*self.transparent_degree()]*3,[c_m_x,c_m_z],5)
        pygame.draw.line( self.small_map, [100*self.transparent_degree()]*3, [next_pos_x,next_pos_z], [c_m_x,c_m_z], 5 )



    def mouse_press(self,mos_pos):
        self.move_dir=True
        self.mouse_pos=mos_pos


    def mouse_release(self):
        self.move_dir=False

    def change_direction(self,new_pos):
        dis_x,dis_y=new_pos[0]-self.mouse_pos[0],new_pos[1]-self.mouse_pos[1]
        self.cam.turning_hori+=dis_x/10
        self.cam.turning_vert+=dis_y/10
        self.mouse_pos=new_pos
        

    def forward_press(self):
        self.check_list[0][0]=True


    def forward_relea(self):
        self.check_list[0][0]=False

    def backward_press(self):
        self.check_list[1][0]=True

    def backward_relea(self):
        self.check_list[1][0]=False


    def left_press(self):
        self.check_list[2][0]=True

    def left_relea(self):
        self.check_list[2][0]=False

    def right_press(self):
        self.check_list[3][0]=True

    def right_relea(self):
        self.check_list[3][0]=False

    def check_win(self):
        c_x,c_z=self.cam.pos[0][0],self.cam.pos[2][0]#wall
        change_x,change_z=round(c_x/10),round(c_z/10)
        len_x,len_z=len(self.map[0]),len(self.map)
        if change_x==len_x-2 and change_z==len_z-2 and self.win==False:
            thread=threading.Thread(target=(self.show_word),args=("赢"))
            thread.start()
            self.win=True
            

    def check_fail(self):
        c_x,c_z=self.cam.pos[0][0],self.cam.pos[2][0]#wall
        change_x,change_z=round(c_x/10),round(c_z/10)
        l_x,l_z=round(self.leo.pos[0][0]/10),round(self.leo.pos[2][0]/10)
        if change_x==l_x and l_z==change_z and self.fail==False:
            thread=threading.Thread(target=(self.show_word),args=("撅"))
            thread.start()
            self.fail=True
            
        


    def show_word(self,text=""):
        
        self.leo.open=False
        for move in self.check_list:
            move[0]=False
        while self.TRANSPARENT<8:
            self.TRANSPARENT+=0.02
            time.sleep(0.001)
            RGB=[(color)*(1-self.transparent_degree()) for color in self.text_color]
            self.text_created = self.font.render(text, 1, (RGB))
            
        




    