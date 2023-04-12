# Import ---------- #
import pygame

import data.scripts.personnages as p
import data.scripts.functions as f
import data.scripts.battle_functions as bf
import data.scripts.mapiso as mi
import data.scripts.Classes.chat as _chat_
import data.scripts.Classes.dragon as _dragon_
import data.scripts.Classes.cerf as _cerf_
import data.scripts.Classes.poulpe as _poulpe_
import data.scripts.Classes.monstre_corrompu as _mob_corrompu_


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
        
        
 
    def update(self, events, app, groupeSortsBouton) :
        clicGauche, *_ = pygame.mouse.get_pressed()
        posPointeur = pygame.mouse.get_pos()
        
        for bs in groupeSortsBouton:
            if bs.rect.collidepoint(*posPointeur) :
                bs.dessiner(self.couleurs['rouge'])
                # Si le clic gauche a été pressé
                if clicGauche :
                # Appel de la fonction du bouton
                    pygame.time.wait(90)
                    bs.executerCommande()
                break
            else :
                # Le pointeur n'est pas au-dessus du bouton
                bs.dessiner()
                 
        for bouton in self._boutons :
            # Si le pointeur souris est au-dessus d'un bouton
            if bouton.rect.collidepoint(*posPointeur) :
                
                # Changement de la couleur du bouton
                bouton.dessiner(self.couleurs['rouge'])
                # Si le clic gauche a été pressé
                if clicGauche :
                    # Appel de la fonction du bouton
                    pygame.time.wait(90)
                    bouton.executerCommande()
                break
            else :
                # Le pointeur n'est pas au-dessus du bouton
                bouton.dessiner(bouton.couleur)
        else :
            # Le pointeur n'est pas au-dessus d'un des boutons
            pass
 
    def detruire(self) :
        pygame.mouse.set_cursor(*pygame.cursors.arrow) # initialisation du pointeur
 
# Menu principal # 
class Menu1(Menu):
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        
        # noms des menus et commandes associées
        items = (
            ('Play', 'styleb', (640,400), (405,275), 'bleu', application.menu2, 0),
            ('Quitter', 'styleb', (640,650), (254,120), 'rouge', application.quitter, 0)
        )
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBouton(texte, self.couleurs[couleur], font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)
            application.groupeGlobal.add(mb)
  
# Choix classes j4 #
class MenuTeam1(Menu): 
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        self._fenetre = application.fenetre
        textes_variables = []
        
        dico_perso = {'Chat' : 0, 'Cerf' : 1, 'Dragon' : 2, 'Epée' : 3, 'Poulpe' : 4, 'Monstre Corrompu' : 5, 'Crapeau Royal' : 6}
        dico_perso2 = {0 : 'Chat', 1 : 'Cerf', 2 : 'Dragon', 3 : 'Epée', 4 : 'Poulpe', 5 : 'Monstre Corrompu', 6 : 'Crapeau Royal'}
        
        for perso in application.J:
            application.nb_perso[dico_perso[perso.nom_classe]] += 1
        for i in range(len(application.nb_perso)):
            textes_variables.append((dico_perso2[i] + ' x' + str(application.nb_perso[i]), 'impact', (150,150+30*i), (250,50), 'blanc', i, True))
            

        self._textes = []
        for texte, font, (x,y), taille, couleur, num, boole in textes_variables :

            mtv = f.TexteVariable(texte, self.couleurs[couleur], font, x, y, taille[0], taille[1], num, boole)
            
            self._textes.append(mtv)
            
            application.groupeTxtVariable.add(mtv)
            application.groupeGlobal.add(mtv)
        
        txts = (
            ('- Team 1 -', 'impact', (420,60), (200,100), 'blanc'), 
        )
                
            
        self.txts = []
        for texte, font, (x,y), taille, couleur in txts :

            mt = f.Texte(texte, self.couleurs[couleur], font, x, y, taille[0], taille[1])
            
            self._textes.append(mt)
            
            application.groupeTxt.add(mt)
            application.groupeGlobal.add(mt)
        
        # noms des menus et commandes associées
        items = (
            ('Chat', 'impact', (60,550), (100,50), 'bleu', application.ajout_perso, 1),
            ('Cerf', 'impact', (180,550), (100,50), 'bleu', application.ajout_perso, 2),
            ('Dragon', 'impact', (300,550), (100,50), 'bleu', application.ajout_perso, 3),
            ('Epée', 'impact', (420,550), (100,50), 'bleu', application.ajout_perso, 4),
            ('Poulpe', 'impact', (540,550), (100,50), 'bleu', application.ajout_perso, 5),
            ('Monstre', 'impact', (660,550), (100,50), 'bleu', application.ajout_perso, 6),
            ('Crapeau', 'impact', (780,550), (100,50), 'orange', application.ajout_perso, 7),
            ('Quit', 'styleb', (1220,60), (100,80), 'orange', application.quitter, 0),
            ('Prêt', 'styleb', (640,700), (100,80), 'vertpasser', application.menu4, 0)
        )
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBouton(texte, self.couleurs[couleur], font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)
            application.groupeGlobal.add(mb)

              
