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

class Sort(pygame.sprite.Sprite):
    '''Id, nom, PO, effet_str, coût, latence, zone tire, type cible, zone cible, taille zone, po mini, ldv '''
    
    def __init__(self, num, nom, po, effet_str, cout, latence, coup_par_tour = 100, zone_tire = 'cercle', type_cibles = 'ennemis', zone_cible = 'case', taille_zone = 1, po_min = 0, ldv = 'avec'):
        
        dico_zone_tire = {'cercle' : 0, 'crois' : 1, 'diago' : 2, 'étoile' : 3}
        dico_type_cible = {'ennemis' : 0, 'alliés' : 1, 'alliés sans moi' : 2, 'invoc' : 3, 'mes invocs' : 4, 'mes invocs et moi' : 5, 'tout' : 6, 'moi' : 7, 'tout sans moi' : 8}
        dico_zone_cible = {'cercle' : 0, 'croix' : 1, 'ligne' : 2, 'colonne' : 3, 'carré' : 4, 'case' : 5, 'T' : 6}
        dico_ldv = {'sans' : 0, 'avec' : 1}
        
        self.num = num
        self.nom = nom
        self.po = po
        self.effet_str = effet_str
        self.cout = cout
        self.latence_max = latence
        self.latence = 0
        self.coup_par_tour_max = coup_par_tour
        self.coup_par_tour = coup_par_tour
        
        self.zone_tire = zone_tire
        self.type_cibles = type_cibles
        self.zone_cible = zone_cible
        self.taille_zone = taille_zone
        self.po_min = po_min
        self.ldv = ldv
        
    

def sort_DG(dg_min, dg_max, joueur, cible, groupePersoCbt, groupePersoHorsCbt, groupeGlobal):
    nb_dg = randint(dg_min, dg_max)
    dg = bf.dg(nb_dg, joueur, cible)
    
    if cible.pv - dg <= 0:
        dg = cible.pv
        bf.mort(cible, groupePersoCbt, groupePersoHorsCbt)
    else:
        cible.pv -= dg
                   
    bf.affiche_dg(dg, nb_dg, cible, groupeGlobal) 
    
def sort_Soin(soin_min, soin_max, joueur, cible, groupePersoCbt, groupeGlobal):
    nb_soin = randint(soin_min, soin_max)
    soin = bf.soin(nb_soin, joueur, cible)
    
    cible.pv += soin
    
    bf.affiche_soin(soin, cible, groupeGlobal)
        
        
class Personnage(pygame.sprite.Sprite):
    
    def __init__(self, pseudo, nom_classe, pv, pa, pm, tacle, fuite, ini, invoc, nom_image):
        super().__init__()
        
        self.pseudo = pseudo
        self.nom_classe = nom_classe
        self.niveau = 1
        self.exp = 0
        self.id = 0
        self.team = 0
        self.isReady = False
        self.ordre_ini = -1
        self.tour = 0
        
        # Stats max -------------------------------------- #
        self.pv_max = pv
        self.pa_max = pa
        self.pm_max = pm
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
               
        self.bPui = []
        self.bPa = []
        self.bPm = []
        self.bRes = []
        self.bDmg = []
        self.bShield = []
        self.bPO = []
        
        self.Boost = [self.bPui, self.bPa, self.bPm, self.bRes, self.bDmg, self.bShield, self.bPO]
        
        # Sorts ------------------------------------------ #
        self.S = []
        
        # Autres attributs utiles ------------------------ #
        self.pos_depart = (0,0)
        self.pos = (0,0)
        self.last_pos = []
        self.image = pygame.image.load('data/images/Char/' + nom_image + '.png').convert_alpha()      
    
    def defS(self, L):
        for i in L:
            self.S.append(i)
        
    def update(self, groupeTxtVariable):
        # Update les textes du joueur #
        txt_pv = str(self.pv)
        txt_pourcent_pv = str(int(self.pv/self.pv_max*100)) +" %" 
        txt_pa = "PA : " + str(self.pa)
        txt_pm = "PM : " + str(self.pm)
        _tv = [txt_pv, txt_pourcent_pv, txt_pa, txt_pm]      
           
        for tv in groupeTxtVariable:
            tv.maj(_tv[tv.num])
    
    def somme_boost(self, nom_boost):
        dico_boost = {'pui' : 0, 'pa' : 1, 'pm' : 2, 'res' : 3, 'dmg' : 4, 'shield' : 5, 'po' : 6}
        num_boost = dico_boost[nom_boost]
        S = 0
        for boost in self.Boost[num_boost]:
            if boost[1] > 0:    #Augmente le total de pui si temps d'effet > 0
                S += boost[0]   
        return S
    
    def debut_tour(self):
        self.last_pos = []
        self.pa = self.pa_max
        self.pm = self.pm_max
        for sort in self.S:         
            sort.coup_par_tour = sort.coup_par_tour_max
            if sort.latence >= 1:
                sort.latence -= 1
            
        # On réduit la latence des boosts et états #
        for i in range(len(self.Boost)):
            for boost in self.Boost[i]:
                boost[1] -= 1
                if boost[1] <= 0:
                    self.Boost[i].remove(boost)            
        for etat in self.etats:
            etat[1] -= 1
            if etat[1] <= 0:
                self.etats.remove(etat)
                
        # Etats spéciaux #
        if self.nom_classe == 'Chat':
            for etat in self.etats:
                if 'Etat aléatoire ON' in etat:
                    chance = randint(1,2)
                    if chance == 1:
                        self.bPui.append([50,1])
                        print("{} gagne 50 puissance pour 1 tour !".format(self.pseudo))
                    else:
                        self.bPui.append([-50,1])
                        print("{} perd 50 puissance pour 1 tour !".format(self.pseudo))
                    break
                

