from camera import Camera


def check_limit(x,z,len_x,len_z):
    return x>=0 and z>=0 and x<len_x and z<len_z

def element_s(ele):
    x_c=ele[1].pos[0][0]#camera pos
    z_c=ele[1].pos[2][0]

    x_b=ele[2].pos[0][0]+ele[0][0]#block pos
    z_b=ele[2].pos[2][0]+ele[0][1]

    return (x_c-x_b)**2+(z_c-z_b)**2

def check_cam(cam:Camera,map):
    x,z=cam.pos[0][0],cam.pos[2][0]
    change_x,change_z=round(x/10),round(z/10)

    changelist=[(-1,0),(1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
    move=5.6

    len_x,len_z=len(map[0]),len(map)
    if check_limit(change_x,change_z,len_x,len_z):
        #print(change_x,change_z,map[change_z][change_x])
        if map[change_z][change_x]:
            check_blocks=[]
            for surface in changelist:
                round_b_x=change_x+surface[0]
                round_b_z=change_z+surface[1]
                if check_limit(round_b_x,round_b_z,len_x,len_z):
                    round_b=map[round_b_z][round_b_x]
                    if not round_b:
                        check_blocks.append([(move*surface[0],move*surface[1]),cam,map[change_z][change_x]])
            check_blocks.sort(key=element_s)
            if check_blocks:
                get_shortest=check_blocks[0]
                if get_shortest[0][0]:
                    cam.pos[0][0]=map[change_z][change_x].pos[0][0]+get_shortest[0][0]
                else:
                    cam.pos[2][0]=map[change_z][change_x].pos[2][0]+get_shortest[0][1]
        

def check_cam_planB(cam:Camera,map):
    x,z=cam.pos[0][0],cam.pos[2][0]
    change_x,change_z=round(x/10),round(z/10)

    len_x,len_z=len(map[0]),len(map)

    changelist_add_x=[(1,0),(-1,0)]# shape:+
    changelist_add_z=[(0,1),(0,-1)]
    

    dis_from_cen=3
    if abs(x-change_x*10)>dis_from_cen:
        if check_limit(change_x,change_z,len_x,len_z):
            for surface in changelist_add_x:
                if (x-change_x*10)/surface[0]>0:
                    round_b_x=change_x+surface[0]
                    round_b_z=change_z+surface[1]
                    if check_limit(round_b_x,round_b_z,len_x,len_z):
                        
                        round_b=map[round_b_z][round_b_x]
                        if round_b:
                            
                            cam.pos[0][0]=change_x*10+dis_from_cen*surface[0]
    if abs(z-change_z*10)>dis_from_cen:
        if check_limit(change_x,change_z,len_x,len_z):
            for surface in changelist_add_z:
                if (z-change_z*10)/surface[1]>0:
                    round_b_x=change_x+surface[0]
                    round_b_z=change_z+surface[1]
                    if check_limit(round_b_x,round_b_z,len_x,len_z):
                        round_b=map[round_b_z][round_b_x]
                        if round_b:
                            cam.pos[2][0]=change_z*10+dis_from_cen*surface[1]

        
        

