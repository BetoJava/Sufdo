# Import ---------- #
import pygame

import data.scripts.personnages as p
import data.scripts.functions as f
import data.scripts.battle_functions as bf
import data.scripts.pathfinding as pf
import data.scripts.mapiso as mi
import data.scripts.ia as ia

import data.scripts.Classes.chat as _chat_
import data.scripts.Classes.dragon as _dragon_
import data.scripts.Classes.cerf as _cerf_
import data.scripts.Classes.poulpe as _poulpe_
import data.scripts.Classes.justicier as _justicier_
import data.scripts.Classes.protecteur as _protecteur_
import data.scripts.Classes.epee as _epee_
import data.scripts.Classes.invocateur as _invocateur_
import data.scripts.Monstres.monstre_corrompu as _mob_corrompu_
import data.scripts.Monstres.bouftou_royal as _bouftou_royal_
import data.scripts.Classes.Chtulu as _chtulu_
import data.scripts.Classes.Gigolo as _gigolo_


# Système --------------------------------------------------------- #



class Menu :
    """ Création et gestion des boutons d'un menu """
    def __init__(self, *groupes) :
        self.couleurs = dict(
            noir = (0,0,0),
            gris_foncé = (50,50,50),
            blanc = (255,255,255),
            vert = (0,255,0),
            bleu = (0,0,200),
            rouge = (200,0,0),
            orange = (255,174,0),
            gold = (255,215,0),
            bleuc = (43,133,167),
            rougepm = (160,87,47),
            vertpasser = (47,136,55)
        )
        self.couleurs_button = dict(
                gris_foncé = 'b',
                blanc = 'bv',
                vert = 'bv',
                bleu = 'b',
                rouge = 'r',
                orange = 'r',
                gold = 'r',
                bleuc = 'bv',
                rougepm = 'r',
                vertpasser = 'bv'
            )
        self.bs_collide = None
        self.name = ''
        self.isWritting = False
        
        
 
    def update(self, events, app, groupeSortsBouton, groupeInfoBulleSort, groupeSurfaceSort, groupeBoutonImage) : 
        clicGaucheup = app.clicGaucheup
        clicGauchedown = app.clicGauchedown
        posPointeur = pygame.mouse.get_pos()
        groupeSurfaceSort.empty()
        
        for bi in groupeBoutonImage:
            if bi.rect.collidepoint(*posPointeur) :
                if clicGaucheup :
                    pygame.time.wait(45)
                    bi.executerCommande()
                break
            else :
                bi.dessiner()
        
        if self.bs_collide != None:
            if not self.bs_collide.rect.collidepoint(*posPointeur):
                groupeInfoBulleSort.empty()
                self.bs_collide = None
         
        else:    
            for bs in groupeSortsBouton:
                if bs.rect.collidepoint(*posPointeur) :
                    self.bs_collide = bs
                    f.InfoBulleSort(app.joueur, app.joueur.S[bs.val], groupeInfoBulleSort)  
                    
        for bs in groupeSortsBouton:
            if bs.rect.collidepoint(*posPointeur) :
                bs.dessiner(self.couleurs['rouge'])
                
                # Si le clic gauche a été pressé
                if clicGaucheup :
                # Appel de la fonction du bouton
                    pygame.time.wait(45)
                    bs.executerCommande()
                break
            else :
                # Le pointeur n'est pas au-dessus du bouton
                bs.dessiner()
        for bs in groupeSortsBouton:
            sort = app.joueur.S[bs.val]
            cout = sort.cout
            if sort.latence > 0 or sort.coup_par_tour <= 0 or cout > app.joueur.pa + app.joueur.somme_boost('pa'):
                dx = sort.num%10*40
                dy = sort.num//10*40
                ms = f.SurfaceRec((0,0,0,100),730+dx,710+dy,40,40)
                groupeSurfaceSort.add(ms)
                    
        for bouton in self._boutons :
            # Si le pointeur souris est au-dessus d'un bouton
            if bouton.rect.collidepoint(*posPointeur) :
                
                # Changement de la couleur du bouton
                if bouton.isStyle:
                    bouton.isOver = True
                    bouton.dessiner()
                else:
                    bouton.dessiner(self.couleurs['rouge'])
                # Si le clic gauche a été pressé
                if clicGaucheup :
                    # Appel de la fonction du bouton
                    pygame.time.wait(45)
                    bouton.executerCommande()
                break
            else :
                # Le pointeur n'est pas au-dessus du bouton
                if bouton.isStyle:
                    bouton.isOver = False
                    bouton.dessiner()
                else:
                    bouton.dessiner(bouton.couleur)
        else :
            # Le pointeur n'est pas au-dessus d'un des boutons
            pass
 
 
# Menu principal # 
class Menu1(Menu):
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        
        mt = f.Texte('- SufDo -', self.couleurs['blanc'], 'Achafexp', 640, 125, 1000, 500)

        application.groupeTxt.add(mt)
        application.groupeGlobal.add(mt)
        
        # noms des menus et commandes associées
        items = (
            ('Play', 'styleb', (640,400), (300,180), 'bv', application.menuPerso, 1),
            ('Quitter', 'styleb', (640,650), (300,120), 'r', application.quitter, 0)
        )
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBoutonStyle(texte, couleur, font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)
            application.groupeGlobal.add(mb)
  
    
class ChoixPerso():
    def __init__(self):
        self.dico_perso = {'Chat' : 0, 'Cerf' : 1, 'Dragon' : 2, 'Justicier' : 3, 'Poulpe' : 4, 'Monstre Corrompu' : 5, 'Protecteur' : 6, 'Épée' : 7, 'Invocateur' : 8, 'Chtulu' : 9,  'Gigolo' : 10}
        self.dico_perso_inv = {0 : 'Chat', 1 : 'Cerf', 2 : 'Dragon', 3 : 'Justicier', 4 : 'Poulpe', 5 : 'Monstre Corrompu', 6 : 'Protecteur', 7 : 'Épée', 8 : 'Invocateur', 9 : 'Chtulu', 10 : 'Gigolo'}
        self.team1 = [0 for i in range(len(self.dico_perso_inv))]
        self.team2 = [0 for i in range(len(self.dico_perso_inv))]
        self.team = [self.team1, self.team2]
    def teams_not_empty(self):
        S = [0, 0]
        for i in self.team1:
            S[0] += i
        for i in self.team2:
            S[1] += i
        if S[0] > 0 and S[1] > 0:
            return True
        else:
            return False
            
