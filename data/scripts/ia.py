import pygame

import data.scripts.functions as f
import data.scripts.personnages as p
import data.scripts.battle_functions as bf
import data.scripts.pathfinding as pf

def is_perso_killed(cibles):
    for perso in cibles:
        if perso.pv <= 0:
            return True
    return False

def recherche_cible(joueur, po_range, groupePersoCbt):
    perso_in_po = []
    for perso in groupePersoCbt:
        if perso.team != joueur.team:
            if perso.pos in po_range:
                perso_in_po.append(perso)
    if perso_in_po == []:
        return [], None
    perso_in_po = sorted(perso_in_po, key=lambda M: M.priorite, reverse=True)
    return [perso_in_po[0]], perso_in_po[0].pos

def ajout_cibles(M, sort, joueur, groupePersoCbt, team_voulue, pos_voulue = None):
    cibles = []
    
    pos_allies, pos_ennemis = [], [] # Dans pos_ennemis on aura les pos des personne de la team non voulue #
    for perso in groupePersoCbt:
        if perso.team == team_voulue:
            pos_allies.append(perso.pos)
        else:
            pos_ennemis.append(perso.pos)
            
    # On créer une liste PO avec toutes les cases ciblables et le nb d'entités voulue dans leur zone (si la pos voulue est dedans) #
    po_range = pf.pathfinding_po(M, groupePersoCbt, joueur, sort.num)[0]
    PO = []
    for case in po_range:  
        if case in pos_allies or case in pos_ennemis or not sort.cible_necessaire:
            zone_cible = pf.ajout_zone(M, joueur, sort.num, case)
            if pos_voulue in zone_cible:
                nb = 0
                for pos in pos_allies:
                    if pos in zone_cible:
                        nb += 1
                PO.append((case, nb, zone_cible))
    
    # On tri la liste PO selon le nb d'entité dedans #
    PO = sorted(PO, key=lambda M: M[1], reverse=True)
    
    if PO == []:
        return [], None
    
    zone_cible = PO[0][2]
    pos = PO[0][0]
    for perso in groupePersoCbt:
        if perso.pos in zone_cible:
            cibles.append(perso)
    
    return cibles, pos

def choix_cible_support(M, sort, joueur, groupePersoCbt, team):
    cibles = []
    
    pos_allies = []
    for perso in groupePersoCbt:
        if perso.team == team:
            pos_allies.append(perso.pos)
            
    # On créer une liste PO avec toutes les cases ciblables et le nb d'entités voulue dans leur zone (si la pos voulue est dedans) #
    po_range = pf.pathfinding_po(M, groupePersoCbt, joueur, sort.num)[0]
    PO = []
    for case in po_range:  
        if case in pos_allies or not sort.cible_necessaire:
            zone_cible = pf.ajout_zone(M, joueur, sort.num, case)
            nb = 0    
            if joueur.pos in zone_cible:
                nb += 2
            
            for pos in pos_allies:
                if pos in zone_cible:
                    nb += 1
            if nb > 0:
                PO.append((case, nb, zone_cible))
    
    # On tri la liste PO selon nb #
    PO = sorted(PO, key=lambda M: M[1], reverse=True)
    
    if PO == []:
        return [], None
    
    zone_cible = PO[0][2]
    pos = PO[0][0]
    for perso in groupePersoCbt:
        if perso.pos in zone_cible:
            cibles.append(perso)
    
    return cibles, pos

