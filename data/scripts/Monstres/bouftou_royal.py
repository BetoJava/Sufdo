import data.scripts.personnages as p
import data.scripts.battle_functions as bf

class BouftouRoyal(p.Classes):
    
    def __init__(self, pseudo):
        
        p.Classes.__init__(self, "Bouftou Royal",-1)
        p.Personnage.__init__(self, pseudo, "Bouftou Royal", 610, 7, 5, 3, 4, 14, 0, 'bouftou_royal', isIA = True, type_ia = 'combatif')
    
        self.s1 = p.Sort(0, "Morsure du Bouftou Royal", 1, "255 DG", 4, 0, 2, zone_tire = 'croix', type_cibles = 'tout sans moi', dg_min = 250, dg_max = 260, type_sort_ia = ['offensif'])
        self.s2 = p.Sort(1, "Cuirasse Laineuse", 7, "30% Res", 3, 2, 1, zone_tire = 'cercle', po_modifiable = True, type_sort_ia = ['support'])
        self.s3 = p.Sort(2, "Guérison Bouftou", 6, "+ 100 PV", 2, 0, 1, dg_min = 95, dg_max = 105, cible_necessaire = True, type_sort = 'Soin', type_sort_ia = ['support'])
        p.Personnage.defS(self, [self.s1, self.s2, self.s3])
    
    def sort1(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[0]
        dg_min = sort.dg_min
        dg_max = sort.dg_max 
        for cible in cibles:
             if cible.team != joueur.team:
                 p.sort_DG(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
                 
    def sort2(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        for cible in cibles:
            cible.bRes.append([30,2])
            ChatTextuel.ajout("{} gagne 30% Res pour 1 tour !".format(cible.pseudo))
        
    def sort3(self, joueur, cibles, M, zone_cible, pos, groupePersoCbt, groupePersoHorsCbt, groupeGlobal, groupeGlobalPerso, groupeGlyphe, ChatTextuel):
        sort = joueur.S[2]
        dg_min = sort.dg_min
        dg_max = sort.dg_max
        for cible in cibles:
            p.sort_Soin(dg_min, dg_max, joueur, cible, pos, sort, groupePersoCbt, groupeGlobal, groupeGlyphe, ChatTextuel)
             