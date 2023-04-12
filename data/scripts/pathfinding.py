# Import ---------- #
import numpy as np

# Pathfinding --------------------------------------- #

class Tile():
    def __init__(self, x, y, xp, yp):
        self.x = x
        self.y = y
        self.xp = xp
        self.yp = yp
        
        self.H = 0
        self.G = 0
        self.T = 0
        self.F = 0
        
    def update(self, end, G_parent, T_parent, val = 0, val2 = 0):
        self.G = G_parent + 10 
        self.T += T_parent
        self.H = abs(end[0] - self.x) + abs(end[1] - self.y)
        self.F = self.H + self.G + self.T


def minTiles(liste_tiles):
    mini = (liste_tiles[0],0)
    for i in range(1,len(liste_tiles)):
        if liste_tiles[i].F < mini[0].F:
            mini = (liste_tiles[i],i)
    return mini

def ajout_zone(M, joueur, sort_selected, pos):
    (x,y) = pos
    (X,Y) = joueur.pos
    zone_cible = joueur.S[sort_selected].zone_cible
    taille_zone = joueur.S[sort_selected].taille_zone + joueur.S[sort_selected].somme_boost('poz')
    po = taille_zone
    po_range = [pos]
    dico = {'cercle' : 0, 'croix' : 1, 'ligne' : 2, 'colonne' : 3, 'carré' : 4, 'case' : 5, 'T' : 6, 'tout' : 7, 'moi' : 8, 'tout sans moi' : 9, 'diago' : 10, 'traînée' : 11}
    
    if dico[zone_cible] == 5: # Case #
        return po_range
    
    if dico[zone_cible] == 11:  # Traînée #
        if abs(X-x) < abs(Y-y):    
            for i in range(abs(Y-y)):
                if Y-y > 0:
                    k = i
                else:
                    k = -i
                
                if x >= 0 and y+k >=0 and x < len(M) and y+k < len(M[0]):
                    if M[x][y+k] in [0,2,3]:
                        po_range.append((x,y+k))

               
        else :
            for i in range(abs(X-x)):
                if X-x > 0:
                    k = i
                else:
                    k = -i
                if x+k >= 0 and y >=0 and x+k < len(M) and y < len(M[0]):
                    if M[x+k][y] in [0,2,3]:
                        po_range.append((x+k,y))

           
    
    if dico[zone_cible] in [7,9]:   # Tout #
        for i in range(len(M)):
            for j in range(len(M[0])):
                if M[i][j] in [0,2,3]:
                    po_range.append((i,j))
                
    if dico[zone_cible] == 9: 
        po_range.remove(joueur.pos)

    if dico[zone_cible] == 0:   # Cercle #
        for i in range(x-po, x+po+1):
            for j in range(y-po,y+po+1):
                if i >= 0 and j >=0 and i < len(M) and j < len(M[0]):
                    if M[i][j] in [0,2,3] and abs(x-i) + abs (y-j) <= po:
                        po_range.append((i,j))

                
    if dico[zone_cible] == 4:   # Carré #
        for i in range(x-po, x+po+1):
            for j in range(y-po,y+po+1):
                if i >= 0 and j >=0 and i < len(M) and j < len(M[0]):
                    if M[i][j] in [0,2,3]:
                        po_range.append((i,j))

                
    if dico[zone_cible] == 1:   # Croix #
        for i in range(1,po+1):
            if x >= 0 and y+i >=0 and x < len(M) and y+i < len(M[0]):
                if M[x][y+i] in [0,2,3]:
                    po_range.append((x,y+i))
                    
            if x >= 0 and y-i >=0 and x < len(M) and y-i < len(M[0]):
                if M[x][y-i] in [0,2,3]:
                        po_range.append((x,y-i))
                
            if x+i >= 0 and y >=0 and x+i < len(M) and y < len(M[0]):
                if M[x+i][y] in [0,2,3]:
                    po_range.append((x+i,y))
                
            if x-i >= 0 and y >=0 and x-i < len(M) and y < len(M[0]):
                if M[x-i][y] in [0,2,3]:
                    po_range.append((x-i,y))
                    
            
    if dico[zone_cible] == 2: # Ligne #
        for i in range(1,po+1):
            if abs(X-x) > abs(Y-y):
                if x >= 0 and y+i >=0 and x < len(M) and y+i < len(M[0]):
                    if M[x][y+i] in [0,2,3]:
                        po_range.append((x,y+i))

                if x >= 0 and y-i >=0 and x < len(M) and y-i < len(M[0]):
                    if M[x][y-i] in [0,2,3]:
                            po_range.append((x,y-i))

            else :
                if x+i >= 0 and y >=0 and x+i < len(M) and y < len(M[0]):
                    if M[x+i][y] in [0,2,3]:
                        po_range.append((x+i,y))
             
                if x-i >= 0 and y >=0 and x-i < len(M) and y < len(M[0]):
                    if M[x-i][y] in [0,2,3]:
                        po_range.append((x-i,y))

            
    if dico[zone_cible] == 3: # Colonne #
        for i in range(1,po):
            if abs(X-x) > abs(Y-y):
                if X-x > 0:
                    k = - i
                else:
                    k = i
                if x+k >= 0 and y >=0 and x+k < len(M) and y < len(M[0]):
                    if M[x+k][y] in [0,2,3]:
                        po_range.append((x+k,y))
            else :
                if Y-y > 0:
                    k = - i
                else:
                    k = i
                if x >= 0 and y+k >=0 and x < len(M) and y+k < len(M[0]):
                    if M[x][y+k] in [0,2,3]:
                        po_range.append((x,y+k))          

                
    if dico[zone_cible] == 10: # Diago #
        for i in range(1,po+1):
            if x >= 0 and y+i >=0 and x < len(M) and y+i < len(M[0]):
                if M[x][y+i] in [0,2,3]:
                    po_range.append((x+i,y+i))

            if x >= 0 and y-i >=0 and x < len(M) and y-i < len(M[0]):
                if M[x][y-i] in [0,2,3]:
                        po_range.append((x+i,y-i))
                
            if x+i >= 0 and y >=0 and x+i < len(M) and y < len(M[0]):
                if M[x+i][y] in [0,2,3]:
                    po_range.append((x-i,y+i))
       
            if x-i >= 0 and y >=0 and x-i < len(M) and y < len(M[0]):
                if M[x-i][y] in [0,2,3]:
                    po_range.append((x-i,y-i))

            
    if dico[zone_cible] == 6:   # T #
        for i in range(1,po+1):
            if abs(X-x) > abs(Y-y):
                if X-x > 0:
                    j = - po
                    k = - i
                else:
                    j = po
                    k = i
                if x+i >= 0 and y+i >=0 and x+i < len(M) and y+i < len(M[0]):
                    if M[x+j][y+i] in [0,2,3]:
                        po_range.append((x+j,y+i))

                if x+i >= 0 and y-i >=0 and x+i < len(M) and y-i < len(M[0]):
                    if M[x+j][y-i] in [0,2,3]:
                            po_range.append((x+j,y-i))

                if x+k >= 0 and y >=0 and x+k < len(M) and y < len(M[0]):
                    if M[x+k][y] in [0,2,3]:
                        po_range.append((x+k,y))

            else :
                if Y-y > 0:
                    j = - po
                    k = - i
                else:
                    j = po
                    k = i
                if x+i >= 0 and y+i >=0 and x+i < len(M) and y+i < len(M[0]):
                    if M[x+i][y+j] in [0,2,3]:
                        po_range.append((x+i,y+j))
              
                if x-i >= 0 and y+i >=0 and x-i < len(M) and y+i < len(M[0]):
                    if M[x-i][y+j] in [0,2,3]:
                        po_range.append((x-i,y+j))

                if x >= 0 and y+k >=0 and x < len(M) and y+k < len(M[0]):
                    if M[x][y+k] in [0,2,3]:
                        po_range.append((x,y+k))
      
    # Pcq certaines cibles sont sûrement en double #
    po_range2 = []
    for pos in po_range:
        if pos not in po_range2:
            po_range2.append(pos)
    
    return po_range2
        