# Choix nombres de joueurs #                
class Menu2(Menu):
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        self._fenetre = application.fenetre
        
        # noms des menus et commandes associées
        items = (
            ('2', 'styleb', (320,400), (200,200), 'bleu', application.menu3j1, 2),
            ('3', 'styleb', (640,400), (200,200), 'bleu', application.menu3j1, 3),
            ('4', 'styleb', (960,400), (200,200), 'bleu', application.menu3j1, 4),
            ('Quitter', 'styleb', (640,650), (254,120), 'rouge', application.quitter, 0)
        )
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBouton(texte, self.couleurs[couleur], font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)
            application.groupeGlobal.add(mb)
        
# Choix classes j1 #
class Menu3j1(Menu): 
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        self._fenetre = application.fenetre
        
        # noms des menus et commandes associées
        items = (
            ('Chat', 'styleb', (326,267), (250,100), 'bleu', application.menu3j2, 1),
            ('Cerf', 'styleb', (326,400), (250,100), 'bleu', application.menu3j2, 2),
            ('Dragon', 'styleb', (326,533), (250,100), 'bleu', application.menu3j2, 3),
            ('Epée', 'styleb', (326,666), (250,100), 'bleu', application.menu3j2, 4),
            ('Poulpe', 'styleb', (960,267), (250,100), 'bleu', application.menu3j2, 5),
            ('Monstre', 'styleb', (960,400), (250,100), 'bleu', application.menu3j2, 6),
            ('Crapeau', 'styleb', (960,533), (250,100), 'orange', application.menu3j2, 7),
            ('Quitter', 'styleb', (640,650), (254,120), 'rouge', application.quitter, 0)
        )
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBouton(texte, self.couleurs[couleur], font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)
            application.groupeGlobal.add(mb)
                            
# Choix classes j2 #
class Menu3j2(Menu): 
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        self._fenetre = application.fenetre
        
        # noms des menus et commandes associées
        items = (
            ('Chat', 'styleb', (326,267), (250,100), 'bleu', application.menu3j3, 1),
            ('Cerf', 'styleb', (326,400), (250,100), 'bleu', application.menu3j3, 2),
            ('Dragon', 'styleb', (326,533), (250,100), 'bleu', application.menu3j3, 3),
            ('Epée', 'styleb', (326,666), (250,100), 'bleu', application.menu3j3, 4),
            ('Poulpe', 'styleb', (960,267), (250,100), 'bleu', application.menu3j3, 5),
            ('Monstre', 'styleb', (960,400), (250,100), 'bleu', application.menu3j3, 6),
            ('Crapeau', 'styleb', (960,533), (250,100), 'orange', application.menu3j3, 7),
            ('Quitter', 'styleb', (640,650), (254,120), 'rouge', application.quitter, 0)
        )
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBouton(texte, self.couleurs[couleur], font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)   
            application.groupeGlobal.add(mb)
                
