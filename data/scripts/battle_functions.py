from random import randint
import pygame
from pygame.locals import *
import data.scripts.functions as f

def distance(pos1, pos2):
    (x, y) = pos1
    (X, Y) = pos2
    return abs(X-x) + abs(Y-y)

def IsoToCano(i,j):
    x = 640 + 32*(i-j) + 48
    y = 0 + 16*(i+j) - 302
    return x, y


# Fonctions de Combat --------------------------------- #


# Classement d'initiative ----------------------------- #

def classement_ini(J):
    '''Renvoie le perso qui commence.'''
    Ini_t1 = [[perso,perso.ini] for perso in J if perso.team == 1]
    Ini_t2 = [[perso,perso.ini] for perso in J if perso.team == 2]
    
    # On cherche la team qui a le plus d'ini ET on range tri les deux listes #
    ini = [0,0]
    j = 0
    L_ini = [Ini_t1,Ini_t2]
    for j in range(2):  
        L_ini[j] = sorted(L_ini[j], key = lambda M : M[1], reverse = True)
        for perso,init in L_ini[j]:
            ini[j] += init

    # La team ayant la plus grande ini sera première dans la liste L #
    L = []
    if ini[0] >= ini[1]:
        L.append(L_ini[0])
        L.append(L_ini[1])
    else:
        L.append(L_ini[1])
        L.append(L_ini[0])
    
    # On complète les deux listes de L (avec des None) pour qu'elles aient la même longueur #
    if len(L[0]) > len(L[1]):
        for i in range(len(L[0]) - len(L[1])):
            L[1].append(None)
    elif len(L[1]) > len(L[0]):
        for i in range(len(L[1]) - len(L[0])):
            L[0].append(None)
               
    # On ajoute dans la liste finale en alterné les joueurs de plus grosse ini #
    Ini = []   
    for i in range(len(L[0])):
        if L[0][i] != None:
            Ini.append(L[0][i])    
        if L[1][i] != None:
            Ini.append(L[1][i])     
    
    # On attribut les ordres d'ini à chaque joueur #
    for i in range(len(Ini)):
        Ini[i][0].ordre_ini = i
    
    return Ini[0][0]

   
        
#Fonctions de fin de Combat --------------------------- #
def init_stats(perso):
    perso.pv = perso.pv_max_basic
    perso.pv_max = perso.pv_max_basic
    perso.pa = perso.pa_max
    perso.pm = perso.pm_max
    perso.isReady = False
    perso.tour = 0
    for B in perso.Boost:
        for boost in B:
            boost[1] = 0
    perso.Invocs = []
    perso.pos_depart = (0,0)
    perso.pos = (0,0)
    perso.last_pos = []
    perso.nb_tour = 0
    

def up_niveau(perso):
    # Vérifie dans les tables d'xp si le nb d'exp fait monter d'un niveau ou pas #
    EXP = [20000]
    for i in range(199):
        EXP.append(EXP[-1] + (i*10000+30000))
    for i in range(len(EXP)):
        if perso.exp >= EXP[i]:
            if perso.niveau < i+1:
                perso.niveau += 1
                print(perso.pseudo + ' passe au niveau ' + str(perso.niveau)+' !')
        
        
        
def xp(team_gagnante, gagnant, perdant, niv_g, niv_p, groupeGlobalPerso):

    nb_exp = int(100000*len(perdant)/len(gagnant) + 10000 * niv_p/niv_g)
    
    EXP = [20000]
    for i in range(199):
        EXP.append(EXP[-1] + (i*10000+30000))
    
    for perso in gagnant:
        perso.exp += nb_exp
        print(perso.pseudo + ' gagne ' + str(nb_exp) + " points d'expérience.")
        
        if perso.niveau < 200:
            print('Xp total : ' + str(perso.exp) + '/' + str(EXP[perso.niveau-1]))
            perso.exp_next_niv = EXP[perso.niveau-1]
        
            up_niveau(perso)
    return nb_exp