def choix_cible_soin(M, sort, joueur, groupePersoCbt, team):
    cibles = []
    
    allies = []
    pos_allies = []
    for perso in groupePersoCbt:
        if perso.team == team:
            pos_allies.append(perso.pos)
            allies.append(perso)
            
    # On créer une liste PO avec toutes les cases ciblables et le nb d'entités voulue dans leur zone (si la pos voulue est dedans) #
    po_range = pf.pathfinding_po(M, groupePersoCbt, joueur, sort.num)[0]
    PO = []
    for case in po_range:  
        if case in pos_allies or not sort.cible_necessaire:
            zone_cible = pf.ajout_zone(M, joueur, sort.num, case)
            nb = 0    
            if joueur.pos in zone_cible:
                if joueur.pv < joueur.pv_max:
                    nb += 2 *(joueur.pv_max - joueur.pv)
            
            for perso in allies:
                if perso.pos in zone_cible:
                    if perso.pv < perso.pv_max:
                        nb += (perso.pv_max - perso.pv)
            if nb > 0:
                PO.append((case, nb, zone_cible))
    
    # On tri la liste PO selon nb #
    PO = sorted(PO, key=lambda M: M[1], reverse=True)
    
    if PO == []:
        return [], None
    
    zone_cible = PO[0][2]
    pos = PO[0][0]
    for perso in groupePersoCbt:
        if perso.pos in zone_cible:
            cibles.append(perso)
    
    return cibles, pos

def liste_sorts(perso):
    sorts_offensifs, sorts_soin, sorts_tp, sorts_boost_deplacement, sorts_attirance, sorts_charge, sorts_boost_dg, sorts_invoc, sorts_malus, sorts_boost, sorts_fuite, sorts_autres = [], [], [], [], [], [], [], [], [], [], [], []
    for sort in perso.S:
        # Si le sort est lançable #
        
        if (sort.latence == 0 and sort.coup_par_tour > 0):
            isAutre = True
            if 'offensif' in sort.type:
                sorts_offensifs.append(sort)
                isAutre = False
            if 'support' in sort.type:
                sorts_soin.append(sort)
                isAutre = False
            if 'tp' in sort.type:
                sorts_tp.append(sort)
                isAutre = False
            if 'boost déplacement' in sort.type:
                sorts_boost_deplacement.append(sort)
                isAutre = False
            if 'attirance' in sort.type:
                sorts_attirance.append(sort)
                isAutre = False
            if 'charge' in sort.type:
                sorts_charge.append(sort)
                isAutre = False
            if 'boost dg' in sort.type:
                sorts_boost_dg.append(sort)
                isAutre = False
            if 'invoc' in sort.type:
                sorts_invoc.append(sort)
                isAutre = False
            if 'malus' in sort.type:
                sorts_malus.append(sort)
                isAutre = False
            if 'boost' in sort.type:
                sorts_boost.append(sort)
                isAutre = False
            if 'fuite' in sort.type:
                sorts_fuite.append(sort)
                isAutre = False
            if isAutre:
                sorts_autres.append(sort)
    return sorts_offensifs, sorts_soin, sorts_tp, sorts_boost_deplacement, sorts_attirance, sorts_charge, sorts_boost_dg, sorts_invoc, sorts_malus, sorts_boost, sorts_fuite, sorts_autres

def sort_prioritaire(liste_sorts):
    if liste_sorts == []:
        return None
    sort_prio = liste_sorts[0]
    for sort in liste_sorts:
        if sort.priorite > sort_prio.priorite and (sort.latence == 0 and sort.coup_par_tour > 0):
            sort_prio = sort   
        elif (sort.latence == 0 and sort.coup_par_tour > 0) and not (sort_prio.latence == 0 and sort_prio.coup_par_tour > 0):
            sort_prio = sort
    return sort_prio


def move_to(perso, way, cout, groupeGlobal):
    if way != []:
        perso.app.wait(250)
        for pos in way:
            perso.app.wait(50)
            perso.pos = pos
        perso.pm -= cout
        bf.affiche_point(-1*cout, perso, groupeGlobal, 'pm')
        
        if len(way) == 1:      # On rajoute la dernière pos dans last_pos #
            perso.last_pos = [perso.pos]
        elif len(way) > 1:
            perso.last_pos = [way[-2]]
        

def liste_entites(joueur, groupePersoCbt):
    j_ennemis = []
    invoc_ennemis = []
    j_allies = []
    invoc_allies = []
    for perso in groupePersoCbt:
        if perso.team == joueur.team:
            if perso.isInvoc:
                invoc_allies.append(perso)
            else:
                j_allies.append(perso)
        else:
            if perso.isInvoc:
                invoc_ennemis.append(perso)
            else:
                j_ennemis.append(perso)
    return j_ennemis, invoc_ennemis, j_allies, invoc_allies


