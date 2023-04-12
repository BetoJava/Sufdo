# Import ---------- #
import pygame

import data.scripts.battle_functions as bf

def distance(pos1, pos2):
    (x, y) = pos1
    (X, Y) = pos2
    return abs(X-x) + abs(Y-y)

def IsoToCano(i,j):
    x = 640 + 32*(i-j) + 48
    y = 0 + 16*(i+j) - 302
    return x, y

def get_size_text(txt, font, hauteur, largeur):
    texte = pygame.font.Font("data/font/" + font + ".ttf", int(hauteur*0.5)).render(txt, True, (0,0,0))
    rectTexte = texte.get_rect()
    largeur = rectTexte.width
    hauteur = rectTexte.height
    return hauteur, largeur


# Objets : Boutons/Sorts/Textes ------- #
class MenuBoutonStyle(pygame.sprite.Sprite) :
    """ Création d'un simple bouton rectangulaire """
    def __init__(self, texte, couleur, font, x, y, largeur, hauteur, commande, val) :
        super().__init__()
        self._commande = commande
        self.val = val
        self.x, self.y = x,y
        self.largeur = largeur
        self.hauteur = hauteur
        self.isStyle = True
        self.isOver = False
        self.couleur = couleur # couleur in {b, bv, r}
 
        self.texte = pygame.font.Font("data/font/" + font + ".ttf", int(hauteur*0.5)).render(texte, True, (255, 255, 255))
        self.rectTexte = self.texte.get_rect()
        self.r = self.rectTexte.width/216
        
        self.dessiner()
 
    def dessiner(self):
        if self.isOver:
            self.image = pygame.image.load('data/images/Texture/button/bt_' + self.couleur + '_over.png').convert_alpha()
        else:
            self.image = pygame.image.load('data/images/Texture/button/bt_' + self.couleur +'.png').convert_alpha()
            
        self.image = pygame.transform.smoothscale(self.image, (self.largeur,self.hauteur))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
            
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (int(self.largeur/2), int(self.hauteur/2))
        self.image.blit(self.texte, self.rectTexte)
 
    def executerCommande(self) :
        self._commande(self.val)

class MenuBouton(pygame.sprite.Sprite) :
    """ Création d'un simple bouton rectangulaire """
    def __init__(self, texte, couleur, font, x, y, largeur, hauteur, commande, val) :
        super().__init__()
        self._commande = commande
        self.val = val
        self.couleur = couleur  
        self.isStyle = False
 
        self.image = pygame.Surface((largeur, hauteur))
    
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
 
        self.texte = pygame.font.Font("data/font/" + font + ".ttf", int(hauteur*0.5)).render(texte, True, (255, 255, 255))
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (int(largeur/2), int(hauteur/2))
 
        self.dessiner(couleur)
 
    def dessiner(self, couleur, boole = False) :
        self.image.fill(couleur)
        self.image.blit(self.texte, self.rectTexte)
 
    def executerCommande(self) :
        self._commande(self.val) 
        
class BoutonImage(pygame.sprite.Sprite) :
    def __init__(self, img, x, y, commande, val, xflip = False, yflip = False) :
        super().__init__()
        self._commande = commande
        self.val = val
        self.image = pygame.image.load('data/images/' + img + '.png').convert_alpha()
        if xflip or yflip:
            self.image = pygame.transform.flip(self.image, xflip, yflip)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.dessiner()
     
    def dessiner(self, couleur = (0,0,0)) :
        self.image.blit(self.image, self.rect)
     
    def executerCommande(self) :
        # Appel de la commande du bouton
        self._commande(self.val)

class Texte(pygame.sprite.Sprite):
    def __init__(self, txt, couleur, font, x, y, largeur, hauteur, opacite = 0) :
        super().__init__()
        self.opacite = opacite
        self.image = pygame.Surface((largeur, hauteur))
        self.image = self.image.convert_alpha()
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.texte = pygame.font.Font("data/font/" + font + ".ttf", int(hauteur*0.5)).render(txt, True, couleur)
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (int(largeur/2), int(hauteur/2))
        self.dessiner()

    def dessiner(self, couleur = (0,0,0)):
        self.image.fill((0,0,0,0))         
        self.image.blit(self.texte, self.rectTexte)

