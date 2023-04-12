'''import pygame

class Sort(pygame.sprite.Sprite):
    
    
    def __init__(self, num, name, po, effet_str, cout, latence, zone_tire = 'cercle', type_cibles = 'ennemis', zone_cible = 'case', taille_zone = 1, po_min = 0, ldv = 'avec'):
        
        dico_zone_tire = {'cercle' : 0, 'ligne' : 1, 'diago' : 2, 'étoile' : 3}
        dico_type_cible = {'ennemis' : 0, 'alliés' : 1, 'alliés sans moi' : 2, 'invoc' : 3, 'mes invocs' : 4, 'mes invocs et moi' : 5, 'tout' : 6, 'moi' : 7, 'tout sans moi' : 8}
        dico_zone_cible = {'cercle' : 0, 'croix' : 1, 'ligne' : 2, 'colonne' : 3, 'carré' : 4, 'case' : 5}
        dico_ldv = {'sans' : 0, 'avec' : 1}
        
        self.num = num
        self.name = name
        self.po = po
        self.effet_str = effet_str
        self.cout = cout
        self.latence = latence
        self.zone_tire = zone_tire
        self.type_cibles = type_cibles
        self.zone_cible = zone_cible
        self.taille_zone = taille_zone
        self.po_min = po_min
        self.ldv = ldv
        '''
        
l = [[1,3], [1,2]]
for i in l:
    i[0] -= 1
print(l)