def fin_de_combat(groupePersoCbt, groupeGlobalPerso):
    team_gagnante = 0
    tours = []
    # On récupère l'équipe gagnante #
    for perso in groupePersoCbt:
        team_gagnante = perso.team
    
    gagnant, perdant = [], []
    niv_g, niv_p = 0, 0
    
    # On comptabilise le nombre et niveaux des perdants #
    for perso in groupeGlobalPerso:
        if perso in groupePersoCbt:
            tours.append(perso.nb_tour)
        if not perso.isInvoc:
            init_stats(perso)
            if perso.team == team_gagnante:
                gagnant.append(perso)
                niv_g += perso.niveau
            else:
                perdant.append(perso)
                niv_p += perso.niveau
            if perso not in groupePersoCbt:
                groupePersoCbt.add(perso)
           
    # On fait xp tout le monde #
    nb_exp = xp(team_gagnante, gagnant, perdant, niv_g, niv_p, groupeGlobalPerso)
    
    # On sauvegarde l'xp #
    for perso in gagnant:
        fichier = open('data/save/joueurs/'+perso.pseudo+'.txt','w', encoding='utf-8')
        fichier.write(perso.pseudo + '\n' + str(perso.niveau) + '\n' + str(perso.exp) + '\n' + perso.nom_classe + '\n')
        fichier.write('\n')
        fichier.close()
    
    return gagnant, perdant, nb_exp, max(tours)
    
# Fonctions d'affichage ------------------------------------------------------- #
def affiche_point(nb, cible, groupeGlobal, point, decalage_y = 0):
    couleur = (255,255,255)
    
    plus_moins = '-'
    if nb >= 0 :
        plus_moins = '+'
        
    if point == 'pa':
        couleur = (0,25,255)
    elif point == 'pm':
        couleur = (160,87,47)
     
    taille = 15
    
    (x,y) = IsoToCano(cible.pos[0], cible.pos[1])
    y += decalage_y
    texte = f.TexteEphemere(plus_moins + str(abs(nb)), couleur, 'styleb', x+32, y+32, taille*25, taille*25, taille-5)
    groupeGlobal.add(texte)

    
def affiche_dg(dg, nb_dg, cible, groupeGlobal, ChatTextuel, decalage_y = 0, couleur = (255,0,0), mort = False):
    plus_moins = ''
    if int(dg-nb_dg) >= 0 :
        plus_moins = '+'
    if mort:
        ChatTextuel.ajout(" - {} perd {} PV !".format(cible.pseudo, dg))
    else:
        ChatTextuel.ajout(" - {} perd {} PV ({}{}{}) !".format(cible.pseudo, dg, int(nb_dg), plus_moins, int(dg-nb_dg)))
    
    taille = 15
    
    (x,y) = IsoToCano(cible.pos[0], cible.pos[1])
    y += decalage_y
    texte = f.TexteEphemere('-' + str(dg), couleur, 'styleb', x+32, y+32, taille*25, taille*25, taille)
    groupeGlobal.add(texte)
    
    
def affiche_soin(soin, cible, groupeGlobal, ChatTextuel):
    if soin > 0:
        ChatTextuel.ajout(" - {} gagne {} PV !".format(cible.pseudo, soin))
        
        taille = 15
            
        (x,y) = IsoToCano(cible.pos[0], cible.pos[1])
        texte = f.TexteEphemere('+' + str(soin), (255,0,0), 'styleb', x+32, y+32, taille*25, taille*25, taille)
        groupeGlobal.add(texte)
 

# Fonctions spéciales sorts --------------------------------------------------- #
def pile_face_etat(cible, ChatTextuel):
    for etat in cible.etats:
        if 'pile-face' in etat:
            chance = randint(1, 2)
            if chance == 1:
                cible.bPui.append([etat[2],2])
                ChatTextuel.ajout("{} gagne {} puissance pour 2 tours !".format(cible.pseudo, etat[2]))
            else:
                cible.bRes.append([etat[3],2])
                ChatTextuel.ajout("{} perd {}% de résistance pour 2 tours !".format(cible.pseudo, etat[3]))
                
              