# Choix classes j3 #
class Menu3j3(Menu): 
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        self._fenetre = application.fenetre
        
        # noms des menus et commandes associées
        items = (
            ('Chat', 'styleb', (326,267), (250,100), 'bleu', application.menu3j4, 1),
            ('Cerf', 'styleb', (326,400), (250,100), 'bleu', application.menu3j4, 2),
            ('Dragon', 'styleb', (326,533), (250,100), 'bleu', application.menu3j4, 3),
            ('Epée', 'styleb', (326,666), (250,100), 'bleu', application.menu3j4, 4),
            ('Poulpe', 'styleb', (960,267), (250,100), 'bleu', application.menu3j4, 5),
            ('Monstre', 'styleb', (960,400), (250,100), 'bleu', application.menu3j4, 6),
            ('Crapeau', 'styleb', (960,533), (250,100), 'orange', application.menu3j4, 7),
            ('Quitter', 'styleb', (640,650), (254,120), 'rouge', application.quitter, 0)
        )
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBouton(texte, self.couleurs[couleur], font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)  
            application.groupeGlobal.add(mb)
                
# Choix classes j4 #
class Menu3j4(Menu): 
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        self._fenetre = application.fenetre
        
        # noms des menus et commandes associées
        items = (
            ('Chat', 'styleb', (326,267), (250,100), 'bleu', application.menu4, 1),
            ('Cerf', 'styleb', (326,400), (250,100), 'bleu', application.menu4, 2),
            ('Dragon', 'styleb', (326,533), (250,100), 'bleu', application.menu4, 3),
            ('Epée', 'styleb', (326,666), (250,100), 'bleu', application.menu4, 4),
            ('Poulpe', 'styleb', (960,267), (250,100), 'bleu', application.menu4, 5),
            ('Monstre', 'styleb', (960,400), (250,100), 'bleu', application.menu4, 6),
            ('Crapeau', 'styleb', (960,533), (250,100), 'orange', application.menu4, 7),
            ('Quitter', 'styleb', (640,650), (254,120), 'rouge', application.quitter, 0)
        )
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBouton(texte, self.couleurs[couleur], font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)
            application.groupeGlobal.add(mb)
                
# Choix Map --- #
class Menu4(Menu): 
    def __init__(self, application, *groupes):
        Menu.__init__(self, *groupes)
        self._fenetre = application.fenetre
        # noms des menus et commandes associées
        items = (
            ('Map 1', 'styleb', (320,400), (300,200), 'bleu', application.choix_pos, 0),
            ('Map 2', 'styleb', (640,400), (300,200), 'bleu', application.choix_pos, 1),
            ('Map 3', 'styleb', (960,400), (300,200), 'bleu', application.choix_pos, 2),
            ('Quit', 'styleb', (1220,60), (100,80), 'orange', application.quitter, 0)
        )
        
        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :
            
            mb = f.MenuBouton(texte, self.couleurs[couleur], font ,x ,y , taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)   
            application.groupeGlobal.add(mb)

