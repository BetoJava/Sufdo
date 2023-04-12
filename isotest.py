import pygame
from pygame.locals import *
import sys

from random import randint 

def map_aleatoire(x,y):
    M = []
    for i in range(x):
        Mi = []
        for j in range(y):
            p = randint(1,8)
            if p == 1:
                case = 1
            elif p == 2:
                case = -1
            else:
                case = 0
                
            if j in (0,y-1) or i in (0,x-1):
                p = randint(1,100)
                if p > 20:
                    case = 1
                else: 
                    case = 0
            Mi.append(case)
        M.append(Mi)
    return M
                


pygame.init()
 
fenetre = pygame.display.set_mode((1280, 800), RESIZABLE)    #set the display mode, window title and FPS clock DOUBLEBUF
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()
 
map_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 1, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 0, 0, 1, 0, 0, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1],
]               #the data for the map expressed as [row[tile]].


'''map_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, -1, 1, 1, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 0, 0, 1],
[1, 0, -1, -1, -1, 1, 0, 0, 1],
[-1, -1, -1, -1, 1, 0, -1, 0, 1],
[-1, -1, -1, -1, 0, 0, 0, 0, 1],
[-1, -1, -1, 0, 1, 0, 0, 0, 1],
[-1, -1, -1, 0, 1, -1, 2, 0, 1],
[-1, -1, 0, 0, 0, 0, 0, 0, 1],
]'''

    
    
x,y = randint(5,17), randint(5,17)
map_data = map_aleatoire(18, 18)

map_data[-3][-3] = 2

map_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]      



wall = pygame.image.load('data/images/wall.png').convert_alpha()  #load images
grass = pygame.image.load('data/images/grass.png').convert_alpha()
void = pygame.image.load('data/images/void.png').convert_alpha()
mob_grass = pygame.image.load('data/images/mob_grass.png').convert_alpha()
 
tile_largeur = 64  #holds the tile width and height
tile_hauteur = 64
tile_hauteur_HALF = tile_hauteur /2
tile_largeur_HALF = tile_largeur /2
 

for i in range(len(map_data)):
    for j in range(len(map_data[i])):
        if map_data[i][j] == 1:
            tileImage = wall
        elif map_data[i][j] == 0:
            tileImage = grass
        elif map_data[i][j] == -1:
            tileImage = void
        elif map_data[i][j] == 2:
            tileImage = mob_grass
        cart_x = -200 + i * tile_largeur_HALF
        cart_y = -200 + j * tile_hauteur_HALF  
        iso_x = (cart_x - cart_y) 
        iso_y = (cart_x + cart_y)/2
        centered_x = int(fenetre.get_rect().centerx + iso_x)
        centered_y = int(fenetre.get_rect().centery/2 + iso_y)
        fenetre.blit(tileImage, (centered_x, centered_y)) #display the actual tile
 
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
 
    pygame.display.flip()
    FPSCLOCK.tick(30)