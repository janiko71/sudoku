import operator
import time
import pprint
import sys

grille = []
nb_iter = 0
FULL = [1, 2, 3, 4, 5, 6, 7, 8, 9]
DEBUG = False


'''
    ========================================================
      Définition d'une classe 'Grille de Sudoku'
    ========================================================
'''

class Grille:

    '''
        On crée une classe Grille, histoire d'utiliser les classes en Python
        et de faire un travail un peu plus propre qu'avec de simples variables,
        notamment parce qu'il y a plusieurs fonctions qu'il est utile de rattacher
        à "l'objet" grille.

        Il n'y a qu'un seul attribut, qui est la liste des valeurs de la grille. 

        La liste est renseignée d'après un fichier texte, et a une longeur de 81 (9x9).
        Elle contient, pour chaque case, une valeur de 0 à 9 :

            - 0 si la case n'est pas renseignée ;
            - Sinon la valeur de la case (de 1 à 9)

    '''

    def __init__(self, item_list):

        #
        # Initialisation de la grille
        #

        self.item = []
        for i in item_list:
            self.item.append(i)


    def __str__(self):

        #
        # Affichage standard de la grille, sous forme lisible
        #

        return self.joli_print()


    def joli_print_brut(self):

        #
        # Fonction d'affichage réelle de la grille, sous la forme d'un tableau 9x9 (forme brute)
        #

        for i in range(0,9):
            lg = " "
            lg = lg + " ".join(str(self.item[i*9+j]) for j in range (0,9))
            print(lg)

        return


    def joli_print(self):

        #
        # Fonction d'affichage améliorée, avec des lignes séparatrices
        #

        disp = ""
        for i in range(0,9):
            if ((i % 3) == 0):
                disp += "------------+-----------+------------\n"
            disp += "! "
            for j in range (0,9):
                disp += " " + str(self.item[i*9+j]) + " "
                if (j % 3) == 2:
                    disp += ' ! '
            disp += "\n"
        disp += "------------+-----------+------------\n"
        return disp


    def ligne(self, i):
        
        #
        # Renvoie le contenu de la ligne 'i', sous forme de liste
        #

        lg = []
        lg = self.item[i*9:i*9+9]
        return (lg)


    def colonne(self, j):

        #
        # Renvoie le contenu de la colonne 'i', sous forme de liste
        #

        col = []
        col = self.item[j:j+80:9]
        return col


    def bloc_xy(self, i, j):

        #
        # Renvoie le contenu du bloc entourant la position cartésienne (i,j), sous forme de liste
        #

        bloc = []
        pos = (int(i // 3) * 3) * 9 + (int(j // 3) * 3)
        bloc = self.item[pos:pos+3] + self.item[pos+9:pos+12] + self.item[pos+18:pos+21]

        return bloc


    def bloc_index(self, index):

        #
        # Renvoie le contenu du bloc entourant la case en position 'index', sous forme de liste
        #

        return self.bloc_xy((index // 3) * 3, (index % 3) * 3)


    def coord(self, pos):

        # 
        # Renvoie la coordonnées cartésienne (sous forme x,y) d'une position (qui est donc un index de liste)
        #

        return (pos // 9, pos % 9)


    def cherche_ordre(self):

        # 
        # Fonction servant à déterminer l'ordre de recherche des cases restantes.
        #
        # Pour cela, on regarde, pour les cases non encore renseignées, quels sont les nombres de 1 à 9 pouvant
        # y être placés. On les classe ensuite par ordre croissant ; ainsi, cela permet de savoir quelles sont 
        # les cases les plus faciles à remplir, ce qui permet de minimiser la profondeur de recherche récursive
        # en minimisant le nombre de combinaisons testées.
        #
        # Le tableau retourné n'indique pas le nombre de possibilités, mais uniquement l'ordre des cases, 
        # en excluant les cases déjà remplies.
        #

        possibilite_grille = {}

        for pos in range(0,81):

            # On examine le nombre de possibilités pour la case donnée.
            nb_possibilites = 0

            # Si la case est remplie (valeur non nulle), c'est 0 ! 
            # Sinon on teste les nombres de 1 à 9, on regarde si on pourrait le mettre dans la case (ou pas)
            if (self.item[pos] == 0):

                # Case non remplie, donc on regarde (pour la case en position 'pos')
                for num in range(1,10):

                    # On vérifie si on peut utiliser 'num' dans la case 'pos'
                    if (self.est_possible(num, pos)):
                        nb_possibilites += 1

                # finalement...
                possibilite_grille[pos] = nb_possibilites

        # On a récupéré, pour chaque case, le nombre de choix possibles. 
        # On trie ce résultat selon le nombre de possibilités.

        ordre_cellules = []

        for possibilite in sorted(possibilite_grille.items(), key=operator.itemgetter(1)):
            cellule, poss = possibilite
            ordre_cellules.append(cellule)

        return ordre_cellules


    def est_resolu(self):

        # 
        # Fonction de vérification de résolution. Retourne vrai si chaque nombre de 1 à 9
        # est présent un et une seule fois dans chaque ligne, chaque colonne, et chaque bloc.
        #
        # Note importante
        # ---------------
        #
        # On crée de nouveaux objets à chaque fois par un ... = []
        # En effet, en Python, lorsqu'on affecte t2 = t1 pour des listes, tableaux, etc., 
        # c'est la référence à l'objet qui est passée, et non le contenu.
        # Si, dans l'exemple précédent on modifie t2, alors on modifie aussi t1 !
        # Et un tri modifie la liste sur laquelle il s'opère...
        #

        # Vérification des lignes
        for i in range(0,9):
            lig = []
            lig = self.ligne(i)
            lig.sort()
            if (lig != FULL):
                return False

        # Vérification des colonnes
        for j in range(0,9):
            col = []
            col = self.colonne(j)
            col.sort()
            if (col != FULL):
                return False

        # Vérification des carrés
        for c in range(0,9):
            car = []
            car = self.bloc_index(c)
            car.sort()
            if (car != FULL):
                return False

        # Si on est ici, c'est que toutes les conditions sont remplies
        return True


    def est_possible(self, num, pos):

        #
        # On regarde, dans la grille donnée, si le nombre 'num' peut être mis à la position 'pos'.
        #

        # Il ne doit apparaître :
        #   1) Ni dans la ligne de la case 'pos' considérée ;
        #   2) Ni dans la colonne ;
        #   3) Ni dans la bloc entourant la case.

        lig, col = self.coord(pos)
        if (num not in self.ligne(lig)) and (num not in self.colonne(col) and (num not in self.bloc_xy(lig, col))):
            if (DEBUG):
                print("On peut mettre {} dans la grille à la position ({}, {}).".format(num, lig, col))
            return True
        else:
            return False



'''
    =====================================================================
      Fonction de lecture de la grille de Sudoku
    =====================================================================
'''
def lecture_fichier(nom_fichier):

    # 
    # On transforme le fichier grille en entrée en un tableau d'entiers
    # Règle : un entier représente une case connue, et n'importe quel autre caractère (sauf espace et retour chariot) une case inconnue
    #

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

    return Grille(grille)


'''
    =====================================================================
      Fonction globale de résolution de la grille de Sudoku
    =====================================================================
'''
def cherche(grille):

    # 
    # Fonction de recherche de solution.
    #
    # Paramètre en entrée : 
    #
    #   - La grille en cours de résolution.
    #   - L'ordre des cases à examiner, afin de minimiser la profondeur de la recherche.
    #
    # Si la grille est remplie, on a terminé. On sort de la boucle infernale.
    #
    # Sinon, on calcule l'ordre des cases à examiner, afin de minimiser la profondeur de la recherche.
    #
    # On va ensuite prendre la grille en cours, et tenter de remplir les cases, dans l'ordre 
    # donné par la liste 'ordre'. On va commencer par la 1ère dans la liste,
    # puis on va relancer la fonction de recherche avec cette nouvelle grille.
    #
    # Il pourra se passer deux choses :
    #
    #   - Soit on arrive sur une grille complète, et on a terminé.
    #   - Soit on arrive à une impasse : on n'arrive pas à remplir la case en cours. On effectue
    #      alors un retour arrière (backtrack). Cela revient à remonter d'un niveau de profondeur,
    #      et de regarder la possibilité suivante pour la case précédente.
    #

    global nb_iter
    nb_iter += 1

    # Affichage/débogage si besoin

    if (nb_iter % 5000) == 0:
        print(nb_iter, 'essais')
    if (DEBUG):
        print("({})".format(nb_iter))
        grille.joli_print()
        print()

    if (grille.est_resolu()):

        # La grille est complète : on a gagné !

        print('='*40)
        print('SOLUTION TROUVEE ({} itérations) :'.format(nb_iter))
        print('='*40)
        print()
        print(grille)

        return

    else:

        # Grille incomplète. Donc on va tenter, par récursivité, de résoudre le problème.
        # 
        # Pour cela, on va tenter de remplir les cases non remplies, selon l'ordre défini
        # par la liste 'ordre' qu'on a calculée auparavant et qu'on a passée en paramètre.
        #
        # Si on trouve qu'un nombre est possible, on le met à la position en cours, on 
        # recalcule l'ordre des cases à remplir (pour optimiser le calcul), et on relance 
        # la recherche avec une grille qui aura donc une case de moins à trouver.

        ordre = grille.cherche_ordre()
        
        if (DEBUG):
            print(ordre)

        for ind in ordre:

            # on examine chacune des cases de la liste 'ordre', pour voir si on peut les remplir.
            for num in range(1,10):

                if (grille.item[ind] == 0):

                    # On ne regarde que les cases non encore renseignées, ce qui devrait être le cas
                    # pour les cases incluses dans 'ordre'. 

                    if (grille.est_possible(num, ind)):

                        # Oui, c'est possible. On peut (pour l'instant) ajouter num dans la case indexée 'ind'.
                        # On relance la recherche sur une NOUVELLE grille (= un nouvel objet Python)
                        new_grille = Grille(grille.item)
                        if (DEBUG):
                            print('grille    ', id(grille))
                            print('new_grille', id(new_grille))
                        new_grille.item[ind] = num

                        cherche(new_grille)

                else:

                    # Pas possible de caser num ? Alors on fait un 'break' car on est dans une impasse.
                    # On va alors remonter (donc revenir en arrière) car cela signifie que la recherche 
                    # précédente (en profondeur) a testé un choix amenant sur un impasse, il faut donc
                    # y revenir et faire un autre choix (s'il en existe)
                    break

            # utilité du break ?
            break

        if (DEBUG):
            print("Fin des recheches (infructueuses)")

    return False


'''
    =====================================================================

       Corps du programme

    =====================================================================
'''

DEFAULT_FILE_NAME = "1.txt"

#
# On demande en imput (ou en argument de ligne de commande) le nom du fichier, avec ou sans extension '.txt' (qui est ajoutée automatiquement)
#
nb_arg = len(sys.argv) - 1
print(nb_arg)

if (nb_arg == 1):
    file_name = sys.argv[1]
else:    
    file_name = input("Nom du fichier (grille), sans .txt [{}]: ".format(DEFAULT_FILE_NAME))

# On rajoute le '.txt' pour les noms de fichiers n'en ayant pas.    
if (len(file_name) == 0):
    file_name = str(DEFAULT_FILE_NAME)
else:
    if (len(file_name) < 4):
        file_name += ".txt"
    elif (file_name[-4:] != ".txt"):
        file_name += ".txt"

#
# On crée ensuite la grille initiale
#   
#       
grille = lecture_fichier(file_name)
print("\nGrille initiale")
print(grille)
print()

# Précaution devenue inutile après diverses optimisations
#sys.setrecursionlimit(99999)

if (grille.est_resolu()):
    print("La grille en entrée est déjà terminée ! Il n'y a rien à faire !")
    exit()

#
# On effectue la recherche. 
#

print('On démarre la recherche...\n')
t0 = time.time()
cherche(grille)
t1 = time.time() 
print("Problème résolu en {:6f} secondes.\n".format(t1 - t0))

# Fin