def pathfinding(M, groupePerso, joueur, end):
    ''' Renvoie la liste des coordonnées du chemin le plus court en fonction de
    la Map, les positions de départ et arrivée. Renvoie liste vide si pas de chemin. '''
    bPm = joueur.somme_boost('pm')
    pm = joueur.pm + bPm
    start = joueur.pos
    pos_joueurs = [perso.pos for perso in groupePerso]
    
    if end[0] >= 0 and end[1] >= 0 and end[0] < len(M) and end[1] < len(M[0]):
        if M[start[0]][start[1]] != 0 or M[end[0]][end[1]] != 0:
            return []
    else:
        return []
    
    if abs(end[0] - start[0]) + abs(end[1] - start[1]) > pm:
        return []
    
    start = Tile(start[0], start[1], start[0], start[1])
    OL = [start]                    # Open list 
    ol = [(start.x,start.y)]        # Open list des coordonnées
    CL = []                         # Close list 
    cl = []                         # Close list des coordonnées
    best_way = []                   # Liste chemin de coordonnées
    isPossible = False
    
    while len(OL) != 0:
        # Tant que OL non vide, on prend la tuile dont le F est le plus petit dans OL #
        tile,i = minTiles(OL)
        x,y = tile.x, tile.y
        
        if (x,y) in cl:
            OL.pop(i)
            ol.pop(i)
            continue
        
        # Si la case est celle d'arrivée, on arrête la boucle #
        if (x,y) == end:
            isPossible = True
            break
        
        # On créer une liste des cases voisines qui auront cette tuile comme parent #
        voisinage = []
        if x != len(M)-1:
            if M[x+1][y] in [0,2,3] and (x+1,y) not in pos_joueurs:  # Si la case n'est pas un mur/vide/Joueur #
                if (x+1,y) not in cl:   # Si la case n'est pas déjà dans la CL #
                    voisinage.append(Tile(x+1,y,x,y))
        if y != len(M[0])-1:
            if M[x][y+1] in [0,2,3] and (x,y+1) not in pos_joueurs:
                if (x,y+1) not in cl:
                    voisinage.append(Tile(x,y+1,x,y))
        if x != 0:
            if M[x-1][y] in [0,2,3] and (x-1,y) not in pos_joueurs:
                if (x-1,y) not in cl:
                    voisinage.append(Tile(x-1,y,x,y))
        if y != 0:
            if M[x][y-1] in [0,2,3] and (x,y-1) not in pos_joueurs:
                if (x,y-1) not in cl:
                    voisinage.append(Tile(x,y-1,x,y))
                
        # On update les G,H,F des cases voisines #      
        for j in range(len(voisinage)):
            voisinage[j].update(end,tile.G,0)
            # Si elles ne sont pas déjà dans l'OL, on les ajoute au voisinage #
            if (voisinage[j].x,voisinage[j].y) not in ol :
                OL.append(voisinage[j])
                ol.append((voisinage[j].x, voisinage[j].y))
        
        # On retire la tuile étudiée de l'OL et on la met dans la CL #
        
        CL.append(OL.pop(i))
        cl.append(ol.pop(i))
        
    # Si l'algo a trouvé un chemin #
    if isPossible:
        # On ajoute à la liste chemin le dernier élément (la tuile d'arrivée) #
        best_way.append((tile.x, tile.y))
        # Tant que le dernier ajout n'est pas la tuile de départ #
        # On remonte à la case de son parent et on ajoute ce parent à la liste chemin #
        while best_way[-1] != (start.x,start.y):         
            xp,yp = tile.xp, tile.yp
            i = cl.index((xp,yp))
            tile = CL[i]
            best_way.append((tile.x, tile.y))
        best_way.pop(len(best_way) - 1)
    if len(best_way) > pm :
        best_way = []
    
    return best_way     # best_way est liste dont le premier élément est la case d'arrivée #
      