# Jeu Map 1 ------- #
class Map1(Menu):
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
                ('Timeline', 'styleb', (110,40), (200,80), 'gris_foncé', application.quitter,0),
                ('Quit', 'styleb', (1220,60), (100,80), 'orange', application.quitter,0),
                (pass_or_start, 'styleb', (610,750),(140,50), 'vertpasser', application.passer,0)
            )
        

        self._boutons = []
        for texte, font, (x,y), taille, couleur, cmd, val in items :

            mb = f.MenuBouton(texte, self.couleurs[couleur], font, x, y, taille[0], taille[1], cmd, val)
            
            self._boutons.append(mb)
            
            application.groupeMenuBouton.add(mb)   
            application.groupeGlobal.add(mb)
                
        sorts = (
                ('s1', (900,660), application.sort, 0),
                ('s2', (980,660), application.sort, 1),
                ('s3', (1060,660), application.sort, 2),
                ('s4', (1140,660), application.sort, 3),
                ('s5', (1220,660), application.sort, 4),
                ('s6', (900,740), application.sort, 5),
                ('s7', (980,740), application.sort, 6),
                ('s8', (1060,740), application.sort, 7),
                ('s9', (1140,740), application.sort, 8),
                ('s10', (1220,740), application.sort, 9),
            )
        sorts = [sorts[i] for i in range(len(joueur.S))]
        
        self._sorts = []
        for nom, (x,y), cmd, val in sorts :
            
            msb = f.SortBouton(nom, x, y, cmd, val, joueur)
            
            self._sorts.append(msb)
            
            application.groupeSortsBouton.add(msb)
            application.groupeGlobal.add(msb)
                
        
        textes_variables = [
            (str(joueur.pv), 'styleb', (770,700), (300,80), 'blanc', 0),
            (str(int(joueur.pv/joueur.pv_max*100)) +" %", 'styleb', (770,740), (150,80), 'blanc', 1),
            ("PA : " + str(joueur.pa + joueur.somme_boost('pa')), 'styleb', (610,680), (250,60), 'bleuc', 2),
            ("PM : " + str(joueur.pm + joueur.somme_boost('pm')), 'styleb', (610,710), (250,60), 'rougepm', 3),
            ]
            
        self._textes = []
        for texte, font, (x,y), taille, couleur, num in textes_variables :

            mtv = f.TexteVariable(texte, self.couleurs[couleur], font, x, y, taille[0], taille[1], num)
            
            self._textes.append(mtv)
            
            application.groupeTxtVariable.add(mtv)
            application.groupeGlobal.add(mtv)
        
        txts = []
        # Affichage de la Timeline #
        i = 0
        for perso in groupePersoCbt:
            if perso.ordre_ini == 0:
                 colo = 'gold'
            else:
                 colo = 'blanc'
            txts.append((perso.pseudo, 'tahoma', (70,75 + 14*(perso.ordre_ini+1)), (200,30), colo))
            i += 1
            
        self.txts = []
        for texte, font, (x,y), taille, couleur in txts :

            mt = f.Texte(texte, self.couleurs[couleur], font, x, y, taille[0], taille[1])
            
            self._textes.append(mt)
            
            application.groupeTxt.add(mt)
            application.groupeGlobal.add(mt)
        
        
        
    