class TexteVariable(pygame.sprite.Sprite):
    def __init__(self, txt, couleur, font, x, y, bordure, hauteur, num = -1, isClasse = False, opacite = 0, isCentered = True) :
        super().__init__()
        self.opacite = opacite
        self.couleur = couleur
        self.font = font
        self.hauteur = hauteur
        self.bordure = bordure
        self.txt = txt
        self.num = num
        self.x,self.y = x,y
        self.isClasse = isClasse
        self.isCentered = isCentered
    
        self.texte = pygame.font.Font("data/font/" + self.font + ".ttf", int(self.hauteur*0.5)).render(self.txt, True, self.couleur)
        self.rectTexte = self.texte.get_rect()
        self.l = self.rectTexte.width+ self.bordure*2
        self.h = self.rectTexte.height+ self.bordure*2
        self.rectTexte.center = (self.l//2+bordure, self.h//2+bordure)
            
        self.image = pygame.Surface((self.l+2*bordure, self.h+2*bordure))
        self.image = self.image.convert_alpha()
        
        self.rect = self.image.get_rect()
        
        if self.isCentered:               
            self.rect.center = (x,y)
        else:     
            self.rect.center = (x+(self.l//2), y)
            
        self.dessiner()

    def maj(self, txt, couleur = (0,0,0)):
        self.txt = txt
        self.texte = pygame.font.Font("data/font/" + self.font + ".ttf", int(self.hauteur*0.5)).render(txt, True, self.couleur)
        self.rectTexte = self.texte.get_rect()      
        self.l = self.rectTexte.width + self.bordure*2
        self.h = self.rectTexte.height + self.bordure*2    
        self.rectTexte.center = (self.l//2+self.bordure, self.h//2+self.bordure)
        self.image = pygame.Surface((self.l+2*self.bordure, self.h+2*self.bordure))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        
        if self.isCentered:               
            self.rect.center = (self.x,self.y)
        else:     
            self.rect.center = (self.x+(self.l//2), self.y)
        self.dessiner()

    def dessiner(self, couleur = (0,0,0)) :
        self.image.fill((0,0,0,self.opacite))         
        self.image.blit(self.texte, self.rectTexte)
    
class TexteEphemere(pygame.sprite.Sprite):
    def __init__(self, txt, couleur, font, x, y, largeur, hauteur, temps) :
        super().__init__()
        self.temps = temps+5
        self.couleur = couleur
        self.font = font
        self.hauteur = hauteur
        self.largeur = largeur
        self.txt = txt
 
        self.image = pygame.Surface((largeur, hauteur))
        self.image = self.image.convert_alpha()
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.texte = pygame.font.Font("data/font/" + self.font + ".ttf", int(50*(1+(self.temps-7)*0.1))).render(self.txt, True, self.couleur)
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (int(self.largeur/2), int(self.hauteur/2))
        self.update()

    def update(self, couleur = (0,0,0)):
        self.sablier()
        self.texte = pygame.font.Font("data/font/" + self.font + ".ttf", int(50*(1+(self.temps-7)*0.1))).render(self.txt, True, self.couleur) #75*self.temps*0.2
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (int(self.largeur/2), int(self.hauteur/2))
        self.dessiner()

    def dessiner(self, couleur = (0,0,0)) :
        self.image.fill((0,0,0,0))         
        self.image.blit(self.texte, self.rectTexte)  
        
    def sablier(self):
        self.temps -= 1
        self.hauteur -= 15
        if self.temps <= 0:
            self.kill()
    
class SortBouton(pygame.sprite.Sprite) :
    """ Création d'un bouton de sort carré """
    def __init__(self, img, x, y, commande, val, joueur, source = '') :
        super().__init__()
        self._commande = commande
        self.val = val
        self.x, self.y = x, y
        if source == '':
            self.image = pygame.image.load('data/images/Classes/'+ joueur.nom_classe + '/sorts/' + img + '.png').convert_alpha()
        else:
            self.image = pygame.image.load(source + img + '.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.dessiner()
 
    def dessiner(self, couleur = (0,0,0)) :
        self.image.blit(self.image, self.rect)
 
    def executerCommande(self) :
        # Appel de la commande du bouton
        self._commande(self.val)
 
class SurfaceRec(pygame.sprite.Sprite):
    def __init__(self, couleur, x, y, largeur, hauteur):
        super().__init__()
        self.couleur = couleur
        self.image = pygame.Surface((largeur, hauteur))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.dessiner()
        
    def dessiner(self, val = 0):
        self.image.fill(self.couleur)
        self.image.blit(self.image, self.rect)
        
class ImageRec(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.dessiner()
        
    def dessiner(self, val = 0):
        self.image.blit(self.image, self.rect)
 
    
class InfoBulleSort(pygame.sprite.Sprite):
    """ Création d'une info bulle de sort """
    def __init__(self, joueur, sort, groupeInfoBulleSort) :
        super().__init__()
        # Fond #
        fond = SurfaceRec((100,100,100,150), 1070, 580, 400, 150)
        groupeInfoBulleSort.add(fond)
        # Icon sort #
        image = pygame.image.load('data/images/Classes/'+ joueur.nom_classe + '/sorts/' + 's' + str(sort.num+1) + '.png').convert_alpha()
        image = pygame.transform.smoothscale(image, (50, 50))
        img = ImageRec(image, 1240,535)
        groupeInfoBulleSort.add(img)
        
        if sort.po_modifiable :
            image = pygame.image.load('data/images/Texture/carac/icon_po_modif.png').convert_alpha()
            img = ImageRec(image, 1225,575)
            groupeInfoBulleSort.add(img)
        
        if not sort.ldv :
            image = pygame.image.load('data/images/Texture/carac/icon_no_ldv.png').convert_alpha()
            img = ImageRec(image, 1253,575)
            groupeInfoBulleSort.add(img)
        
        po = sort.po + sort.somme_boost('po')
        if sort.po_modifiable:
            po += joueur.somme_boost('po')
            
        if sort.po_min != 0 and sort.po_min != po or sort.po_min < sort.po:
            txt_po = 'PO : {} - {} '.format(sort.po_min, po)
        else:
            txt_po = 'PO : {} '.format(po)
        if sort.zone_tire != 'cercle':
            if sort.zone_tire == 'croix':
                txt_po += '(lancer en ligne)'
            else:
                txt_po += '(lancer en {})'.format(sort.zone_tire)
           
        txt_dg = ''
        boost = sort.somme_boost('dg')
        dg = (sort.dg_min + boost, sort.dg_max + boost)
        if dg[0] > 0:
            txt_dg = 'Dg : {} - {} {}'.format(dg[0], dg[1], sort.type_sort)
    
        txt_lpt = 'Nb lancers par tour : {}/{}'.format(sort.coup_par_tour, sort.coup_par_tour_max)
        if sort.coup_par_tour_max >= 100:
            txt_lpt = 'Nb lancers par tour : ∞' 
            
        txt_des = 'Description : ' + sort.effet_str
        txt_des2 = ''
        txt_des3 = ''
        if len(txt_des) > 48:
            nb = 48
            while txt_des[nb] != ' ':
                nb-=1
            txt_des2 = txt_des[nb:]
            txt_des = txt_des[:nb]
        if len(txt_des2) > 48:
            nb = 48
            while txt_des2[nb] != ' ':
                nb-=1
            txt_des3 = txt_des2[nb:]
            txt_des2 = txt_des2[:nb]
        
        font = 'futurah'   
        x = 880
        y = 520
        dico_touches = ['&','é','"',"'",'(','-','è','_','ç','à','a','z','e','r','t','y','u','i','o','p']
        textes = [
            ('{} ({})'.format(sort.nom, dico_touches[sort.num]), font, (x,y), (300,30), (255,255,255), 0),
            ('PA : {}'.format(sort.cout), font, (x,y+15), (300,30), (255,255,255), 0),
            (txt_po, font, (x,y+30), (300,30), (255,255,255), 0),
            (txt_dg, font, (x,y+45), (300,30), (255,255,255), 0),
            (txt_lpt, font, (x,y+60), (300,30), (255,255,255), 0),
            ('Intervalle de relance : {}/{}'.format(sort.latence_max-sort.latence, sort.latence_max), font, (x,y+75), (300,30), (255,255,255), 0),
            (txt_des, font, (x,y+90), (400,30), (255,255,255), 0),
            (txt_des2, font, (x,y+105), (400,30), (255,255,255), 0),
            (txt_des3, font, (x,y+120), (400,30), (255,255,255), 0),
            ]
         
        for texte, font, (x,y), taille, couleur, opacite in textes :
            mt = TexteVariable(texte, (255,255,255), font, x, y, 5, taille[1], opacite=opacite, isCentered = False)
            groupeInfoBulleSort.add(mt)
            mt.update()
        self.kill()      
        
class InfoBullePerso(pygame.sprite.Sprite):
    """ Création d'une info bulle de perso """
    def __init__(self, x, y, groupePersoCbt, groupeGlobal, groupeInfoBullePerso, sort, joueur, M, joueurs_zone = []) :
        super().__init__()
        
        cible = None
        for perso in groupePersoCbt:
            if perso.pos == (x,y):
                cible = perso
        
        if cible != None:
            joueurs_zone.append(cible)
        
        (X,Y) = IsoToCano(x,y)   
        
        
        if sort != None:    
            '''
            for perso in joueurs_zone:
                if sort.type_cibles in ['ennemis']:
                    if perso.team == joueur.team:
                        joueurs_zone.remove(perso)
                if sort.type_cibles in ['alliés', 'alliés sans moi']:
                    if perso.team != joueur.team:
                        joueurs_zone.remove(perso)
                if sort.type_cibles in ['mes invocs', 'mes invocs et moi']:
                    if perso.parent != joueur:
                        joueurs_zone.remove(perso)
                
                if sort.type_cibles in ['invocs']:
                    if not perso.isInvoc:
                        joueurs_zone.remove(perso)
                        
            if sort.type_cibles in ['alliés sans moi', 'tout sans moi', 'mes invocs']:
                if joueur in joueurs_zone:
                    joueurs_zone.remove(joueur)'''
                    
                        
            sum_pui = joueur.somme_boost('pui')
            sum_dmg = joueur.somme_boost('dmg')
            sum_res = [perso.somme_boost('res') for perso in joueurs_zone]
        
            boubou = [str(perso.somme_boost('shield')) for perso in joueurs_zone]
            txt_boubou = ['' for perso in joueurs_zone]
            for i in range(len(boubou)):
                if boubou[i] != '0':
                    txt_boubou[i] = '+' + boubou[i]
            
            if txt_boubou == []:
                txt_boubou = ['']
            
    
            # Puissance négative correspond à puissance nulle #
            if sum_pui < 0:
                sum_pui = 0
            # On ajoute les redéuctions dûes à la distance #
            if sort.reduct_dist:
                reduction_distance = 0.1
            else:
                reduction_distance = 0
                
            
            dg_max = [int((1 - reduction_distance*distance((x,y),joueurs_zone[i].pos))*(1 + (sum_pui/100))*(1 - (sum_res[i]/100))* (sort.dg_max + sort.somme_boost('dg'))) + sum_dmg for i in range(len(joueurs_zone))]
            dg_min = [int((1 - reduction_distance*distance((x,y),joueurs_zone[i].pos))*(1 + (sum_pui/100))*(1 - (sum_res[i]/100))* (sort.dg_min + sort.somme_boost('dg'))) + sum_dmg for i in range(len(joueurs_zone))]
            if sort.poussee > 0:
                for i in range(len(joueurs_zone)):
                    perso = joueurs_zone[i]
                    dg_poussee = bf.dg_de_poussee(sort.poussee, joueur, perso, (x,y), M, sort, groupePersoCbt)
                    dg_max[i] += dg_poussee
                    dg_min[i] += dg_poussee
                
            text = [joueurs_zone[i].pseudo + ' (' + str(joueurs_zone[i].pv) + txt_boubou[i] + ')'+'|' +'(' + str(dg_min[i]) + ' - ' + str(dg_max[i]) + ')' for i in range(len(joueurs_zone))]
            for i in range(len(dg_max)):
                if dg_max[i] <= 0:
                    text[i] = joueurs_zone[i].pseudo + ' (' + str(joueurs_zone[i].pv) + txt_boubou[i] + ')'
        else:
            if cible != None:
            
                boubou_cible = str(cible.somme_boost('shield'))
                txt_boubou = ['']
                if boubou_cible != '0':
                        txt_boubou[-1] = '+' + boubou_cible
                text = [cible.pseudo + ' (' + str(cible.pv) + txt_boubou[-1] + ')']
        
        font = 'futurah'
        if cible != None:
                    
            x = 710
            y = 668
            
            image = pygame.image.load('data/images/Texture/infobulle_perso.png').convert_alpha()
            fond = ImageRec(image, x+200, y+50)
            groupeInfoBullePerso.add(fond)
            image_cible = pygame.transform.smoothscale(cible.image, (100, 100))
            img = ImageRec(image_cible, x+370,y+60)
            groupeInfoBullePerso.add(img)  
            
            
            
            y = 660
            
            images = ['icon_pv', 'icon_pa', 'icon_pm', 'icon_pui', 'icon_shield', 'icon_damage', 'icon_escape', 'icon_tackle']
            for i in range(len(images)):
                image = pygame.image.load('data/images/Texture/carac/'+images[i]+'.png').convert_alpha()
                if i < 4:
                    image = ImageRec(image, x+6, y + 30 + i*25)
                else:
                    image = ImageRec(image, x+183, y + 30 + (i-4)*25)
                groupeInfoBullePerso.add(image)
                  
            x = 730
            dx = 180
            textes = [
                (cible.pseudo + " - Niv."+str(cible.niveau), font, (x-30,y-3), (200,37), (255,255,255), 0, False),
                ("PV : " + str(cible.pv) + txt_boubou[-1] + '/' + str(cible.pv_max), font, (x,y+30), (200,30), (255,255,255), 0, False),
                ("PA : " + str(cible.pa + cible.somme_boost('pa')), font, (x,y+55), (200,30), (255,255,255), 0, False),
                ("PM : " + str(cible.pm + cible.somme_boost('pm')), font, (x,y+80), (200,30), (255,255,255), 0, False),
                ("Pui : " + str(cible.somme_boost('pui')), font, (x,y+105), (200,30), (255,255,255), 0, False),
                ("Res : " + str(cible.somme_boost('res')) + '%', font, (x+dx,y+30), (200,30), (255,255,255), 0, False),
                ("Dmg : " + str(cible.somme_boost('dmg')), font, (x+dx,y+55), (200,30), (255,255,255), 0, False),
                ("Fuite : " + str(cible.fuite + cible.somme_boost('fuite')), font, (x+dx,y+80), (200,30), (255,255,255), 0, False),
                ("Tacle : " + str(cible.tacle + cible.somme_boost('tacle')), font, (x+dx,y+105), (200,30), (255,255,255), 0, False),
                ]
        else:
            textes = []
        
        if joueurs_zone != []:
            for i in range(len(joueurs_zone)):
                textes.append((text[i], font, (X+32,Y-32-i*29), (5,35), (255,255,255), 100, True))
        else:
            if text != []:
                textes.append((text[0], font, (X+32,Y-32), (5,35), (255,255,255), 100, True))
        
        for texte, font, (x,y), taille, couleur, opacite, boole in textes :
            mt = TexteVariable(texte, couleur, font, x, y, 2, taille[1], opacite=opacite, isCentered = boole)
            groupeInfoBullePerso.add(mt)
            mt.update()
        self.kill()
                 
class ChatTextuel(pygame.sprite.Sprite):
    """ Création du Chat textuel """
    def __init__(self, groupeChatTextuel) :
        super().__init__()
        self.n = 7
        self.decalage = 0
        self.L = ['' for i in range(self.n-2)] # Liste des affichandes #
        self.L.append('                         Bienvenu sur Sufdo ' + 'v.1.4.0')
        self.L.append('')
        self.groupeChatTextuel = groupeChatTextuel
        self.cursor= SurfaceRec((220,180,5,255), 510, 756, 14, 10)
        self.groupeChatTextuel.add(self.cursor)
        
    def ajout(self, elem):
        nb = 60
        if len(elem) > nb:
            while elem[nb] != ' ':
                nb -= 1
            self.L.append(elem[:nb])
            self.L.append(elem[nb:])
        else:
            self.L.append(elem)
    
    def up(self, val = 0):
        if not (self.decalage + self.n >= len(self.L) - 1): 
            self.decalage += 1
            self.update()
    
    def down(self, val = 0):
        if self.decalage > 0:
            self.decalage -= 1
            self.update()
    
    def update(self):
        self.groupeChatTextuel.empty()
        self.cursor= SurfaceRec((220,180,5,255), 510, 766 - (80*self.decalage/len(self.L)), 14, 10)
        self.groupeChatTextuel.add(self.cursor)
        
        nb_ligne_max = 100
        if len(self.L) >= nb_ligne_max: #Nb max 
            self.L = self.L[len(self.L)-nb_ligne_max:]
        font = 'futurah'   
        x = 20
        y = 665
        textes = []
        for i in range(self.n + self.decalage):
            if y+15*(self.n+ self.decalage-i) < 770:
                textes.append((self.L[-i], font, (x,y+15*(self.n + self.decalage-i)),(400,30),(255,255,255)))
         
        for texte, font, (x,y), taille, couleur in textes :
            mt = TexteVariable(texte, (255,255,255), font, x, y, 5, taille[1], isCentered = False)
            self.groupeChatTextuel.add(mt)
            mt.update()
        
     