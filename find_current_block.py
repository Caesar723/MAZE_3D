from camera import Camera
from block import Block

import numpy
import pygame

def angle2rad(angle):
    return 2*numpy.pi*angle/360

def element1(lis):#used in sort
    return lis[1]



def find_block(map:list[list[Block]],camera:Camera,scope=8)->list[Block]:
    # calculate 3 points(z,y)
    max_x,max_z=len(map[0]),len(map)
    result=[]
    #arr=[]
    point_cam=[camera.pos[2][0]/10,camera.pos[0][0]/10]# z,y
    #print(camera.pos)
    sortElement=lambda blo:(blo.pos[2][0]-camera.pos[2][0])**2+(blo.pos[0][0]-camera.pos[0][0])**2

    point1_angle=angle2rad(camera.turning_hori-camera.VISION_RANGE_A/2)
    point1=[
        point_cam[0]+scope*(numpy.cos(point1_angle)),
        point_cam[1]+scope*(numpy.sin(point1_angle))
    ]

    point2_angle=camera.VISION_RANGE_R-(0.5*numpy.pi-point1_angle)
    point2=[
        (point_cam[0]-scope*(numpy.sin(point2_angle))),
        point_cam[1]+scope*(numpy.cos(point2_angle))
        
    ]

    points=[point_cam,point1,point2]
    points.sort(key=element1)
    #print(points)

    


    k_1=(points[1][0]-points[0][0])/(points[1][1]-points[0][1]+0.01)# z=kx+b k:left tri
    b_1=points[0][0]-k_1*points[0][1]
    #print(k_1)

    k_2=(points[2][0]-points[0][0])/(points[2][1]-points[0][1]+0.01)# z=kx+b 
    b_2=points[0][0]-k_2*points[0][1]
    #print(k_2)

    k_3=(points[2][0]-points[1][0])/(points[2][1]-points[1][1]+0.01)# z=kx+b 
    b_3=points[1][0]-k_3*points[1][1]

    for x_l in range(round(points[0][1])-1,round(points[1][1])):
        if x_l<max_x and x_l>=0:
            two_p=[
                round(k_1*x_l+b_1),
                round(k_2*x_l+b_2)
                ]
            
            for z_l in range(min(two_p),max(two_p)+1):
                if z_l<max_z and z_l>=0 and map[z_l][x_l]:
                    result.append(map[z_l][x_l])
                    #arr.append([z_l,x_l])
                    

    for x_r in range(round(points[1][1]),round(points[2][1])+1):
        if x_r<max_x and x_r>=0:
            two_p=[
                round(k_3*x_r+b_3),
                round(k_2*x_r+b_2)
                ]
            #print(two_p)
            for z_r in range(min(two_p)-1,max(two_p)+1):
                if z_r<max_z and z_r>=0 and map[z_r][x_r]:
                    result.append(map[z_r][x_r])
                    #arr.append([z_r,x_r])
    
    #result.sort(key=sortElement,reverse=True)

    return (result,sortElement)
    




if __name__=="__main__":
    from maze_generator import *
    map=create_maze(30,30)
    main_map=initinal_map(map)
    #print(main_map)
    cam=Camera()
    print()
    arr=(find_block(main_map,cam))

    run=True

    screen=pygame.display.set_mode((1160, 800))

    while run:
        screen.fill((0 ,0 ,0))

        for eve in pygame.event.get():
            if eve.type==pygame.QUIT:
                run=False
            if eve.type == pygame.TEXTINPUT:
                if eve.text=="h":
                    cam.turning_hori-=1
                elif eve.text=="l":
                    cam.turning_hori+=1
                elif eve.text=="k":
                    cam.turning_vert+=1
                elif eve.text=="j":
                    cam.turning_vert-=1
                elif eve.text=="w":
                    cam.forward()
                elif eve.text=="a":
                    cam.left()
                elif eve.text=="s":
                    cam.backward()
                elif eve.text=="d":
                    cam.right()

        arr1,arr2=find_block(main_map,cam)
        pygame.draw.polygon(screen, (255,0,0), [[i[0]+400,i[1]+400] for i in arr2], 0)
        for arr in arr1:
            pygame.draw.circle(screen,(255,255,0),[arr[0]+400,arr[1]+400],1)



        pygame.display.flip()
