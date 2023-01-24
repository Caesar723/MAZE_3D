from block import Block
from character import Leo


import random


def create_maze(len_x,len_z):#2:fix wall 1:wall 0:road(read) 3:not read road(prim)
    four_dir=[(0,-1),(0,1),(1,0),(-1,0)]
    map=[
        [
            (1 if z%2==1 or x%2==1 else 3 )+ (1 if z%2==1 and x%2==1 else 0) 
            for x in range(len_x) 
        ] 
        for z in range(len_z)
    ]

    map[0][0]=0# 0,0 read
    wall_list=[[0,1,0,0],[1,0,0,0]]#[[y,x,orginal pos]]

    while wall_list:
        get_wall=wall_list.pop(random.randint(0,len(wall_list)-1))
        newpos=[2*get_wall[0]-get_wall[2],2*get_wall[1]-get_wall[3]]


        if newpos[0]<len_z and newpos[1]<len_x\
            and newpos[0]>=0 and newpos[1]>=0:
            if map[newpos[0]][newpos[1]]==3:
                map[get_wall[0]][get_wall[1]]=0
                map[newpos[0]][newpos[1]]=0
                for dir in four_dir:
                    next_pos=[newpos[0]+dir[0],newpos[1]+dir[1]]
                    #print(next_pos)
                    if next_pos[0]<len_z and next_pos[1]<len_x and\
                         next_pos[0]>=0 and next_pos[1]>=0 and\
                         map[next_pos[0]][next_pos[1]]==1:
                        wall_list.append([next_pos[0],next_pos[1],newpos[0],newpos[1]])

            elif map[newpos[0]][newpos[1]]==0:
                map[get_wall[0]][get_wall[1]]=2
        #print(wall_list)

    
    return map

def initinal_map(map):
    len_x,len_z=len(map[0])+1,len(map)+1
    arr=[]
    add_leo=True
    leo=0
    for z in range(len_z):
        row=[]
        for x in range(len_x):
            if z==0 or x==0 :
                row.append(Block(x,0,z))
            else:
                if map[z-1][x-1]:
                    block=Block(x,0,z)
                    if x==len_x-2 and z==len_z-1 or x==len_x-1 and z==len_z-2:
                        block.color=(255,50,50)
                    row.append(block)
                else:
                    row.append(0)
                    if add_leo and random.random()*100<0.5:
                        add_leo=False
                        leo=Leo(x,0,z)
                        
        arr.append(row)
        if leo==0:
            leo=Leo(len_x-2,0,len_z-2)
    return (arr,leo)



if __name__=="__main__":
    print()
    map=create_maze(30,30)
    main_map=initinal_map(map)
    print(main_map)