# Choix classes #
class MenuTeam(Menu): 
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        self.name = 'Menu Team'
        self._fenetre = application.fenetre
        textes_variables = []
        
        dico_perso2 = {0 : 'Chat', 1 : 'Cerf', 2 : 'Dragon', 3 : 'Justicier', 4 : 'Poulpe', 5 : 'Monstre Corrompu', 6 : 'Protecteur', 7 : 'Épée', 8 : 'Invocateur', 9 : 'Chtulu', 10 : 'Gigolo'}

        for i in range(len(application.choixPerso.team1)):
            textes_variables.append((dico_perso2[i] + ' x' + str(application.choixPerso.team1[i]), 'futurah', (250,100+30*i), (250,40), 'blanc', i, True))
        for i in range(len(application.choixPerso.team2)):
            textes_variables.append((dico_perso2[i] + ' x' + str(application.choixPerso.team2[i]), 'futurah', (1030,100+30*i), (250,40), 'blanc', i+len(application.choixPerso.team1), True))
            
        for texte, font, (x,y), taille, couleur, num, boole in textes_variables :
            mtv = f.TexteVariable(texte, self.couleurs[couleur], font, x, y, 5, taille[1], num, boole)
       
            application.groupeTxtVariableJoueur.add(mtv)
            application.groupeGlobal.add(mtv)
        
        txts = (
            ('- Team 1 -', 'impact', (250,60), (200,100), 'blanc'), 
            ('- Team 2 -', 'impact', (1030,60), (200,100), 'blanc')
        )
                

        for texte, font, (x,y), taille, couleur in txts :
            mt = f.Texte(texte, self.couleurs[couleur], font, x, y, taille[0], taille[1])

            application.groupeTxt.add(mt)
            application.groupeGlobal.add(mt)
        
        # noms des menus et commandes associées
        items = (
            ('Chat', 'impact', (80,450), (100,50), 'bleu', application.ajout_perso, (1,0)),
            ('Cerf', 'impact', (190,450), (100,50), 'bleu', application.ajout_perso, (2,0)),
            ('Dragon', 'impact', (300,450), (100,50), 'bleu', application.ajout_perso, (3,0)),
            ('Justicier', 'impact', (410,450), (100,50), 'gris_foncé', application.ajout_perso, (4,0)),
            ('Poulpe', 'impact', (80,510), (100,50), 'bleu', application.ajout_perso, (5,0)),
            ('Monstre', 'impact', (190,510), (100,50), 'bleu', application.ajout_perso, (6,0)),
            ('Crapeau', 'impact', (300,510), (100,50), 'gris_foncé', application.ajout_perso, (7,0)),
            ('Chat', 'impact', (870,450), (100,50), 'bleu', application.ajout_perso, (1,1)),
            ('Cerf', 'impact', (980,450), (100,50), 'bleu', application.ajout_perso, (2,1)),
            ('Dragon', 'impact', (1090,450), (100,50), 'bleu', application.ajout_perso, (3,1)),
            ('Justicier', 'impact', (1200,450), (100,50), 'gris_foncé', application.ajout_perso, (4,1)),
            ('Poulpe', 'impact', (870,510), (100,50), 'bleu', application.ajout_perso, (5,1)),
            ('Monstre', 'impact', (980,510), (100,50), 'bleu', application.ajout_perso, (6,1)),
            ('Crapeau', 'impact', (1090,510), (100,50), 'gris_foncé', application.ajout_perso, (7,1)),
            ('Quit', 'styleb', (1180,740), (100,80), 'orange', application.quitter, 0),  
            ('Retour', 'styleb', (1180,650), (200,80), 'orange', application.retour, 1),
            ('Prêt', 'styleb', (640,700), (200,150), 'vertpasser', application.menu3, 0)
        )
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBoutonStyle(texte, self.couleurs_button[couleur], font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)
            application.groupeGlobal.add(mb)

class MenuPerso(Menu): 
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        self._fenetre = application.fenetre
        val = application.choixT - 1
        txts = (
                ('- Team {} -'.format(val+1), 'impact', (640,60), (200,100), 'blanc'), 
                )
                
        for texte, font, (x,y), taille, couleur in txts :
            mt = f.Texte(texte, self.couleurs[couleur], font, x, y, taille[0], taille[1])

            application.groupeTxt.add(mt)
            application.groupeGlobal.add(mt)
        
        Pseudo = [perso.pseudo for perso in application.J]
        Perso = []
        dico_perso = {'Chat':0, 'Cerf':1, 'Dragon':2, 'Justicier':3, 'Poulpe':4, 'Monstre Corrompu':5, 'Protecteur':6, 'Epée':7, 'Invocateur':8,'Chtulu':9, 'Gigolo':10}
        for pseudo in application.liste_pseudo:        
            fichier = open('data/save/joueurs/'+pseudo+'.txt','r', encoding='utf-8')
            C = fichier.readlines()
            if C!= []:
                if pseudo not in Pseudo:
                    Perso.append([pseudo, dico_perso[C[3][:-1]], int(C[1][:-1])]) # Pseudo et nom_classe #
            fichier.close()
        
        
        items = []
        xi = 110
        yi = 150
        for i in range(len(Perso)):
            txt = Perso[i][0]+' Niv.'+str(Perso[i][2])
            if xi >= 1200:
                xi = 110
                yi += 60
            items.append((txt,'impact', (xi,yi), (200,50), 'bleu', application.ajout_perso, (Perso[i][1],val,Perso[i][0])))
            xi = xi + 200 + 10
        if xi >= 1200:
            xi = 110
            yi += 60
        items.append(('+','impact', (xi,yi), (200,50), 'bleu', application.new_perso, val))
            
        
        items.append(('Quit', 'styleb', (1180,740), (200,80), 'orange', application.quitter, 0))
        items.append(('Retour', 'styleb', (1180,650), (200,80), 'orange', application.retour, 1))
        if application.choixT == 1:
            items.append(('Suivant', 'styleb', (640,700), (400,150), 'vertpasser', application.menuPerso, 2))
        else:
            items.append(('Prêt', 'styleb', (640,700), (250,150), 'vertpasser', application.menu3, 1))
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBoutonStyle(texte, self.couleurs_button[couleur], font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)
            application.groupeGlobal.add(mb)