# Fonctions pour le combat ---------------------------------------------------- #
def tp(M, position, joueur, groupePersoCbt):
    pesanteur = False
    for etat in joueur.etats:
        if 'Pesanteur' in etat and etat[1] > 0:
            pesanteur = True
            break
    if not pesanteur:    
        (x,y) = position
        lastpos = joueur.pos
        presence = False
        if x >= 0 and y >=0 and x < len(M) and y < len(M[0]):
            if M[x][y] in [0,2,3]:
                for perso in groupePersoCbt:
                    if perso.pos == (x,y):
                        presence = True
                        joueur.pos, perso.pos = perso.pos, joueur.pos
                        perso.last_pos.append((x,y))
                        joueur.last_pos.append(lastpos)
                if not presence:
                    joueur.last_pos.append(lastpos)
                    joueur.pos = (x,y)


def mort(cible, groupePersoCbt, groupePersoHorsCbt, groupeGlyphe, ChatTextuel):
    cible.pv = 0
    
    for g in cible.Glyphes:
        groupeGlyphe.remove(g)
    cible.Glyphes = []
    
    if cible.isInvoc:
        if cible in cible.parent.Invocs:
            cible.parent.Invocs.remove(cible)
        
    joueur = None
    for perso in groupePersoCbt:
        if perso.ordre_ini == 0:
            joueur = perso
            break
    
    ChatTextuel.ajout("{} est mort !".format(cible.pseudo))
    groupePersoHorsCbt.add(cible)
    groupePersoCbt.remove(cible)
    # Change les ordre d'initiative #
    for perso in groupePersoCbt :
        if perso.ordre_ini > cible.ordre_ini:
            perso.ordre_ini -= 1
    
    for invoc in cible.Invocs:
        invoc.pv = 0
        ChatTextuel.ajout("{} est mort !".format(invoc.pseudo))
        groupePersoHorsCbt.add(invoc)
        groupePersoCbt.remove(invoc)
        # Change les ordre d'initiative #
        for perso in groupePersoCbt :
            if perso.ordre_ini > cible.ordre_ini:
                perso.ordre_ini -= 1
    
    if joueur == cible:
        # On modifie l'ordre d'ini pour ne pas passer le tour du joueur qui joue après le mort #
        for perso in groupePersoCbt:
            if perso.ordre_ini == len(groupePersoCbt):
                perso.ordre_ini = 0
            else:
                perso.ordre_ini += 1
    
    
    for i in range(joueur.ordre_ini):
        for perso in groupePersoCbt:       
            if perso.ordre_ini == 0:
                perso.ordre_ini = len(groupePersoCbt)-1
            else:
                perso.ordre_ini -= 1
            
    
    
def erosion(dg, cible):
    if dg > 0:
        sum_ero = cible.somme_boost('ero') + 0.1
        cible.pv_max = int(cible.pv_max - sum_ero*dg)
        if cible.pv_max <= 0:
            cible.pv_max = 1
       
def dg(nb_DG, joueur, cible, pos, sort, ChatTextuel):
    reduc_dist = sort.reduct_dist
    
    if reduc_dist:
        reduction_distance = 0.1*(abs(cible.pos[0]-pos[0])+abs(cible.pos[1]-pos[1]))
    else:
        reduction_distance = 0
        
    for etat in cible.etats:
        if "Invunérable distance" in etat:
            reduction_distance = 10000*(abs(cible.pos[0]-joueur.pos[0]) + abs(cible.pos[1]-joueur.pos[1]))
            
    sum_pui = joueur.somme_boost('pui')
    sum_dmg = joueur.somme_boost('dmg')
    sum_res = cible.somme_boost('res')
    
    if distance(joueur.pos, cible.pos) > 1:
        sum_res += cible.somme_boost('res dis')
    else:
        sum_res += cible.somme_boost('res cac') 
    
    # Puissance négative correspond à puissance nulle #
    if sum_pui < 0:
        sum_pui = 0
    
    Dg = int((1 - reduction_distance)*((1 + (sum_pui/100))*(1 - (sum_res/100))* nb_DG + sum_dmg))
    erosion(Dg, cible)  # On applique l'érosion avant la perte de bouclier #
    
    # Perte de bouclier #
    perte_boubou = 0
    for boubou in cible.Boost[5]:
        if boubou[1] > 0:
            if boubou[0] < Dg:
                perte_boubou += boubou[0]
                Dg -= boubou[0]
                boubou[0] = 0
            else:
                perte_boubou += Dg
                boubou[0] -= Dg
                Dg = 0
    if perte_boubou > 0:
        ChatTextuel.ajout(" - {} perd {} Bouclier !".format(cible.pseudo, perte_boubou))       
          
    # Effet Pile-face #
    if cible.nom_classe == 'Chat':
        pile_face_etat(cible, ChatTextuel)
        
    return Dg

