from rotate import *
from camera import Camera
from block import Block
from display import *
from maze_generator import *
from find_current_block import find_block
from game import Game
from character import *

import pygame
import numpy



def a_game(state):
    maps=[initinal_map(create_maze(20,30)) for i in range(6)]
    map=maps.pop()
    cam=Camera()
    gam=Game(map,maps,cam,state)
    while state[0] and state[1]:
        gam.update()
        pygame.display.flip()

if __name__=="__main__":
    
    pygame.init()
    pygame.mixer.init()
    gaming_state=[True,True]#run,gaming

    while gaming_state[0]:
        a_game(gaming_state)
        gaming_state[1]=True
        