class NewPerso(Menu):
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        self.name = 'New Perso'
        self.isWritting = True
        self._fenetre = application.fenetre
        self.classe = 0
        self.team = application.choixT
        self.pseudo = ''
        self.majuscule = False
        
        
        fond_titre1 = f.SurfaceRec((51,52,46,255), 640, 60, 410, 110)
        application.groupeSurface.add(fond_titre1)   
        fond_titre2 = f.SurfaceRec((61,62,56,255), 640, 60, 390, 90)
        application.groupeSurface.add(fond_titre2)  
     
        txts = (
                ('- Nouveau Perso -', 'impact', (640,60), (400,100), 'blanc'), 
                )
            
        for texte, font, (x,y), taille, couleur in txts :
            mt = f.Texte(texte, self.couleurs[couleur], font, x, y, taille[0], taille[1])
   
            application.groupeTxt.add(mt)
            application.groupeGlobal.add(mt)         
          
        textes_variables = []
        
        self.dico_perso = {0 : 'Chat', 1 : 'Cerf', 2 : 'Dragon', 3 : 'Justicier', 4 : 'Poulpe', 5 : 'Monstre Corrompu', 6 : 'Protecteur', 7 : 'Épée', 8 : 'Invocateur', 9 : 'Chtulu', 10 : 'Gigolo'}
        textes_variables.append(('Pseudo : ' + self.pseudo, 'futurah', (150,150), 50, 'blanc'))
        textes_variables.append(('Classe : ' + self.dico_perso[self.classe], 'futurah', (150,250), 50, 'blanc'))
        
        self._tv = []
        for texte, font, (x,y), taille, couleur in textes_variables :
            mtv = f.TexteVariable(texte, self.couleurs[couleur], font, x, y, 5, taille, opacite = 255, isCentered = False)
       
            self._tv.append(mtv)
            application.groupeTxtVariable.add(mtv)
            application.groupeGlobal.add(mtv)
            
        items = [
            ('Chat', 'impact', (80,450), (100,50), 'bleu', self.changement_classe, 0),
            ('Cerf', 'impact', (190,450), (100,50), 'bleu', self.changement_classe, 1),
            ('Dragon', 'impact', (300,450), (100,50), 'bleu', self.changement_classe, 2),
            ('Justicier', 'impact', (410,450), (100,50), 'gris_foncé', self.changement_classe, 3),
            ('Poulpe', 'impact', (520,450), (100,50), 'bleu', self.changement_classe, 4),
            ('Monstre', 'impact', (630,450), (100,50), 'bleu', self.changement_classe, 5),
            ('Protecteur', 'impact', (745,450), (110,50), 'gris_foncé', self.changement_classe, 6),
            ('Épée', 'impact', (855,450), (100,50), 'gris_foncé', self.changement_classe, 7),
            ('Invocateur', 'impact', (960,450), (110,50), 'gris_foncé', self.changement_classe, 8),
            ('Chtulu', 'impact', (1085,450), (130,50), 'gris_foncé', self.changement_classe, 9),
            ('Gigolo', 'impact', (80,550), (130,50), 'bleu', self.changement_classe, 10),
            ('Quit', 'styleb', (1180,740), (200,80), 'orange', application.quitter, 0),  
            ('Retour', 'styleb', (1180,650), (200,80), 'orange', application.retour, 1),
            ('Créer', 'styleb', (640,700), (300,150), 'vertpasser', self.creer, application)
        ]
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBoutonStyle(texte, self.couleurs_button[couleur], font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)
            application.groupeGlobal.add(mb)
            
    def changement_classe(self, val):
        self.classe = val
        self._tv[1].maj('Classe : ' + self.dico_perso[val])
        
    def ajout_nom(self, ajout):
        if ajout == 'backspace' and len(self.pseudo) > 0:
            self.pseudo = self.pseudo[:-1]
        elif ajout in [str(i) for i in range (10)]:
            pass
        elif ajout == 'caps lock':
            if self.majuscule:
                self.majuscule = False
            else:
                self.majuscule = True
        elif ajout in [chr(i) for i in range(97,123)]:
            if self.majuscule:
                self.pseudo += ajout.upper()
            else:
                self.pseudo += ajout
            
        self._tv[0].maj('Pseudo : ' + self.pseudo)
    
    def creer(self, application):
        application.ajout_perso((self.classe, self.team - 1, self.pseudo), True)
        application.menuPerso(self.team)
                   
                              
# Choix Map --- #
class Menu3(Menu): 
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        self._fenetre = application.fenetre
        # noms des menus et commandes associées
        items = [
            ('Charger', 'impact', (320,400), (300,100), 'bleu', application.menu_load, 0),
            ('Dj Squelette', 'impact', (640,400), (300,100), 'bleu', application.choix_pos, 1),
            ('Map aléatoire', 'impact', (960,400), (300,100), 'bleu', application.choix_pos, 2),    
            ('Retour', 'styleb', (1180,140), (200,80), 'orange', application.retour, 2),
            ('Quit', 'styleb', (1180,50), (200,80), 'orange', application.quitter, 0)
        ]
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBoutonStyle(texte, self.couleurs_button[couleur], font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)   
            application.groupeGlobal.add(mb)