def pathfinding2(M, groupePerso, joueur, end, pos_depart = None):
    ''' Renvoie la liste des coordonnées du chemin le plus court en fonction de
    la Map, les positions de départ et arrivée. Renvoie liste vide si pas de chemin. '''
    bPm = joueur.somme_boost('pm')
    pm = joueur.pm + bPm
    fuite = joueur.fuite + joueur.somme_boost('fuite')
    if fuite < 0:
        fuite = 0
    if pos_depart == None:
        start = joueur.pos
    else:
        start = pos_depart
    pos_joueurs_autres = [perso.pos for perso in groupePerso if perso.pos != start]
    pos_joueurs = pos_joueurs_autres + [start]
    
    J = [[perso.pos, perso] for perso in groupePerso if perso.team != joueur.team]
 
    # On créer une liste de cases des malus de tacle #
    tuiles_taclee = [[0 for i in range(len(M[0]))] for j in range(len(M))]
    for j in J:
        (x,y) = j[0]
        if x < len(M):
            if M[x+1][y] in [0,2,3] and (x+1,y) not in pos_joueurs_autres:  # Si la case n'est pas un mur/vide/Joueur #
                tuiles_taclee[x+1][y] += j[1].tacle + j[1].somme_boost('tacle')
        if y < len(M[0]):
            if M[x][y+1] in [0,2,3] and (x,y+1) not in pos_joueurs_autres:
                tuiles_taclee[x][y+1] += j[1].tacle + j[1].somme_boost('tacle')
        if x >= 0:
            if M[x-1][y] in [0,2,3] and (x-1,y) not in pos_joueurs_autres:
                tuiles_taclee[x-1][y] += j[1].tacle + j[1].somme_boost('tacle')
        if y >= 0:
            if M[x][y-1] in [0,2,3] and (x,y-1) not in pos_joueurs_autres:
                tuiles_taclee[x][y-1] += j[1].tacle + j[1].somme_boost('tacle')
    
    # On retire pour chaque case au tacle, la fuite du perso #
    for i in range(len(tuiles_taclee)):
        for j in range(len(tuiles_taclee[i])):
            tuiles_taclee[i][j] -= fuite
            if tuiles_taclee[i][j] < 0:
                tuiles_taclee[i][j] = 0
                
    if end[0] >= 0 and end[1] >= 0 and end[0] < len(M) and end[1] < len(M[0]):
        if M[start[0]][start[1]] != 0 or M[end[0]][end[1]] != 0:
            return [], pm + 1
    else:
        return [], pm + 1
    
    if abs(end[0] - start[0]) + abs(end[1] - start[1]) > pm:
        return [], pm + 1
    
    start = Tile(start[0], start[1], start[0], start[1])
    start.T += tuiles_taclee[start.x][start.y]*10
    OL = [start]                    # Open list 
    ol = [(start.x,start.y)]        # Open list des coordonnées
    CL = []                         # Close list 
    cl = []                         # Close list des coordonnées
    best_way = []                   # Liste chemin de coordonnées
    isPossible = False
    
    while len(OL) != 0:
        # Tant que OL non vide, on prend la tuile dont le F est le plus petit dans OL #
        tile,i = minTiles(OL)
        x,y = tile.x, tile.y
        
        if (x,y) in cl:
            OL.pop(i)
            ol.pop(i)
            continue
        
        # Si la case est celle d'arrivée, on arrête la boucle #
        if (x,y) == end:
            isPossible = True
            break
        
        # On créer une liste des cases voisines qui auront cette tuile comme parent #
        voisinage = []
        if x+1 < len(M):
            if M[x+1][y] in [0,2,3] and (x+1,y) not in pos_joueurs:  # Si la case n'est pas un mur/vide/Joueur #
                if (x+1,y) not in cl:   # Si la case n'est pas déjà dans la CL #
                    t = Tile(x+1,y,x,y)
                    voisinage.append(t)
        if y+1 < len(M[0]):
            if M[x][y+1] in [0,2,3] and (x,y+1) not in pos_joueurs:
                if (x,y+1) not in cl:
                    t = Tile(x,y+1,x,y)
                    voisinage.append(t)
        if x-1 >= 0:
            if M[x-1][y] in [0,2,3] and (x-1,y) not in pos_joueurs:
                if (x-1,y) not in cl:
                    t = Tile(x-1,y,x,y)
                    voisinage.append(t)
        if y-1 >= 0:
            if M[x][y-1] in [0,2,3] and (x,y-1) not in pos_joueurs:
                if (x,y-1) not in cl:
                    t = Tile(x,y-1,x,y)
                    voisinage.append(t)
                
        # On update les G,H,F des cases voisines #      
        for j in range(len(voisinage)):
            voisinage[j].T += tuiles_taclee[voisinage[j].x][voisinage[j].y]*10
            voisinage[j].update(end, tile.G, tile.T)
            # Si elles ne sont pas déjà dans l'OL, on les ajoute au voisinage #
            if (voisinage[j].x,voisinage[j].y) not in ol :
                OL.append(voisinage[j])
                ol.append((voisinage[j].x, voisinage[j].y))
        
        # On retire la tuile étudiée de l'OL et on la met dans la CL #
        
        CL.append(OL.pop(i))
        cl.append(ol.pop(i))
        
    # Si l'algo a trouvé un chemin #
    cout = 0
    if isPossible:
        try:
            tile_avant_derniere = CL[cl.index((tile.xp,tile.yp))]
            cout += tile_avant_derniere.T//10
        except ValueError:
            pass
        
        # On ajoute à la liste chemin le dernier élément (la tuile d'arrivée) #
        best_way.append((tile.x, tile.y))
        # Tant que le dernier ajout n'est pas la tuile de départ #
        # On remonte à la case de son parent et on ajoute ce parent à la liste chemin #
        while best_way[-1] != (start.x,start.y):         
            xp,yp = tile.xp, tile.yp
            i = cl.index((xp,yp))
            tile = CL[i]
            best_way.append((tile.x, tile.y))
        best_way.pop(len(best_way) - 1)
        cout += len(best_way)  
    
    return best_way, cout           
                
