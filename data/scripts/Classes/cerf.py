from random import randint

import data.scripts.personnages as p
import data.scripts.battle_functions as bf

class Cerf(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Cerf", 6)
        p.Personnage.__init__(self, pseudo, "Cerf", 1100, 11, 6, 3, 6, 12, 4, 'cerf')
    
        """num, nom, po, effet_str, cout, latence, coup_par_tour = 0, zone_tire = 'cercle', type_cibles = 'ennemis', zone_cible = 'case', taille_zone = 1, po_min = 0, ldv = 'avec'"""
        self.s1 = p.Sort(0, "Coup de bois", 1, "15 DG",2, 0, 6, dg_min = 13, dg_max = 17)
        self.s2 = p.Sort(1, "Coup de queue", 2, "40 DG", 4, 0, zone_tire = 'croix', po_modifiable = True, dg_min = 37, dg_max = 43)
        self.s3 = p.Sort(2, "Atterissage", 0, "20 DG et repousse les cibles de 2 cases", 3, 0, 1, type_cibles = 'moi', zone_cible = 'croix', dg_min = 18, dg_max = 22, poussee = 2)
        self.s4 = p.Sort(3, "Cerfaser", 3, "• consomme tous les PM • +50% DG/2PM sur le sort • 50 DG", 6, 0, 1, 'croix', zone_cible = 'colonne', taille_zone = 3, po_modifiable = True, dg_min = 45, dg_max = 55)
        self.s5 = p.Sort(4, "Sabots qui courent vite", 0, "+ 4 PM (1t)", 1, 2, type_cibles = 'moi')
        self.s6 = p.Sort(5, "Arbrification", 0, "• consomme tous les PM • soin 25/2PM • 25% resi + état indéplaçable (1t)", 3, 2, type_cibles = 'moi')
        self.s7 = p.Sort(6, "Appel de la forêt", 0, '• réduit de 1t Latence sort invoc • invocs "cerf" avance de 1 vers vous • 20/35 soin (allié/cerf) à 3 PO', 3, 0, 3, 'cercle', 'moi', 'cercle', 3, dg_min = 18, dg_max = 22, type_sort = 'Soin')
        self.s8 = p.Sort(7, "Mode royal", 0, "• coût des sort -1PA • -2 PM (∞) • -3 fuite +3 tacle (∞)", 2, 0, 1, type_cibles = 'moi')
        self.s9 = p.Sort(8, "Invoc Faon", 1, "Faon : 100 PV, 6PA, 3PM ", 4, 3, type_cibles = 'vide', isSortInvoc = True)
        self.s10 = p.Sort(9, "Invoc Tricerf", 2, "Sacrifie 3 Cerfs pour invoquer un Tricerf : 350 PV, 8PA, 3PM ", 12, 0)
        self.s11 = p.Sort(10, "Libération", 0, "Repousse de 2 cases", 4, 2, 1, type_cibles = 'moi', zone_cible = 'croix', poussee = 2)
        self.s12 = p.Sort(11, "Invoc Arbre", 3, "Arbre : 100 PV", 5, 4, 1, po_modifiable = True, isSortInvoc = True)
        self.s13 = p.Sort(12, "Cervela", 1, "25 DG | -2 fuite (1t) (max 2)", 3, 0, 2, 'croix', zone_cible = 'ligne', po_modifiable = True, dg_min = 22, dg_max = 28)
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
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                
    def sort3(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[2]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        pouss = sort.poussee 
        for cible in cibles:
            if cible != joueur:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                if cible.pv > 0:
                    p.sort_poussee(pouss, joueur, cible, pos, M, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
    def sort4(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[3]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        pm = joueur.pm + joueur.somme_boost('pm')
        if pm >= 0:
            joueur.pm -= pm
        else:
            pm = 0
        dg = 50 + 25*(pm//2)
        for cible in cibles:
            p.sort_DG(dg-5, dg+5, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                                       
    def sort5(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        joueur.bPm.append([4,1])
        ChatTextuel.ajout("{} gagne 4 PM pour 1 tour !".format(joueur.pseudo))
        bf.affiche_point(4, joueur, groupeGlobal, 'pm')
     
    def sort6(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):  
        sort = joueur.S[5]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        pm = joueur.pm + joueur.somme_boost('pm')
        if pm >= 0:
            joueur.pm -= pm
        else:
            pm = 0
        soin = 25*(pm//2)
    
        p.sort_Soin(soin, soin, joueur, joueur, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        joueur.bRes.append([25,1])
        ChatTextuel.ajout("{} gagne 25% rési pour 1 tours !".format(joueur.pseudo))
        joueur.etats.append(['Indéplaçable', 1])
        ChatTextuel.ajout("{} gagne est indéplaçable pour 1 tours !".format(joueur.pseudo))
              
    def sort7(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[6]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        for sort in joueur.S:
            if sort.isSortInvoc and sort.latence > 0:
                sort.latence -= 1
        for perso in groupePersoCbt:
            if perso.parent == joueur and perso.nom_classe in ["Tricerf", "Faon"]:
                p.sort_Attire(1, joueur.pos, perso, M, groupePersoCbt)
        for cible in cibles:
            if cible.team == joueur.team and cible != joueur:
                if cible.parent == joueur:
                    p.sort_Soin(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                else:
                    p.sort_Soin(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        
    def sort8(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            presence = False
            for etat in cible.etats:
                if 'Mode royal' in etat:
                    cible.etats.remove(etat)
                    presence = True
                    for sort in cible.S :
                        sort.cout = sort.cout_initial
                    cible.fuite += 3
                    cible.tacle -= 3
                    
                    for type_boost in cible.Boost:
                        for boost in type_boost:
                            if len(boost) >= 3:
                                if boost[2] == 'royal':
                                    type_boost.remove(boost)
            if not presence:
                cible.etats.append(['Mode royal', 100000000,'royal'])  
                cible.bPm.append([-2,100000000,'royal'])
                for sort in cible.S :
                    sort.cout -= 1
                bf.affiche_point(2, joueur, groupeGlobal, 'pm')
                cible.fuite -= 3
                cible.tacle += 3
                
                
                
    def sort9(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Faon':
                i+=1
        perso = Faon('Faon '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)   
            
                
    def sort10(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        faonIsCibled = False
        for cible in cibles:
            if cible in joueur.Invocs:
                for invoc in joueur.Invocs:
                    if invoc.pos == cible.pos:
                        faonIsCibled = True
                        break
        nb_faon = 0  
        for invoc in joueur.Invocs:
            if invoc.nom_classe == 'Faon':
                nb_faon += 1
                 
        if nb_faon >= 3 and faonIsCibled:
            toKill = []
            for invoc in joueur.Invocs:
                if invoc.nom_classe == 'Faon' and nb_faon > 0:
                    nb_faon -= 1
                    toKill.append(invoc)
            for invoc in toKill:
                bf.mort(invoc, groupePersoCbt, groupePersoHorsCbt, groupeGlyphe, ChatTextuel)
                
            i = 1
            for perso in groupeGlobalPerso:
                if perso.nom_classe == 'Tricerf à Taupe':
                    i+=1
                 
            perso = Tricerf('Tricerf à Taupe '+str(i))
            p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
        else:
            joueur.pa += 11
            bf.affiche_point(11, joueur, groupeGlobal, 'pa')
   
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
            for boost in cible.bFuite:
                if "cervela" in boost:
                    a += 1
            if a < 2:
                cible.bFuite.append([-2,3,"cervela"])
                ChatTextuel.ajout("{} perd 2 de fuite pour 2 tours.".format(cible.pseudo))

class Faon(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Faon", 7)
        p.Personnage.__init__(self, pseudo, "Faon", 100, 6, 3, 3, 4, 12, 0, 'faon', True)
    
        self.s1 = p.Sort(0, "Bois", 1, "18 DG", 4, 0, 100, zone_tire = 'croix', type_cibles = 'tout sans moi', dg_min = 16, dg_max = 20)
        self.s2 = p.Sort(1, "Chouchou", 1, "+ 1 PM (1t) à l'allié ciblé", 2, 1, 1, zone_tire = 'croix', type_cibles = 'alliés')
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
            if cible == joueur:
                cible.bPm.append([1,1])
            elif cible.team == joueur.team:
                cible.bPm.append([1,2])
            
            bf.affiche_point(1, cible, groupeGlobal, 'pm')
            ChatTextuel.ajout("{} gagne 1 PM pour 1 tour !".format(cible.pseudo))
             
class Tricerf(p.Classes):
  
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Tricerf", 8)
        p.Personnage.__init__(self, pseudo, "Tricerf", 350, 8, 4, 2, 5, 12, 0, 'tricerf', True)
    
        self.s1 = p.Sort(0, "Cerf vis", 1, "Faons présents • 0/1/2/3 : 50/70/90/110 DG ", 6, 0, dg_min = 20, dg_max = 85)
        self.s2 = p.Sort(1, "Cervifiant", 1, "+ 2 PA (1t) à l'allié ciblé", 2, 0, 1)
        p.Personnage.defS(self, [self.s1, self.s2])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        nb_faon = 0
        for invoc in joueur.parent.Invocs:
            if invoc.nom_classe == 'Faon' and invoc.pv > 0:
                nb_faon += 1
        if nb_faon < 4:
            dg = 50 + 20*nb_faon
        else:
            dg = 110
            
        for cible in cibles:
            p.sort_DG(dg-5,dg+5, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)     
        
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            if cible.team == joueur.team:
                cible.bPa.append([2,2])
                ChatTextuel.ajout("{} gagne 2 PA pour 1 tour !".format(cible.pseudo))
                bf.affiche_point(2, cible, groupeGlobal, 'pa')
             
    