class MenuLoad(Menu):
    def __init__(self, app, M, *groupes):
        Menu.__init__(self, *groupes)
        self._fenetre = app.fenetre
        self.myMap = app.myMap
        self.isWritting = True
        self.majuscule = False
        self.name = 'load'
        
        fond_titre1 = f.SurfaceRec((51,52,46,255), 640, 60, 410, 110)
        app.groupeSurface.add(fond_titre1)   
        app.groupeGlobal.add(fond_titre1)   
        fond_titre2 = f.SurfaceRec((61,62,56,255), 640, 60, 390, 90)
        app.groupeSurface.add(fond_titre2)  
        app.groupeGlobal.add(fond_titre2)    
        
     
        txts = (
                ('- Charger Map -', 'impact', (640,60), (400,100), (255,255,255)), 
                )
            
        for texte, font, (x,y), taille, couleur in txts :
            mt = f.Texte(texte, couleur, font, x, y, taille[0], taille[1])
   
            app.groupeTxt.add(mt)
            app.groupeGlobal.add(mt)         
          
        textes_variables = []
        
        textes_variables.append(('Nom : ' + self.myMap.name, 'futurah', (150,150), 50, (255,255,255)))
        
        self._tv = []
        for texte, font, (x,y), taille, couleur in textes_variables :
            mtv = f.TexteVariable(texte, couleur, font, x, y, 5, taille, opacite = 255, isCentered = False)
       
            self._tv.append(mtv)
            app.groupeTxtVariable.add(mtv)
            app.groupeGlobal.add(mtv)
            
        items = [
            ('Quit', 'styleb', (1180,740), (200,80), 'r', app.quitter, 0),       
            ('Retour', 'styleb', (1180,650), (200,80), 'r', app.retour, 1),
            ('Charger', 'styleb', (640,700), (300,150), 'bv', app.load_map, self.myMap.name)
        ]
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBoutonStyle(texte, couleur, font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            app.groupeMenuBouton.add(mb)
            app.groupeGlobal.add(mb)
            
    def ajout_nom(self, ajout):
        if ajout == 'backspace' and len(self.myMap.name) > 0:
            self.myMap.name = self.myMap.name[:-1]
        elif ajout in [str(i) for i in range (10)]:
            pass
        elif ajout == 'caps lock':
            if self.majuscule:
                self.majuscule = False
            else:
                self.majuscule = True
        elif ajout in [chr(i) for i in range(97,123)]+['[1]','[2]','[3]','[4]','[5]','[6]','[7]','[8]','[9]','[0]', 'space']:
            if ajout in ['[1]','[2]','[3]','[4]','[5]','[6]','[7]','[8]','[9]','[0]']:
                self.myMap.name += ajout[1:-1]
            elif ajout == 'space':
                self.myMap.name += ' '
            elif self.majuscule:
                self.myMap.name += ajout.upper()
            else:
                self.myMap.name += ajout
            
        self._tv[0].maj('Nom : ' + self.myMap.name)

# Jeu ------------ #
class Jeu(Menu):
    def __init__(self, application, num_map, joueur, groupePersoCbt, *groupes):
        Menu.__init__(self, *groupes)
        self._fenetre = application.fenetre
        self.num_map = num_map
        
        # MenuBoutons et TexteVariables
        if application.combat_started:
            pass_or_start = 'Passer'
        else:
            pass_or_start = 'Prêt'
        items = (
                ('Timeline', 'styleb', (75,35), (140,45), 'gris_foncé', application.hide_timeline,0),
                ('Quit', 'styleb', (1235,25), (90,35), 'orange', application.retour,1),
                (pass_or_start, 'styleb', (1200,730),(120,40), 'vertpasser', application.passer,0)
                )
        

        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :

            mb = f.MenuBoutonStyle(texte, self.couleurs_button[couleur], font, x, y, taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)   
            application.groupeGlobal.add(mb)
            
        
        image = pygame.image.load('data/images/Texture/barChat.png').convert_alpha()
        img = f.ImageRec(image, 511, 710)
        application.groupeGlobal.add(img)
            
        boutons_image = (
                ('Texture/arrow', (510,679), application.ChatTextuel.up, False, True, 0),
                ('Texture/arrow',  (510,780), application.ChatTextuel.down, False, False, 0),
                )
        
        for image, (x,y), cmd, xbool, ybool, val in boutons_image :

            mb = f.BoutonImage(image, x, y, cmd, val, xbool, ybool)
        
            application.groupeBoutonImage.add(mb)   
            application.groupeGlobal.add(mb)
                
        # Sorts #
        if not application.joueur.isIA and not application.joueur.isStatic:
            x,y = 730,710
            sorts = [('s'+str(i+1), (x+i*40,y), application.sort, i,'') for i in range(10)]
            for i in range(10):
                sorts.append((('s'+str(i+11), (x+i*40,y+40), application.sort, i+10,'')))
          
            sorts = [sorts[i] for i in range(len(joueur.S))]
            
            self._sorts = []
            for nom, (x,y), cmd, val, source in sorts :
                
                msb = f.SortBouton(nom, x, y, cmd, val, joueur, source)
                
                self._sorts.append(msb)
                
                application.groupeSortsBouton.add(msb)
                application.groupeGlobal.add(msb)
        
        # PV/PA/PM #
        x,y = 583, 715
        boubou = str(joueur.somme_boost('shield'))
        if boubou != '0':
            txt_boubou = '+' + boubou
        else:
            txt_boubou = ''
        textes_variables = [
            (txt_boubou, 'futura', (x,y-30), (150,40), 'bleuc', 4),
            (str(joueur.pv), 'futura', (x,y), (300,50), 'blanc', 0),
            (str(int(joueur.pv/joueur.pv_max*100)) +" %", 'futura', (x,y+30), (150,40), 'blanc', 1),
            (str(joueur.pa + joueur.somme_boost('pa')), 'futura', (x+75,y-8), (250,35), 'blanc', 2),
            (str(joueur.pm + joueur.somme_boost('pm')), 'futura', (x+74,y+44), (250,35), 'blanc', 3),
            ]
            
        self._textes = []
        for texte, font, (x,y), taille, couleur, num in textes_variables :

            mtv = f.TexteVariable(texte, self.couleurs[couleur], font, x, y, 5, taille[1], num)
            
            self._textes.append(mtv)
            
            application.groupeTxtVariableJoueur.add(mtv)
            application.groupeGlobal.add(mtv)
        
        txts = []
        # Affichage de la Timeline #
        if not application.timeline_hidden:
            i = 0
            for perso in groupePersoCbt:
                if perso.ordre_ini == 0:
                     colo = 'gold'
                else:
                     colo = 'blanc'
                txts.append((perso.pseudo, 'futurah', (70,55 + 14*(perso.ordre_ini+1)), (200,30), colo))
                i += 1
                
            self.txts = []
            for texte, font, (x,y), taille, couleur in txts :
        
                mt = f.TexteVariable(texte, self.couleurs[couleur], font, x, y, 5, taille[1])
                
                self._textes.append(mt)
                application.timeline.append([mt,texte]) # Pour cacher/montrer la timeline
                
                application.groupeTxtVariable.add(mt)
                application.groupeGlobal.add(mt)
  
# Menu de fin de combat --- #
class FinCbt(Menu): 
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        self._fenetre = application.fenetre
        
        temps = int((application.timer[1]-application.timer[0])//1000)
        h = temps//3600
        m = (temps-h*3600)//60
        s = temps-h*3600-m*60
        
        gagnant, perdant, nb_exp, tours = bf.fin_de_combat(application.groupePersoCbt, application.groupeGlobalPerso)    
        
        # Fond #
        fond2 = f.SurfaceRec((33,34,29,255), 640, 150, 900, 50)
        fond3 = f.SurfaceRec((41,42,36,255), 640, 200, 900, 50)
        
        if len(gagnant)<= 13:
            fond4 = f.SurfaceRec((41,42,36,255), 640, 250+len(gagnant)*30, 900, 50)
            application.groupeSurface.add(fond4)
        
        
        application.groupeSurface.add(fond3)
        application.groupeSurface.add(fond2)
        
        # Persos #
        textes_variables = []
        for i in range(len(gagnant)):
            perso = gagnant[i]
            
            textes_variables.append((perso.pseudo, 'futura', (220,240+30*i), (5,30), 'blanc', False))
            textes_variables.append(('Niv.' + str(perso.niveau), 'futura', (400,240+30*i), (5,30), 'blanc', False))
            textes_variables.append(('Exp : ' + str(nb_exp) + '   |   ' + str(perso.exp) + '/' + str(perso.exp_next_niv), 'futura', (500,240+30*i), (5,30), 'blanc', False))
            
            if i%2 == 0:
                fond = f.SurfaceRec((61,62,56,255), 640, 240+30*i, 900, 30)
                application.groupeSurface.add(fond)
            else:
                fond = f.SurfaceRec((51,52,46,255), 640, 240+30*i, 900, 30)
                application.groupeSurface.add(fond)
            
            image_cible = pygame.transform.smoothscale(perso.image, (100, 100))
            img = f.ImageRec(image_cible, 240+100*i,75)
            application.groupeSurface.add(img)
        
        for i in range(len(perdant)):
            perso = perdant[i]
            
            textes_variables.append((perso.pseudo, 'futura', (220,290+len(gagnant)*30+30*i), (5,30), 'blanc', False))
            textes_variables.append(('Niv.' + str(perso.niveau), 'futura', (400,290+len(gagnant)*30+30*i), (5,30), 'blanc', False))
            
            if i%2 == 0:
                fond = f.SurfaceRec((61,62,56,255), 640, 290+len(gagnant)*30+30*i, 900, 30)
                application.groupeSurface.add(fond)
            else:
                fond = f.SurfaceRec((51,52,46,255), 640, 290+len(gagnant)*30+30*i, 900, 30)
                application.groupeSurface.add(fond)
            
        
        if h//10 > 0:
            txt_h = str(h)
        else:
            txt_h = '0'+str(h)
        if m//10 > 0:
            txt_m = str(m)
        else:
            txt_m = '0'+str(m)
        if s//10 > 0:
            txt_s = str(s)
        else:
            txt_s = '0'+str(s)
            
        txt_temps = txt_h + ':' + txt_m + ':' + txt_s + ' (' + str(tours) + ' tours)' 
        
        
        
        textes_variables.append((txt_temps, 'futura', (220,150), (5,50), 'blanc', False))
        textes_variables.append(('Gagnants :', 'futura', (200,200), (5,35), 'blanc', False))
        textes_variables.append(('Perdants :', 'futura', (200,250+len(gagnant)*30), (5,35), 'blanc', False))
            
       
        for texte, font, (x,y), taille, couleur, boole in textes_variables :

            mtv = f.TexteVariable(texte, self.couleurs[couleur], font, x, y, 5, taille[1], isCentered = boole)

            application.groupeTxtVariable.add(mtv)
            application.groupeGlobal.add(mtv)
        
        items = (
            ('Menu', 'impact', (500,720), (200,100), 'bleu', application.menu1, 0),
            ('Map', 'impact', (780,720), (200,100), 'bleu', application.menu3, 1),
            ('Quit', 'styleb', (1180,40), (180,60), 'orange', application.quitter, 0)
        )
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBoutonStyle(texte, self.couleurs_button[couleur], font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)   
            application.groupeGlobal.add(mb)
        
class Application :
    """ Classe maîtresse gérant les différentes interfaces du jeu """
    def __init__(self, liste_pseudo) :
        self.J = []
        self.choixPerso = ChoixPerso()
        
        self.joueur = None # Joueur dont c'est le tour #
        self.choix_classes = []
        self.choix_map = 0
        self.liste_pseudo = liste_pseudo
        self.tick = 0
        self.clock = pygame.time.Clock()
        self.isStaticDone = False
        self.fps = 60
        self.timer = [0,0]
        self.tour = 0   
        self.choixT = 1
        self.version = 'v.1.5.2'
        
        self.clicGaucheup = False
        self.clicGauchedown = False
            
        pygame.init()
        pygame.display.set_caption('Sufdo '+ self.version)
        self.fenetre = pygame.display.set_mode((1280,790), 0, 32) # pygame.FULLSCREEN, pygame.SCALED, 0, 32
        
        self.myMap = mi.MapIso(self.fenetre)
        self.myMap.combat_started = False
        
        self.icon = pygame.image.load("data/images/icon1.png").convert_alpha()
        pygame.display.set_icon(self.icon)
        self.fond = pygame.image.load("data/images/Menu/fondviergeb.png").convert()
        
        self.jauge_pv_empty = pygame.image.load('data/images/Texture/icon_hp_empty.png').convert_alpha()
        self.jauge_pv_full = pygame.image.load('data/images/Texture/icon_hp_full.png').convert_alpha()
        self.jauge_pv_25 = pygame.image.load('data/images/Texture/icon_hp_25.png').convert_alpha()
        self.jauge_pv_50 = pygame.image.load('data/images/Texture/icon_hp_50.png').convert_alpha()
        self.jauge_pv_75 = pygame.image.load('data/images/Texture/icon_hp_75.png').convert_alpha()
        self.jauge_pv_low = pygame.image.load('data/images/Texture/icon_hp_low.png').convert_alpha()
        self.jauge_pv_not_full = pygame.image.load('data/images/Texture/icon_hp_not_full.png').convert_alpha()
        self.icon_pa = pygame.image.load('data/images/Texture/icon_pa.png').convert_alpha()
        self.icon_pm = pygame.image.load('data/images/Texture/icon_pm.png').convert_alpha()
        
        # Groupe de sprites utilisé pour l'affichage
        self.timeline = []
        self.groupeGlobal = pygame.sprite.Group()
        self.groupeMenuBouton = pygame.sprite.Group()
        self.groupeSortsBouton = pygame.sprite.Group()
        self.groupeBoutonImage = pygame.sprite.Group()
        self.groupeTxtVariableJoueur = pygame.sprite.Group()
        self.groupeTxtVariable = pygame.sprite.Group()
        self.groupeTxt = pygame.sprite.Group()
        self.groupeInfoBullePerso = pygame.sprite.Group()
        self.groupeInfoBulleSort = pygame.sprite.Group()
        self.groupeSurface = pygame.sprite.Group()
        self.groupeSurfaceSort = pygame.sprite.Group()
        # Groupes de perso #
        self.groupeGlobalPerso = pygame.sprite.Group()
        self.groupePersoCbt = pygame.sprite.Group()
        self.groupePersoHorsCbt = pygame.sprite.Group()
        self.groupeChatTextuel = pygame.sprite.Group()
        self.groupeGlyphe = pygame.sprite.Group()
        
        # Chat Textuel #
        self.ChatTextuel = f.ChatTextuel(self.groupeChatTextuel)
        
        self.statut = True
        self.gameOn = False
        self.combat_started = False
        self.timeline_hidden = False
 
    def _initialiser(self) :
        try:
            # Suppression de tous les sprites du groupe
            for perso in self.groupeGlobalPerso:
                perso.app = self
            self.groupeGlobal.empty()
            self.groupeMenuBouton.empty()
            self.groupeSortsBouton.empty()
            self.groupeTxtVariableJoueur.empty()
            self.groupeTxtVariable.empty()
            self.groupeInfoBullePerso.empty()
            self.groupeInfoBulleSort.empty()
            self.groupeSurface.empty()
            self.groupeSurfaceSort.empty()
            self.groupeTxt.empty()
        except AttributeError:
            pass

    def hide_timeline(self, val = 0):
        # Cache/Montre la timeline #
        if self.timeline_hidden:
            self.timeline_hidden = False
            for txt in self.timeline:
                txt[0].maj(txt[1])
        else:
            self.timeline_hidden = True
            for txt in self.timeline:
                txt[0].maj('')
        self.updateJeu()

    def menu1(self, val = 0) :
        # Affichage du menu 1
        self._initialiser()
        self.fond = pygame.image.load("data/images/Menu/fondviergen.png").convert()  
        self.ecran = Menu1(self, self.groupeGlobal)

    def menuPerso(self, val = 1):
        if val == 1:
            self.__init__(self.liste_pseudo)
        self.choixT = val
        self._initialiser()
        self.fond = pygame.image.load("data/images/Menu/fondviergen.png").convert()  
        self.ecran = MenuPerso(self, self.groupeGlobal)       
        
    def menu2(self, val = 0):
        self._initialiser()
        self.__init__(self.liste_pseudo)
        self.fond = pygame.image.load("data/images/Menu/fondvierge.png").convert()
        self.ecran = MenuTeam(self, self.groupeGlobal)
    
    def new_perso(self, val = 0):
        self._initialiser()
        self.fond = pygame.image.load("data/images/Menu/fondviergen.png").convert()  
        self.ecran = NewPerso(self, self.groupeGlobal)   
        
    def ajout_perso(self, couple, new = False):
        (num_perso, num_team, pseudo) = couple
        
        if len(self.J) < 20:
            self.choixPerso.team[num_team][num_perso] += 1
            self.choix_classe(num_perso, num_team, pseudo, new)   
    
    def choix_classe(self, num_classe, num_team, pseudo, new):       
        self.choix_classes.append(num_classe)
          
        dico_perso = {0 : 'Chat', 1 : 'Cerf', 2 : 'Dragon', 3 : 'Justicier', 4 : 'Poulpe', 5 : 'Monstre Corrompu', 6 : 'Protecteur', 7 : 'Épée', 8 : 'Invocateur', 9 : 'Chtulu', 10 : 'Gigolo'}
        
        if not new:
            if self.choix_classes[-1] == 0:
                perso = _chat_.Chat(pseudo)
            elif self.choix_classes[-1] == 1:
                perso = _cerf_.Cerf(pseudo)
            elif self.choix_classes[-1] == 2:
                perso = _dragon_.Dragon(pseudo)
            elif self.choix_classes[-1] == 3:
                perso = _justicier_.Justicier(pseudo)
            elif self.choix_classes[-1] == 4:
                perso = _poulpe_.Poulpe(pseudo)
            elif self.choix_classes[-1] == 5:
                perso = _mob_corrompu_.MonstreCorrompu(pseudo)
            elif self.choix_classes[-1] == 6:
                perso = _protecteur_.Protecteur(pseudo)
            elif self.choix_classes[-1] == 7:
                perso = _epee_.Epee(pseudo)
            elif self.choix_classes[-1] == 8:
                perso = _invocateur_.Invocateur(pseudo)
            elif self.choix_classes[-1] == 9:
                perso = _chtulu_.Chtulu(pseudo)
            elif self.choix_classes[-1] == 10:
                perso = _gigolo_.Gigolo(pseudo)
            else:
                perso = None
            
            self.J.append(perso)
            perso.team = num_team + 1
            self.groupeGlobalPerso.add(perso)
            self.groupePersoCbt.add(perso)
            self.J[-1].id = len(self.J)-1     # l'id du joueur est sa position dans la liste J
        
        # On vérifie si le joueur a déjà été créé #
        fichier = open('data/save/joueurs/'+pseudo+'.txt','a', encoding='utf-8')
        fichier.close()
          
        fichier = open('data/save/joueurs/'+pseudo+'.txt','r', encoding='utf-8')
        C = fichier.readlines()
        if C!= []:
            perso.niveau = int(C[1][:-1])
            perso.exp = int(C[2][:-1])
            perso.pv_max_basic = perso.pv
            perso.pa_max = perso.pa + perso.niveau//50
            perso.pm_max = perso.pm + perso.niveau//50
            bf.init_stats(perso)
            fichier.close()
        else:
            fichier = open('data/save/joueurs/'+pseudo+'.txt','w', encoding='utf-8')
            fichier.write(pseudo + '\n' + '1' + '\n' + '0' + '\n' + dico_perso[num_classe] + '\n')
            fichier.write('\n')
            fichier.close()
            fichier = open('data/save/joueurs/1_liste_pseudo.txt','a', encoding='utf-8')
            fichier.write(pseudo + '\n')
        
            self.liste_pseudo.append(pseudo)
            fichier.close()
                       
    def menu_load(self, val = 0):
        self._initialiser()
        self.fond = pygame.image.load("data/images/Menu/fondviergen.png").convert()  
        self.ecran = MenuLoad(self, self.groupeGlobal)
        
    def load_map(self, name):
        name = self.myMap.name
        try :
            self.myMap.map_data = []
            fichier = open('data/map/'+name+'.txt','r', encoding='utf-8')
            C = fichier.readlines()
            for ligne in C:
                ligne = ligne[:-2]
                ligne = ligne.split(',')
                ligne = [int(i) for i in ligne]
                self.myMap.map_data.append(ligne)
            fichier.close()
            pos_depart1, pos_depart2 = [], []
            for i in range(len(self.myMap.map_data)):
                for j in range(len(self.myMap.map_data[0])):
                    if self.myMap.map_data[i][j] ==2:
                        pos_depart1.append((i,j))
                        self.myMap.map_data[i][j] = 0
                    if self.myMap.map_data[i][j] ==3:
                        pos_depart2.append((i,j))
                        self.myMap.map_data[i][j] = 0
            
            self._initialiser() 
            self.myMap.pos_depart1 = pos_depart1
            self.myMap.pos_depart2 = pos_depart2
            self.myMap.maps.append([self.myMap.map_data, pos_depart1, pos_depart2])
            self.myMap.choix_map = len(self.myMap.maps) - 1
            self.fond = pygame.image.load("data/images/Menu/fondvierge.png").convert()
            self.fenetre.blit(self.fond, (0,0))
            self.gameOn = True
            i = 0
            for perso in self.groupePersoCbt:
                if perso.team == 1:
                    perso.pos_depart = self.myMap.pos_depart1[i] 
                    perso.pos = self.myMap.pos_depart1[i] 
                i += 1
            i = 0
            for perso in self.groupePersoCbt:
                if perso.team == 2:
                    perso.pos_depart = self.myMap.pos_depart2[i] 
                    perso.pos = self.myMap.pos_depart2[i] 
                    i += 1
        
            self.jeu()     
            self.timer[0] = pygame.time.get_ticks()           
            self.ChatTextuel.L = ['' for i in range(self.ChatTextuel.n-2)]
            self.ChatTextuel.L.append('                         Bienvenu sur Sufdo ' + self.version)
            self.ChatTextuel.L.append('')
            
        except FileNotFoundError:
            self.retour(3)
    
    def menu3(self, val = 0):
        # Affichage du menu 3 du choix des Map
        if self.choixPerso.teams_not_empty():        
            self._initialiser()
            self.joueur = bf.classement_ini(self.J)
            
            self._initialiser()
            self.myMap.combat_started = False
            self.fond = pygame.image.load("data/images/Menu/fond4.png").convert()
            self.ecran = Menu3(self, self.groupeGlobal) 
        
    def choix_pos(self, choix_map):
        self.choix_map = choix_map
        self.myMap.choix_map = choix_map
        self.myMap.map_data = self.myMap.maps[choix_map][0]
        self.myMap.pos_depart = self.myMap.maps[choix_map][1]
        self.fond = pygame.image.load("data/images/Menu/fondvierge.png").convert()
        self.fenetre.blit(self.fond, (0,0))
        self.gameOn = True
        i = 0
        for perso in self.groupePersoCbt:
            perso.pos_depart = self.myMap.pos_depart[i] 
            perso.pos = self.myMap.pos_depart[i] 
            i += 1
        self.jeu()
        self.timer[0] = pygame.time.get_ticks()
        self.ChatTextuel.L = ['' for i in range(self.ChatTextuel.n-2)]
        self.ChatTextuel.L.append('                         Bienvenu sur Sufdo ' + self.version)
        self.ChatTextuel.L.append('')
        
    def jeu(self, val = 0):
        self._initialiser() 
        self.ecran = Jeu(self, self.choix_map, self.joueur, self.groupePersoCbt, self.groupeGlobal)

    def menu_fin_cbt(self, val = 0) :
        self._initialiser()
        self.fond = pygame.image.load("data/images/Menu/fondviergen.png").convert()  
        self.ecran = FinCbt(self, self.groupeGlobal)
    
    def passer(self, val = 0):  
        
        #´Sauvegarde #
        fichier = open('data/save/map.txt','w', encoding='utf-8')
        M = self.myMap.map_data
        for i in range(len(M)):
            for j in range(len(M[0])):
                fichier.write(str(M[i][j]) +',')
            fichier.write('\n')
        fichier.close()
        
        # On deselectionne le sort déjà selectionné #
        self.myMap.sort_selected = -1
        
        # Si le combat n'a pas commencé, on met ready le joueur qui vient de jouer #
        if not self.combat_started:
            self.joueur.isReady = True
        
        # On redonne les PA/PM au joueur
        self.joueur.pa = self.joueur.pa_max
        self.joueur.pm = self.joueur.pm_max
        
        # On vérifie si le combat est terminé #
        t1, t2 = 0, 0
        for perso in self.groupePersoCbt:
            if perso.team == 1:
                t1 += 1
            else:
                t2 += 1
        if t1 == 0 or t2 == 0:
            self.gameOn = False
            self.combat_started = False
            self.timer[1] = pygame.time.get_ticks()
            self.menu_fin_cbt()
        else:
            # On change l'ordre d'initiative #
            for perso in self.groupePersoCbt:
                # On fait début de tour au joueur suivant #
                if perso.ordre_ini == 1:
                    perso.ordre_ini = 0
                    perso.debut_tour(self.groupePersoCbt, self.groupePersoHorsCbt, self.groupeGlobal, self.groupeGlyphe, self.ChatTextuel)
                    perso.ordre_ini = 1 # Sinon ça bug 

                if perso.ordre_ini == 0:
                    perso.ordre_ini = len(self.groupePersoCbt)-1
                    
                elif perso.ordre_ini == 1:
                    perso.ordre_ini -= 1
                    self.joueur = perso
                else:
                    perso.ordre_ini -= 1
           
            
            #Si tous les joueurs ont fait "Prêt" #        
            if not (False in [perso.isReady for perso in self.groupePersoCbt]): 
                self.combat_started = True
                self.myMap.combat_started = True
                
            self.jeu(self.choix_map)
            if self.joueur.isIA and self.combat_started:
                ia_player = ia.IA(self.joueur, 'combatif')
                ia_player.tour(self, self.myMap.map_data, self.groupePersoCbt, self.groupePersoHorsCbt, self.groupeGlobal, self.groupeGlobalPerso, self.ChatTextuel)
                self.tick = pygame.time.get_ticks()
                
    
    def sort(self, num_sort):
        if num_sort < len(self.joueur.S):
            self.myMap.sort_selected = num_sort  
    
    def retour(self, val):
        if val == 1:
            self.gameOn = False
            self.menu1()
        elif val == 2:
            self.menuPerso()
        elif val == 3:
            self.menu3()
    
    def quitter(self, val = 0) :
        self.statut = False
 
    def wait(self, time):
        self.tick = pygame.time.get_ticks()
        while pygame.time.get_ticks() - self.tick < time :
            if self.gameOn:
                self.updateJeu()
            else:
                self.update()
            self.clock.tick(self.fps)
 
    def update(self) :
        events = pygame.event.get()
        for event in events :
            self.clicGaucheup = (event.type == pygame.MOUSEBUTTONUP and event.button == 1)
            self.clicGauchedown = (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
            if event.type == pygame.QUIT :
                self.quitter()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.ecran.name == 'load':
                        self.load_map('')
                if self.ecran.name == 'New Perso' or self.ecran.isWritting:
                    self.ecran.ajout_nom(pygame.key.name(event.key))
            
         
        self.fenetre.blit(self.fond, (0,0))
        self.ecran.update(events, self, self.groupeSortsBouton, self.groupeInfoBulleSort, self.groupeSurfaceSort, self.groupeBoutonImage)
        self.groupeGlobal.update()
        
        # Maj affichage du nb de classes choisi sur le menu de classe #
        dico_perso2 = {0 : 'Chat', 1 : 'Cerf', 2 : 'Dragon', 3 : 'Justicier', 4 : 'Poulpe', 5 : 'Monstre Corrompu', 6 : 'Protecteur', 7 : 'Épée', 8 : 'Invocateur', 9 : 'Chtulu', 10 : 'Gigolo'}
        textes_variables = []

        for i in range(len(self.choixPerso.team1)+len(self.choixPerso.team2)):
            if i < len(self.choixPerso.team1):
                textes_variables.append(dico_perso2[i] + ' x' + str(self.choixPerso.team1[i]))     
            else:
                textes_variables.append(dico_perso2[i-len(self.choixPerso.team1)] + ' x' + str(self.choixPerso.team2[i-len(self.choixPerso.team1)]))   
        for tv in self.groupeTxtVariableJoueur:
            if tv.isClasse:
                tv.maj(textes_variables[tv.num])
        # ---- #
        
        
        self.groupeSurface.draw(self.fenetre)
        self.groupeGlobal.draw(self.fenetre)
        
        pygame.display.update()
        if self.clicGaucheup:
            self.clicGaucheup = False
        
    
    def updateJeu(self) :
        events = pygame.event.get()
 
        for event in events :
            self.clicGaucheup = (event.type == pygame.MOUSEBUTTONUP and event.button == 1)
            self.clicGauchedown = (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
            if event.type == pygame.QUIT :
                self.quitter()
                return
            if event.type == pygame.KEYDOWN and not self.joueur.isActing:
                if event.key == pygame.K_F1 and (not self.joueur.isIA or not self.combat_started):
                    self.passer()
                if event.key == pygame.K_F2:
                    self.joueur.pa += 5
                    bf.affiche_point(5, self.joueur, self.groupeGlobal, 'pa')
                if event.key == pygame.K_F3:
                    self.joueur.pm += 5
                    bf.affiche_point(5, self.joueur, self.groupeGlobal, 'pm')
                if event.key == pygame.K_F4:
                    self.joueur.bPui.append([100,3000000])
                if event.key == pygame.K_F5:
                    self.joueur.bPo.append([1,30000000])
                if event.key == pygame.K_F6:
                    self.joueur.pv_max += 100
                    self.joueur.pv += 100
                if event.key == pygame.K_F7:
                    self.joueur.bDmg.append([50,3000000])
                if event.key == pygame.K_1:
                    self.sort(0)
                if event.key == pygame.K_2:
                    self.sort(1)
                if event.key == pygame.K_3:
                    self.sort(2)
                if event.key == pygame.K_4:
                    self.sort(3)
                if event.key == pygame.K_5:
                    self.sort(4)
                if event.key == pygame.K_6:
                    self.sort(5)
                if event.key == pygame.K_7:
                    self.sort(6)
                if event.key == pygame.K_8:
                    self.sort(7)
                if event.key == pygame.K_9:
                    self.sort(8)
                if event.key == pygame.K_0:
                    self.sort(9)
                if event.key == pygame.K_a:
                    self.sort(10)
                if event.key == pygame.K_z:
                    self.sort(11)
                if event.key == pygame.K_e:
                    self.sort(12)
                if event.key == pygame.K_r:
                    self.sort(13)
                if event.key == pygame.K_t:
                    self.sort(14)
                if event.key == pygame.K_y:
                    self.sort(15)
                if event.key == pygame.K_u:
                    self.sort(16)
                if event.key == pygame.K_i:
                    self.sort(17)
                if event.key == pygame.K_o:
                    self.sort(18)
                if event.key == pygame.K_p:
                    self.sort(19)
        # IA #  
        if pygame.time.get_ticks() - self.tick > 100 and self.joueur.isIA and not self.combat_started:
            self.passer()
        if self.joueur.isIA and self.combat_started:
            if self.joueur.tour_fini and pygame.time.get_ticks() - self.tick > 300:
                self.passer()
                
        # Invocs statiques #
        if self.joueur.isStatic and not self.isStaticDone:
            if self.joueur.S != []:
                zone_cible = pf.ajout_zone(self.myMap.map_data, self.joueur, 0, self.joueur.pos)
                pos_tous_joueurs = [perso.pos for perso in self.groupePersoCbt]
                cibles = []
                for (i,j) in zone_cible:
                    if (i,j) in pos_tous_joueurs:
                        for perso in self.groupePersoCbt:
                            if perso.pos == (i,j):
                                cibles.append(perso)
                self.joueur.use_sort(0, self.joueur, cibles, self.myMap.map_data, None, self.joueur.pos, self.groupePersoCbt, self.groupePersoHorsCbt, self.groupeGlobal, self.groupeGlobalPerso, self.groupeGlyphe, self.ChatTextuel)
            self.isStaticDone = True
        
        if pygame.time.get_ticks() - self.tick > self.joueur.time_to_pass and self.isStaticDone and self.joueur.isStatic: 
            self.passer()
            self.isStaticDone = False
            
        self.myMap.updateMapIso(self.fenetre, self.joueur, self.groupePersoCbt, self.groupePersoHorsCbt, self.groupeGlobalPerso, self.groupeGlobal, self.groupeInfoBullePerso, self.groupeGlyphe, self.ChatTextuel)
        
        x,y = 530,675
        r = self.joueur.pv/self.joueur.pv_max*100
        if int(r) == 100:
            self.fenetre.blit(self.jauge_pv_full, (x,y))
        elif int(r) == 0:
            self.fenetre.blit(self.jauge_pv_empty, (x,y))
        elif r > 75:
            self.fenetre.blit(self.jauge_pv_not_full, (x,y))
        elif r > 50:
            self.fenetre.blit(self.jauge_pv_75, (x,y))
        elif r > 25:
            self.fenetre.blit(self.jauge_pv_50, (x,y))
        elif r > 10:
            self.fenetre.blit(self.jauge_pv_25, (x,y))
        else:
            self.fenetre.blit(self.jauge_pv_low, (x,y))
        self.fenetre.blit(self.icon_pa, (x+102,y+5))
        self.fenetre.blit(self.icon_pm, (x+102,y+60))
            
        self.ecran.update(events, self, self.groupeSortsBouton, self.groupeInfoBulleSort, self.groupeSurfaceSort, self.groupeBoutonImage)
        self.ChatTextuel.update()
        self.groupeChatTextuel.update()
        self.groupeGlobal.update()
        self.groupeInfoBullePerso.update()
        self.groupeInfoBulleSort.update()
        self.groupeSurface.update()
        self.groupeSurfaceSort.update()
        self.joueur.update(self.groupeTxtVariableJoueur)
        
        self.groupeGlobal.draw(self.fenetre)
        self.groupeSurfaceSort.draw(self.fenetre)
        self.groupeChatTextuel.draw(self.fenetre)
        self.groupeInfoBullePerso.draw(self.fenetre)
        self.groupeInfoBulleSort.draw(self.fenetre)
        self.groupeSurface.draw(self.fenetre)
        
        
        
        
        pygame.display.update()
        if self.clicGaucheup:
            self.clicGaucheup = False