def pathfinding_pm(M, groupePerso, joueur):
    ''' Renvoie la liste des coordonnées des chemins possibles en fonction de
    la Map, la position de départ et le nombre de pm. Renvoie liste vide si pas de chemin. '''
    
    bPm = joueur.somme_boost('pm')
    pm = joueur.pm + bPm
    start = joueur.pos   
    pos_joueurs = [perso.pos for perso in groupePerso]
        
    if pm <=0:
        return []
    
    start = Tile(start[0], start[1], start[0], start[1])
    OL = [start]                    # Open list 
    ol = [(start.x,start.y)]        # Open list des coordonnées 
    CL = []                         # Close list 
    cl = []                         # Close list des coordonnées
    pm_range = []                   # Liste coordonnées des cases possibles
    
    while len(OL) != 0:
        # Tant que OL non vide, on prend la tuile dont le F est la première tuile de OL #
        tile,i = OL[0],0
        x,y = tile.x, tile.y
        
        if (x,y) in cl:
            OL.pop(i)
            ol.pop(i)
            continue
        
        if tile.G > pm*10:
            OL.pop(i)
            ol.pop(i)
            continue
        
        # On créer une liste des cases voisines qui auront cette tuile comme parent #
        voisinage = []
        if x != len(M)-1:
            if M[x+1][y] in [0,2,3] and (x+1,y) not in pos_joueurs:  # Si la case n'est pas un mur/vide/Joueur #
                if (x+1,y) not in cl:   # Si la case n'est pas déjà dans la CL #
                    voisinage.append(Tile(x+1,y,x,y))
        if y != len(M[0])-1:
            if M[x][y+1] in [0,2,3] and (x,y+1) not in pos_joueurs:
                if (x,y+1) not in cl:
                    voisinage.append(Tile(x,y+1,x,y))
        if x != 0:
            if M[x-1][y] in [0,2,3] and (x-1,y) not in pos_joueurs:
                if (x-1,y) not in cl:
                    voisinage.append(Tile(x-1,y,x,y))
        if y != 0:
            if M[x][y-1] in [0,2,3] and (x,y-1) not in pos_joueurs:
                if (x,y-1) not in cl:
                    voisinage.append(Tile(x,y-1,x,y))
                    
        # On update les G,H,F des cases voisines #      
        for j in range(len(voisinage)):
            voisinage[j].update((0,0),tile.G, tile.T)
            # Si elles ne sont pas déjà dans l'OL, on les ajoute au voisinage #
            if (voisinage[j].x,voisinage[j].y) not in ol :
                OL.append(voisinage[j])
                ol.append((voisinage[j].x, voisinage[j].y))
        
        # On retire la tuile étudiée de l'OL et on la met dans la CL #        
        CL.append(OL.pop(i))
        cl.append(ol.pop(i))
               
    cl.pop(0)
    for t in cl:
        pm_range.append(t)
        
    return pm_range  

