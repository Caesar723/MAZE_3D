from rotate import *
from camera import Camera


import pygame
import numpy






def calculate_a(vec1,vec2):#included angle
    cos=numpy.dot(vec1,vec2)/(numpy.linalg.norm(vec2)*numpy.linalg.norm(vec1)+0.000001)
    angle=360*np.arccos(cos)/(2*np.pi)
    return angle


def check_round(block,vec,map):#round of each block
    displacement=vec/5
    x,z=int(displacement[0]),int(displacement[2])
    if z+block.pos_in_map[1]>=0 and x+block.pos_in_map[0]>=0\
    and z+block.pos_in_map[1]<len(map) and x+block.pos_in_map[0]<len(map[0]):# it have <=

        check=map[z+block.pos_in_map[1]][x+block.pos_in_map[0]]
        return not(bool(check))
    else:
        return True

def check_angle(camera:Camera,block,line):
    surface_pos=(block.points[:,line[0][0]]+block.points[:,line[0][2]])/2
    vec_cb=np.reshape(camera.pos,(1,3))-np.reshape(surface_pos,(1,3))
    #print(vec_cb)
    angle_vs=calculate_a(vec_cb,line[1])#angle of surface
    
    angle_back=calculate_a(vec_cb,camera.direct_vec[0])
    
    # if angle_vs<90 and angle_back<56:
    #     print(angle_back,camera.direct_vec[0])
    return (angle_vs<90 and angle_back<80 ,surface_pos)


def display_t(camera:Camera,block,screen,map,transparent_degree):
    locals=change_loca(camera,block)
    for line in block.four_sur:
        
        check_a,surface_pos=check_angle(camera,block,line)
        check_r=check_round(block,line[1],map)
        check_limit=True
        
        
        loc=[]
        

        if check_a and check_r:
            for i in range(4):
                #print(locals[line[0][i]])
                counter=0
                while abs(locals[line[0][i]][0]) >7000 or abs(locals[line[0][i]][1])>7000:

                    if i%2==0:
                        index=i+1
                    else:
                        index=i-1
                    locals[line[0][i]][0]=locals[line[0][i]][0]+locals[line[0][index]][0]
                    locals[line[0][i]][1]=locals[line[0][i]][1]+locals[line[0][index]][1]
                    counter+=1
                    if counter>=6:
                        check_limit=False
                        break
                else:
                    loc.append(locals[line[0][i]])


            distance=((surface_pos[0]-camera.pos[0,0])**2+(surface_pos[2]-camera.pos[2,0])**2)**0.5
            RGB=[(color-(1/(1 + 2.718281**-abs(distance/8)))*(color-30))*transparent_degree() for color in block.color]# 30 background color
            if check_limit:
                
                #print(color)

                pygame.draw.polygon(screen, RGB, loc, 0)
            else:
                for ii in range(4):
                    pygame.draw.line( screen, RGB, locals[line[0][ii]], locals[line[0][(ii+1)%4]], 1 )
                #print(time.time()-startT,angle_back,[locals[line[0][i]] for i in range(4)])
        
    
        


def change_loca(camera:Camera,block):#  vision_rotate-> similar tri
    ###################################################

    displacement=block.points-camera.pos
    # print(displacement)
    # print(0)
    rotate_y_v=Ry(camera.turning_hori)
    rotate_x_v=Rx(camera.turning_vert)
    displacement=rotate_x_v*rotate_y_v*displacement
    # print(displacement)
    # print()
    
    #########################################################

    arr=[]
    for i in range(8):
        orig_p=(displacement[:,i])
        
        final_p=[orig_p[0,0]*camera.dis_to_scree/(abs(orig_p[2,0]+2)+0.001),
                orig_p[1,0]*camera.dis_to_scree/(abs(orig_p[2,0]+2)+0.001)]#x,y
        # if orig_p[2,0]<0:
        #     print(orig_p,final_p)
        arr.append([final_p[0]+725,final_p[1]+400])
    # print(arr)
    # print(1)

    return arr


