from random import randint

import data.scripts.personnages as p
import data.scripts.battle_functions as bf

class Justicier(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Justicier", 12)
        p.Personnage.__init__(self, pseudo, "Justicier", 950, 11, 6, 3, 2, 4.5, 0, 'justicier')
    
       
        """num, nom, po, effet_str, cout, latence, coup_par_tour = 0, zone_tire = 'cercle', type_cibles = 'ennemis', zone_cible = 'case', taille_zone = 1, po_min = 0, ldv = True"""
        
        self.s1 = p.Sort(0, "Coup d'arc", 1, "• 32 DG | +1 PO (2t) (max 3)", 3, 0, 3,'croix', dg_min = 30, dg_max = 34)
        self.s2 = p.Sort(1,"Flèche électrique", 8, "• 25 DG • retire 0-1 PA (1t) non cumulable", 3, 0, 2, po_min = 4, dg_min = 23, dg_max = 27, po_modifiable = True)
        self.s3 = p.Sort(2,"Saut", 2, "téléporte à la case ciblée", 3, 0, 1, 'croix', 'vide', ldv = False)
        self.s4 = p.Sort(3,"Flèche stratégique",1,"• 26 Vol de Vie • recule de 2 cases", 4, 0, 2, 'croix', zone_cible = 'colonne', taille_zone = 3, dg_min = 24, dg_max = 28, type_sort = 'Vdv')
        self.s5 = p.Sort(4,"Flèche Justicière", 7, "• 30 DG (+20 DG du sort (3t))", 4, 0, 1, dg_min = 27, dg_max = 33, po_min = 4, po_modifiable =True)
        self.s6 = p.Sort(5,"Flèche enflammée",6 ,"• 15 DG • Poison 10 DG (2t)", 3, 2, po_modifiable = True, dg_min = 13, dg_max = 17)
        self.s7 = p.Sort(6,"Filet", 4, "• retire 1-3 PM (1t)", 3, 0, 1, po_modifiable = True)
        self.s8 = p.Sort(7,"Flèche tumultueuse", 4, "• 30 DG/entitée touchée", 4,0 ,1 ,zone_cible = 'croix', po_min = 3, po_modifiable = True, dg_min = 27, dg_max = 33, ldv = False, reduct_dist = False)
        self.s9 = p.Sort(8,"Flèche Monstrueuse", 10, "• 50 DG (+60 DG du sort (3t)/+70 DG si relancé)", 5, 3, 1, po_min = 6, po_modifiable = True, dg_min = 46, dg_max = 54)
        self.s10 = p.Sort(9,"Mode Royal", 0, "• +20 DG", 2, 4, 1, 'croix', 'moi')
        self.s11 = p.Sort(10, "Libération", 0, "Repousse de 2 cases", 4, 2, 1, type_cibles = 'moi', zone_cible = 'croix', poussee = 2)
        self.s12 = p.Sort(11, "Invoc Arbre", 3, "Arbre : 100 PV", 5, 4, 1, po_modifiable = True, isSortInvoc = True)
        self.s13 = p.Sort(12, "Flèche de recul", 5, "Repousse de 4 cases", 3, 3, 1, zone_tire = 'croix', po_modifiable = True, poussee = 4)
        p.Personnage.defS(self, [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9, self.s10, self.s11, self.s12, self.s13])
            
    def MR(self, dis_cac, sort, joueur, cibles, ChatTextuel):
        presence = False
        for etat in joueur.etats:
            if 'Mode royal' in etat:
                presence = True
                break
        if len(cibles) > 0 and presence:
            sort.bDg.append([int(0.25*(sort.dg_max + sort.dg_min)//2),1,'Jroyal',joueur.S[9].latence-2])
            ChatTextuel.ajout("{} gagnera 25 Pui {} (2t) dans 2 tours.".format(joueur.pseudo, dis_cac))
        
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
            a = 0
            for boost in joueur.bPo:
                if "coup d'arc" in boost:
                    a += 1
            if a < 3:
                joueur.bPo.append([1,2,"coup d'arc"])
                ChatTextuel.ajout("{} gagne 1 PO pour 2 tours.".format(joueur.pseudo))
            if cible.team != joueur.team:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        
        self.MR('distance', sort, joueur, cibles, ChatTextuel)
                    
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[1]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        ret = randint(0,1)
        
        for cible in cibles:
            for boost in cible.bPa:
                if "flèche électrique" in boost:
                    cible.bPa.remove(boost)
            cible.bPa.append([-ret,2,"flèche électrique"])
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            if ret > 0:
                bf.affiche_point(-1, cible, groupeGlobal, 'pa')
                ChatTextuel.ajout("{} perd 1 PA pour 1 tour.".format(cible.pseudo))
            
        self.MR('mélée', sort, joueur, cibles, ChatTextuel)
                
    def sort3(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        bf.tp(M, pos, joueur, groupePersoCbt)
            
    def sort4(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[3]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
             p.sort_Vdv(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        (x,y) = pos
        (X,Y) = joueur.pos
        if abs(X-x) > abs(Y-y):
            pos = (2*(X-x) + X ,Y)
        else:
            pos = (X, 2*(Y-y) + Y)
        p.sort_Attire(2, pos, joueur, M, groupePersoCbt)
        
        self.MR('distance', sort, joueur, cibles, ChatTextuel)

    def sort5(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[4]
        boost = sort.somme_boost('dg')
        dg_min = sort.dg_min + boost
        dg_max = sort.dg_max + boost
        
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        sort.bDg.append([20,3])
        ChatTextuel.ajout("Le sort {} est boosté de 20 DG pour 3 tour.".format(sort.nom))   
    
        self.MR('mélée', sort, joueur, cibles, ChatTextuel)
     
    def sort6(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel): 
        sort = joueur.S[5]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            cible.poison.append([10,3,joueur, "est enflammé."])
            ChatTextuel.ajout("{} est enflammé 2 tour (10 DG/t).".format(cible.pseudo))
        
        self.MR('mélée', sort, joueur, cibles, ChatTextuel)
            
                
    def sort7(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            if cible.team != joueur.team:
                ret = randint(1,3)
                cible.bPm.append([-ret,2])
                bf.affiche_point(-ret, cible, groupeGlobal, 'pm')
                ChatTextuel.ajout("{} perd {} PM pour 1 tour !".format(cible.pseudo, ret))
        
    def sort8(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[7]
        coeff = len(cibles)
        
        dg_min = sort.dg_min*coeff
        dg_max = sort.dg_max*coeff           
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
        self.MR('mélée', sort, joueur, cibles, ChatTextuel)
            
    def sort9(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[8]
                
        boost = sort.somme_boost('dg')
        dg_min = sort.dg_min + boost
        dg_max = sort.dg_max + boost
        
        boost = 60
        for b in sort.bDg:
            if 'monstrueuse' in b:
                boost = 70
                break
        
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        sort.bDg.append([boost,4,'monstrueuse'])
        ChatTextuel.ajout("Le sort {} est boosté de 40 DG pour 3 tour.".format(sort.nom))     
    
        self.MR('mélée', sort, joueur, cibles, ChatTextuel)
                
    def sort10(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        joueur.bDmg.append([20,2])
        ChatTextuel.ajout("{} gagne 20 DMG pour 2 tour !".format(joueur.pseudo))
        #joueur.etats.append(['Mode royal', 2,'Jroyal'])
        
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
        pouss = sort.poussee
        for cible in cibles:
            p.sort_poussee(pouss, joueur, cible, pos, M, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)