def distance(pos1, pos2):
    (x, y) = pos1
    (X, Y) = pos2
    return abs(X-x) + abs(Y-y)

def cout_to(M, groupePerso, joueur, end, pos_depart = None):
    joueur.pm += 100
    best_way, cout = pf.pathfinding2(M, groupePerso, joueur, end, pos_depart)
    joueur.pm -= 100
    return cout

def cases_voisines(M, pos):
    voisinage = []
    (x, y) = pos
    if x+1 >= 0 and y >= 0 and x+1 < len(M) and y < len(M[0]):
        voisinage.append([(x+1,y),M[x+1][y]])
    if x-1 >= 0 and y >= 0 and x-1 < len(M) and y < len(M[0]):
        voisinage.append([(x-1,y),M[x-1][y]])
    if x >= 0 and y+1 >= 0 and x < len(M) and y+1 < len(M[0]):
        voisinage.append([(x,y+1),M[x][y+1]])
    if x >= 0 and y-1 >= 0 and x < len(M) and y-1 < len(M[0]):
        voisinage.append([(x,y-1),M[x][y-1]])
    return voisinage

def check_sides(M, pos, pos_joueurs):
    (x, y) = pos
    
    liberte = [[False, (x+1, y)], [False, (x-1, y)], [False,(x, y+1)], [False, (x, y-1)]]  # Droite/Gauche/Bas/Haut
    if x+1 >= 0 and y >= 0 and x+1 < len(M) and y < len(M[0]):
        if M[x+1][y] in [0,2,3]:
            if (x+1, y) not in pos_joueurs:
                liberte[0][0] = True
    if x-1 >= 0 and y >= 0 and x-1 < len(M) and y < len(M[0]):
        if M[x-1][y] in [0,2,3]:
            if (x-1, y) not in pos_joueurs:
                liberte[1][0] = True
    if x >= 0 and y+1 >= 0 and x < len(M) and y+1 < len(M[0]):
        if M[x][y+1] in [0,2,3]:
            if (x, y+1) not in pos_joueurs:
                liberte[2][0] = True
    if x >= 0 and y-1 >= 0 and x < len(M) and y-1 < len(M[0]):
        if M[x][y-1] in [0,2,3]:
            if (x, y-1) not in pos_joueurs:
                liberte[3][0] = True
    return liberte

def check_zone(M, sort, groupePersoCbt, joueur, pos_joueurs_sans_ia, pos_cible):
    #liberte = [[False, pos] for pos in zone_cible = pf.ajout_zone(self.map_data, joueur, sort.num, (X,Y))] ICI Il faudra aussi ajouter à la zone, la zone d'effet
    liberte = [[False, pos] for pos in pf.pathfinding_po(M, groupePersoCbt, joueur, sort.num, pos_cible)[0]]
    for i in range(len(liberte)):
        pos = liberte[i][1]
        if pos not in pos_joueurs_sans_ia and M[pos[0]][pos[1]] in [0,2,3]:
            liberte[i][0] = True
    return liberte
    


def way_to_closest_pos(M, joueur, liste_pos, groupePersoCbt):
    """ Retourne le chemin le moins coûteux de liste_pos """
    best_ways = []
    joueur.pm += 100
    for pos in liste_pos:
        best_way, cout = pf.pathfinding2(M, groupePersoCbt, joueur, pos)
        if best_way != []:
            best_ways.append((best_way, cout))
        elif pos == joueur.pos:
            best_ways.append(([pos], 0))
    joueur.pm -= 100
    # Si il n'y a pas de chemin possible #
    if best_ways == []:
        return [([],0)]

    best_ways = sorted(best_ways, key=lambda M: M[1], reverse=False)
    return best_ways

