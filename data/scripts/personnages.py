# Import ---------- #
import pygame
from random import randint

import data.scripts.functions as f
import data.scripts.battle_functions as bf


couleurs = dict(
            noir = (0,0,0),
            gris_foncé = (50,50,50),
            blanc = (255,255,255),
            vert = (0,255,0),
            bleu = (0,0,200),
            rouge = (200,0,0),
            orange = (255,174,0),
            gold = (255,215,0),
            bleuc = (43,133,167),
            rougepm = (160,87,47),
            vertpasser = (47,136,55)
        )

class Glyphe(pygame.sprite.Sprite):
    def __init__(self, sort, joueur, time, zone, dg_min = -100000000, dg_max = -100000000, type_glyphe = 'début', type_sort = 'DG', only_allies = False, only_ennemis = False
                 , bPui = [], bPa = [], bPm = [], bRes = [], bDmg = [], bShield = [], bPo = [], bDopou = [], bEro = [], bFuite = [], bTacle = []
                 , bResCac = [], bResDis = [], bResPou = [], bDgFinaux = [], couleur = 'blanc'):
 
        super().__init__()
        
        self.sort = sort
        self.joueur = joueur
        self.zone = zone
        self.time = time
        self.couleur = couleur
        self.image = pygame.image.load('data/images/Tileset/glyphe_'+couleur+'.png').convert_alpha()
        self.type_sort = type_sort
        self.only_allies = only_allies
        self.only_ennemis = only_ennemis
        self.type_glyphe = type_glyphe
        
        # Dégats/Soin #
        self.dg_min = dg_min
        self.dg_max = dg_max
        
        # Boost #
        self.bPui = bPui
        self.bPa = bPa
        self.bPm = bPm
        self.bRes = bRes
        self.bDmg = bDmg
        self.bShield = bShield
        self.bPo = bPo
        self.bDopou = bDopou
        self.bEro = bEro
        self.bFuite = bFuite
        self.bTacle = bTacle
        self.bResCac = bResCac
        self.bResDis = bResDis
        self.bResPou = bResPou
        self.bDgFinaux = bDgFinaux # 25% --> 0.25 #
        
        self.Boost = [self.bPui, self.bPa, self.bPm, self.bRes, self.bDmg, self.bShield, self.bPo, self.bDopou, self.bEro, self.bFuite, self.bTacle, self.bResCac, self.bResDis, self.bResPou, self.bDgFinaux]
        
    def appliquer(self, cible, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel):
        
        # Glyphe Dg/Soin #
        if self.type_sort == 'DG' and self.dg_min > 0:
            sort_DG(self.dg_min, self.dg_max, self.joueur, cible, cible.pos, self.sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        elif self.type_sort == 'DG/Soin':
            if cible.team == self.joueur.team:
                sort_Soin(self.dg_min, self.dg_max, self.joueur, cible, cible.pos, self.sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            else:
                sort_DG(self.dg_min, self.dg_max, self.joueur, cible, cible.pos, self.sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        elif self.type_sort == 'Soin':
            if self.only_allies:
                if cible.team == self.joueur.team:
                    sort_Soin(self.dg_min, self.dg_max, self.joueur, cible, cible.pos, self.sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            else:
                sort_Soin(self.dg_min, self.dg_max, self.joueur, cible, cible.pos, self.sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                
        # Boost #
        dico_boost = {0:'Pui', 1:'Pa', 2:'Pm', 3:'Res', 4:'Dmg', 5:'Bouclier', 6:'Po', 7:'Do pou', 8:'érosion', 9:'fuite', 10:'tacle', 11:'Res cac', 12:'Res dis', 13:'Res pou', 14:'Dg finaux'}
        if (self.only_allies and cible.team == self.joueur.team) or (self.only_ennemis and cible.team != self.joueur.team) or (not self.only_allies and not self.only_ennemis):
            for i in range(len(self.Boost)):
                if self.Boost[i] != []:
                    boost = [self.Boost[i][0][0], self.Boost[i][0][1], self.type_glyphe]
                    cible.Boost[i].append(boost)
                    
                    if self.type_glyphe != 'instantané':
                        if i == 1:
                            bf.affiche_point(boost[0], cible, groupeGlobal, 'pa')
                        elif i == 2:
                            bf.affiche_point(boost[0], cible, groupeGlobal, 'pm')
                            
                        if boost[0] > 0:
                            perd_gagne = 'gagne'
                        else:
                            perd_gagne = 'perd'
                        
                        if i in [8,14]:
                            boost = [self.Boost[i][0][0]*100, self.Boost[i][0][1], self.type_glyphe]
                        add = ''
                        if i in [3,8,11,12,14]:
                            add = '%'
                            
                        ChatTextuel.ajout("{} {} {} {}{} pour {} tour(s) !".format(cible.pseudo, perd_gagne, int(abs(boost[0])), add, dico_boost[i], boost[1]))
        

class Sort(pygame.sprite.Sprite):
    '''Id, nom, PO, effet_str, coût, latence, zone tire, type cible, zone cible, taille zone, po mini, ldv '''
    
    def __init__(self, num, nom, po, effet_str, cout, latence, coup_par_tour = 100, zone_tire = 'cercle', type_cibles = 'ennemis', zone_cible = 'case', taille_zone = 1
                 , po_min = 1, ldv = True, po_modifiable = False, isSortInvoc = False, dg_min = -100000000, dg_max = -100000000, poussee = 0, cible_necessaire = False, type_sort = 'DG'
                 , reduct_dist = True, poussee_selon_centre = False, isGliphe = False, type_sort_ia = ['offensif'], priorite = 100):
        super().__init__()
        
        dico_zone_tire = {'cercle' : 0, 'croix' : 1, 'diago' : 2, 'étoile' : 3}
        dico_type_cible = {'ennemis' : 0, 'alliés' : 1, 'alliés sans moi' : 2, 'invocs' : 3, 'mes invocs' : 4, 'mes invocs et moi' : 5, 'tout' : 6, 'moi' : 7, 'tout sans moi' : 8, 'vide' : 9}
        dico_zone_cible = {'cercle' : 0, 'croix' : 1, 'ligne' : 2, 'colonne' : 3, 'carré' : 4, 'case' : 5, 'T' : 6, 'tout' : 7, 'moi' : 8, 'tout sans moi' : 9, 'diago' : 10, 'traînée' : 11}
        dico_type_sort = {'offensif' : 0, 'support' : 1, 'tp' : 3, 'boost déplacement' : 4, 'attirance' : 5, 'charge' : 6, 'boost dg' : 7, 'invoc' : 8, 'malus' : 9, 'boost' : 10, 'fuite' : 11, 'autre' : 12}
        
        self.num = num
        self.nom = nom
        self.po = po
        self.effet_str = effet_str
        self.cout = cout
        self.cout_initial = cout
        self.latence_max = latence
        self.latence = 0
        self.coup_par_tour_max = coup_par_tour
        self.coup_par_tour = coup_par_tour
        self.isSortInvoc = isSortInvoc
        self.reduct_dist = reduct_dist
        self.poussee_selon_centre = poussee_selon_centre
        
        self.dg_min = dg_min
        self.dg_max = dg_max
        self.poussee = poussee
        self.cible_necessaire = cible_necessaire
        
        self.bDg = []
        self.bPo = []
        self.bPoz = []
        self.bPa = []
        self.Boost = [self.bDg, self.bPo, self.bPoz, self.bPa]
        
        self.type = type_sort_ia
        self.priorite = priorite
        
        self.type_sort = type_sort
        self.zone_tire = zone_tire
        self.type_cibles = type_cibles
        self.zone_cible = zone_cible
        self.taille_zone = taille_zone
        self.po_min = po_min
        self.ldv = ldv
        self.po_modifiable = po_modifiable    

    def somme_boost(self, name):
        dico_boost = {'dg' : 0, 'po' : 1, 'poz' : 2, 'pa' : 3}
        S = 0
        for boost in self.Boost[dico_boost[name]]:
            if boost[1] > 0:    #Augmente le total de pui si temps d'effet > 0
                S += boost[0]   
        return S
    
    def debut_tour(self):
        Boosts_to_remove = []
        To_add = []
        for type_boost in self.Boost:
            boosts_to_remove = []
            to_add = []
            for boost in type_boost:
                if 'Jroyal' in boost:
                    boost[3] -=1
                    if boost[3] <= 0:
                        to_add.append(boost[:2])
                        print(boost[:2])
                else:
                    boost[1] -= 1
                    if boost[1] <= 0:
                        boosts_to_remove.append(boost) 
            Boosts_to_remove.append(boosts_to_remove)
            To_add.append(to_add)
         
        for i in range(len(Boosts_to_remove)):
            for boost in Boosts_to_remove[i]:            
                self.Boost[i].remove(boost)
        for i in range(len(To_add)):
            for boost in To_add[i]:            
                self.Boost[i].remove(boost)
    

def sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel, poison = False, multiplicateur = 1):
    if cible.pv > 0:
        nb_dg = randint(dg_min, dg_max)
        dg = bf.dg(nb_dg, joueur, cible, pos, sort, ChatTextuel)
        multiplicateur += joueur.somme_boost('dg finaux')
        dg = int(dg * multiplicateur)
        
        if dg > 0:
            if cible.pv - dg <= 0 and not poison:
                dg = cible.pv
                bf.affiche_dg(dg, nb_dg, cible, groupeGlobal, ChatTextuel, mort = True) 
                bf.mort(cible, groupePersoCbt, groupePersoHorsCbt, groupeGlyphe, ChatTextuel)
            elif cible.pv - dg <= 0 and poison:
                dg = cible.pv - 1
                cible.pv -= dg
                bf.affiche_dg(dg, nb_dg, cible, groupeGlobal, ChatTextuel) 
            else:
                cible.pv -= dg
                bf.affiche_dg(dg, nb_dg, cible, groupeGlobal, ChatTextuel)
                   
def sort_Vdv(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel, multiplicateur = 1):
    if cible.pv > 0:
        nb_dg = randint(dg_min, dg_max)
        dg = bf.dg(nb_dg, joueur, cible, pos, sort, ChatTextuel)
        multiplicateur += joueur.somme_boost('dg finaux')
        dg = int(dg * multiplicateur)
        if dg > 0:
            if cible.pv - dg <= 0:
                dg = cible.pv
                bf.affiche_dg(dg, nb_dg, cible, groupeGlobal, ChatTextuel, mort = True) 
                bf.mort(cible, groupePersoCbt, groupePersoHorsCbt, groupeGlyphe, ChatTextuel)
            else:
                cible.pv -= dg
                bf.affiche_dg(dg, nb_dg, cible, groupeGlobal, ChatTextuel)    
                
            soin = bf.Vdv(dg, joueur)
            cible.pv += soin
            
            bf.affiche_soin(soin, joueur, groupeGlobal, ChatTextuel)
    
def sort_Soin(soin_min, soin_max, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel, naff = False, multiplicateur = 1):
    nb_soin = randint(soin_min, soin_max)
    soin = bf.soin(nb_soin, joueur, cible, pos, sort)
    multiplicateur += joueur.somme_boost('dg finaux')
    soin = int(soin * multiplicateur)
    
    cible.pv += soin
    if not naff:
        bf.affiche_soin(soin, cible, groupeGlobal, ChatTextuel)
    
def sort_poussee(nb_cases, joueur, cible, pos, M, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel):
    indep = False
    for etat in cible.etats:
        if 'Indéplaçable' in etat and etat[1] > 0:
            indep = True
            break
        
    if not indep:
        dg = bf.poussee(nb_cases, joueur, cible, pos, M, sort, groupePersoCbt, ChatTextuel)
        
        if cible.pv - dg <= 0:
            dg = cible.pv
            bf.affiche_dg(dg, dg, cible, groupeGlobal, ChatTextuel, 32, (255,100,0))
            bf.mort(cible, groupePersoCbt, groupePersoHorsCbt, groupeGlyphe, ChatTextuel)
        else:
            cible.pv -= dg
            if dg > 0:
                bf.affiche_dg(dg, dg, cible, groupeGlobal, ChatTextuel, 32, (255,100,0)) 
    
def sort_Invoc(invoc, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel):
    
    invoc.pos_depart = pos
    invoc.pos = pos
    invoc.isReady = True
    invoc.team = joueur.team
    
    i = joueur.ordre_ini
    invoc.ordre_ini = i + 1

    for perso in groupePersoCbt:
        if perso.ordre_ini >= i + 1:
            perso.ordre_ini += 1
            
    groupePersoCbt.add(invoc)
    groupeGlobalPerso.add(invoc)
    joueur.Invocs.append(invoc)
    invoc.parent = joueur

    ChatTextuel.ajout("{} invoque un {} !".format(joueur.pseudo, invoc.nom_classe))
        
def sort_Attire(nb_cases, centre, cible, M, groupePersoCbt):
    indep = False
    for etat in cible.etats:
        if 'Indéplaçable' in etat and etat[1] > 0:
            indep = True
            break
        
    if not indep:
        (x,y) = cible.pos
        cible.last_pos.append((x,y))
        (X,Y) = (centre[0], centre[1])
        pos_joueurs = [perso.pos for perso in groupePersoCbt]
        for i in range(nb_cases):
            (x,y) = cible.pos
            if abs(X-x) > abs(Y-y):
                if X-x > 0:
                    k = 1
                else:
                    k = -1
                if M[x+k][y] == 0 and (x+k,y) not in pos_joueurs:
                        cible.pos = (x+k,y)
            else:
                if Y-y > 0:
                    k = 1
                else:
                    k = -1   
                if M[x][y+k] == 0 and (x,y+k) not in pos_joueurs:
                        cible.pos = (x,y+k)
    
        
class Personnage(pygame.sprite.Sprite):
    
    def __init__(self, pseudo, nom_classe, pv, pa, pm, tacle, fuite, ini, invoc, nom_image, isInvoc = False, isIA = False, isStatic = False, type_ia = 'combatif', coeff_de_base = 40):
        super().__init__()
        
        self.pseudo = pseudo
        self.nom_classe = nom_classe
        self.isInvoc = isInvoc
        self.isStatic = isStatic
        self.niveau = 1
        self.exp = 0
        self.exp_next_niv = 0
        self.id = 0
        self.team = 0
        self.isReady = False
        self.ordre_ini = -1
        self.tour = 0
        
        # IA --------------------------------------------- #
        self.isIA = isIA
        self.type_ia = type_ia
        self.priorite = 0
        self.tour_fini = False
        
        # Stats max -------------------------------------- #
        self.pv_max = pv + (self.niveau-1)*100
        self.pv_max_basic = self.pv_max
        self.pa_max = pa + self.niveau//5
        self.pm_max = pm + self.niveau//5
        self.tacle_max = tacle
        self.fuite_max = fuite
        self.ini_max = ini
        self.invoc_max = invoc
        
        # Stats ------------------------------------------ #
        self.pv = pv
        self.pa = pa
        self.pm = pm
        self.tacle = tacle
        self.fuite = fuite
        self.ini = ini
        self.invoc = invoc
        
        # Boost ------------------------------------------ #
        self.etats = []
        self.poison = []
               
        self.bPui = []
        self.bPa = []
        self.bPm = []
        self.bRes = []
        self.bDmg = []
        self.bShield = []
        self.bPo = []
        self.bDopou = []
        self.bEro = []
        self.bFuite = []
        self.bTacle = []
        self.bResCac = []
        self.bResDis = []
        self.bResPou = []
        self.bDgFinaux = []
        
        self.Boost = [self.bPui, self.bPa, self.bPm, self.bRes, self.bDmg, self.bShield, self.bPo, self.bDopou, self.bEro, self.bFuite, self.bTacle, self.bResCac, self.bResDis, self.bResPou, self.bDgFinaux]
        
        # Sorts ------------------------------------------ #
        self.S = []
        self.Glyphes = []
        
        # Invocs ----------------------------------------- #
        self.Invocs = []
        self.parent = None
        self.coeff_de_base = coeff_de_base
        
        # Autres attributs utiles ------------------------ #
        self.app = None
        self.isActing = False
        self.time_to_wait = 0
        self.time_to_pass = 0
        self.pos_depart = (0,0)
        self.pos = (0,0)
        self.last_pos = []
        self.nb_tour = 0
        self.image = pygame.image.load('data/images/Char/' + nom_image + '.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (64, 64))
        
        
    
    def defS(self, L):
        for i in L:
            self.S.append(i)
        
    def update(self, groupeTxtVariable):
        # Update les textes du joueur #
        boubou = str(self.somme_boost('shield'))
        if boubou != '0':
            txt_boubou = '+' + boubou
        else:
            txt_boubou = ''
        txt_pv = str(self.pv)
        txt_pourcent_pv = str(int(self.pv/self.pv_max*100)) +" %" 
        txt_pa = str(self.pa + self.somme_boost('pa'))
        txt_pm = str(self.pm + self.somme_boost('pm'))
        _tv = [txt_pv, txt_pourcent_pv, txt_pa, txt_pm, txt_boubou]      
           
        for tv in groupeTxtVariable:
            if not tv.isClasse:
                tv.maj(_tv[tv.num])
    
    def somme_boost(self, nom_boost):
        dico_boost = {'pui' : 0, 'pa' : 1, 'pm' : 2, 'res' : 3, 'dmg' : 4, 'shield' : 5, 'po' : 6, 'dopou' : 7, 'ero' : 8, 'fuite' : 9, 'tacle' : 10, 'res cac' : 11, 'res dis' : 12, 'res pou' : 13, 'dg finaux' : 14}
        num_boost = dico_boost[nom_boost]
        S = 0
        for boost in self.Boost[num_boost]:
            if boost[1] > 0:    #Augmente le total de pui si temps d'effet > 0
                S += boost[0]   
        return S
    
    def debut_tour(self, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel):
        self.nb_tour += 1
        self.last_pos = []
        for sort in self.S:         
            sort.coup_par_tour = sort.coup_par_tour_max
            if sort.latence >= 1:
                sort.latence -= 1
            sort.debut_tour()
                         
            
        # On réduit la latence des boosts et états #
        for i in range(len(self.Boost)):
            boosts_to_remove = []
            for boost in self.Boost[i]:
                boost[1] -= 1
                if boost[1] <= 0:
                    boosts_to_remove.append(boost)
                    
            for boost in boosts_to_remove:            
                self.Boost[i].remove(boost)  
        
        etat_to_remove = []
        for etat in self.etats:
            etat[1] -= 1
            if etat[1] <= 0:
                etat_to_remove.append(etat)
        for etat in etat_to_remove:
            self.etats.remove(etat)
            
        # On applique les effets de glyphe début de tour #
        for g in groupeGlyphe:
            if self.pos in g.zone:
                g.appliquer(self, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
        # On réduit le temps des glyphes #
        g_to_remove = []
        for g in self.Glyphes:
            g.time -= 1
            if g.time <= 0:
                g_to_remove.append(g)
        for g in g_to_remove:
            self.Glyphes.remove(g)
            groupeGlyphe.remove(g)
           
        # On applique les poisons #
        poison_to_remove = []
        for poison in self.poison:
            poison[1] -= 1
            if poison[1] <= 0:
                poison_to_remove.append(poison)
            else:
                ChatTextuel.ajout("{} {}".format(self.pseudo, poison[-1]))
                sort_DG(poison[0], poison[0], poison[2], self, self.pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel, poison = True)
                
        for poison in poison_to_remove:
            self.poison.remove(poison)   
        
           
        # Etats spéciaux #
        if self.nom_classe == 'Chat':
            for etat in self.etats:
                if 'EA' in etat:
                    chance = randint(1,2)
                    if chance == 1:
                        self.bPui.append([50,1])
                        ChatTextuel.ajout("{} gagne 50 puissance pour 1 tour !".format(self.pseudo))
                    else:
                        self.bRes.append([-25,1])
                        ChatTextuel.ajout("{} perd 25% Res pour 1 tour !".format(self.pseudo))
                    break
                
    def fin_tour(self, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, ChatTextuel):
        pass
            

class Classes(Personnage):
    
    def __init__(self, nom_classe, id_classe):
        
        self.nom_classe = nom_classe
        self.id_classe = id_classe
  
    def ciblage(self, fenetre, num_sort):
        pass
        
  
    def use_sort(self, num_sort, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):     # dm = derniers mouvements #
        if not self.isActing:
            self.isActing = True
                        
            # Si la latence n'est pas terminée #
            if joueur.S[num_sort].latence > 0 or joueur.S[num_sort].coup_par_tour <= 0:
                if ChatTextuel.L[-1] != "Le sort n'est pas prêt...":
                    ChatTextuel.ajout("Le sort n'est pas prêt...")
            else:
                # Retire les pa du coût du sort #
                cout = self.S[num_sort].cout
                if self.pa + self.somme_boost('pa') >= cout or cout == 0:
                    #print("J'ai {} PA et j'utilise {} PA.".format(self.pa + self.somme_boost('pa'), cout))
                    if not joueur.S[num_sort].isSortInvoc and joueur.S[num_sort].nom != '':
                        ChatTextuel.ajout("{} utilise {} !".format(joueur.pseudo, joueur.S[num_sort].nom))
                    
                    # On applique la latence #
                    joueur.S[num_sort].latence = joueur.S[num_sort].latence_max
                    joueur.S[num_sort].coup_par_tour -= 1
                    
                    self.pa -= cout
                    if cout > 0:
                        bf.affiche_point(-1*cout, joueur, groupeGlobal, 'pa')
                    self.app.wait(self.time_to_wait)
            
                    if num_sort == 0:
                        self.sort1(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 1:
                        self.sort2(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 2:
                        self.sort3(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 3:
                        self.sort4(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 4:
                        self.sort5(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 5:
                        self.sort6(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 6:
                        self.sort7(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 7:
                        self.sort8(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 8:
                        self.sort9(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 9:
                        self.sort10(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 10:
                        self.sort11(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 11:
                        self.sort12(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 12:
                        self.sort13(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 13:
                        self.sort14(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 14:
                        self.sort15(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 15:
                        self.sort16(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 16:
                        self.sort17(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 17:
                        self.sort18(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 18:
                        self.sort19(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
                    elif num_sort == 19:
                        self.sort20(joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel)
            self.isActing = False
                    
        
class Arbre(Classes):
    
    def __init__(self, pseudo):
        
        Classes.__init__(self, "Arbre", 15)
        Personnage.__init__(self, pseudo, "Arbre", 100, 0, 0, 0, 0, 0, 0, 'arbre', isInvoc = True, isStatic = True)
  
        Personnage.defS(self, [])

class Epee(Classes):
    
    def __init__(self, pseudo):
         
        Classes.__init__(self, "Epée", 4)
        Personnage.__init__(self, pseudo, "Epée", 1000, 11, 5, 6, 2, 11, 6, 'mob1')

class Monstre(Classes):
    
    def __init__(self, pseudo):
        
        Classes.__init__(self, "Monstre", 6)
        Personnage.__init__(self, pseudo, "Monstre", 1000, 12, 1, 5, 4, 0, 2, 'mob1')
        
class Crapeaud(Classes):
    
    def __init__(self, pseudo):
        
        Classes.__init__(self, "Crapeau Royal", 20)
        Personnage.__init__(self, pseudo, "Crapeau Royal", 5000, 14, 11, 3, 10, 22, 6, 'crapeau')