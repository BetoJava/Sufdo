import pygame
from random import randint

import data.scripts.personnages as p
import data.scripts.battle_functions as bf

class Poulpe(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Poulpe", 9)
        p.Personnage.__init__(self, pseudo, "Poulpe", 1100, 11, 6, 3, 3, 4, 5, 'poulpe')
    
        """num, nom, po, effet_str, cout, latence, coup_par_tour = 0, zone_tire = 'cercle', type_cibles = 'ennemis', zone_cible = 'case', taille_zone = 1, po_min = 0, ldv = 'avec'"""
        self.s1 = p.Sort(0, "Danse tentaculaire", 0, "• 20 DG pousse de 1 case |MR : • 10 DG pousse de 2 cases", 3, 0, 2, zone_tire = 'croix', type_cibles = 'moi', zone_cible = 'croix', dg_min = 17, dg_max = 23, poussee = 1)
        self.s2 = p.Sort(1, "Typhon", 4, "• 45 DG • attire au centre du typhon de 1 case", 5, 0, 100, zone_cible = 'carré', taille_zone = 2, po_modifiable = True, dg_min = 42, dg_max = 48)
        self.s3 = p.Sort(2, "Houle", 5, "pousse de 3 cases | lancé sur tentacule : pousse de 2 cases au cac de la tentacule", 4, 0, 1, zone_tire = 'croix', po_modifiable = True, poussee = 3)
        self.s4 = p.Sort(3, "Tentaculation", 6, "• 30 DG/soin (ennemi/allié)", 4, 0, po_min = 1, dg_min = 27, dg_max = 33, type_sort = 'DG/Soin')
        self.s5 = p.Sort(4, "Evolution", 6, "Sur invocs : • 50 soin • 50 pui (1t)", 2, 1, po_min = 1, po_modifiable = True)
        self.s6 = p.Sort(5, "Courant", 7, "-1PM (1t)", 2, 0, 2, po_min = 1, po_modifiable = True)
        self.s7 = p.Sort(6, "Mode royal (MR)", 0, "• -25% resistance • +50 Do pou", 2, 0, 1, type_cibles = 'moi')
        self.s8 = p.Sort(7, "Invoc Tentacule", 3, "Tentacule : 100 PV, 2 PA, 0 PM", 3, 0, 1, zone_tire = 'croix', type_cibles = 'vide', isSortInvoc = True)
        self.s9 = p.Sort(8, "Invoc Requin", 4, "Requin : 100 PV, 0 PA, 2 PM", 5, 4, type_cibles = 'vide', po_min = 3, isSortInvoc = True, ldv = False)
        self.s10 = p.Sort(9, "Union tentaculaire", 1, "1/2/3/4 tenta : 30/60/100/150 DG", 5, 0, zone_tire = 'croix', dg_min = 1, dg_max = 150)
        self.s11 = p.Sort(10, "Libération", 0, "Repousse de 2 cases", 4, 2, 1, type_cibles = 'moi', zone_cible = 'croix', poussee = 2)
        self.s12 = p.Sort(11, "Invoc Arbre", 3, "Arbre : 100 PV", 5, 4, 1, po_modifiable = True, isSortInvoc = True)
        self.s13 = p.Sort(12, "Naufrage", 6, "15 DG | -25% Res poussée (2t) (max 2)", 3, 0, 2, po_modifiable = True, dg_min = 17, dg_max = 23)
        p.Personnage.defS(self, [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9, self.s10, self.s11, self.s12, self.s13])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        pouss = joueur.S[0].poussee
        for cible in cibles:
            if cible != joueur:
      
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                if cible.pv > 0:
                        p.sort_poussee(pouss, joueur, cible, pos, M, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                    
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[1]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
  
        for cible in cibles:
            if cible != joueur:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            if cible.pos != pos:
                p.sort_Attire(1, pos, cible, M, groupePersoCbt)
                
    def sort3(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[2]
        pouss = sort.poussee
        for cible in cibles:
            p.sort_poussee(pouss, joueur, cible, pos, M, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
    def sort4(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[3]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        for cible in cibles:
            if cible.team == joueur.team:
                p.sort_Soin(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            else:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                                       
    def sort5(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[4]
        for cible in cibles:
            if cible in joueur.Invocs:
                if cible.niveau == 3:
                    p.sort_Soin(50, 50, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                cible.bPui.append([50,2])
                ChatTextuel.ajout("{} gagne 50 puissance pour 1 tours !".format(cible.pseudo))
                if cible.niveau < 3:
                    cible.pv_max += 50
                    p.sort_Soin(50, 50, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                    cible.niveau += 1
                    if cible.nom_classe == 'Tentacule':
                        cible.bPo.append([1, 100000000])
                        cible.image = pygame.image.load('data/images/Char/' + 'tenta'+str(cible.niveau) + '.png').convert_alpha()
                        if cible.niveau == 3:
                            cible.pm_max += 1
                            
                            cible.pa = cible.pa_max
                            cible.pm = cible.pm_max
                    if cible.nom_classe == 'Requin':
                        cible.image = pygame.image.load('data/images/Char/' + 'requin'+str(cible.niveau) + '.png').convert_alpha()
                        cible.pm_max += 1
                        cible.pa_max += 4
                        if cible.niveau == 3:
                            cible.S[0].poussee = 2
                            cible.S[0].dg_min = 0
                            cible.S[0].dg_max = 0
                        cible.pa = cible.pa_max
                        cible.pm = cible.pm_max
                    ChatTextuel.ajout("{} évolue niveau {} !".format(cible.pseudo, cible.niveau))
     
    def sort6(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):  
        for cible in cibles:
            if cible.team != joueur.team:
                cible.bPm.append([-1,2])
            
                bf.affiche_point(-1, cible, groupeGlobal, 'pm')
                ChatTextuel.ajout("{} perd 1 PM pour 1 tour !".format(cible.pseudo))
              
    def sort7(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            presence = False
            for etat in cible.etats:
                if 'Mode royal' in etat:
                    cible.etats.remove(etat)
                    presence = True
                    
                    joueur.S[0].dg_min, joueur.S[0].dg_max, joueur.S[0].poussee = 17,23,1
                    
                    for type_boost in cible.Boost:
                        for boost in type_boost:
                            if len(boost) >= 3:
                                if boost[2] == 'royal':
                                    type_boost.remove(boost)
            if not presence:
                joueur.S[0].dg_min, joueur.S[0].dg_max, joueur.S[0].poussee = 7,13,2
                cible.etats.append(['Mode royal', 100000000,'royal']) 
                cible.bRes.append([-25,100000000,'royal'])
                cible.bDopou.append([50,100000000,'royal'])
        
    def sort8(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Tentacule':
                i+=1
        perso = Tentacule('Tentacule '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)   
                
                
                
    def sort9(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Requin':
                i+=1
        perso = Requin('Requin '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)   
            
                
    def sort10(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[9]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        nb_tenta = 0
        for invoc in joueur.Invocs:
            if invoc.nom_classe == 'Tentacule' and invoc.pv > 0:
                nb_tenta += 1
        if nb_tenta <= 2:
            dg = 30*nb_tenta
        elif nb_tenta <= 4:
            dg = -50 + 50*nb_tenta
        else:
            dg = 150
        for cible in cibles:
            p.sort_DG(dg,dg+5, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)

    def sort11(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[10]
        pouss = sort.poussee 
        for cible in cibles:
            if cible != joueur:
                p.sort_poussee(pouss, joueur, cible, pos, M, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
    
    def sort12(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Arbre':
                i+=1      
        perso = p.Arbre('Arbre '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
        
    def sort13(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[12]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            a = 0
            for boost in cible.bResPou:
                if "naufrage" in boost:
                    a += 1
            if a < 2:
                cible.bResPou.append([-25,3,"naufrage"])
                ChatTextuel.ajout("{} perd 25% Res poussée pour 2 tours.".format(cible.pseudo))
   
class Tentacule(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Tentacule", 10)
        p.Personnage.__init__(self, pseudo, "Tentacule", 100, 2, 0, 0, 0, 1, 0, 'tenta1', True)
    
        self.s1 = p.Sort(0, "Ventouse", 2, "attire de 1/1/2 case(s)", 2, 0, zone_tire = 'croix', po_min = 1, po_modifiable = True)
        p.Personnage.defS(self, [self.s1])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
         for cible in cibles:
            if joueur.niveau <= 2:
                case_attire = 1
            else:
                case_attire = 2
                
            p.sort_Attire(case_attire, joueur.pos, cible, M, groupePersoCbt)
        
             
class Requin(p.Classes):
  
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Requin", 11)
        p.Personnage.__init__(self, pseudo, "Requin", 100, 0, 2, 0, 5, 1, 0, 'requin1', True)
   
       
        self.s1 = p.Sort(0, "Requinerie", 2, " niv 2 : 15 DG | niv 3 : pousse de 2 cases", 4, 0, zone_tire = 'diago', po_modifiable = True, dg_min = 13, dg_max = 17)
        p.Personnage.defS(self, [self.s1])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        pouss = joueur.S[0].poussee
        for cible in cibles:
            if joueur.niveau == 2:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)   
            if joueur.niveau == 3:
                p.sort_poussee(pouss, joueur, cible, pos, M, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        
             
    