def tp_to_closest_pos(M, joueur, pos_cible, groupePersoCbt, po_range):
    """ Retourne le chemin le moins coûteux de liste_pos """
    best_ways = []
    joueur.pm += 100
    for pos in po_range:
        best_way, cout = pf.pathfinding2(M, groupePersoCbt, joueur, pos_cible, pos_depart = pos)
        if best_way != []:
            best_ways.append((best_way, cout, pos))
        elif pos == joueur.pos:
            best_ways.append(([pos], 0, pos))
    joueur.pm -= 100
    # Si il n'y a pas de chemin possible #
    if best_ways == []:
        return [([],0, pos)]

    best_ways = sorted(best_ways, key=lambda M: M[1], reverse=False)
    return best_ways


def gradient_perso(M, M_priorite, x, y, coeff = 1):
    for i in range(len(M_priorite)):
        for j in range(len(M_priorite[0])):
            if (i,j) != (x,y):
                M_priorite[i][j] += round(2 + 1/(2*coeff*(distance((i,j), (x,y)))), 2)
            if M[i][j] in [1,-1]:
                M_priorite[i][j] = -1000

def way_to_pos_cible(pos_cible, perso, M, groupePersoCbt):
    perso.pm += 100
    best_way, cout = pf.pathfinding2(M, groupePersoCbt, perso, pos_cible)
    perso.pm -= 100
    # On inverse la liste pour que le dernier élément soit la dernière case voulue #
    best_way.reverse()
    # On cherche jusqu'où peut avancer l'ia #
    pm = perso.pm + perso.somme_boost('pm')
    if cout > pm :
        possible = False
    else:
        return best_way, cout, True
    
    if best_way != []:
        
        i = pm - 1
        if pm > len(best_way):
            i = len(best_way)-1
        way, cout = pf.pathfinding2(M, groupePersoCbt, perso, best_way[i])
        way.reverse()
        while way == [] and i > 0:
            i-=1
            way, cout = pf.pathfinding2(M, groupePersoCbt, perso, best_way[i])
            way.reverse()
        
     
        return way, cout, possible
    else:
        return [], cout, False
    
def ajout_priorite_perso(M_priorite, ennemi, coeff_de_base, M, sort, groupePersoCbt, joueur, pos_joueurs_sans_ia, coeff_gradient = 1):
    " Modifie M_priorite "
    (i, j) = ennemi.pos
    M_priorite[i][j] += coeff_de_base + 3*ennemi.somme_boost('po') - ennemi.somme_boost('res') + int(60*(1-ennemi.pv/ennemi.pv_max)) + 5*(joueur.somme_boost('tacle')+joueur.tacle - ennemi.fuite - ennemi.somme_boost('fuite'))
    gradient_perso(M, M_priorite, i, j, coeff = coeff_gradient)
    ennemi.priorite = M_priorite[i][j]
    # On veut ajouter un boost selon le coût pour aller sur la case adjacente à ce perso #
    # On récupère le voisinage #
    liberte = check_zone(M, sort, groupePersoCbt, joueur, pos_joueurs_sans_ia, (i,j))
    # liberte = check_sides(M, ennemi.pos, pos_joueurs_sans_ia)
    liste_pos = []
    for libre,pos in liberte:
        if libre:
            liste_pos.append(pos)
            
    # On cherche la pos la moins coûteuse #
    L = way_to_closest_pos(M, joueur, liste_pos, groupePersoCbt)
    
    best_ways, couts = [], []
    for best_way in L:
        best_ways.append(best_way[0])
        couts.append(best_way[1])
    
    # Si la case n'est pas accessible #
    if best_ways == [[]] and distance(joueur.pos, ennemi.pos) > 1:
        M_priorite[i][j] = -10000
        ennemi.priorite = -10000
    else:
        # Sinon pour chaque case possibles, on ajoute un bonus #
        priorite_cible = M_priorite[i][j]
        presence = False
        for k in range(len(best_ways)):
            if best_ways[k] != []:
                (x,y) = best_ways[k][0]
                M_priorite[x][y] = priorite_cible + 4*int(1/((0.15 + couts[k]/100)**2))
                if (x,y) == (i,j):
                    presence = True
                    ennemi.priorite += priorite_cible + 4*int(1/((0.15 + couts[k]/100)**2))
        if not presence:
            M_priorite[i][j] = 0
            