def pathfinding_pm3(M, groupePerso, joueur):
    bPm = joueur.somme_boost('pm')
    pm = joueur.pm + bPm
    (x,y) = joueur.pos
    if pm <=0:
        return [], []
    pm_range = []
    pm_no_range = []
    for i in range(len(M)):
        for j in range(len(M[0])):
            if abs(i-x) + abs(j-y) <= pm:
                best_way, cout = pathfinding2(M, groupePerso, joueur, (i,j))
                if best_way != []:
                    if cout > pm:
                        pm_no_range.append((i,j))
                    else:
                        pm_range.append((i,j))
    return pm_range, pm_no_range
                
def pathfinding_pm2(M, groupePerso, joueur):
    ''' Renvoie la liste des coordonnées des chemins possibles en fonction de
    la Map, la position de départ et le nombre de pm. Renvoie liste vide si pas de chemin. '''
    
    bPm = joueur.somme_boost('pm')
    pm = joueur.pm + bPm
    fuite = joueur.fuite + joueur.somme_boost('fuite')
    if fuite < 0:
        fuite = 0
    start = joueur.pos   
    pos_joueurs = [perso.pos for perso in groupePerso]
        
    if pm <=0:
        return [], []
    
    pos_joueurs_autres = [perso.pos for perso in groupePerso if perso != joueur]
    
    J = [[perso.pos, perso] for perso in groupePerso if perso.team != joueur.team]
 
    # On créer une liste de cases des malus de tacle #
    tuiles_taclee = [[0 for i in range(len(M[0]))] for j in range(len(M))]
    for j in J:
        (x,y) = j[0]
        if x != len(M)-1:
            if M[x+1][y] in [0,2,3] and (x+1,y) not in pos_joueurs_autres:  # Si la case n'est pas un mur/vide/Joueur #
                tuiles_taclee[x+1][y] += j[1].tacle + j[1].somme_boost('tacle')
        if y != len(M[0])-1:
            if M[x][y+1] in [0,2,3] and (x,y+1) not in pos_joueurs_autres:
                tuiles_taclee[x][y+1] += j[1].tacle + j[1].somme_boost('tacle')
        if x != 0:
            if M[x-1][y] in [0,2,3] and (x-1,y) not in pos_joueurs_autres:
                tuiles_taclee[x-1][y] += j[1].tacle + j[1].somme_boost('tacle')
        if y != 0:
            if M[x][y-1] in [0,2,3] and (x,y-1) not in pos_joueurs_autres:
                tuiles_taclee[x][y-1] += j[1].tacle + j[1].somme_boost('tacle')
    
    # On retire pour chaque case au tacle, la fuite du perso #
    for i in range(len(tuiles_taclee)):
        for j in range(len(tuiles_taclee[i])):
            tuiles_taclee[i][j] -= fuite
            if tuiles_taclee[i][j] < 0:
                tuiles_taclee[i][j] = 0
    
    
    start = Tile(start[0], start[1], start[0], start[1])
    start.T += tuiles_taclee[start.x][start.y]*10
    OL = [start]                    # Open list 
    ol = [(start.x,start.y)]        # Open list des coordonnées 
    OL2 = [start]                    # Open list 
    ol2 = [(start.x,start.y)]        # Open list des coordonnées
    CL2 = []                         # Close list 
    cl2 = []                         # Close list des coordonnées
    CL = []                         # Close list 
    cl = []                         # Close list des coordonnées
    pm_range = []                   # Liste coordonnées des cases possibles
    pm_range_avec_tacle = []        # Liste coordonnées des cases possibles en prenant en compte le tacle
    
    while len(OL) != 0:
        # Tant que OL non vide, on prend la première tuile de OL #
        tile,i = OL[0],0
        x,y = tile.x, tile.y
        
        if (x,y) in cl:
            OL.pop(i)
            ol.pop(i)
            continue
        
        if tile.G > pm*10:
            OL.pop(i)
            ol.pop(i)
            continue
        
        # On créer une liste des cases voisines qui auront cette tuile comme parent #
        voisinage = []
        if x != len(M)-1:
            if M[x+1][y] in [0,2,3] and (x+1,y) not in pos_joueurs:  # Si la case n'est pas un mur/vide/Joueur #
                if (x+1,y) not in cl:   # Si la case n'est pas déjà dans la CL #
                    voisinage.append(Tile(x+1,y,x,y))
        if y != len(M[0])-1:
            if M[x][y+1] in [0,2,3] and (x,y+1) not in pos_joueurs:
                if (x,y+1) not in cl:
                    voisinage.append(Tile(x,y+1,x,y))
        if x != 0:
            if M[x-1][y] in [0,2,3] and (x-1,y) not in pos_joueurs:
                if (x-1,y) not in cl:
                    voisinage.append(Tile(x-1,y,x,y))
        if y != 0:
            if M[x][y-1] in [0,2,3] and (x,y-1) not in pos_joueurs:
                if (x,y-1) not in cl:
                    voisinage.append(Tile(x,y-1,x,y))
                    
        # On update les G,H,F des cases voisines #      
        for j in range(len(voisinage)):
            voisinage[j].update((0,0),tile.G, tile.T)
            # Si elles ne sont pas déjà dans l'OL, on les ajoute au voisinage #
            if (voisinage[j].x,voisinage[j].y) not in ol :
                OL.append(voisinage[j])
                ol.append((voisinage[j].x, voisinage[j].y))
        
        # On retire la tuile étudiée de l'OL et on la met dans la CL #        
        CL.append(OL.pop(i))
        cl.append(ol.pop(i))
                    
    while len(OL2) != 0:
        tile2,i2 = OL2[0],0
        x2,y2 = tile2.x, tile2.y
      
        if (x2,y2) in cl2:
            OL2.pop(i2)
            ol2.pop(i2)
            continue
     
        if tile2.F > pm*10 and tile.G > pm*10:
            OL2.pop(i2)
            ol2.pop(i2)
            continue
             
        voisinage2 = []
        if x2 != len(M)-1:
            if M[x2+1][y2] in [0,2,3] and (x2+1,y2) not in pos_joueurs:  # Si la case n'est pas un mur/vide/Joueur #
                if (x2+1,y2) not in cl2:   # Si la case n'est pas déjà dans la CL #
                    t = Tile(x2+1,y2,x2,y2)
                    #t.futurT += tuiles_taclee[x2+1][y2]*10
                    voisinage2.append(t)
        if y2 != len(M[0])-1:
            if M[x2][y2+1] in [0,2,3] and (x2,y2+1) not in pos_joueurs:
                if (x2,y2+1) not in cl2:
                    t = Tile(x2,y2+1,x2,y2)
                    #t.futurT += tuiles_taclee[x2][y2+1]*10
                    voisinage2.append(t)
        if x2 != 0:
            if M[x2-1][y2] in [0,2,3] and (x2-1,y2) not in pos_joueurs:
                if (x2-1,y2) not in cl2:
                    t = Tile(x2-1,y2,x2,y2)
                    #t.futurT += tuiles_taclee[x2-1][y2]*10
                    voisinage2.append(t)
        if y2 != 0:
            if M[x2][y2-1] in [0,2,3] and (x2,y2-1) not in pos_joueurs:
                if (x2,y2-1) not in cl2:
                    t = Tile(x2,y2-1,x2,y2)
                    #t.futurT += tuiles_taclee[x2][y2-1]*10
                    voisinage2.append(t)
                
        
        for j in range(len(voisinage2)):
            voisinage2[j].update((0,0),tile.G, tile.T, 'tile.futurT')
            # Si elles ne sont pas déjà dans l'OL, on les ajoute au voisinage #
            if (voisinage2[j].x,voisinage2[j].y) not in ol2 :
                OL2.append(voisinage2[j])
                ol2.append((voisinage2[j].x, voisinage2[j].y))
        
        CL2.append(OL2.pop(i2))
        cl2.append(ol2.pop(i2))
              
    
    cl.pop(0)
    for t in cl:
        pm_range.append(t)
    cl2.pop(0)
    for t in cl2:
        pm_range_avec_tacle.append(t)
    pm_no_range = [pos for pos in pm_range if pos not in pm_range_avec_tacle]
       
    return pm_range_avec_tacle, pm_no_range     
   
