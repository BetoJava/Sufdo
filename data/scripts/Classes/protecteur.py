from random import randint

import data.scripts.personnages as p
import data.scripts.battle_functions as bf

class Protecteur(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Protecteur", 14)
        p.Personnage.__init__(self, pseudo, "Protecteur", 1050, 11, 6, 4, 2, 13, 0, 'protecteur')
    
       
        """num, nom, po, effet_str, cout, latence, coup_par_tour = 0, zone_tire = 'cercle', type_cibles = 'ennemis', zone_cible = 'case', taille_zone = 1, po_min = 0, ldv = True"""
        
        self.s1 = p.Sort(0, "Coup de bouclier", 1, "• 35 DG | -5% Res (1t) (lanceur)", 4, 0, 2, 'croix', dg_min = 32, dg_max = 38)
        self.s2 = p.Sort(1,"Epée croisée", 4, "• 15 DG | +1 PO sur la zone (1t)", 2, 0, 4, 'croix', dg_min = 13, dg_max = 17, zone_cible = 'croix', po_modifiable = True)
        self.s3 = p.Sort(2,"Casse briques", 4, "• 27 DG | 10% érosion (2t) (max 2) (nécessite une cible)", 4, 0, 2, 'croix', dg_min = 24, dg_max = 30, zone_cible = 'ligne', po_modifiable = True)
        self.s4 = p.Sort(3,"Fureur",1,"• 70 DG (+70 DG du sort (3t)", 7, 3, 1, 'croix', dg_min = 65, dg_max = 75)
        self.s5 = p.Sort(4,"Repli", 4, "• échange de position avec l'allié ciblé", 2, 2, 1, 'croix', po_modifiable =True)
        self.s6 = p.Sort(5,"Slide de bouclier", 5,"• 30 DG | Avance jusqu'à la case ciblée", 4, 2, 1, 'croix', po_modifiable = True, dg_min = 27, dg_max = 33)
        self.s7 = p.Sort(6,"Rempart", 0, "• +10% Res (2t) (alliés)", 3, 4, 1, 'croix', 'moi', zone_cible = 'cercle', taille_zone = 3)
        self.s8 = p.Sort(7,"Ecu", 0, "• +75 Bouclier (2t) (alliés) | 15% d'érosion (2t)", 3, 4 ,1 , 'croix', 'moi', zone_cible = 'carré')
        self.s9 = p.Sort(8,"Mode Combat", 0, "• +50 Pui • + 10 DG • -35% Res", 2, 0, 1, 'croix', 'moi')
        self.s10 = p.Sort(9,"Jet de bouclier", 3, "• 25 DG | Invoc un bouclier : 50PV/5% Res (si case libre)", 3, 2, 1, zone_cible = 'croix', dg_min = 22, dg_max = 28, po_modifiable = True, isSortInvoc = True, reduct_dist = False)
        self.s11 = p.Sort(10, "Libération", 0, "Repousse de 2 cases", 4, 2, 1, type_cibles = 'moi', zone_cible = 'croix', poussee = 2)
        self.s12 = p.Sort(11, "Invoc Arbre", 3, "Arbre : 100 PV", 5, 4, 1, po_modifiable = True, isSortInvoc = True)
        self.s13 = p.Sort(12, "Siège", 1, "- 100 PM (1t) +1000% Res distance (ennemi) + état indéplaçable (1t)", 3, 4, 1, 'croix')
        p.Personnage.defS(self, [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9, self.s10, self.s11, self.s12, self.s13])
        
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
            joueur.bRes.append([-5,1,"coup de bouclier"])
            ChatTextuel.ajout("{} perd 5% Res pour 1 tour.".format(joueur.pseudo))
            if cible.team != joueur.team:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                    
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[1]
        boost = sort.somme_boost('dg')
        dg_min = sort.dg_min + boost
        dg_max = sort.dg_max + boost
        for cible in cibles:
            if cible != joueur:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        
        if len(cibles) > 0 and not (cibles == [joueur]):
            sort.bPoz.append([1,1])
            
                
    def sort3(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[2]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        pos_cibles = []
        for cible in cibles:
            pos_cibles.append(cible.pos)
            
        for cible in cibles:
            if pos in pos_cibles:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                a = 0
                for boost in cible.bEro:
                    if "casse briques" in boost:
                        a += 1
                if a < 2:
                    cible.bEro.append([0.10,3,"casse briques"])
                    ChatTextuel.ajout("{} est érodé de 10% pour 2 tours.".format(cible.pseudo))
            
    def sort4(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[3]
        boost = sort.somme_boost('dg')
        dg_min = sort.dg_min + boost
        dg_max = sort.dg_max + boost
        
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        sort.bDg.append([70,4,'monstrueuse'])
        ChatTextuel.ajout("Le sort {} est boosté de 70 DG pour 3 tour.".format(sort.nom))     

    def sort5(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            if cible.team == joueur.team:
                bf.tp(M, cible.pos, joueur, groupePersoCbt)
     
    def sort6(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel): 
        sort = joueur.S[5]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        (x,y) = pos
        (X,Y) = joueur.pos
        d = abs(x-X) + abs(Y-y)
        if len(cibles) > 0:
            if abs(X-x) > abs(Y-y):
                pos = ((x-X) + X ,Y)
            else:
                pos = (X, (y-Y) + Y)
            p.sort_Attire(d+1, pos, joueur, M, groupePersoCbt)
        else:
            p.sort_Attire(d, pos, joueur, M, groupePersoCbt)
            
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
                
    def sort7(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            if cible.team == joueur.team:
                cible.bRes.append([10,2,"rempart"])
                ChatTextuel.ajout("{} gagne 10% Res pour 2 tours.".format(cible.pseudo))
        
    def sort8(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            cible.bEro.append([0.15,2,"ecu"])
            ChatTextuel.ajout("{} est érodé de 15% pour 2 tours.".format(cible.pseudo))
            if cible.team == joueur.team:
                cible.bShield.append([75,2,"ecu"])
                ChatTextuel.ajout("{} gagne 75 Points de Bouclier pour 2 tours.".format(cible.pseudo))
            
    def sort9(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[8]
        presence = False
        for etat in joueur.etats:
            if 'Mode Combat' in etat:
                joueur.etats.remove(etat)
                sort.nom = 'Mode Combat'
                presence = True
                for type_boost in joueur.Boost:
                    for boost in type_boost:
                        if 'MC' in boost:
                            type_boost.remove(boost)
        if not presence:
            sort.nom = 'Mode Défense'
            joueur.etats.append(['Mode Combat', 100000000,'MC']) 
            joueur.bRes.append([-35,100000000,'MC'])
            joueur.bDmg.append([10,100000000,'MC'])
            joueur.bPui.append([50,100000000,'MC'])
            joueur.bTacle.append([-2, 100000000,'MC'])
                
    def sort10(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[9]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
        pos_cibles = []
        for cible in cibles:
            pos_cibles.append(cible.pos)
        
        if pos not in pos_cibles:
            i = 1
            for perso in groupeGlobalPerso:
                if perso.nom_classe == 'Bouclier':
                    i+=1
                     
            perso = Bouclier('Bouclier '+str(i))
            perso.bRes.append([5,100000000,'naturel'])
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
        for cible in cibles:
            if cible.team != joueur.team:
                cible.bPm.append([-100,2]) 
                cible.etats.append(['Invunérable distance', 2])     
                cible.etats.append(['Pesanteur', 2])
                bf.affiche_point(-100, cible, groupeGlobal, 'pm') 
                ChatTextuel.ajout("{} perd 100 PM, gagne l'état pesanteur et invulnérable à distance pour 1 tour.".format(cible.pseudo))
        
class Bouclier(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Bouclier", 14)
        p.Personnage.__init__(self, pseudo, "Bouclier", 50, 0, 0, 0, 0, 0, 0, 'bouclier', isInvoc = True, isStatic = True)
  
        p.Personnage.defS(self, [])