from random import randint

import data.scripts.personnages as p
import data.scripts.battle_functions as bf

class Gigolo(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Gigolo", 12)
        p.Personnage.__init__(self, pseudo, "Gigolo", 820, 11, 6, 4, 1, 10, 0, 'gigolo')
    
       
        """num, nom, po, effet_str, cout, latence, coup_par_tour = 0, zone_tire = 'cercle', type_cibles = 'ennemis', zone_cible = 'case', taille_zone = 1, po_min = 0, ldv = True"""
        
        self.s1 = p.Sort(0,"Lance gigo", 7, "• 35 DG", 4, 0, 3,'croix', po_min = 2, dg_min = 33, dg_max = 37, po_modifiable = True)
        self.s2 = p.Sort(1,"Lèche cul", 2, "• 35 DG • retire 0-3 PM (1t) non cumulable", 3, 0, 2, dg_min = 33, dg_max = 37, po_modifiable = True)
        self.s3 = p.Sort(2,"Saute mouton", 4, "téléporte à la case ciblée", 3, 0, 1, 'diago', 'vide', po_modifiable = True)
        self.s4 = p.Sort(3,"Charme", 0,"• Attire toutes les entitées de 2 cases | +50 pui", 3, 0, 1, type_cibles = 'moi', zone_cible = 'tout')
        self.s5 = p.Sort(4,"Frappe séductrice", 1, "• 30 DG (+10 DG du sort (3t))", 5, 0, 2, dg_min = 48, dg_max = 52)
        self.s6 = p.Sort(5,"Lunettes stylées", 0,"• + 3PO (2t)", 2, 3, zone_cible = 'cercle', taille_zone = 3)
        self.s7 = p.Sort(6,"Pêche mignonne", 2, "• 15 DG", 2, 0, 4, zone_tire = 'croix', po_modifiable = True, dg_min = 13, dg_max = 17)
        self.s8 = p.Sort(7,"Pogo de fans", 5, "• glyphe : 35 DG | retire 1 PM (1t) | retire 2 fuite", 6, 3, 1, zone_cible = 'cercle', taille_zone = 4, po_modifiable = True, ldv = False, isGliphe = True)
        self.s9 = p.Sort(8,"Danse de star", 0, "20 Soin/entité dans la zone", 5, 3, 1, type_cibles = 'moi', zone_cible = 'cercle', taille_zone = 2, dg_min = 19, dg_max = 21, type_sort = 'Soin')
        self.s10 = p.Sort(9,"Mode Star", 0, "• +1 PM +1 PA +15 Pui | -20"+"%"+" res", 2, 0, 1, 'croix', 'moi')
        self.s11 = p.Sort(10, "Libération", 0, "Repousse de 2 cases", 4, 2, 1, type_cibles = 'moi', zone_cible = 'croix', poussee = 2)
        self.s12 = p.Sort(11, "Invoc Arbre", 3, "Arbre : 100 PV", 5, 4, 1, po_modifiable = True, isSortInvoc = True)
        self.s13 = p.Sort(12, "Flemme", 5, "Repousse de 1 case", 1, 0, 2, zone_tire = 'croix', po_modifiable = True, poussee = 1)
        p.Personnage.defS(self, [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9, self.s10, self.s11, self.s12, self.s13])
      
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
            if cible.team != joueur.team:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        
                    
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[1]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        ret = randint(0,3)
        
        for cible in cibles:
            for boost in cible.bPm:
                if "lc" in boost:
                    cible.bPm.remove(boost)
            cible.bPm.append([-ret,2,"lc"])
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            if ret > 0:
                bf.affiche_point(-1, cible, groupeGlobal, 'pm')
                ChatTextuel.ajout("{} perd 1 PM pour 1 tour.".format(cible.pseudo))
   
                
    def sort3(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        bf.tp(M, pos, joueur, groupePersoCbt)
            
    def sort4(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[3]
        
        for perso in groupePersoCbt:
            if perso != joueur:
                p.sort_Attire(2, joueur.pos, perso, M, groupePersoCbt)

        joueur.bPui.append([50,2])         
        ChatTextuel.ajout("{} gagne 50 puissance pour 2 tours !".format(joueur.pseudo))

    def sort5(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[4]
        boost = sort.somme_boost('dg')
        dg_min = sort.dg_min + boost
        dg_max = sort.dg_max + boost
        
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        sort.bDg.append([10,3])
        ChatTextuel.ajout("Le sort {} est boosté de 20 DG pour 3 tour.".format(sort.nom))   

     
    def sort6(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel): 
        for cible in cibles:
            cible.bPo.append([3,3])
            ChatTextuel.ajout("{} gagne 3 PO pour 3 tours.".format(cible.pseudo))
            
                
    def sort7(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[6]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
        
    def sort8(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[7]
        
        glyphe = p.Glyphe(sort, joueur, 2, zone_cible, dg_min = 33, dg_max = 37, bFuite = [[-3,1]], bPm = [[-1,1]], couleur = 'rouge')
        joueur.Glyphes.append(glyphe)
        groupeGlyphe.add(glyphe)
            
    def sort9(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[8]
        
        dg_min = sort.dg_min*(len(cibles)-1)
        dg_max = sort.dg_max*(len(cibles)-1)
        
        p.sort_Soin(dg_min, dg_max, joueur, joueur, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                
    def sort10(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            presence = False
            for etat in cible.etats:
                if 'Mode star' in etat:
                    cible.etats.remove(etat)
                    presence = True
                    for type_boost in cible.Boost:
                        for boost in type_boost:
                            if len(boost) >= 3:
                                if boost[2] == 'MS':
                                    type_boost.remove(boost)
                                    
            if not presence:
                cible.etats.append(['Mode star', 100000000,'MS'])  
                cible.bRes.append([-20,100000000,'MS'])
                cible.bPa.append([1,100000000,'MS'])
                cible.bPm.append([1,100000000,'MS'])
                cible.bPui.append([15,100000000,'MS'])

        
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