class Classes(Personnage):
    
    def __init__(self, nom_classe, id_classe):
        
        self.nom_classe = nom_classe
        self.id_classe = id_classe
  
    def ciblage(self, fenetre, num_sort):
        pass
        
  
    def use_sort(self, num_sort, joueur, cibles, M, dm, groupePersoCbt, groupePersoHorsCbt, groupeGlobal):     # dm = derniers mouvements #
        a = 0
        namelanceur = self.nom_classe
        if namelanceur == 'Cerf':
            for couple_etat in self.etats:
                if 'Mode royal cerf' in couple_etat: 
                    a = 1
                    
        # Si la latence n'est pas terminée #
        if joueur.S[num_sort].latence > 0 or joueur.S[num_sort].coup_par_tour <= 0 :
            print("le sort n'est pas prêt...")
        else:
            # Retire les pa du coût du sort #
            cout = self.S[num_sort].cout - a
            if self.pa + self.somme_boost('pa') >= cout:
                
                print("{} utilise {} !".format(joueur.pseudo, joueur.S[num_sort].nom))
                
                # On applique la latence #
                joueur.S[num_sort].latence = joueur.S[num_sort].latence_max
                joueur.S[num_sort].coup_par_tour -= 1
                
                self.pa -= cout
        
                if num_sort == 0:
                    self.sort1(joueur, cibles, M, dm, groupePersoCbt, groupePersoHorsCbt, groupeGlobal)
                elif num_sort == 1:
                    self.sort2(joueur, cibles, M, dm, groupePersoCbt, groupePersoHorsCbt, groupeGlobal)
                elif num_sort == 2:
                    self.sort3(joueur, cibles, M, dm, groupePersoCbt, groupePersoHorsCbt, groupeGlobal)
                elif num_sort == 3:
                    self.sort4(joueur, cibles, M, dm, groupePersoCbt, groupePersoHorsCbt, groupeGlobal)
                elif num_sort == 4:
                    self.sort5(joueur, cibles, M, dm, groupePersoCbt, groupePersoHorsCbt, groupeGlobal)
                elif num_sort == 5:
                    self.sort6(joueur, cibles, M, dm, groupePersoCbt, groupePersoHorsCbt, groupeGlobal)
                elif num_sort == 6:
                    self.sort7(joueur, cibles, M, dm, groupePersoCbt, groupePersoHorsCbt, groupeGlobal)
                elif num_sort == 7:
                    self.sort8(joueur, cibles, M, dm, groupePersoCbt, groupePersoHorsCbt, groupeGlobal)
                elif num_sort == 8:
                    self.sort9(joueur, cibles, M, dm, groupePersoCbt, groupePersoHorsCbt, groupeGlobal)
                elif num_sort == 9:
                    self.sort10(joueur, cibles, M, dm, groupePersoCbt, groupePersoHorsCbt, groupeGlobal)
                    
        

        
class Cerf(Classes):
    
    def __init__(self, pseudo):
        
        Classes.__init__(self, "Cerf", 2)
        Personnage.__init__(self, pseudo, "Cerf", 1000, 11, 5, 3, 6, 12, 4, 'mob1')
        
class Dragon(Classes):
    
    def __init__(self, pseudo):
        
        Classes.__init__(self, "Dragon", 3)
        Personnage.__init__(self, pseudo, "Dragon", 900, 11, 5, 4, 4, 6, 3, 'mob1')

class Epee(Classes):
    
    def __init__(self, pseudo):
         
        Classes.__init__(self, "Epée", 4)
        Personnage.__init__(self, pseudo, "Epée", 1000, 11, 5, 6, 2, 11, 6, 'mob1')
        
class Poulpe(Classes):
    
    def __init__(self, pseudo):
        
        Classes.__init__(self, "Poulpe", 5)
        Personnage.__init__(self, pseudo, "Poulpe", 1000, 11, 5, 3, 5, 4, 5, 'mob1')
        
class Monstre(Classes):
    
    def __init__(self, pseudo):
        
        Classes.__init__(self, "Monstre", 6)
        Personnage.__init__(self, pseudo, "Monstre", 1000, 12, 1, 5, 4, 0, 2, 'mob1')
        
class Crapeaud(Classes):
    
    def __init__(self, pseudo):
        
        Classes.__init__(self, "Crapeau Royal", 20)
        Personnage.__init__(self, pseudo, "Crapeau Royal", 5000, 14, 11, 3, 10, 22, 6, 'crapeau')