class Application :
    """ Classe maîtresse gérant les différentes interfaces du jeu """
    def __init__(self, liste_pseudo) :
        self.J = []
        self.nb_joueurs = 0
        self.nb_perso = [0,0,0,0,0,0,0]
        
        self.joueur = None # Joueur dont c'est le tour #
        self.choix_classes = []
        self.choix_map = 0
        self.liste_pseudo = liste_pseudo
            
        pygame.init()
        pygame.display.set_caption('Sufdo')
        self.fenetre = pygame.display.set_mode((1280,800), 0, 32)
        
        self.myMap = mi.MapIso(self.fenetre)
        
        self.icon = pygame.image.load("data/images/icon1.png").convert_alpha()
        pygame.display.set_icon(self.icon)
        self.fond = pygame.image.load("data/images/Menu/fond.png").convert()
        
        self.jauge_pv = pygame.image.load('data/images/hp.png').convert_alpha()
        
        # Groupe de sprites utilisé pour l'affichage
        self.groupeGlobal = pygame.sprite.Group()
        self.groupeMenuBouton = pygame.sprite.Group()
        self.groupeSortsBouton = pygame.sprite.Group()
        self.groupeTxtVariable = pygame.sprite.Group()
        self.groupeTxt = pygame.sprite.Group()
        self.groupeInfoBullePerso = pygame.sprite.Group()
        # Groupes de perso #
        self.groupeGlobalPerso = pygame.sprite.Group()
        self.groupePersoCbt = pygame.sprite.Group()
        self.groupePersoHorsCbt = pygame.sprite.Group()
        
        self.statut = True
        self.gameOn = False
        self.combat_started = False
 
    def _initialiser(self) :
        try:
            self.ecran.detruire()
            # Suppression de tous les sprites du groupe
            self.groupeGlobal.empty()
            self.groupeMenuBouton.empty()
            self.groupeSortsBouton.empty()
            self.groupeTxtVariable.empty()
            self.groupeTxt.empty()
        except AttributeError:
            pass

    
    def menu1(self, val = 0) :
        # Affichage du menu 1
        self._initialiser()
        self.ecran = Menu1(self, self.groupeGlobal)
 
    def menu2(self, val = 0) :
        # Affichage du menu 2
        self._initialiser()
        self.fond = pygame.image.load("data/images/Menu/fond2.png").convert()
        self.ecran = Menu2(self, self.groupeGlobal)
        
    def menu3j1(self, nb_joueurs):
        self.nb_joueurs = nb_joueurs
        self._initialiser()
        self.fond = pygame.image.load("data/images/Menu/fondvierge.png").convert()
        self.ecran = MenuTeam1(self, self.groupeGlobal)
    
    def menu3j2(self, num_classej1):
        self.choix_classe(num_classej1)
        
        self._initialiser()
        self.fond = pygame.image.load("data/images/Menu/fondj2.png").convert()
        self.ecran = Menu3j2(self, self.groupeGlobal)
        
    def menu3j3(self, num_classej2):
        self.choix_classe(num_classej2)
        
        self._initialiser()
        self.fond = pygame.image.load("data/images/Menu/fondj3.png").convert()
        self.ecran = Menu3j3(self, self.groupeGlobal)    
        
    def menu3j4(self, num_classej3):
        self.choix_classe(num_classej3)

        self._initialiser()
        self.fond = pygame.image.load("data/images/Menu/fondj4.png").convert()
        self.ecran = Menu3j4(self, self.groupeGlobal)  
    
    def ajout_perso(self, num_perso):
        if len(self.J) < 16:
            self.nb_joueurs += 1
            self.nb_perso[num_perso-1] += 1
            self.choix_classe(num_perso)
    
    def choix_classe(self, num_classe):
        self.choix_classes.append(num_classe)
        i = len(self.J)
        
        if i >= len(self.liste_pseudo):
            self.liste_pseudo.append('Perso '+str(i))
        if i < 16:    
            if self.choix_classes[-1] == 1:
                perso = _chat_.Chat(self.liste_pseudo[i])
            elif self.choix_classes[-1] == 2:
                perso = _cerf_.Cerf(self.liste_pseudo[i])
            elif self.choix_classes[-1] == 3:
                perso = _dragon_.Dragon(self.liste_pseudo[i])
            elif self.choix_classes[-1] == 4:
                perso = p.Epee(self.liste_pseudo[i])
            elif self.choix_classes[-1] == 5:
                perso = _poulpe_.Poulpe(self.liste_pseudo[i])
            elif self.choix_classes[-1] == 6:
                perso = _mob_corrompu_.MonstreCorrompu(self.liste_pseudo[i])
            else:
                perso = p.Crapeaud(self.liste_pseudo[i])
                
            if self.nb_joueurs > len(self.J):    
                self.J.append(perso)
                perso.team = len(self.J)%2 + 1
                self.groupeGlobalPerso.add(perso)
                self.groupePersoCbt.add(perso)
                self.J[-1].id = len(self.J)-1     # l'id du joueur est sa position dans la liste J
        
    
    def menu4(self, num_classej4):
        # Affichage du menu 4 du choix des Map
        for perso in self.groupePersoCbt:
            print(perso.nom_classe)
        self.joueur = bf.classement_ini(self.J)
        
        self._initialiser()
        self.fond = pygame.image.load("data/images/Menu/fond4.png").convert()
        self.ecran = Menu4(self, self.groupeGlobal)
        
        
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
        
    def jeu(self, val = 0):
        self._initialiser() 
        self.ecran = Map1(self, self.choix_map, self.joueur, self.groupePersoCbt, self.groupeGlobal)

    def passer(self, val = 0):     
        print('')
        
        fichier = open('data/save/map.txt','w', encoding='utf-8')
        M = self.myMap.map_data
        for i in range(len(M)):
            for j in range(len(M[0])):
                fichier.write(str(M[i][j]) +',')
            fichier.write('\n')
        fichier.close()
        
        fichier = open('data/save/save.txt','w', encoding='utf-8')
        fichier.write(self.joueur.pseudo + '\n' + str(self.joueur.pv) + '\n' + str(self.joueur.ordre_ini) + '\n' + str(self.joueur.pos))
        fichier.write('\n')
        fichier.close()
        
        # On deselectionne le sort déjà selectionné #
        self.myMap.sort_selected = -1
        
        # Si le combat n'a pas commencé, on met ready le joueur qui vient de jouer #
        if not self.combat_started:
            self.joueur.isReady = True
        
        # On change l'ordre d'initiative #
        for perso in self.groupePersoCbt:
            # On fait début de tour au joueur suivant #
            if perso.ordre_ini == 1:
                perso.debut_tour()
                
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
    
    def sort(self, num_sort):
        s = self.joueur.S[num_sort]
        if s.latence_max == 0:
            if s.coup_par_tour_max >= 100:
                print('{} | Coût : {} | Effet : {}'.format(s.nom, s.cout, s.effet_str))
            else:
                print('{} | Coût : {} | Effet : {} | Coups restant : {}/{}'.format(s.nom, s.cout, s.effet_str, s.coup_par_tour, s.coup_par_tour_max))
        else:
            print('{} | Coût : {} | Effet : {} | Latence : {}/{}'.format(s.nom, s.cout, s.effet_str, s.latence, s.latence_max))
        
        print('')
        self.myMap.sort_selected = num_sort  
    
    def sortgris(self, val=0):
        pass
    
    def quitter(self, val = 0) :
        self.statut = False
 
    def update(self) :
        events = pygame.event.get()
        for event in events :
            if event.type == pygame.QUIT :
                self.quitter()
                return
            
         
        self.fenetre.blit(self.fond, (0,0))
        self.ecran.update(events, self, self.groupeSortsBouton)
        self.groupeGlobal.update()
        
        # Maj affichage du nb de classes choisi sur le menu de classe #
        dico_perso2 = {0 : 'Chat', 1 : 'Cerf', 2 : 'Dragon', 3 : 'Epée', 4 : 'Poulpe', 5 : 'Monstre Corrompu', 6 : 'Crapeau Royal'}
        textes_variables = []

        for i in range(len(self.nb_perso)):
            textes_variables.append(dico_perso2[i] + ' x' + str(self.nb_perso[i]))     
        for tv in self.groupeTxtVariable:
            if tv.isClasse:
                tv.maj(textes_variables[tv.num])
        # ---- #
        
        self.groupeGlobal.draw(self.fenetre)
        
        pygame.display.update()
        
    
    def updateJeu(self) :
        events = pygame.event.get()
 
        for event in events :
            if event.type == pygame.QUIT :
                self.quitter()
                return
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_F1:
                    self.passer()
                if event.key == pygame.K_F2:
                    self.joueur.pa += 5
                    bf.affiche_point(5, self.joueur, self.groupeGlobal, 'pa')
                if event.key == pygame.K_F3:
                    self.joueur.pm += 5
                    bf.affiche_point(5, self.joueur, self.groupeGlobal, 'pm')
                if event.key == pygame.K_F4:
                    self.joueur.bPui.append([50,3000000])
                if event.key == pygame.K_F5:
                    self.joueur.bPo.append([1,30000000])
                if event.key == pygame.K_F6:
                    self.joueur.pv_max += 100
                    self.joueur.pv += 100
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
                    
                    
        self.myMap.updateMapIso(self.fenetre, self.joueur, self.groupePersoCbt, self.groupePersoHorsCbt, self.groupeGlobalPerso, self.groupeGlobal, self.groupeInfoBullePerso)
        
        
        
        self.fenetre.blit(self.jauge_pv, (690,635))
        
        self.ecran.update(events, self, self.groupeSortsBouton)
        self.groupeGlobal.update()
        self.groupeInfoBullePerso.update()
        self.joueur.update(self.groupeTxtVariable)
        
        self.groupeGlobal.draw(self.fenetre)
        self.groupeInfoBullePerso.draw(self.fenetre)
        
        pygame.display.update()