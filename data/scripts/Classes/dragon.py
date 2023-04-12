from random import randint

import data.scripts.personnages as p
import data.scripts.battle_functions as bf

class Dragon(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Dragon", 3)
        p.Personnage.__init__(self, pseudo, "Dragon", 950, 11, 6, 3, 4, 6, 3, 'dragon')
    
        """num, nom, po, effet_str, cout, latence, coup_par_tour = 0, zone_tire = 'cercle', type_cibles = 'ennemis', zone_cible = 'case', taille_zone = 1, po_min = 0, ldv = 'avec'"""
        self.s1 = p.Sort(0, "Flamme harcelante", 7, "20 DG", 3, 0, 3, ldv = False, po_modifiable = True, dg_min = 17, dg_max = 23)
        self.s2 = p.Sort(1, "Guillotine", 1, "75 DG sur invoc, +50 pui (2t) si invoc tuée", 3, 0, 2, po_modifiable = True, dg_min = 70, dg_max = 77, type_cibles = 'invocs')
        self.s3 = p.Sort(2, "Griffe du dragon", 1, "45 DG", 4, 0, 2, dg_min = 42, dg_max = 48)
        self.s4 = p.Sort(3, "Vomi draconique", 3, "-25 DMG et + 50% Res (1t) (alliés) | Sur oeuf : 23 soin", 2, 1, po_modifiable = True, dg_min = 20, dg_max = 25, type_sort = 'Soin')
        self.s5 = p.Sort(4, "Souffle du dragon", 4, "pousse 2 case, 25 DG | MD : 20 DG", 4, 0, 1, zone_tire = 'croix', zone_cible = 'ligne', po_modifiable = True, dg_min = 23, dg_max = 27, poussee = 2)
        self.s6 = p.Sort(5, "Rase motte", 4, "téléporte sur case ciblée • 35 DG sur le chemin | MD : 30 DG", 4, 3, 1, 'croix', 'vide', zone_cible = 'traînée', po_min = 2, ldv = False, po_modifiable = True, dg_min = 32, dg_max = 38, reduct_dist = False)
        self.s7 = p.Sort(6, "Union draconique", 2, "nb de Dragonnets : 1/2/3 : 80/100/120 DG | MD : 1/2/3 : 50/70/90 DG", 5, 1, 1, po_modifiable = True, dg_min = 31, dg_max = 125)
        self.s8 = p.Sort(7, "Mode draconique (MD)", 0, "• -30% Res • -3 tacle • +2 PO • +3 fuite", 2, 0, 1, type_cibles = 'moi')
        self.s9 = p.Sort(8, "Invoc Dragonnet", 1, "Dragonnet : 85PV, 6PA, 4PM ", 4, 4, 1, type_cibles = 'vide', isSortInvoc = True)
        self.s10 = p.Sort(9, "Invoc Oeuf", 3, "Oeuf : 50 PV dans 1t : • si blessé : explose 2PO, pousse 1 case, 75 DG(-20% DG à 2PO) • Sinon invoc Dragonnet", 3, 1, 1, type_cibles = 'vide', isSortInvoc = True)
        self.s11 = p.Sort(10, "Libération", 0, "Repousse de 2 cases", 4, 2, 1, type_cibles = 'moi', zone_cible = 'croix', poussee = 2)
        self.s12 = p.Sort(11, "Invoc Arbre", 3, "Arbre : 100 PV", 5, 4, 1, po_modifiable = True, isSortInvoc = True)
        self.s13 = p.Sort(12,"Torrent de flammes", 0,"• Poison 22 DG (2t) • -2 tacle (1t)", 4, 3, type_cibles = 'moi', zone_cible = 'cercle', taille_zone = 3)
        p.Personnage.defS(self, [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9, self.s10, self.s11, self.s12, self.s13])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                    
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[1]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        for cible in cibles:
            if cible.isInvoc:
                nb = len(groupePersoCbt)
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                if len(groupePersoCbt) < nb:
                    joueur.bPui.append([50,2])          
                    ChatTextuel.ajout("{} gagne 50 puissance pour 2 tours !".format(joueur.pseudo))
                
    def sort3(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[2]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
    def sort4(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[3]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        for cible in cibles:
            if cible in joueur.Invocs:
                p.sort_Soin(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            if cible.team == joueur.team:
                cible.bDmg.append([-25,2])
                cible.bRes.append([50,2])
                ChatTextuel.ajout("{} perd 25 Dmg et gagne 50% Res pour 1 tours !".format(cible.pseudo))
                                       
    def sort5(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[4]
        boost = sort.somme_boost('dg')
        dg_min = sort.dg_min + boost
        dg_max = sort.dg_max + boost
        pouss = sort.poussee 
            
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            if cible.pv > 0:
                p.sort_poussee(pouss, joueur, cible, pos, M, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
     
    def sort6(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):  
        sort = joueur.S[5]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        bf.tp(M, pos, joueur, groupePersoCbt)

              
    def sort7(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[6]
        
        nb_dragonnet = 0
        for invoc in joueur.Invocs:
            if invoc.nom_classe == 'Dragonnet' and invoc.pv > 0:
                nb_dragonnet += 1
        if nb_dragonnet > 3:
            nb_dragonnet = 3
            
        boost1 = 20*nb_dragonnet + 60
        boost = sort.somme_boost('dg')
        
        dg_min = 1 + boost1 + boost
        dg_max = 9 + boost1 + boost
            
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        
    def sort8(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[7]
        for cible in cibles:
            presence = False
            for etat in cible.etats:
                if 'Mode draconique' in etat:
                    cible.etats.remove(etat)
                    presence = True
                    cible.fuite -= 3
                    cible.tacle += 3
                    for type_boost in cible.Boost:
                        for boost in type_boost:
                            if len(boost) >= 3:
                                if boost[2] == 'MD':
                                    type_boost.remove(boost)
                                    
                    for sort in [joueur.S[4], joueur.S[6]]:                
                        for type_boost in sort.Boost:
                            for boost in type_boost:
                                if len(boost) >= 3:
                                    if boost[2] == 'MD':
                                        type_boost.remove(boost)
                                    
            if not presence:
                cible.etats.append(['Mode draconique', 100000000,'MD'])  
                cible.bRes.append([-30,100000000,'MD'])
                cible.bPo.append([2,100000000,'MD'])
                cible.fuite += 3
                cible.tacle -= 3
                # Boost/Malus des sort #
                joueur.S[4].bDg.append([-5,100000000, 'MD'])
                joueur.S[6].bDg.append([-30,100000000, 'MD'])
                
                
    def sort9(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Dragonnet':
                i+=1
        perso = Dragonnet('Dragonnet '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)   
            
                
    def sort10(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Oeuf':
                i+=1
                 
        perso = Oeuf('Oeuf '+str(i))
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
            if cible != joueur:
                cible.poison.append([22,3,joueur, "est enflammé."])
                cible.bTacle.append([-2,3])
                ChatTextuel.ajout("{} est enflammé (22 DG/t) et perd 2 de tacle pour 2 tours.".format(cible.pseudo))
            

class Dragonnet(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Dragonnet", 4)
        p.Personnage.__init__(self, pseudo, "Dragonnet", 85, 6, 3, 0, 4, 2, 0, 'dragonnet', True)
    
        self.s1 = p.Sort(0, "Crocs", 1, "20 DG", 6, 0, 100, zone_tire = 'croix', type_cibles = 'tout sans moi', dg_min = 18, dg_max = 22)
        self.s2 = p.Sort(1, "Envolée", 0, "+ 2 PM (1t)", 4, 0, 1, zone_tire = 'croix', type_cibles = 'moi')
        p.Personnage.defS(self, [self.s1, self.s2])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max 
        for cible in cibles:
             if cible.team != joueur.team:
                 p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
         for cible in cibles:
             cible.bPm.append([2,1])

             bf.affiche_point(2, cible, groupeGlobal, 'pm')
             ChatTextuel.ajout("{} gagne 2 PM pour 1 tour !".format(cible.pseudo))
             
class Oeuf(p.Classes):
  
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Oeuf", 5)
        p.Personnage.__init__(self, pseudo, "Oeuf", 50, 0, 0, 0, 0, 2, 0, 'oeuf', isInvoc = True, isStatic = True)
    
        self.s1 = p.Sort(0, "", 0, "Effet : explose 75 DG à 2 PO (-20% DG à 2 PO)", 0, 0, type_cibles = 'moi', zone_cible = 'cercle', taille_zone = 2, dg_min = 70, dg_max = 80, poussee = 1)
        p.Personnage.defS(self, [self.s1])
        
        self.time_to_pass = 250
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        if self.nb_tour >= 2:
            if self.pv == self.pv_max:
                ChatTextuel.ajout("{} éclot !".format(joueur.pseudo))
                i = 1
                for perso in groupeGlobalPerso:
                    if perso.nom_classe == 'Dragonnet':
                        i+=1
                perso = Dragonnet('Dragonnet '+str(i))
                p.sort_Invoc(perso, self.parent, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel) 
                bf.mort(self, groupePersoCbt, groupePersoHorsCbt, groupeGlyphe, ChatTextuel)
                
            else:
                ChatTextuel.ajout("{} explose !".format(joueur.pseudo))
                sort = joueur.S[0]
                dg_min = sort.dg_min
                dg_max = sort.dg_max 
                pouss = sort.poussee
                for cible in cibles:
                    if cible != joueur:
                        p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                        if cible.pv > 0:
                            p.sort_poussee(pouss, joueur, cible, pos, M, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                bf.mort(joueur, groupePersoCbt, groupePersoHorsCbt, groupeGlyphe, ChatTextuel)
        
             
    