def Vdv(nb_dg, cible):
    Soin = nb_dg//2    
    if cible.pv + Soin > cible.pv_max:
        Soin = cible.pv_max - cible.pv
    return Soin

def soin(nb_soin, joueur, cible, pos, sort):
    reduc_dist = sort.reduct_dist
    if reduc_dist:
        reduction_distance = 0.1*(abs(cible.pos[0]-pos[0])+abs(cible.pos[1]-pos[1]))
    else:
        reduction_distance = 0
    sum_pui = joueur.somme_boost('pui')
    
    # Puissance négative correspond à puissance nulle #
    if sum_pui < 0:
        sum_pui = 0
        
    Soin = int((1 - reduction_distance)*(1 + (sum_pui/100))* nb_soin)
    
    if cible.pv + Soin > cible.pv_max:
        Soin = cible.pv_max - cible.pv

    return Soin
    

def poussee(nb_cases, joueur, cible, pos, M, sort, groupePersoCbt, ChatTextuel, poussee_selon_pos = False):
    
    sum_dopou = joueur.somme_boost('dopou')
    sum_respou = cible.somme_boost('res pou')
    
    (X,Y) = joueur.pos
    if sort.poussee_selon_centre:
        (X,Y) = pos

    (x,y) = cible.pos
    i,j = x,y 
    pos_joueurs = [perso.pos for perso in groupePersoCbt]
    
    # Si la case cible est en diago #
    if abs(X-x) == abs(Y-y):
        cases_range = nb_cases//2+1
        if cases_range == 1:
            cases_range += 1
        for k in range(1, cases_range):
            if Y-y > 0:
                l = -k
                m1 = 1
            else:
                l = k
                m1 = -1
            if X-x > 0:
                n = -k
                m2 = 1
            else:
                n = k
                m2 = -1
                
            if y+l < len(M[0]) and y+l >= 0 and x+n < len(M[0]) and x+n >= 0:
                if (M[x+n][y+l] in [0,2,3] and (x+n,y+l) not in pos_joueurs) and (M[x+n+m2][y+l] in [0,2,3] and (x+n+m2,y+l) not in pos_joueurs) and (M[x+n][y+l+m1] in [0,2,3] and (x+n,y+l+m1) not in pos_joueurs):
                    i,j = x+n,y+l
                else:
                    i,j = x+n+m2,y+l+m1
                    break 
            else:
                i,j = x+n+m2,y+l+m1
                break
                
    elif abs(X-x) < abs(Y-y):
        for k in range(1, nb_cases+1):
            if Y-y > 0:
                l = -k
                m = 1
            else:
                l = k
                m = -1
            if y+l < len(M[0]) and y+l >= 0:
                if M[x][y+l] in [0,2,3] and (x,y+l) not in pos_joueurs:
                    i,j = x,y+l
                else:
                    i,j = x,y+l+m
                    break
            else:
                i,j = x,y+l+m
                break
 
    else:
        for k in range(1, nb_cases+1):
            if X-x > 0:
                l = -k
                m = 1
            else:
                l = k
                m = -1
            if x+l < len(M) and x+l >= 0:
                if M[x+l][y] in [0,2,3] and (x+l,y) not in pos_joueurs:
                     i,j = x+l,y
                else:
                    i,j = x+l+m,y
                    break
            else:
                i,j = x+l+m,y
                break
                
    d = abs(i-x) + abs(j-y)
    cible.pos = (i,j)
    cases = nb_cases - d
    if cases < 0:
        cases = 0
    
    nb_DG = 20*cases
        
    Dg = int((1 + ((sum_dopou - sum_respou)/100))* nb_DG)
    
    # Perte de bouclier #
    perte_boubou = 0
    for boubou in cible.Boost[5]:
        if boubou[1] > 0:
            if boubou[0] < Dg:
                perte_boubou += boubou[0]
                Dg -= boubou[0]
                boubou[0] = 0
            else:
                perte_boubou += Dg
                boubou[0] -= Dg
                Dg = 0
    if perte_boubou > 0:
        ChatTextuel.ajout(" - {} perd {} Bouclier !".format(cible.pseudo, perte_boubou))   
        
    return Dg
     