def pathfinding_po(M, groupePerso, joueur, sort_selected, pos_ciblee = None):
    ''' Renvoie la liste des coordonnées des chemins possibles en fonction de
    la Map, la position de départ et le nombre de po et le type de zone. Renvoie liste vide si pas de chemin. '''
    bPo = 0
    po_min = joueur.S[sort_selected].po_min
    if joueur.S[sort_selected].po_modifiable:
        bPo = joueur.somme_boost('po') + joueur.S[sort_selected].somme_boost('po')
    po = joueur.S[sort_selected].po + bPo
    if po < 1:
        po = po_min
    ldv = joueur.S[sort_selected].ldv
    po_min = joueur.S[sort_selected].po_min
    zone_tire = joueur.S[sort_selected].zone_tire
    cibles = joueur.S[sort_selected].type_cibles
    if pos_ciblee != None:
        (x,y) = pos_ciblee
    else:
        (x,y) = joueur.pos
    pos_joueurs = [perso.pos for perso in groupePerso]
    if (x,y) in pos_joueurs:
        pos_joueurs.remove((x,y))

    po_range = []                   # Liste des coordonnées des cases possibles
    po_range_novisible = []         # Liste des coordonnées sans ldv
    
    dico_zone_tire = {'cercle' : 0, 'croix' : 1, 'diago' : 2, 'étoile' : 3}
    type_cibles = {'ennemis' : 0, 'alliés' : 1, 'alliés sans moi' : 2, 'invocs' : 3, 'mes invocs' : 4, 'mes invocs et moi' : 5, 'tout' : 6, 'moi' : 7, 'tout sans moi' : 8, 'vide' : 9}
 
    
    if cibles == 'moi':
        return [(x,y)], po_range_novisible
    
    if cibles in ['alliés', 'mes invocs et moi', 'tout', 'moi']: # moi #
        po_min = 0
        po_range.append((x,y))    
            
    if zone_tire in ['cercle', 'diago', 'étoile']:   # Diago #
        for i in range(1,po//2+1):
            if x+i >= 0 and y+i >=0 and x+i < len(M) and y+i < len(M[0]):
                if M[x+i][y+i] != 1:
                    if (x+i,y+i) in pos_joueurs:
                        po_range.append((x+i,y+i))
                        if ldv:
                            break
                    elif M[x+i][y+i] in [0,2,3]:
                        po_range.append((x+i,y+i))
                else:
                    if ldv:
                        break
            else:
                break
        for i in range(1,po//2+1):
            if x-i >= 0 and y+i >=0 and x-i < len(M) and y+i < len(M[0]):
                if M[x-i][y+i] != 1:
                    if (x-i,y+i) in pos_joueurs:
                        po_range.append((x-i,y+i))
                        if ldv:
                            break
                    elif M[x-i][y+i] in [0,2,3]:
                        po_range.append((x-i,y+i))
                else:
                    if ldv:
                        break
            else:
                break
        for i in range(1,po//2+1):
            if x+i >= 0 and y-i >=0 and x+i < len(M) and y-i < len(M[0]):
                if M[x+i][y-i] != 1:
                    if (x+i,y-i) in pos_joueurs:
                        po_range.append((x+i,y-i))
                        if ldv:
                            break
                    elif M[x+i][y-i] in [0,2,3]:
                        po_range.append((x+i,y-i))
                else:
                    if ldv:
                        break
            else:
                break
        for i in range(1,po//2+1):
            if x-i >= 0 and y-i >=0 and x-i < len(M) and y-i < len(M[0]):
                if M[x-i][y-i] != 1:
                    if (x-i,y-i) in pos_joueurs:
                        po_range.append((x-i,y-i))
                        if ldv:
                            break
                    elif M[x-i][y-i] in [0,2,3]:
                        po_range.append((x-i,y-i))
                else:
                    if ldv:
                        break
            else:
                break
                  
    if zone_tire in ['cercle', 'croix', 'étoile']:   # Lignes #
        for i in range(1,po+1):
            if x+i >= 0 and y >=0 and x+i < len(M) and y < len(M[0]):
                if M[x+i][y] != 1:
                    if (x+i,y) in pos_joueurs:
                        po_range.append((x+i,y))
                        if ldv:
                            break
                    elif M[x+i][y] in [0,2,3]:
                        po_range.append((x+i,y))
                else:
                    if ldv:
                        break
            else:
                break
        for i in range(1,po+1):
            if x-i >= 0 and y >=0 and x-i < len(M) and y < len(M[0]):
                if M[x-i][y] != 1:
                    if (x-i,y) in pos_joueurs:
                        po_range.append((x-i,y))
                        if ldv:
                            break
                    elif M[x-i][y] in [0,2,3]:
                        po_range.append((x-i,y))
                else:
                    if ldv:
                        break
            else:
                break
        for i in range(1,po+1):
            if x >= 0 and y+i >=0 and x < len(M) and y+i < len(M[0]):
                if M[x][y+i] != 1:
                    if (x,y+i) in pos_joueurs:
                        po_range.append((x,y+i))
                        if ldv:
                            break
                    elif M[x][y+i] in [0,2,3]:
                        po_range.append((x,y+i))
                else:
                    if ldv:
                        break
            else:
                break
        for i in range(1,po+1):
            if x >= 0 and y-i >=0 and x < len(M) and y-i < len(M[0]):
                if M[x][y-i] != 1:
                    if (x,y-i) in pos_joueurs:
                        po_range.append((x,y-i))
                        if ldv:
                            break
                    elif M[x][y-i] in [0,2,3]:
                        po_range.append((x,y-i))
                else:
                    if ldv:
                        break
            else:
                break
        
        if po_min > 1:              # On retire les cases qui sont avant la po_min #
            pos_to_remove = []
            for pos in po_range:
                if abs(pos[0]-joueur.pos[0]) + abs(pos[1] - joueur.pos[1]) < po_min:
                    pos_to_remove.append(pos)
            for pos in pos_to_remove:
                po_range.remove(pos)
        
    if zone_tire in ['cercle']:     # Cercle #
        blocks = []
        for i in range(x-po,x+po+1):
            for j in range(y-po,y+po+1):
                if i >= 0 and j >=0 and i < len(M) and j < len(M[0]):
                    if (M[i][j] == 1 or (i,j) in pos_joueurs) and ldv:
                        blocks.append((i,j))
                else:
                    continue
        
        angles = []
        for block in blocks:
            thetas = []
            for i in [-0.5,0.5]:
                for j in [-0.5,0.5]:
                
                    Y,X = (block[1]+j-y), (block[0]+i-x)
                    theta = -np.arctan(Y/X) + np.pi/2
                    if X < 0 :
                        theta += np.pi
          
                    thetas.append(theta)
            thetamax = max(thetas)
            thetamin = min(thetas)
            if thetamax - thetamin > np.pi: # Si on se trouve à la limite 0/2Pi, la zone cachée n'est pas celle entre thetamax et thetamin #
                thetas.remove(thetamax)
                thetas.remove(thetamin)
                angles.append((min(thetas), max(thetas), abs(block[0]-x) + abs(block[1]-y)))
            else:
                angles.append((thetamin, thetamax, abs(block[0]-x) + abs(block[1]-y)))
                    
        for i in range(x-po,x+po+1):
            for j in range(y-po,y+po+1):
                if i >= 0 and j >=0 and i < len(M) and j < len(M[0]):    
                    x2,y2 = i, j
                    visible = False
                    if po >= abs(x2-x) + abs(y2-y) and x2 != x and y2 != y and M[x2][y2] in [0,2,3]:
                        theta = -np.arctan((y2-y)/(x2-x)) + np.pi/2
                        if x2-x < 0:
                            theta += np.pi
                        
                        visible = True
                        d = abs(x2-x) + abs(y2-y)
                        for angle in angles:
                            if d > angle[2]:
                                if angle[1]-angle[0] >= np.pi: # On gère le cas où il on doit passer de 2Pi à 0 pour la zone cachée #
                                    if theta > angle[1] or theta < angle[0]:
                                        visible = False
                                        break
                                elif theta < angle[1] and theta > angle[0]:
                                     visible = False
                                     break

                    if visible:
                        if (x2,y2) not in po_range:
                            po_range.append((x2,y2))
                
                else:
                    continue
        cl = []
        for pos in po_range:
            if pos not in cl:
                cl.append(pos)
            if abs(pos[0] - x) + abs(pos[1] - y) < po_min:
                cl.remove(pos)
        po_range = cl
                
    if cibles == 'vide':     # Vide #
        for pos in pos_joueurs:
            if pos in po_range:
                po_range.remove(pos)
    
    # Ajout des zones sans po #
    if zone_tire == 'cercle':
        for i in range(len(M)):
            for j in range(len(M[0])):
                if abs(i - x) + abs(j - y) <= po:
                    if (i,j) not in po_range:
                        if M[i][j] in [0,2,3]:
                            po_range_novisible.append((i,j))
    
    if zone_tire == 'croix':
        for i in range(1,po+1):
            if x+i >= 0 and y >=0 and x+i < len(M) and y < len(M[0]):
                if (x+i,y) not in po_range:
                    if M[x+i][y] in [0,2,3]:
                        po_range_novisible.append((x+i,y))
        for i in range(1,po+1):
            if x-i >= 0 and y >=0 and x-i < len(M) and y < len(M[0]):
                if (x-i,y) not in po_range:
                    if M[x-i][y] in [0,2,3]:
                        po_range_novisible.append((x-i,y))
        for i in range(1,po+1):
            if x >= 0 and y+i >=0 and x < len(M) and y+i < len(M[0]):
                if (x,y+i) not in po_range:
                    if M[x][y+i] in [0,2,3]:
                        po_range_novisible.append((x,y+i))
        for i in range(1,po+1):
            if x >= 0 and y-i >=0 and x < len(M) and y-i < len(M[0]):
                if (x,y-i) not in po_range:
                    if M[x][y-i] in [0,2,3]:
                        po_range_novisible.append((x,y-i))
                        
    if zone_tire == 'diago':
        for i in range(1,po//2+1):
            if x+i >= 0 and y+i >=0 and x+i < len(M) and y+i < len(M[0]):
                if (x+i,y+i) not in po_range:
                    if M[x+i][y+i] in [0,2,3]:
                        po_range_novisible.append((x+i,y+i))
        for i in range(1,po//2+1):
            if x-i >= 0 and y+i >=0 and x-i < len(M) and y+i < len(M[0]):
                if (x-i,y+i) not in po_range:
                    if M[x-i][y+i] in [0,2,3]:
                        po_range_novisible.append((x-i,y+i))
        for i in range(1,po//2+1):
            if x+i >= 0 and y-i >=0 and x+i < len(M) and y-i < len(M[0]):
                if (x+i,y-i) not in po_range:
                    if M[x+i][y-i] in [0,2,3]:
                        po_range_novisible.append((x+i,y-i))
        for i in range(1,po//2+1):
            if x-i >= 0 and y-i >=0 and x-i < len(M) and y-i < len(M[0]):
                if (x-i,y-i) not in po_range:
                    if M[x-i][y-i] in [0,2,3]:
                        po_range_novisible.append((x-i,y-i))
    
    # On retire les doublets de positions s'il y en a #
    clean_po_range = []
    clean_po_range_novisible = []
    for pos in po_range:
        if pos not in clean_po_range:
            clean_po_range.append(pos)
    for pos in po_range_novisible:
        if pos not in clean_po_range_novisible:
            clean_po_range_novisible.append(pos)
        
    if po_min > 1:
        range_to_remove = []
        range_novisible_to_remove = []
        for (i,j) in clean_po_range:
            if abs(i - x) + abs(j - y) < po_min:
                if (i,j) in range_to_remove:
                    range_to_remove.append((i,j))
        for (i,j) in clean_po_range_novisible:
            if abs(i - x) + abs(j - y) < po_min:
                if (i,j) in clean_po_range_novisible:
                    range_novisible_to_remove.append((i,j))
        for pos in range_to_remove:
            clean_po_range.remove(pos)
        for pos in range_novisible_to_remove:
            clean_po_range_novisible.remove(pos)
    
    return clean_po_range, clean_po_range_novisible
