# Import ---------- #
import pygame
from random import randint
import data.scripts.functions as f
import data.scripts.pathfinding as pf
import data.scripts.battle_functions as bf


# Fonction utiles ---------- #
def IsoToCano(i,j):
    x = 640 + 32*(i-j) + 48
    y = 0 + 16*(i+j) - 302
    return x, y

def CanoToIso(x,y):
    ajoutx = -48
    ajouty = 302
    x += ajoutx
    y += ajouty
    i = -10 + 1/64 * (x + 2*y) + 1/64 * (-32 - 2*32)
    j = 10 + 1/64 * (2*y - x) + 1/64 * (32 - 2*32) # + 1/64 * (32 - 2*32) pour ajuster
    return i,j



# Classe MapIso ----------- #
class MapIso():
    '''Classes des maps. On retrouve :
        - les images chargées
        - les différentes maps et leurs positions de départ
        - une fonction updateMapIso qui permet de mettre à our la map
        - une fonction map aléatoire
        '''
    def __init__(self, fenetre, choix_map = 0):
        self.combat_started = False
        self.choix_map = choix_map
        self.sort_selected = -1
        self.pos_info_bulle = (0,0)
        self.tick = 0
        self.pv_cible = 0
        self.boubou_cible = 0
        self.pm_range_cible = []
        self.pm_no_range_cible = []
        self.name = ''
        self.zone_pm_afficher = True
        
        self.fond = pygame.image.load("data/images/Menu/fondvierge.png").convert()
        self.wall = pygame.image.load('data/images/Tileset/wall.png').convert_alpha()  #load images
        self.groundpair = pygame.image.load('data/images/Tileset/groundpair.png').convert_alpha()
        self.groundimpair = pygame.image.load('data/images/Tileset/groundimpair.png').convert_alpha()
        self.groundb = pygame.image.load('data/images/Tileset/gzonepo.png').convert_alpha()
        self.groundbc = pygame.image.load('data/images/Tileset/gzonenopo.png').convert_alpha()
        self.groundr = pygame.image.load('data/images/Tileset/gzone.png').convert_alpha()
        self.groundv = pygame.image.load('data/images/Tileset/gpath.png').convert_alpha()
        self.groundvc = pygame.image.load('data/images/Tileset/gzonepm.png').convert_alpha()
        self.groundvf = pygame.image.load('data/images/Tileset/g_no_pm.png').convert_alpha()
        self.groundvf2 = pygame.image.load('data/images/Tileset/g_no_pm2.png').convert_alpha()
        self.groundvc2 = pygame.image.load('data/images/Tileset/gzonepm2.png').convert_alpha()
        self.cercleb = pygame.image.load('data/images/Tileset/cercleb.png').convert_alpha()
        self.cercler = pygame.image.load('data/images/Tileset/cercler.png').convert_alpha()
        self.void = pygame.image.load('data/images/Tileset/void.png').convert_alpha()
        self.tileImage = self.groundpair
        
        self.maps = []
        
        self.map_data, self.pos_depart1, self.pos_depart2 = [], [], []
    


    def updateMapIso(self, fenetre, joueur, groupePersoCbt, groupePersoHorsCbt, groupeGlobalPerso, groupeGlobal, groupeInfoBullePerso, groupeGlyphe, ChatTextuel):
        
        po_range, po_range_novisible = [], []
        (X,Y,isClick) = self.pointeurIso(self.maps[self.choix_map][0])
        (x,y) = joueur.pos
        pos_tous_joueurs = [perso.pos for perso in groupePersoCbt]
        joueur_cible = joueur
        for player in groupePersoCbt:
            if player.pos == (X,Y):
                joueur_cible = player 
                break
        
        # Récupération des glyphes #
        cases_glyphe = []
        for g in groupeGlyphe:
            for case in g.zone:
                cases_glyphe.append(case)
        
        zone_cible = []
        # Si un sort est selectionné, on affiche sa zone ---------------------- #
        if self.sort_selected != -1:
            po_range, po_range_novisible = pf.pathfinding_po(self.map_data, groupePersoCbt, joueur, self.sort_selected)
            if (X,Y) in po_range:
                zone_cible = pf.ajout_zone(self.map_data, joueur, self.sort_selected, (X,Y))   
         
        # Si la souris est au dessus d'un joueur, on affiche une info bulle --- #
        if (X,Y) in pos_tous_joueurs or zone_cible != []:
            if len(groupeInfoBullePerso) == 0:
                self.pos_info_bulle = (X,Y)
                self.pv_cible = joueur_cible.pv
                self.boubou_cible = joueur_cible.somme_boost('shield') 
                
                joueurs_zone = []
                if self.sort_selected != -1 and zone_cible != [] and joueur.S != []:
                    if not joueur.S[self.sort_selected].cible_necessaire or (X,Y) in pos_tous_joueurs:
                        # Ajout des cibles dans la zone #
                        for (i,j) in zone_cible:
                            if (i,j) in pos_tous_joueurs:
                                for perso in groupePersoCbt:
                                    if perso.pos == (i,j) and perso.pos != (X,Y):
                                        joueurs_zone.append(perso)
                
                if joueur.S != []:
                    if self.sort_selected == -1:
                        f.InfoBullePerso(X, Y, groupePersoCbt, groupeGlobal, groupeInfoBullePerso, None, joueur, self.map_data, joueurs_zone=joueurs_zone)
                    else:
                        f.InfoBullePerso(X, Y, groupePersoCbt, groupeGlobal, groupeInfoBullePerso, joueur.S[self.sort_selected], joueur, self.map_data, joueurs_zone=joueurs_zone)
                    self.pm_range_cible = pf.pathfinding_pm(self.map_data, groupePersoCbt, joueur_cible) 
        else:
            self.pm_range_cible = []
            self.pm_no_range_cible = []
        if (X,Y) != self.pos_info_bulle or joueur_cible.pv != self.pv_cible or joueur_cible.somme_boost('shield') != self.boubou_cible:
            groupeInfoBullePerso.empty()
        
           
        if self.zone_pm_afficher:
            pm_range = pf.pathfinding_pm(self.map_data, groupePersoCbt, joueur) 
        else:
            pm_range = []
        best_way, cout = pf.pathfinding2(self.map_data, groupePersoCbt, joueur, (X,Y))
        if joueur.pm + joueur.somme_boost('pm') < cout:
            best_way = []
        
        # Si on clique -------------------------------------------------------- #
        if isClick and not joueur.isActing:
            if self.combat_started:
                # Si un sort est selectionné et qu'une case valide est ciblée, alors on utilise le sort, sinon on retire la zone de po #
                temps = pygame.time.get_ticks()
                if self.sort_selected != -1:
                    if (X,Y) in po_range:
                        dm = None # dm = derniers mouvements 
                        
                        # Ajout des cibles #
                        cibles = []
                        for (i,j) in zone_cible:
                            if (i,j) in pos_tous_joueurs:
                                for perso in groupePersoCbt:
                                    if perso.pos == (i,j):
                                        cibles.append(perso)
                                        
                        joueur.use_sort(self.sort_selected, joueur, cibles, self.map_data, zone_cible, (X,Y), groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                        
                        
                        self.sort_selected = -1
                        self.tick = temps
                    else:
                        self.sort_selected = -1
                        self.tick = temps
                        
                # Si la portée du sort n'est pas activée, on déplace à la case voulue #        
                elif (X,Y) in best_way and temps - self.tick > 250 and joueur.pm + joueur.somme_boost('pm') >= cout and not joueur.isActing:
                    best_way.reverse()
                    if best_way != []:
                        joueur.isActing = True
                        joueur.pm -= cout
                        for pos in best_way:
                            joueur.app.wait(50)
                            joueur.pos = pos
                        bf.affiche_point(-1*cout, joueur, groupeGlobal, 'pm')
                        joueur.isActing = False
                        
                    for i in range(len(best_way)-1):
                        joueur.last_pos.append(best_way[i])
                    joueur.pos = (X,Y)          # On change la position du joueur #
                    
                    # On applique ou retire les boosts de glyphes instantanés #          
                    for type_boost in joueur.Boost: 
                        boost_to_remove = []
                        for boost in type_boost:
                            if 'instantané' in boost:
                                boost_to_remove.append(boost)
                        for boost in boost_to_remove:
                            type_boost.remove(boost)
                            
                    if joueur.pos in cases_glyphe:
                        for g in groupeGlyphe:
                            if g.type_glyphe == 'instantané':
                                if joueur.pos in g.zone:
                                    g.appliquer(joueur, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                    
                    
            else:
                # Si le combat n'a pas commencé, on déplace sur la case de départ voulue #
                if (X,Y) not in pos_tous_joueurs and (X,Y) in self.maps[self.choix_map][joueur.team]:
                    joueur.pos = (X,Y)
         
        
                
        # Affichage des tiles-------------------------------------------------- #
        fenetre.blit(self.fond,(0,0))       
        
        for i in range(len(self.map_data)):
            for j in range(len(self.map_data[i])):
                if self.map_data[i][j] != -2:
                    self.tileImage = None 
                    if self.sort_selected != -1 and self.combat_started and not joueur.isActing:
                        if (i,j) in po_range:
                            self.tileImage = self.groundb  
                        if (i,j) in po_range_novisible and self.map_data[i][j] in [0,2,3]:
                            self.tileImage = self.groundbc
                        if (X,Y) in po_range:
                            if (i,j) in zone_cible:
                                self.tileImage = self.groundr
                    elif self.sort_selected == -1 and not joueur.isActing:
                        if (i,j) in best_way and self.combat_started:
                            self.tileImage = self.groundv                                      
                        elif (i,j) in self.pm_range_cible and self.combat_started:
                            self.tileImage = self.groundvc2 
                        elif (i,j) in pm_range and self.combat_started:
                            self.tileImage = self.groundvc 
                            
                    if self.tileImage == None:
                        # Pos de départ  --- #
                        if not self.combat_started and (i,j) in self.pos_depart1:
                            self.tileImage = self.groundb
                        elif not self.combat_started and (i,j) in self.pos_depart2:
                            self.tileImage = self.groundr
                        # Tiles de la Map -- #
                        elif self.map_data[i][j] == 1:
                            self.tileImage = self.wall
                        elif self.map_data[i][j] in [0,2,3]:
                            if (i+j)%2 == 0:
                                self.tileImage = self.groundpair
                            else:
                                self.tileImage = self.groundimpair
                        elif self.map_data[i][j] == -1:
                            self.tileImage = self.void
                        elif self.map_data[i][j] == 2:
                            self.tileImage = self.groundb
                        elif self.map_data[i][j] == 3:
                            self.tileImage = self.groundr
                            
                    self.centered_x, self.centered_y = IsoToCano(i, j)
                    fenetre.blit(self.tileImage, (self.centered_x, self.centered_y)) #display the actual tile 
                    
                    # Glyphes #
                    if (i,j) in cases_glyphe:
                        for g in groupeGlyphe:
                            if (i,j) in g.zone:
                                fenetre.blit(g.image, (self.centered_x, self.centered_y))
                        
                
                    # Pos des joueurs -- #
                    for perso in groupePersoCbt:
                        if (i,j) == perso.pos:
                            self.centered_x, self.centered_y = IsoToCano(i, j)
                            if perso.team == 1:
                                fenetre.blit(self.cercleb, (self.centered_x, self.centered_y))
                            else:
                                fenetre.blit(self.cercler, (self.centered_x, self.centered_y))
                            fenetre.blit(perso.image, (self.centered_x, self.centered_y-10))
                            to_blit = []
                            for etat in perso.etats:
                                if 'royal' in etat or 'Jroyal' in etat :
                                    to_blit.append(pygame.image.load('data/images/Texture/etats/royal.png').convert_alpha())
                                if 'EA' in etat or 'MD' in etat or 'MC' in etat:  
                                    to_blit.append(pygame.image.load('data/images/Texture/etats/special.png').convert_alpha())        
                                if 'Pesanteur' in etat:
                                    to_blit.append(pygame.image.load('data/images/Texture/etats/pesanteur.png').convert_alpha())
                                if 'Indéplaçable' in etat:
                                    to_blit.append(pygame.image.load('data/images/Texture/etats/indeplacable.png').convert_alpha())
                                if 'Lourd' in etat:
                                    to_blit.append(pygame.image.load('data/images/Texture/etats/lourd.png').convert_alpha())
                                if "Invunérable distance" in etat:
                                    to_blit.append(pygame.image.load('data/images/Texture/etats/invudis.png').convert_alpha())
                                if "Invunérable" in etat:
                                    to_blit.append(pygame.image.load('data/images/Texture/etats/invu.png').convert_alpha())
                            
                            X_img,Y_img = self.centered_x+26 - len(to_blit)*10, self.centered_y-35
                            for k in range(len(to_blit)):
                                fenetre.blit(to_blit[k], (X_img+k*20,Y_img))
                        
       
        
    def pointeurIso(self, M):
        clicGauche = pygame.mouse.get_pressed()[0]  # bool
        (x,y) = pygame.mouse.get_pos() 
       
        
        i,j = CanoToIso(x,y)
        if i < 0 or j < 0:
            return (1000, 1000, False) 
        
        i = int(i)
        j = int(j)
        
        if (i >= 0 and i < len(M)) and (j >= 0 and j < len(M[0])):
            return i,j, clicGauche
        else:
            return (1000, 1000, False)    
    
    
    def map_aleatoire(self, x, y):
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
        
        pos_depart = []
        for a in range(20):
            i,j= randint(1,x-2),randint(1,y-2)
            while (i,j) in pos_depart or (M[i][j] != 0):
                i,j= randint(1,x-2),randint(1,y-2)
            pos_depart.append((i,j))
        
        return (M, pos_depart)