def choix_cible(M, joueur, groupePersoCbt, sort, ChatTextuel):
    j_ennemis, invoc_ennemis, j_allies, invoc_allies = liste_entites(joueur, groupePersoCbt)
    pos_ennemis = [perso.pos for perso in j_ennemis + invoc_ennemis]
    pos_joueurs = pos_ennemis + [perso.pos for perso in j_allies + invoc_allies]
    pos_joueurs_sans_ia = [pos for pos in pos_joueurs if pos != joueur.pos]

    
    M_priorite = [[0 for i in range(len(M[0]))] for j in range(len(M))]

    # Si l'IA est de type combatif #
    if joueur.type_ia == 'combatif':
        for ennemi in j_ennemis:
            ajout_priorite_perso(M_priorite, ennemi, 75, M, sort, groupePersoCbt, joueur, pos_joueurs_sans_ia)
                
        for invoc_ennemi in invoc_ennemis:
            coeff_de_base = invoc_ennemi.coeff_de_base
            if invoc_ennemi.isStatic:
                coeff_de_base = 5
            ajout_priorite_perso(M_priorite, invoc_ennemi, coeff_de_base, M, sort, groupePersoCbt, joueur, pos_joueurs_sans_ia, coeff_gradient=2)

        for allie in j_allies:
            (i, j) = allie.pos
            if allie != joueur:
                voisinage = cases_voisines(M, allie.pos)
                for (x,y),val in voisinage:
                    if (x,y) not in pos_joueurs:
                        M_priorite[x][y] += 5

        # On met un malus pour les cases en ligne des ennemis si l'ennemi est à plus de 2 cases #
        for ennemi in j_ennemis:
            (i, j) = ennemi.pos
            if distance((i,j),ennemi.pos) > 2:
                for l in range(len(M)):
                    for k in range(len(M[0])):
                        if k == j and (l,k) not in pos_ennemis:
                            M_priorite[l][k] -= 10
                        if l == i and (l,k) not in pos_ennemis:
                            M_priorite[l][k] -= 10
            
            '''
            M_print = [[M_priorite[i-2][j+2], M_priorite[i-2][j+1], M_priorite[i-2][j], M_priorite[i-2][j-1], M_priorite[i-2][j-2]],
                       [M_priorite[i-1][j+2], M_priorite[i-1][j+1], M_priorite[i-1][j], M_priorite[i-1][j-1], M_priorite[i-1][j-2]],
                       [M_priorite[i][j+2], M_priorite[i][j+1], print(ennemi.priorite), M_priorite[i][j-1], M_priorite[i][j-2]],
                       [M_priorite[i+1][j+2], M_priorite[i+1][j+1], M_priorite[i+1][j], M_priorite[i+1][j-1], M_priorite[i+1][j-2]],
                       [M_priorite[i+2][j+2], M_priorite[i+2][j+1], M_priorite[i+2][j], M_priorite[i+2][j-1], M_priorite[i+2][j-2]]]
            print(M_print[0])
            print(M_print[1])
            print(M_print[2])
            print(M_print[3])
            print(M_print[4])'''
            
            
        for ennemi in invoc_ennemis:
            (i, j) = ennemi.pos
            if distance((i,j),ennemi.pos) > 2:
                for l in range(len(M)):
                    for k in range(len(M[0])):
                        if k == j and (l,k) not in pos_ennemis:
                            M_priorite[l][k] -= 3
                        if l == i and (l,k) not in pos_ennemis:
                            M_priorite[l][k] -= 3
                 
    
    # On récupère la case de priorité maximale ----------------------------------------------------------- #
    max_M= [0,0,0]
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M_priorite[i][j] > max_M[0]:
                max_M = [M_priorite[i][j], i, j]
                
    # Si la case de priorité max est celle du joueur ----------------------------------------------------- #
    if (max_M[1],max_M[2]) == joueur.pos:
        return joueur.pos, joueur.pos, joueur
    
    # Sinon on cherche celle libre la plus proche -------------------------------------------------------- #
    # On cherche le joueur avec la plus grosse priorité
    cible = joueur
    for perso in groupePersoCbt:
        print(perso.pseudo,' : ', perso.priorite)
        if perso.team != joueur.pos:
            if perso.priorite > cible.priorite:
                cible = perso

    return (max_M[1],max_M[2]), cible.pos, cible

    
