from random import randint

import data.scripts.personnages as p
import data.scripts.battle_functions as bf

class Invocateur(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Invocateur", 19)
        p.Personnage.__init__(self, pseudo, "Invocateur", 900, 11, 6, 3, 1, 2.5, 6, 'invocateur')
    
       
        """num, nom, po, effet_str, cout, latence, coup_par_tour = 0, zone_tire = 'cercle', type_cibles = 'ennemis', zone_cible = 'case', taille_zone = 1, po_min = 0, ldv = True"""
        
        self.s1 = p.Sort(0, "Onde plane", 5, "22 DG", 3, 0, 3, dg_min = 20, dg_max = 24, po_modifiable = True)
        self.s2 = p.Sort(1, "Tornade", 6, "30 DG | retire 1 fuite (2t) (max 2)", 4, 0, 2, 'croix', dg_min = 27, dg_max = 33, zone_cible = 'colonne', taille_zone = 2, po_modifiable = True, po_min = 2)
        self.s3 = p.Sort(2, "Mercurocrum", 4, "25/30 Soin (alliés/invocs)", 3, 0, 2, type_cibles = 'alliés', dg_min = 24, dg_max = 26, po_modifiable = True, type_sort = 'Soin')
        self.s4 = p.Sort(3, "Glyphe protecteur", 3, "Pose un glyphe (2t) : débuter son tour dedans : 35 Bouclier (2t) (alliés)", 4, 5, 1, type_cibles = 'tout', zone_cible = 'cercle', taille_zone = 3, po_modifiable = True, ldv = False, isGliphe = True)
        self.s5 = p.Sort(4, "Inspiration", 0, "+2PM/+2PA/+35Pui (mes invocs) | +1PM/+1PA (alliés sauf lanceur)", 3, 4, 1, 'croix', 'moi', zone_cible = 'cercle', taille_zone = 3)
        self.s6 = p.Sort(5, "Invocation du Démon", 2, "Démon : 150 PV, 8PA, 3PM", 4, 5, 1, type_cibles = 'vide', po_modifiable = True, isSortInvoc = True)
        self.s7 = p.Sort(6, "Invocation de l'Ange", 2, "Ange : 150 PV, 6PA, 3PM", 4, 5, 1, type_cibles = 'vide', po_modifiable = True, isSortInvoc = True)
        self.s8 = p.Sort(7, "Invocation de l'Axolotl", 2, "Axolotl : 150 PV, 6PA, 2PM", 4, 5, 1, type_cibles = 'vide', po_modifiable = True, isSortInvoc = True)
        self.s9 = p.Sort(8, "Invocation du Serpent", 2, "Serpent : 150 PV, 6PA, 4PM", 4, 5, 1, type_cibles = 'vide', po_modifiable = True, isSortInvoc = True)
        self.s10 = p.Sort(9, "Invocation du Dieu Malus", 1, "Dieu Malus : 300 PV, 8PA, 3PM (1 max sur le terrain allié)", 6, 7, 1, type_cibles = 'vide', isSortInvoc = True)
        self.s11 = p.Sort(10, "Libération", 0, "Repousse de 2 cases", 4, 2, 1, type_cibles = 'moi', zone_cible = 'croix', poussee = 2)
        self.s12 = p.Sort(11, "Invoc Arbre", 3, "Arbre : 100 PV", 5, 4, 1, po_modifiable = True, isSortInvoc = True)
        self.s13 = p.Sort(12, "Surcharge physique", 6, "• 5DG (feu, air, eau, terre) • Chaque attaque d'une invoc boost de 5 DG dans son élément associé", 6, 0, 1, zone_tire = 'diago', dg_min = 16, dg_max = 24, po_modifiable = True)
        self.s14 = p.Sort(13, "Invoc Mur", 8, "Invoque un mur", 1, 0, 1000, type_cibles = 'vide', po_modifiable = True)
    
        p.Personnage.defS(self, [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9, self.s10, self.s11, self.s12, self.s13, self.s14])
     
    
    def sort14(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        M[pos[0]][pos[1]] = 1
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        boost = 0
        
        for cible in cibles:
            if cible.nom_classe == 'Lentille':
                cibles = []
                (X,Y) = joueur.pos
                (x,y) = cible.pos
                boost = (abs(x-X) + abs(Y-y))*0.05
                dx, dy = x-X, y-Y
                pos = (X+2*dx, Y+2*dy)
                for perso in groupePersoCbt:
                    if perso.pos == pos:
                        cibles = [perso]
                        
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel, multiplicateur = (1+boost))
                    
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[1]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            a = 0
            for boost in cible.bFuite:
                if "tornade" in boost:
                    a += 1
            if a < 2:
                cible.bFuite.append([-1,3,"tornade"])
                ChatTextuel.ajout("{} perd 1 de fuite pour 2 tours.".format(cible.pseudo))
            
                
    def sort3(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[2]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        for cible in cibles:
            if cible.team == joueur.team:
                if cible.isInvoc:
                    p.sort_Soin(dg_min+5, dg_max+5, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                else:
                    p.sort_Soin(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
    def sort4(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[3]
        glyphe = p.Glyphe(sort, joueur, 2, zone_cible, only_allies = True, bShield = [[35,2]], couleur = 'bleu')
        joueur.Glyphes.append(glyphe)
        groupeGlyphe.add(glyphe)

    def sort5(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            if cible in joueur.Invocs:
                cible.bPa.append([2,3])
                cible.bPm.append([2,3])
                cible.bPui.append([35,3])
                bf.affiche_point(2, cible, groupeGlobal, 'pm')
                bf.affiche_point(2, cible, groupeGlobal, 'pa')
                ChatTextuel.ajout("{} gagne 2 PA, 2 PM et 35 Pui pour 2 tours !".format(cible.pseudo))
            elif cible.team == joueur.team and cible != joueur:
                cible.bPa.append([1,3])
                cible.bPm.append([1,3])
                bf.affiche_point(1, cible, groupeGlobal, 'pm')
                bf.affiche_point(1, cible, groupeGlobal, 'pa')
                ChatTextuel.ajout("{} gagne 1 PA et 1 PM pour 2 tours !".format(cible.pseudo))
     
    def sort6(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel): 
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Démon':
                i+=1
                 
        perso = Demon('Démon '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
        
        for sort in [self.s6, self.s7, self.s8, self.s9]:
            if sort.latence == 0:
                sort.latence = 1
                
    def sort7(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Ange':
                i+=1
                 
        perso = Ange('Ange '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
        
        for sort in [self.s6, self.s7, self.s8, self.s9]:
            if sort.latence == 0:
                sort.latence = 1
        
    def sort8(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Axolotl':
                i+=1
                 
        perso = Axolotl('Axolotl '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
        
        for sort in [self.s6, self.s7, self.s8, self.s9]:
            if sort.latence == 0:
                sort.latence = 1
        
    def sort9(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Serpent':
                i+=1
                 
        perso = Serpent('Serpent '+str(i))
        p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
        
        for sort in [self.s6, self.s7, self.s8, self.s9]:
            if sort.latence == 0:
                sort.latence = 1
            
    def sort10(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 0
        for perso in groupePersoCbt:
            if perso.team == joueur.team:
                if perso.nom_classe == 'Dieu Malus':
                    i+=1
        if i == 0:         
            perso = Malus('Dieu Malus')
            p.sort_Invoc(perso, joueur, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)   
        else:
            joueur.pa += self.s10.cout
            
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
        
        dg_feu = 5
        dg_air = 5
        dg_eau = 5
        dg_terre = 5
        
        for boost in sort.bDg:
            if 'feu' in boost:
                dg_feu += boost[0]
            elif 'air' in boost:
                dg_air += boost[0]
            elif 'eau' in boost:
                dg_eau += boost[0]
            elif 'terre' in boost:
                dg_terre += boost[0]
        
        
        for cible in cibles:
            p.sort_DG(dg_feu-1, dg_feu+1, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            p.sort_DG(dg_air-1, dg_air+1, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            p.sort_DG(dg_eau-1, dg_eau+1, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            p.sort_DG(dg_terre-1, dg_terre+1, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        
        if cibles != []:
            sort.Boost[0] = []
            sort.bDg = []
        
class Demon(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Démon", 20)
        p.Personnage.__init__(self, pseudo, "Démon", 150, 8, 3, 2, 2, 2.5, 0, 'demon', True)
  
        self.s1 = p.Sort(0, "Griffe satanique", 4, "22 DG", 4, 0, 2, 'diago', dg_min = 21, dg_max = 23)
        self.s2 = p.Sort(1, "Malédiction", 4, "Retire 5 Dmg à la cible (1t) (max 1)", 2, 0, 3, po_min = 2)
        p.Personnage.defS(self, [self.s1, self.s2])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max 
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        if cibles != []:
            joueur.parent.S[12].bDg.append([5,100000000, 'feu'])
        
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            if cible.team != joueur.team:
                a = 0
                for boost in cible.bDmg:
                    if "malédiction" in boost:
                        a += 1
                        break
                if a == 0:
                    cible.bDmg.append([-5,2,"malédiction"])
                    ChatTextuel.ajout("{} perd 5 Dmg pour 1 tours !".format(cible.pseudo))
            
class Ange(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Ange", 21)
        p.Personnage.__init__(self, pseudo, "Ange", 150, 6, 3, 0, 4, 2.5, 0, 'ange', True)
  
        self.s1 = p.Sort(0, "Ventilation", 3, "18 DG", 4, 0, 2, zone_tire = 'croix', dg_min = 17, dg_max = 19)
        self.s2 = p.Sort(1, "Support angélique", 3, "15 Soin", 3, 0, 3, dg_min = 14, dg_max = 16, type_sort = 'Soin')
        p.Personnage.defS(self, [self.s1, self.s2])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max 
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        if cibles != []:
            joueur.parent.S[12].bDg.append([5,100000000, 'air'])
        
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[1]
        dg_min = sort.dg_min
        dg_max = sort.dg_max 
        for cible in cibles:
            if cible.team == joueur.team:
                p.sort_Soin(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            
class Axolotl(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Axolotl", 22)
        p.Personnage.__init__(self, pseudo, "Axolotl", 150, 6, 2, 4, 1, 2.5, 0, 'triton', True)
  
        self.s1 = p.Sort(0, "Marteau aquatique", 1, "24 DG, pose un glyphe (1t) autour de la cible qui augmente les dégats finaux de 15%", 5, 0, 1, zone_tire = 'croix', zone_cible = 'croix', dg_min = 23, dg_max = 25)
        self.s2 = p.Sort(1, "Axolotion", 1, "retire 1 fuite (2t) (max 2)", 2, 0, 3, zone_tire = 'croix')
        p.Personnage.defS(self, [self.s1, self.s2])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max 
        for cible in cibles:
            if cible.pos == pos:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
        
        if cibles != []:
            joueur.parent.S[12].bDg.append([5,100000000, 'eau'])        
            # On veut pas la case du milieu dans le glyphe #
            zone_cible.remove(pos)
            
            glyphe = p.Glyphe(sort, joueur.parent, 2, zone_cible, only_allies = True, bDgFinaux = [[0.15,1]], type_glyphe = 'instantané', couleur = 'blanc')
            joueur.Glyphes.append(glyphe)
            groupeGlyphe.add(glyphe)
        
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            if cible.team != joueur.team:
                a = 0
                for boost in cible.bFuite:
                    if "axolotion" in boost:
                        a += 1
                if a < 2:
                    cible.bFuite.append([-1,3,"axolotion"])
                    ChatTextuel.ajout("{} perd 1 de fuite pour 2 tours.".format(cible.pseudo))
            
class Serpent(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Serpent", 23)
        p.Personnage.__init__(self, pseudo, "Serpent", 150, 6, 4, 0, 4, 2.5, 0, 'serpent', True)
  
        self.s1 = p.Sort(0, "Venin", 2, "• 10 DG • Poison : 7 DG (2t)", 4, 0, 2, zone_tire = 'croix', dg_min = 9, dg_max = 11)
        self.s2 = p.Sort(1, "Peur", 1, "Repousse de 1 case et applique 5% d'érosion (2t)", 4, 0, 1, zone_tire = 'croix', poussee = 1)
        p.Personnage.defS(self, [self.s1, self.s2])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max 
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            cible.poison.append([10,3,joueur, "est envenimé."])
            ChatTextuel.ajout("{} est envenimé pour 2 tour (7 DG/t).".format(cible.pseudo))
        if cibles != []:
            joueur.parent.S[12].bDg.append([5,100000000, 'terre'])
    
        
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[1]
        pouss = sort.poussee
        
        for cible in cibles:
            p.sort_poussee(pouss, joueur, cible, pos, M, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
            a = 0
            for boost in cible.bEro:
                if "peur" in boost:
                    a += 1
            if a < 2:
                cible.bEro.append([0.05,3,"peur"])
                ChatTextuel.ajout("{} est érodé de 5% pour 2 tours.".format(cible.pseudo))
            
class Malus(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Dieu Malus", 24)
        p.Personnage.__init__(self, pseudo, "Dieu Malus", 300, 8, 3, 3, 3, 2.5, 0, 'malus', True)
  
        self.s1 = p.Sort(0, "OPPH", 3, "20 DG", 4, 0, 2, dg_min = 18, dg_max = 22, po_modifiable = True)
        self.s2 = p.Sort(1, "Lentille mince", 3, "Lentille : 30 PV, les ondes lancées sur la lentille sont reportées symétriquement et amplifiées avec la distance", 2, 2, 1, type_cibles = 'vide', po_modifiable = True)
        self.s3 = p.Sort(2, "Glyphe optique", 3, "Pose un glyphe (2t) : débuter son tour dedans : +2 PO (1t)", 4, 4, 1, type_cibles = 'tout', zone_cible = 'cercle', taille_zone = 2, isGliphe = True)
        p.Personnage.defS(self, [self.s1, self.s2, self.s3])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        
        boost = 0
        
        for cible in cibles:
            if cible.nom_classe == 'Lentille':
                cibles = []
                (X,Y) = joueur.pos
                (x,y) = cible.pos
                boost = (abs(x-X) + abs(Y-y))*0.05
                dx, dy = x-X, y-Y
                pos = (X+2*dx, Y+2*dy)
                for perso in groupePersoCbt:
                    if perso.pos == pos:
                        cibles = [perso]
                        
        for cible in cibles:
            p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel, multiplicateur = (1+boost))
        
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        i = 1
        for perso in groupeGlobalPerso:
            if perso.nom_classe == 'Lentille':
                i+=1
        
        for perso in groupePersoCbt:
            if perso.nom_classe == 'Lentille' and perso.parent == joueur.parent :
                bf.mort(perso, groupePersoCbt, groupePersoHorsCbt, groupeGlyphe, ChatTextuel)
                
        perso = Lentille('Lentille '+str(i))
        p.sort_Invoc(perso, joueur.parent, pos, groupePersoCbt, groupeGlobalPerso, ChatTextuel)
        
    def sort3(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[2]
        glyphe = p.Glyphe(sort, joueur, 2, zone_cible, only_allies = True, bPo = [[2,1]], couleur = 'blanc')
        joueur.Glyphes.append(glyphe)
        groupeGlyphe.add(glyphe)
            
class Lentille(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Lentille", 25)
        p.Personnage.__init__(self, pseudo, "Lentille", 50, 0, 0, 0, 0, 0, 0, 'lentille', isInvoc = True, isStatic = True)

        p.Personnage.defS(self, [])

    

       