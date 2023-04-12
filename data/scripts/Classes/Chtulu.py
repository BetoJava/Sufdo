from random import randint

import data.scripts.personnages as p
import data.scripts.battle_functions as bf

class Chtulu(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Chtulu", 12)
        p.Personnage.__init__(self, pseudo, "Chtulu", 800, 11, 6, 2, 4, 5, 3, 'chtulu')
    
       
        """num, nom, po, effet_str, cout, latence, coup_par_tour = 0, zone_tire = 'cercle', type_cibles = 'ennemis', zone_cible = 'case', taille_zone = 1, po_min = 0, ldv = True"""
        
        self.s1 = p.Sort(0,"Amitié", 4, "+15 DMG (2t) allié et lanceur", 3, 0, 1,'cercle', po_modifiable = True, ldv = False)
        self.s2 = p.Sort(1,"Invoc de Chauve-Souris", 3, "Chauve-Souris : 80 PV, 5PA, 6PM", 4, 2, 1, type_cibles = 'vide', po_modifiable = True, isSortInvoc = True)
        self.s3 = p.Sort(2,"Invoc de Araignée", 2, "Araignée : 120 PV, 6PA, 2PM", 4, 2, 1, type_cibles = 'vide', po_modifiable = True, isSortInvoc = True)
        self.s4 = p.Sort(3,"Invoc de Zombie", 5,"Zombie : 80 PV, 6PA, 4PM", 4, 2, 1, type_cibles = 'vide', po_modifiable = True, isSortInvoc = True)
        self.s5 = p.Sort(4,"Croc vampire", 5, "• 30 DG (ennemis) | vole 50"+"%"+" de la vie de l'invoc alliée", 3, 0, 2, dg_min = 28, dg_max = 32, po_modifiable = True)
        self.s6 = p.Sort(5,"Surchauffe", 4,"• 30 DG/invoc ", 5, 2, 1, zone_tire = 'croix', taille_zone = 3, po_modifiable = True, dg_min = 28, dg_max = 32)
        self.s7 = p.Sort(6,"Rempart", 5, "+10"+"%"+" res (3t) allié et lanceur", 2, 3, 1, zone_tire = 'cercle', ldv = False)
        self.s8 = p.Sort(7,"Pousse pousse", 4, "• 30 DG et pousse de 2 cases", 3, 0, 2, zone_tire = 'croix', po_modifiable = True, dg_min = 28, dg_max = 32, poussee = 2)
        self.s9 = p.Sort(8,"Attirance", 4, "• 30 DG et attire de 2 cases", 3, 0, 2, zone_tire = 'cercle', po_modifiable = True, dg_min = 28, dg_max = 32, poussee = 2, ldv = False)
        self.s10 = p.Sort(9,"Fuyance", 2, "• +3 PM +3 fuite | -3PA", 2, 0, 1, 'croix', 'moi')
        self.s11 = p.Sort(10, "Libération", 0, "Repousse de 2 cases", 4, 2, 1, type_cibles = 'moi', zone_cible = 'croix', poussee = 2)
        self.s12 = p.Sort(11, "Invoc Arbre", 3, "Arbre : 100 PV", 5, 4, 1, po_modifiable = True, isSortInvoc = True)
        self.s13 = p.Sort(12, "Déplacement stratégique", 6, "CS : se repousse de 2 cases, A : s'avance de 2 cases, Z : échange de place", 3, 2, 1, zone_tire = 'cercle', po_modifiable = True)
        p.Personnage.defS(self, [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9, self.s10, self.s11, self.s12, self.s13])
            
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
            if cible in joueur.Invocs:
                cible.bDmg.append([15,3])
                joueur.bDmg.append([15,2])
                ChatTextuel.ajout(cible.pseudo+" et " + joueur.pseudo + " gagnent 15 Dmg pour 2 tours !")
        
                    
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Chauve Souris':
                i+=1
                 
        perso = ChauveSouris('Chauve Souris '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
        
   
                
    def sort3(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Araignée':
                i+=1
                 
        perso = Araignee('Araignée '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
        
            
    def sort4(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Zombie':
                i+=1
                 
        perso = Zombie('Zombie '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
        

    def sort5(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[4]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
            if cible.team != joueur.team:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            elif cible in joueur.Invocs:
                dg = cible.pv//2
                p.sort_DG(dg, dg, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                p.sort_Soin(dg, dg, joueur, joueur, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            

     
    def sort6(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel): 
        sort = joueur.S[5]
        coeff = 1
        for invo in joueur.Invocs:
            if invo.pv > 0:
                coeff += 1

        dg_min = sort.dg_min*coeff
        dg_max = sort.dg_max*coeff

        for cible in cibles:
            if cible.team != joueur.team:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
            
                
    def sort7(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            if cible in joueur.Invocs:
                cible.bRes.append([10,2])
                joueur.bRes.append([10,1])
                ChatTextuel.ajout("{} et {} gagnent 10"+"%"+" res pour 1 tours !".format(cible.pseudo, joueur.pseudo))


    def sort8(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[7]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        pouss = sort.poussee

        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            p.sort_poussee(pouss, joueur, cible, pos, M, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        
            
    def sort9(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[8]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        pouss = sort.poussee

        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            p.sort_Attire(2, joueur.pos, cible, M, groupePersoCbt)

    def sort10(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            presence = False
            for etat in cible.etats:
                if 'Mode fuyance' in etat:
                    cible.etats.remove(etat)
                    presence = True
                    for type_boost in cible.Boost:
                        for boost in type_boost:
                            if len(boost) >= 3:
                                if boost[2] == 'MF':
                                    type_boost.remove(boost)
                                    
            if not presence:
                cible.etats.append(['Mode fuyance', 100000000,'MF'])  
                cible.fuite += 3
                cible.bPa.append([-2,100000000,'MF'])
                cible.bPm.append([3,100000000,'MF'])
                cible.bPui.append([15,100000000,'MF'])

        
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
        
        for cible in cibles:
            if cible in joueur.Invocs:
                if cible.nom_classe == "Chauve Souris":
                    p.sort_poussee(2, cible, joueur, pos, M, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)

                if cible.nom_classe == "Araignée":
                    p.sort_Attire(2, cible.pos, joueur, M, groupePersoCbt)

                if cible.nom_classe == "Zombie":
                    bf.tp(M, cible.pos, joueur, groupePersoCbt)
                    

class ChauveSouris(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Chauve Souris", 23)
        p.Personnage.__init__(self, pseudo, "Chauve Souris", 80, 5, 6, 0, 10, 0, 0, 'chauveSouris', True)
  
        self.s1 = p.Sort(0, "Croc", 1, "• 15 DG", 3, 0, 1, zone_tire = 'croix', dg_min = 14, dg_max = 16)
        self.s2 = p.Sort(1, "Peur", 1, "Retire 7 DMG (1t)", 2, 0, 2)
        p.Personnage.defS(self, [self.s1, self.s2])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max 
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
    
        
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[1]
        pouss = sort.poussee
        
        for cible in cibles:
            cible.bDmg.append([-7,2,"venin"])
            ChatTextuel.ajout("{} perd 7 DMG pour 1 tour.".format(cible.pseudo))


class Araignee(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Araignée", 23)
        p.Personnage.__init__(self, pseudo, "Araignée", 120, 6, 2, 0, 1, 2, 0, 'saltik', True)
  
        self.s1 = p.Sort(0, "Venin", 1, "• 15 DG • -5"+"%"+"res (1t)", 3, 0, 2, zone_tire = 'croix', dg_min = 14, dg_max = 16)
        p.Personnage.defS(self, [self.s1])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max 
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            cible.bRes.append([-5,2,"venin"])
            ChatTextuel.ajout("{} perd 5"+"%"+" res pour 1 tour.".format(cible.pseudo))
    
        

class Zombie(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Zombie", 23)
        p.Personnage.__init__(self, pseudo, "Zombie", 80, 6, 4, 0, 2, 0, 0, 'zombie', True)
  
        self.s1 = p.Sort(0, "Jette pierre", 6, "• 10 DG", 3, 0, 2, zone_tire = 'cercle', dg_min = 9, dg_max = 11)
        self.s2 = p.Sort(1, "Crachat", 4, "Retire 1PA (1t)", 3, 0, 1, zone_tire = 'cercle')
        p.Personnage.defS(self, [self.s1, self.s2])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max 
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
    
        
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[1]
        pouss = sort.poussee
        
        for cible in cibles:
            cible.bPa.append([-1,2,"crachat"])
            ChatTextuel.ajout("{} perd 1 PA pour 1 tour.".format(cible.pseudo))