import data.scripts.personnages as p
import data.scripts.battle_functions as bf

class MonstreCorrompu(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Monstre Corrompu",11)
        p.Personnage.__init__(self, pseudo, "Monstre Corrompu", 450, 8, 3, 3, 4, 13, 0, 'pekidark', isIA = True, type_ia = 'combatif')
    
        self.s1 = p.Sort(0, "Morsure", 1, "155 DG", 4, 0, 2, zone_tire = 'croix', type_cibles = 'tout sans moi', dg_min = 150, dg_max = 160, type_sort_ia = ['offensif'])
        self.s2 = p.Sort(1, "Bond du poi", 4, "tp + 15%res", 2, 2, 1, zone_tire = 'cercle', type_cibles = 'vide', ldv = False, po_modifiable = True, type_sort_ia = ['tp'])
        self.s3 = p.Sort(2, "Soin", 0, "+ 100 PV", 2, 4, type_cibles = 'moi', dg_min = 68, dg_max = 72, cible_necessaire = True, type_sort = 'Soin', type_sort_ia = ['support'])
        self.s4 = p.Sort(3, "Epée divine", 0, "20 DG et + 20 DMG (1t)", 3, 0, 2, type_cibles = 'moi', zone_cible = 'croix', taille_zone = 3, dg_min = 17, dg_max = 23, type_sort_ia = ['offensif', 'boost'], priorite = 50)
        self.s5 = p.Sort(4, "Accélération", 0, "+ 3 PM (1t)", 1, 4, type_cibles = 'moi', type_sort_ia = ['boost déplacement'])
        self.s6 = p.Sort(5,"Charge",5 ,"• 60 DG | Avance jusqu'à la case ciblée", 3, 2, 1, 'croix', po_modifiable = True, dg_min = 55, dg_max = 65, type_sort_ia = ['charge'])
        p.Personnage.defS(self, [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max 
        for cible in cibles:
             if cible.team != joueur.team:
                 p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                 
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        bf.tp(M, pos, joueur, groupePersoCbt)
        joueur.bRes.append([15,1])
        ChatTextuel.ajout("{} gagne 15% Res pour 1 tour !".format(joueur.pseudo))
        
    def sort3(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[2]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        p.sort_Soin(dg_min, dg_max, joueur, joueur, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
             
    def sort4(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[3]
        dg_min = sort.dg_min
        dg_max = sort.dg_max 
        for cible in cibles:
            if cible.team == joueur.team:
                cible.bDmg.append([20,2])
                ChatTextuel.ajout("{} gagne 20 DMG pour 2 tour !".format(cible.pseudo))
            else:
                p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                
    def sort5(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        joueur.bPm.append([3,1])
        ChatTextuel.ajout("{} gagne 3 PM pour 1 tour !".format(joueur.pseudo))
        bf.affiche_point(3, joueur, groupeGlobal, 'pm')
        
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