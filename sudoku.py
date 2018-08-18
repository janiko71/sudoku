import operator
import pprint
import sys

grille = []
nb_iter = 0
FULL = [1, 2, 3, 4, 5, 6, 7, 8, 9]
DEBUG = False
STOP = False
NB_STOPS = 99

def lecture_fichier(nom_fichier):
    '''
        On transforme le fichier grille en entrée en un tableau d'entiers
        Règle : un entier représente une case connue, et n'importe quel autre caractère (sauf espace et retour chariot) une case inconnue
    '''
    with open(nom_fichier,"r") as f:
        lignes = f.readlines()
    grille = []
    for ligne in lignes:
        lg = ligne.rstrip('\n')
        lg = lg.replace(' ','')
        if (len(lg) == 9):
            for c in lg:
                try:
                    grille.append(int(c))
                except:
                    grille.append(int(0))
        elif (len(lg) == 0):
            pass
        else:
            print('\nMauvais format de ligne (longueur attendue : 9, lue : {})\n'.format(len(lg)))
            exit()
    if len(grille) != 81:
        print('\nMauvais nombre de lignes (longueur attendue : 9, lue : {})\n'.format(len(grille)))
        exit()

    return grille


def joli_print_brut(grille):
    for i in range(0,9):
        lg = " "
        lg = lg + " ".join(str(grille[i*9+j]) for j in range (0,9))
        print(lg)
    return


def joli_print(grille):
    for i in range(0,9):
        lg = "! "
        for j in range (0,9):
            lg += " " + str(grille[i*9+j]) + " "
            if (j % 3) == 2:
                lg += ' ! '
        if ((i % 3) == 0):
            print('------------+-----------+------------')
        print(lg)
    print('------------+-----------+------------')
    return


def ligne(grille, i):
    lg = []
    lg = grille[i*9:i*9+9]
    return (lg)


def colonne(grille, j):
    col = []
    col = grille[j:j+80:9]
    return col


def carre_xy(grille, i, j):
    carre = []
    pos = (int(i // 3) * 3) * 9 + (int(j // 3) * 3)
    carre = grille[pos:pos+3] + grille[pos+9:pos+12] + grille[pos+18:pos+21]
    return carre


def carre_index(grille, index):
    return carre_xy(grille, (index // 3) * 3, (index % 3) * 3)


def coord(grille, pos):
    return (pos // 9, pos % 9)


def cherche_ordre(grille):
    possibilite_grille = {}
    for pos in range(0,81):
        nb_possibilites = 0
        # Si la case est remplie (valeur non nulle), donc aucune possibilité.
        # Sinon on teste les nombres de 1 à 9, on regarde si on pourrait le mettre dans la case
        if (grille[pos] == 0):
            l,c = coord(grille, pos)
            for num in range(1,10):
                if (num not in ligne(grille, l) and num not in colonne(grille, c) and num not in carre_xy(grille, l, c)):
                    nb_possibilites += 1
            # finalement...
            possibilite_grille[pos] = nb_possibilites
    # On trie selon le nombre de possibilités
    ordre_cellules = []
    for possibilite in sorted(possibilite_grille.items(), key=operator.itemgetter(1)):
        cellule, poss = possibilite
        ordre_cellules.append(cellule)

    return ordre_cellules


def est_resolu(grille):

    # Vérification des lignes
    for i in range(0,9):
        lig = []
        lig = ligne(grille, i)
        lig.sort()
        if (lig != FULL):
            return False

    # Vérification des colonnes
    for j in range(0,9):
        col = []
        col = colonne(grille, j)
        col.sort()
        if (col != FULL):
            return False

    # Vérification des carrés
    for c in range(0,9):
        car = []
        car = carre_index(grille, c)
        car.sort()
        if (car != FULL):
            return False

    # Si on est ici, c'est que toutes les conditions sont remplies
    return True


def est_possible(grille, num, pos):
    '''
        On regarde, dans la grille donnée, si le nombre 'num' peut être mis à la position 'pos'.
        Il ne doit apparaître ni dans sa ligne, ni dans sa colonne, ni dans le carré correspondant.
    '''
    lig = (pos // 9)
    col = (pos % 9)
    if (num not in ligne(grille, lig)) and (num not in colonne(grille, col) and (num not in carre_xy(grille, lig, col))):
        if (DEBUG):
            print("On peut mettre {} dans la grille à la position ({}, {}).".format(num, lig, col))
        return True
    else:
        return False


def cherche(grille, ordre):

    global nb_iter
    nb_iter += 1

    if (nb_iter % 5000) == 0:
        print(nb_iter, 'essais')
    if (DEBUG):
        print("({})".format(nb_iter))
        print(ordre, "-->" ,len(ordre))
        joli_print(grille)
        print()
    if (STOP):
        if (nb_iter > NB_STOPS):
            exit()

    if (est_resolu(grille)):
        print('='*40)
        print('SOLUTION TROUVEE ({} itérations) :'.format(nb_iter))
        print('='*40)
        print()
        joli_print(grille)
        print()
        exit()
    else:
        if (len(ordre) == 0):
            # On ne devrait jamais passer par ici ;)
            return False
        else:
            for ind in ordre:
                for num in range(1,10):
                    if (grille[ind] == 0):
                        if (est_possible(grille, num, ind)):
                            # Oui, c'est possible
                            new_grille = [] + grille
                            if (DEBUG):
                                print('grille    ', id(grille))
                                print('new_grille', id(new_grille))
                            new_grille[ind] = num
                            # Optimisation : au lieu de simplement retirer la case qu'on vient de remplir
                            # dans la liste des cases à traiter, on la recalcule pour repartir sur une case
                            # la plus simple possible (avec le moins de possibilités pour choisir son contenu)
                            # new_ordre = [] + ordre
                            # new_ordre.remove(ind)
                            new_ordre = cherche_ordre(new_grille)
                            cherche(new_grille, new_ordre)
                    else:
                        # pas possible de caser num ?
                        break
                # utilité du break ?
                break
        if (DEBUG):
            print("Fin des recheches (infructueuses)")

    return False


'''
    =====================================================================
      On lance la résolution
    =====================================================================
'''

DEFAULT_FILE_NAME = "1.txt"

file_name = input("Nom du fichier (grille), sans .txt [{}]: ".format(DEFAULT_FILE_NAME))
if (len(file_name) == 0):
    file_name = str(DEFAULT_FILE_NAME)
else:
    if (len(file_name) < 4):
        file_name += ".txt"
    elif (file_name[-4:] != ".txt"):
        file_name += ".txt"
grille = lecture_fichier(file_name)
print("\nGrille initiale")
joli_print(grille)
print()

sys.setrecursionlimit(99999)

ordre = []
ordre = cherche_ordre(grille)
if (DEBUG):
    print(ordre)

if (est_resolu(grille)):
    print("La grille en entrée est déjà terminée ! Il n'y a rien à faire !")
    exit()

try:
    print('On démarre la recherche...\n')
    cherche(grille, ordre)
except Exception as e:
    print(e)

