# Import ---------------------------------------------------------- #
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" 

import pygame

import data.scripts.menu as m

if __name__ == '__main__':

    liste_pseudo = []

    fichier = open('data/save/joueurs/1_liste_pseudo.txt','a', encoding='utf-8')
    fichier.close()
    fichier = open('data/save/joueurs/1_liste_pseudo.txt','r', encoding='utf-8')
    C = fichier.readlines()
    if C!= []:
        for i in range(len(C)):
            liste_pseudo.append(C[i][:-1])
    fichier.close()

    app = m.Application(liste_pseudo)
    app.menu1()
    
    app.clock = pygame.time.Clock()
    
    # Loop Menu 1 -------------------- #
    while app.statut:
        if app.gameOn:
            app.updateJeu()
        else:
            app.update()
        app.clock.tick(app.fps)
    pygame.quit()