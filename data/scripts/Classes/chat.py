from random import randint

import data.scripts.personnages as p
import data.scripts.battle_functions as bf

class Chat(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Chat", 1)
        p.Personnage.__init__(self, pseudo, "Chat", 1000, 11, 6, 5, 2, 10, 1, 'chat')
    
        '''None s1_3 : sort n°3 de la classe id : 1 
        
        Sorts basiques : [Nom, PO, Effet, nb DG, Latence, Coût, type cible(-2=aucune, -1=all, 0=soi, 1=nb de cible), nb Latence(ok=1, sinon=0), nb Coût, id_sort]
       None Sorts d'invocation : [Nom, PO, Caracs invoc (PV, PA, PM), sort 1 :[Nom, PO, Effet, Latence, Coût, nb Latence, nb Coût], Latence, Coût, id_sort] LATENCE +1
        '''
        """num, nom, po, effet_str, cout, latence, coup_par_tour = 0, zone_tire = 'cercle', type_cibles = 'ennemis', zone_cible = 'case', taille_zone = 1, po_min = 0, ldv = 'avec'"""
        
        self.s1 = p.Sort(0, "Puissance", 1, "+100 pui (2t)", 2, 3, 1,'croix', 'alliés')
        self.s2 = p.Sort(1,"Pile ou face", 0, "à 66% : pour chaque coup reçu(2t) : +25pui(2t) ou -15% resi | a 33% : +35pui/-15% resi", 2, 2, 1, 'croix', 'moi')
        self.s3 = p.Sort(2, "Déplacement alétoire", 0, "à 50% : se téléporte sur une case aléatoire | à 50% : se soigne du 35", 3, 3, 1, 'croix', 'moi', dg_min = 35, dg_max = 38, type_sort = 'Soin')
        self.s4 = p.Sort(3,"Rollback",0,"annule les dernières téléportations | 20 DG/Soin (ennemi/allié) ",2, 2, 1, 'croix', 'moi', zone_cible = 'tout', dg_min = 18, dg_max = 22, type_sort = 'DG/Soin', reduct_dist = False)
        self.s5 = p.Sort(4,"Expolsion", 0, "20 DG à 33% à 1 PO | 33% à 2 PO | 33% à 3 PO", 2, 0, 100, 'croix', 'moi', 'cercle', 3, dg_min = 17, dg_max = 23)
        self.s6 = p.Sort(5,"Hijacking", 4,"20 DG et à 50% échange de position | 50 % se téléporte symétriquement", 3, 0, po_modifiable = True, dg_min = 17, dg_max = 23)
        self.s7 = p.Sort(6, "Lance flammes", 1, "40 DG + 20 DG (2t)", 4, 0, 1, 'croix', 'ennemis', 'T', 1, po_modifiable = True, dg_min = 38, dg_max = 42)
        self.s8 = p.Sort(7,"Fracas", 1, "33% : 30 soin | 33% : 70 DG| 33% : 150 DG", 6, 1, zone_tire = 'croix', po_modifiable = True, dg_min = -30, dg_max = 150)
        self.s9 = p.Sort(8, "Changement d'état", 0, "si actif : chaque tour à 50% : +50 pui | 50% : -25 % Res ",2, 0, 1, 'croix', 'moi')
        self.s10 = p.Sort(9, "Invoc Chaton", 2, "Chaton : 100 PV, 6PA, 4PM ", 4, 4, 1, 'cercle', 'vide',isSortInvoc = True)
        self.s11 = p.Sort(10, "Libération", 0, "Repousse de 2 cases", 4, 2, 1, type_cibles = 'moi', zone_cible = 'croix', poussee = 2)
        self.s12 = p.Sort(11, "Invoc Arbre", 3, "Arbre : 100 PV", 5, 4, 1, po_modifiable = True, isSortInvoc = True)
        self.s13 = p.Sort(12, "Cancerization", 2, "50% : - 1 à 2 PM (2t) | 50% : + 3 PO (2t)", 3, 4, 1,'cercle', zone_cible = 'carré', taille_zone = 2, po_modifiable = True)
        p.Personnage.defS(self, [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9, self.s10, self.s11, self.s12, self.s13])
            
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            cible.bPui.append([100,2])          # ajoute 100 pour 2t, (liste de tuples dans boost pui du lanceur)
            ChatTextuel.ajout("{} gagne 100 puissance pour 2 tours !".format(cible.pseudo))
                    
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            chance = randint(1, 90)
            presence = False
            for etat in joueur.etats:
                if 'pile-face' in etat:
                    presence = True
            if not presence:
                if chance <= 30:
                    bpui,mres = 35,-15
                else:
                    bpui,mres = 25,-15
                joueur.etats.append(['pile-face', 2, bpui, mres])
                ChatTextuel.ajout("Pour chaque coup reçu, {} gagnera {} puissance ou perdra {}% de résistance.".format(joueur.pseudo, bpui, mres))
                
    def sort3(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[2]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
            chance = randint(1,100)
            if chance <= 50:
                i = randint(0,len(M)-1)
                j = randint(0,len(M[0])-1)
                while M[i][j] != 0:
                    i = randint(0,len(M)-1)
                    j = randint(0,len(M[0])-1)
                bf.tp(M, (i,j), joueur, groupePersoCbt)
            else:
                p.sort_Soin(dg_min, dg_max, joueur, joueur, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
    def sort4(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[3]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
            if cible.last_pos != []:
                if cible.team == joueur.team:
                    p.sort_Soin(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                else:
                    p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                bf.tp(M, cible.last_pos.pop(-1), cible, groupePersoCbt)
         
            
                                       
    def sort5(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[4]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        for cible in cibles:
            if cible == joueur:
                continue
            chance = randint(1,90)
            if chance <= 30:
                po = 1
            elif chance <=60:
                po = 2
            else:
                po = 3
            (X,Y) = joueur.pos
            (x,y) = cible.pos
            if abs(X-x) + abs(Y-y) <= po:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
     
    def sort6(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):  
        sort = joueur.S[5]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        for cible in cibles:
            if cible.team != joueur.team:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            chance = randint(1,100)
            (X,Y) = joueur.pos
            (x,y) = cible.pos
            
            if chance <= 50:
                bf.tp(M, cible.pos, joueur, groupePersoCbt)
            else:
                dx, dy = x-X, y-Y
                bf.tp(M,(X+2*dx, Y+2*dy), joueur, groupePersoCbt)
                
    def sort7(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[6]
        boost = sort.somme_boost('dg')
        dg_min = sort.dg_min + boost
        dg_max = sort.dg_max + boost
        
        presence = False
        
        for b in sort.bDg:
            if 'Lance-flamme boosté' in b:
                if b[1] > 1:    # On reboost si c'est le dernier tour de boost #
                    presence = True
                    
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        if len(cibles) > 0:
            if not presence:
                sort.bDg.append([20,3,'Lance-flamme boosté'])
                ChatTextuel.ajout("Le sort {} est boosté de 20 DG pour 3 tour.".format(sort.nom)) 
        
    def sort8(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[7]
        
        for cible in cibles:
            chance = randint(1,90)
            if chance <= 32:
                p.sort_Soin(28, 32, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            elif chance <= 64:
                p.sort_DG(68, 73, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            else:
                p.sort_DG(145, 155, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                
    def sort9(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
         for cible in cibles:
            presence = False
            for etat in cible.etats:
                if 'Etat aléatoire ON' in etat:
                    cible.etats.remove(etat)
                    presence = True
            if not presence:
                cible.etats.append(['Etat aléatoire', 100000000, 'EA'])     
                
    def sort10(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Chaton':
                i+=1
                 
        perso = Chaton('Chaton '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
        
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
        chance = randint(1,100)
        if chance <= 50:
            for cible in cibles:
                if cible == joueur:
                    temps = 2
                else:
                    temps = 3
                ret = randint(1,2)
                cible.bPm.append([-ret,temps])
                bf.affiche_point(-ret, cible, groupeGlobal, 'pm')
                ChatTextuel.ajout("{} perd {} PM pour 2 tour !".format(cible.pseudo, ret)) 
        else:
            for cible in cibles:
                if cible == joueur:
                    temps = 2
                else:
                    temps = 3
                cible.bPo.append([3,temps])
                ChatTextuel.ajout("{} gagne 3 PO pour 2 tours.".format(cible.pseudo))

class Chaton(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Chaton", 2)
        p.Personnage.__init__(self, pseudo, "Chaton", 100, 6, 4, 3, 2, 4, 0, 'chaton', True)
  
        self.s1 = p.Sort(0, "Griffes", 1, "20 DG/20 Soin (ennemi/allié)", 4, 0, 100, zone_tire = 'croix', type_cibles = 'tout sans moi', dg_min = 19, dg_max = 21, type_sort = 'DG/Soin')
        self.s2 = p.Sort(1, "Bond du Chaton", 1, "+ 1 PM (1t) à l'allié ciblé", 2, 1, 1, zone_tire = 'croix', type_cibles = 'alliés')
        p.Personnage.defS(self, [self.s1, self.s2])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max 
        for cible in cibles:
             if cible.team == joueur.team:
                 p.sort_Soin(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
             else:
                 p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
         for cible in cibles:
            if cible == joueur:
                cible.bPm.append([1,1])
            elif cible.team == joueur.team:
                cible.bPm.append([1,2])
            
            bf.affiche_point(1, cible, groupeGlobal, 'pm')
            ChatTextuel.ajout("{} gagne 1 PM pour 1 tour !".format(cible.pseudo))
       