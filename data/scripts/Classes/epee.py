from random import randint

import data.scripts.personnages as p
import data.scripts.battle_functions as bf

class Epee(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Epée", 16)
        p.Personnage.__init__(self, pseudo, "Epée", 1000, 11, 6, 2, 3, 11, 6, 'epee')
    
       
        """num, nom, po, effet_str, cout, latence, coup_par_tour = 0, zone_tire = 'cercle', type_cibles = 'ennemis', zone_cible = 'case', taille_zone = 1, po_min = 0, ldv = True"""
        
        self.s1 = p.Sort(0, "Invoc Épéemit", 4, "Épéemit : 50PV (+3% Res/tour)", 3, 0, 1, type_cibles = 'vide', po_modifiable = True, isSortInvoc = True)
        self.s2 = p.Sort(1,"Entrailles", 3, "20 DG | repousse de 1 case | invoque une épéemit si la case est libre", 4, 2, 1, dg_min = 17, dg_max = 23, zone_cible = 'croix', po_min = 2, ldv = False, po_modifiable = True, poussee = 1, isSortInvoc = True, reduct_dist = False, poussee_selon_centre = True)
        self.s3 = p.Sort(2,"Éportée", 4, "25 DG | -1PO (1t) (max 1)", 4, 0, 2, 'croix', dg_min = 22, dg_max = 28, zone_cible = 'croix', taille_zone = 3)
        self.s4 = p.Sort(3,"Épée dévorante", 5, "15/30 DG selon le nombre de lancé sur la même cible, réinitialise lorsque lancé sur une autre cible (45 DG)", 4, 0, 2, dg_min = 13, dg_max = 17, po_modifiable = True, reduct_dist = False)
        self.s5 = p.Sort(4,"Transport mitique", 4, "Tue et prend la place de l'épéemit ciblée | 25 Soin", 2, 0, 1, po_modifiable = True, ldv = False,  dg_min = 24, dg_max = 26, type_sort = 'Soin')
        self.s6 = p.Sort(5,"Épée boomerang", 6, "50 DG | invoc une épée boomerang (60PV) qui fait le chemin inverse le tour suivant en infligeant 70 DG", 5, 2, 1, 'croix', 'vide', zone_cible = 'traînée', po_min = 1, po_modifiable = True, dg_min = 45, dg_max = 55, ldv = False, reduct_dist = False, isSortInvoc = True)
        self.s7 = p.Sort(6,"Crucification", 5, "Retire 1 à 3 PM (1t)", 3, 2, 1, 'croix', po_modifiable = True)
        self.s8 = p.Sort(7,"Glacis", 4, "+100 Bouclier (2t) +10 PV max (épée) | +50 Bouclier (2t) (alliés)", 3, 3 ,1 , 'croix', po_modifiable = True)
        self.s9 = p.Sort(8,"Déluge", 6, "50 DG/épéemit sacrifiée", 6, 0, 1, po_modifiable = True, dg_min = 45, dg_max = 55)
        self.s10 = p.Sort(9,"Châtiment", 2, "150 DG | coûte 1 PA en moins pour chaque point de retrait effectué", 11, 0, 1, 'croix', dg_min = 145, dg_max = 155)
        self.s11 = p.Sort(10, "Libération", 0, "Repousse de 2 cases", 4, 2, 1, type_cibles = 'moi', zone_cible = 'croix', poussee = 2)
        self.s12 = p.Sort(11, "Invoc Arbre", 3, "Arbre : 100 PV", 5, 4, 1, po_modifiable = True, isSortInvoc = True)
        self.s13 = p.Sort(12, "Confusion", 2, "- 3 PA (1t)", 2, 4, 1, zone_cible = 'cercle', taille_zone = 3, ldv = False)
        p.Personnage.defS(self, [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9, self.s10, self.s11, self.s12, self.s13])
     
    def retrait(self, nb):
        sort = self.S[9]
        sort.cout -= nb
        if sort.cout < 0:
            sort.cout = 0
     
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Epéemit':
                i+=1
                 
        perso = Epeemit('Epéemit '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
                    
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[1]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        pouss = sort.poussee
        
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            if cible.pv > 0 and cible.pos != pos:
                p.sort_poussee(pouss, joueur, cible, pos, M, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
        pos_cibles = []
        for cible in cibles:
            pos_cibles.append(cible.pos)
        
        if pos not in pos_cibles:
            i = 1
            for perso in groupeGlobalPerso:
                if perso.nom_classe == 'Epéemit':
                    i+=1
                     
            perso = Epeemit('Epéemit '+str(i))
            p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
            
                
    def sort3(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[2]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        presence = False
        
        for cible in cibles:
            if cible != joueur:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                a = 0
                for boost in cible.bPo:
                    if "éportée" in boost:
                        a = 1
                        break
                if a == 0:
                    presence = True
                    cible.bPo.append([-1,2,"éportée"])
                    ChatTextuel.ajout("{} perd 1 PO pour 1 tour.".format(cible.pseudo))
        if cibles != [] and presence:
            self.retrait(1)
            
    def sort4(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[3]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
            a = 0
            boost = 0
            for etat in cible.etats:
                if 'épée dévorante' in etat:
                    a += 1
            if a > 0:
                boost = 15
            dg_min += boost
            dg_max += boost
            
            if cible.team != joueur.team:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                cible.etats.append(['épée dévorante', 100000000000])
            
        if cible != []:
            for cible in groupeGlobalPerso:
                if cible not in cibles:
                    a = 0
                    etats_to_remove = []
                    for etat in cible.etats:
                        if 'épée dévorante' in etat:
                            a += 1
                            etats_to_remove.append(etat)
                    for etat in etats_to_remove:
                        cible.etats.remove(etat)
                        
                    if a > 0:
                        if cible.team != joueur.team:
                            dg_min = sort.dg_min + a*15
                            dg_max = sort.dg_max + a*15
                            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)

    def sort5(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[4]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
            if cible in joueur.Invocs and cible.nom_classe == 'Epéemit':
                bf.tp(M, cible.pos, joueur, groupePersoCbt)
                bf.mort(cible, groupePersoCbt, groupePersoHorsCbt, groupeGlyphe, ChatTextuel)
                p.sort_Soin(dg_min, dg_max, joueur, joueur, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
     
    def sort6(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel): 
        sort = joueur.S[5]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Epée boomerang':
                i+=1
                 
        perso = Epeeboomerang('Epée boomerang '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
        
        # On récupère la zone de retour de l'épée boomerang #
        (X,Y) = joueur.pos
        (x,y) = pos
        if x == X:
            if y > Y:
                zone = [(X,Y+i) for i in range(1,abs(Y-y))]
            else:
                zone = [(X,Y-i) for i in range(1,abs(Y-y))]
        else:
            if x > X:
                zone = [(X+i,Y) for i in range(1,abs(X-x))]
            else:
                zone = [(X-i,Y) for i in range(1,abs(X-x))]
        
        perso.zone = zone
            
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
                
    def sort7(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            if cible.team != joueur.team:
                ret = randint(1,3)
                self.retrait(ret)        
                cible.bPm.append([-ret,2])
                bf.affiche_point(-ret, cible, groupeGlobal, 'pm')
                ChatTextuel.ajout("{} perd {} PM pour 1 tour !".format(cible.pseudo, ret))
        
    def sort8(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[7]
        for cible in cibles:
            if cible.team == joueur.team:
                shield = 50
                if cible.nom_classe in ['Epéemit', 'Epéetite', 'Epée boomerang']:
                    shield = 100
                    cible.pv_max += 10
                    p.sort_Soin(10, 10, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                    
                cible.bShield.append([shield,2,"glacis"])
                ChatTextuel.ajout("{} gagne {} Points de Bouclier pour 2 tours.".format(cible.pseudo, shield))
            
    def sort9(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[8]
        
        boost = -45
        to_kill = []
        for invoc in joueur.Invocs:
            if invoc.nom_classe == 'Epéemit':
                boost += 50
                to_kill.append(invoc)
                
        if boost > 250:
            boost = 250
        
        dg_min = sort.dg_min + boost
        dg_max = sort.dg_max + boost
        
        if cibles != []:
            for invoc in to_kill:
                bf.mort(invoc, groupePersoCbt, groupePersoHorsCbt, groupeGlyphe, ChatTextuel)
        
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
            
    def sort10(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[9]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        sort.cout = sort.cout_initial
            
            
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
        for cible in cibles:
            time = 2
            if cible == joueur:
                time = 2
            ret = 3
            cible.bPa.append([-ret,time])
            bf.affiche_point(-ret, cible, groupeGlobal, 'pa')
            ChatTextuel.ajout("{} perd {} PA pour 1 tour !".format(cible.pseudo, ret))
        self.retrait(3)
        
class Epeemit(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Epéemit", 17)
        p.Personnage.__init__(self, pseudo, "Epéemit", 50, 0, 0, 0, 0, 0, 0, 'epeemit', isInvoc = True, isStatic = True)
        
        self.s1 = p.Sort(0, "", 0, "", 0, 0, 1, type_cibles = 'moi')
        
        p.Personnage.defS(self, [self.s1])
        
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        self.bRes.append([3,100000000])
    
        
class Epeeboomerang(p.Classes):
    
    def __init__(self, pseudo):
        self.zone = []
        p.Classes.__init__(self, "Epée boomerang", 18)
        p.Personnage.__init__(self, pseudo, "Epée boomerang", 60, 0, 0, 0, 0, 0, 0, 'epeeboomerang', isInvoc = True, isStatic = True)
        
        self.s1 = p.Sort(0, "", 0, "", 0, 0, 1, type_cibles = 'moi', reduct_dist = False)
  
        p.Personnage.defS(self, [self.s1])
        
        self.time_to_pass = 250
        
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        if self.nb_tour >= 2:
            sort = self.s1
            dg_min = 65
            dg_max = 75
            for cible in groupePersoCbt:
                if cible.pos in self.zone:
                    p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            bf.mort(joueur, groupePersoCbt, groupePersoHorsCbt, groupeGlyphe, ChatTextuel)