def dg_de_poussee(nb_cases, joueur, cible, pos, M, sort, groupePersoCbt):
    
    sum_dopou = joueur.somme_boost('dopou')
    sum_respou = cible.somme_boost('res pou')
    
    (X,Y) = joueur.pos
    if sort.poussee_selon_centre:
        (X,Y) = pos
    '''
    (X,Y) = pos
    if pos != joueur.pos:
        # On rapproche d'un la case centre vers le lanceur #
        (x,y) = joueur.pos
        # Si la case cible est en diago #
        if abs(X-x) == abs(Y-y):
            (X,Y) = joueur.pos
        elif abs(X-x) < abs(Y-y):
            if Y-y > 0:
                Y -= 1
            else:
                Y += 1
        elif abs(X-x) > abs(Y-y):
            if X-x > 0:
                X -= 1
            else:
                X += 1'''

    (x,y) = cible.pos
    i,j = x,y 
    pos_joueurs = [perso.pos for perso in groupePersoCbt]
    
    # Si la case cible est en diago #
    if abs(X-x) == abs(Y-y):
        cases_range = nb_cases//2+1
        if cases_range == 1:
            cases_range += 1
        for k in range(1, cases_range):
            if Y-y > 0:
                l = -k
                m1 = 1
            else:
                l = k
                m1 = -1
            if X-x > 0:
                n = -k
                m2 = 1
            else:
                n = k
                m2 = -1
                
            if y+l < len(M[0]) and y+l >= 0 and x+n < len(M[0]) and x+n >= 0:
                if (M[x+n][y+l] in [0,2,3] and (x+n,y+l) not in pos_joueurs) and (M[x+n+m2][y+l] in [0,2,3] and (x+n+m2,y+l) not in pos_joueurs) and (M[x+n][y+l+m1] in [0,2,3] and (x+n,y+l+m1) not in pos_joueurs):
                    i,j = x+n,y+l
                else:
                    i,j = x+n+m2,y+l+m1
                    break 
            else:
                i,j = x+n+m2,y+l+m1
                break
                
    elif abs(X-x) < abs(Y-y):
        for k in range(1, nb_cases+1):
            if Y-y > 0:
                l = -k
                m = 1
            else:
                l = k
                m = -1
            if y+l < len(M[0]) and y+l >= 0:
                if M[x][y+l] in [0,2,3] and (x,y+l) not in pos_joueurs:
                    i,j = x,y+l
                else:
                    i,j = x,y+l+m
                    break
            else:
                i,j = x,y+l+m
                break
 
    else:
        for k in range(1, nb_cases+1):
            if X-x > 0:
                l = -k
                m = 1
            else:
                l = k
                m = -1
            if x+l < len(M) and x+l >= 0:
                if M[x+l][y] in [0,2,3] and (x+l,y) not in pos_joueurs:
                     i,j = x+l,y
                else:
                    i,j = x+l+m,y
                    break
            else:
                i,j = x+l+m,y
                break
                
    d = abs(i-x) + abs(j-y)
    cases = nb_cases - d
    if cases < 0:
        cases = 0
    
    nb_DG = 20*cases
        
    Dg = int((1 + ((sum_dopou - sum_respou)/100))* nb_DG)
        
    return Dg