class IA(pygame.sprite.Sprite):
    def __init__(self, perso, type_ia):
        self.perso = perso
        self.team_adverse = 1
        if self.perso.team == 1:
            self.team_adverse = 2
        self.type_ia = type_ia
        self.tick = 0
        self.perso.time_to_wait = 300
        self.ia_killed_someone = False

    def tour(self, app, M, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, ChatTextuel):
        if self.type_ia == 'combatif':
            self.combatif(app, M, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, app.groupeGlyphe, ChatTextuel)

    def combatif(self, app, M, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        pos_ennemis = [perso.pos for perso in groupePersoCbt if perso.team != self.perso.team]
        (X, Y) = self.perso.pos
        isPlaying = True
        self.perso.tour_fini = False
        i = 0
        while pos_ennemis != [] and isPlaying and i < 4:
            
            self.ia_killed_someone = False
            sorts_offensifs, sorts_soin, sorts_tp, sorts_boost_deplacement, sorts_attirance, sorts_charge, sorts_boost_dg, sorts_invoc, sorts_malus, sorts_boost, sorts_fuite, sorts_autres = liste_sorts(self.perso)
            
            sort_offensif_prioritaire = sort_prioritaire(sorts_offensifs)
            
            # On récupère la case prioritaire #
            pos_cible, pos_max, cible = choix_cible(M, self.perso, groupePersoCbt, sort_offensif_prioritaire, ChatTextuel)
            
            if cible.priorite < -1000:
                pos_max = pos_cible
                
            if pos_cible != None or pos_cible != self.joueur.pos:
                # On récupère le chemin jusqu'à cette case #   
                way, cout, possible = way_to_pos_cible(pos_cible, self.perso, M, groupePersoCbt)
    
            # PHASE 1 : Si on ne peut pas atteindre, on utilise les sorts TP/PM/FUITE -------------------------------------------------- #
            po_range_sort_offensif = pf.pathfinding_po(M, groupePersoCbt, self.perso, sort_offensif_prioritaire.num, pos_max)[0]
            if way != []:
                if not possible and way[-1] not in po_range_sort_offensif:
                    for sort in sorts_tp:
                        while (sort.latence == 0 and sort.coup_par_tour > 0) and sort.cout <= self.perso.pa + self.perso.somme_boost('pa'):
                            po_range = pf.pathfinding_po(M, groupePersoCbt, self.perso, sort.num)[0]
                            # Si on peut se tp à la meilleure case #
                            if pos_cible in po_range:
                                self.perso.use_sort(sort.num, self.perso, [], M, None, pos_cible, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, app.ChatTextuel)
                            else:
                                best_ways = tp_to_closest_pos(M, self.perso, pos_cible, groupePersoCbt, po_range)
                                if best_ways[0][0] != []:
                                    # On vérifie que se tp en vaut la peine ----------- #
                                    # On cherche un nouveau chemin à partir de la pos tp #
                                    cout1 = cout_to(M, groupePersoCbt, self.perso, pos_cible)
                                    cout2 = cout_to(M, groupePersoCbt, self.perso, pos_cible, pos_depart = best_ways[0][2])
                                    if cout2 < cout1:
                                        self.perso.use_sort(sort.num, self.perso, [], M, None, best_ways[0][2], groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, app.ChatTextuel)
                                    else:
                                        break
                                else:
                                    break
                
                    # On cherche un nouveau chemin #
                    pos_cible, pos_max, cible = choix_cible(M, self.perso, groupePersoCbt, sort_offensif_prioritaire, ChatTextuel)
                    if cible.priorite < -1000:
                        pos_max = pos_cible
                    if pos_cible != None:       
                        way, cout, possible = way_to_pos_cible(pos_cible, self.perso, M, groupePersoCbt)
                        
            if way != []:        
                if not possible and way[-1] not in po_range_sort_offensif:            
                    for sort in sorts_boost_deplacement:
                        while (sort.latence == 0 and sort.coup_par_tour > 0) and sort.cout <= self.perso.pa + self.perso.somme_boost('pa'):
                            if sort.zone_cible != 'case':
                                cibles, pos = ajout_cibles(M, sort, self.perso, groupePersoCbt, self.perso.team, pos_voulue = self.perso.pos)
                            else:
                                cibles, pos = [self.perso], self.perso.pos
                            if cibles != []:
                                self.perso.use_sort(sort.num, self.perso, cibles, M, None, self.perso.pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, app.ChatTextuel)     
                                self.ia_killed_someone = is_perso_killed(cibles)
                                if self.ia_killed_someone:
                                    break
                            else:
                                break
                        
                    # On cherche un nouveau chemin #
                    pos_cible, pos_max, cible = choix_cible(M, self.perso, groupePersoCbt, sort_offensif_prioritaire, ChatTextuel)
                    if cible.priorite < -1000:
                        pos_max = pos_cible
                    if pos_cible != None:       
                        way, cout, possible = way_to_pos_cible(pos_cible, self.perso, M, groupePersoCbt)
            if self.ia_killed_someone:
                continue
            
            # On bouge #
            if way != []:
                move_to(self.perso, way, cout, groupeGlobal)
            
            # Sorts d'attirance/charge SI on ne peut pas lancer le sort offensif
            if way != [] and self.perso.pos not in po_range_sort_offensif:
                for sort in sorts_attirance:
                    while (sort.latence == 0 and sort.coup_par_tour > 0) and sort.cout <= self.perso.pa + self.perso.somme_boost('pa') and not self.ia_killed_someone:
                        po_range = pf.pathfinding_po(M, groupePersoCbt, self.perso, sort.num)[0]
                        cibles, pos = recherche_cible(self.perso, po_range, groupePersoCbt)
                        if cibles != []:
                            self.perso.use_sort(sort.num, self.perso, cibles, M, None, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, app.ChatTextuel)  
                            self.ia_killed_someone = is_perso_killed(cibles)
                            if self.ia_killed_someone:
                                break
                        else:
                            break  
            if self.ia_killed_someone:
                continue
                    
            if way != [] and self.perso.pos not in po_range_sort_offensif:   
                for sort in sorts_charge:
                    while (sort.latence == 0 and sort.coup_par_tour > 0) and sort.cout <= self.perso.pa + self.perso.somme_boost('pa') and not self.ia_killed_someone:
                        po_range = pf.pathfinding_po(M, groupePersoCbt, self.perso, sort.num)[0]
                        cibles, pos = recherche_cible(self.perso, po_range, groupePersoCbt)                               
                        if cibles != []:
                            self.perso.use_sort(sort.num, self.perso, cibles, M, None, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, app.ChatTextuel) 
                            self.ia_killed_someone = is_perso_killed(cibles)
                            if self.ia_killed_someone:
                                break
                        else:
                            break
            if self.ia_killed_someone:
                continue
                    
            # PHASE 2 : Si on peut atteindre la cible, on se boost et tape ---------------------------------------------------- #
            for sort in sorts_boost_dg:
                while (sort.latence == 0 and sort.coup_par_tour > 0) and sort.cout <= self.perso.pa + self.perso.somme_boost('pa') and not self.ia_killed_someone:
                    
                    cibles, pos = choix_cible_support(M, sort, self.perso, groupePersoCbt, self.perso.team)                              
                    if cibles != []:
                        self.perso.use_sort(sort.num, self.perso, cibles, M, None, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, app.ChatTextuel)     
                        self.ia_killed_someone = is_perso_killed(cibles)
                        if self.ia_killed_someone:
                            break
                    else:
                        break
            if self.ia_killed_someone:
                continue
                        
            while sorts_offensifs != [] and not self.ia_killed_someone: 
                sort = sort_prioritaire(sorts_offensifs)
                po_range = pf.pathfinding_po(M, groupePersoCbt, self.perso, sort.num)[0]
                if sort.zone_cible != 'case':
                    cibles, pos = ajout_cibles(M, sort, self.perso, groupePersoCbt, self.team_adverse, pos_max)
                else:
                    cibles, pos = recherche_cible(self.perso, po_range, groupePersoCbt)
        
                while (sort.latence == 0 and sort.coup_par_tour > 0) and sort.cout <= self.perso.pa + self.perso.somme_boost('pa') and not self.ia_killed_someone:
                    if cibles != []:
                        self.perso.use_sort(sort.num, self.perso, cibles, M, None, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, app.ChatTextuel)  
                        self.ia_killed_someone = is_perso_killed(cibles)
                        if self.ia_killed_someone:
                            break
                    else:
                        break
                sorts_offensifs.remove(sort)
            if self.ia_killed_someone:
                continue
            
            
            # PHASE 3 : Sorts autres : soins/invoc/malus/boost ----------------------------------------------------------------- #
            for sort in sorts_soin:
                while (sort.latence == 0 and sort.coup_par_tour > 0) and sort.cout <= self.perso.pa + self.perso.somme_boost('pa') and not self.ia_killed_someone:
                    cibles, pos = choix_cible_soin(M, sort, self.perso, groupePersoCbt, self.perso.team)
                    if cibles != []:
                        self.perso.use_sort(sort.num, self.perso, cibles, M, None, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, app.ChatTextuel)     
                        self.ia_killed_someone = is_perso_killed(cibles)
                        if self.ia_killed_someone:
                            break
                    else:
                        break   
            if self.ia_killed_someone:
                continue
                                  
            for sort in sorts_invoc:
                while (sort.latence == 0 and sort.coup_par_tour > 0) and sort.cout <= self.perso.pa + self.perso.somme_boost('pa') and not self.ia_killed_someone:
                    #cible = choix_cible_invoc(M, sort, self.perso, groupePersoCbt)
                    if cibles != []:
                        self.perso.use_sort(sort.num, self.perso, cibles, M, None, self.perso.pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, app.ChatTextuel)     
                        self.ia_killed_someone = is_perso_killed(cibles)
                        if self.ia_killed_someone:
                            break
                    else:
                        break  
            if self.ia_killed_someone:
                continue
                    
            for sort in sorts_malus:
                while (sort.latence == 0 and sort.coup_par_tour > 0) and sort.cout <= self.perso.pa + self.perso.somme_boost('pa') and not self.ia_killed_someone:
                    if sort.zone_cible != 'case':
                        cibles, pos = ajout_cibles(M, sort, self.perso, groupePersoCbt, self.team_adverse, pos_max)
                    else:
                        cibles, pos = recherche_cible(self.perso, po_range, groupePersoCbt)
                    if cibles != []:
                        self.perso.use_sort(sort.num, self.perso, cibles, M, None, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, app.ChatTextuel)  
                        self.ia_killed_someone = is_perso_killed(cibles)
                        if self.ia_killed_someone:
                            break
                    else:
                        break  
            if self.ia_killed_someone:
                continue
            
            for sort in sorts_boost:
                while (sort.latence == 0 and sort.coup_par_tour > 0) and sort.cout <= self.perso.pa + self.perso.somme_boost('pa') and not self.ia_killed_someone:
                    cibles, pos = choix_cible_support(M, sort, self.perso, groupePersoCbt, self.perso.team)
                    if cibles != []:
                        self.perso.use_sort(sort.num, self.perso, cibles, M, None, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, app.ChatTextuel)     
                        self.ia_killed_someone = is_perso_killed(cibles)
                        if self.ia_killed_someone:
                            break
                    else:
                        break
            if self.ia_killed_someone:
                continue
                    
            (x,y) = self.perso.pos
            po_range = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
            cibles, pos = recherche_cible(self.perso, po_range, groupePersoCbt) 
            if self.perso.pm + self.perso.somme_boost('pm') <= 0 or pos in po_range:
                isPlaying = False
            i += 1
        
        self.perso.tour_fini = True
        self.perso.app.tick = pygame.time.get_ticks()