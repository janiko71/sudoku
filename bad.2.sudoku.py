import pprint
import sys

#from functools import lru_cache

grille_depart = []
nb_it = 0
FULL = [1, 2, 3, 4, 5, 6, 7, 8, 9]

''' 
    On crée une classe spéciale, ça sera plus simple
'''
class Grille:

    def __init__(self, lignes):

        self.ligne_grille = []
        for lg in lignes:
            self.ligne_grille.append(lg)


    def __str__(self):

        return "\n".join(str(lg) for lg in self.ligne_grille)


    def colonne(self, i):

        return list(lg[i] for lg in self.ligne_grille)


    def ligne(self, i):

        return list(self.ligne_grille[i])


    def carre(self, i, j):
        # retourne le carré contenant la case (i,j), sous forme de ligne
        carre = []
        lc = int(i // 3) * 3
        cc = int(j // 3) * 3
        carre = self.ligne_grille[lc][cc:cc+3] + self.ligne_grille[lc+1][cc:cc+3] + self.ligne_grille[lc+2][cc:cc+3]
        return list(carre)


    def carre_par_numero(self, num):
        # num compris entre 0 et 8
        lc = (num // 3) * 3
        cc = (num % 3) * 3
        return self.carre(lc, cc)


    def get_element(self, i, j):
        return self.ligne_grille[i][j]


    def set_element(self, i, j, num):
        self.ligne_grille[i][j] = num


    def get_lignes(self):
        lignes = []
        for l in self.ligne_grille:
            lignes.append(l)
        return list(lignes)



def est_resolu(grille):

    '''
        Cette fonction regarde si la grille est résolue.
        Pour être résolue, il faut :

        - Qu'elle soit remplie (ce qui est vrai si chacune des 3 conditions ci-dessous est remplie) !
        - Que chaque ligne comporte chacun des chiffres de 1 à 9
        - Que chaque colonne comporte chacun des chiffres
        - Que chaque carré de 3x3 comporte chacune des chiffres
    '''
   
    for i in range(0,9):
        # Vérification des lignes
        tmp_ligne = grille.ligne(i)
        tmp_ligne.sort()
        if (tmp_ligne != FULL):
            return False
        # Vérification des colonnes
        tmp_col = grille.colonne(i)
        tmp_col.sort()
        if (tmp_col != FULL):
            return False
        # Vérification des carrés
        tmp_carre = grille.carre_par_numero(i)
        tmp_carre.sort()
        if (tmp_carre != FULL):
            return False

    # Si on est ici, c'est que toutes les conditions sont remplies
    print('-'*50)
    print("trouvé")
    print(gr)
    return True


#@lru_cache(maxsize=None)
def cherche(grille, num_depart, ligne_depart):

    global nb_it
    nb_it = nb_it + 1
    print('---------------')
    print(nb_it)
    print(grille)
    print()
    if (nb_it > 99999):
        exit()

    if (est_resolu(grille)):
        # Fin de la boucle infernale : on a trouvé ce qu'on voulait !
        exit()
    else:
        '''a = ""
        a = input()'''
        tmp_grille = Grille(grille.get_lignes())
        for num in range(num_depart, 10):
            for lg in range(ligne_depart, 9):
                print('on cherche à positionner le nombre ',str(num), ' ligne ', lg)
                if (num not in tmp_grille.ligne(lg)):
                    print("il n'est pas dans la ligne ",str(lg), tmp_grille.ligne(lg))
                    for cl in range(0,9):
                        if (num not in tmp_grille.colonne(cl)):
                            print("il n'est pas dans la colonne ", str(cl), tmp_grille.colonne(cl))
                            if (num not in tmp_grille.carre(lg, cl)):
                                print("il n'est pas dans le carré ", str(lg), str(cl), tmp_grille.carre(lg, cl))
                                new_grille = Grille(tmp_grille.get_lignes())
                                print("position possible pour ", num, " : ", lg, cl)
                                new_grille.set_element(lg, cl, num)
                                print('on retente avec la grille:')
                                print(new_grille)
                                print()
                                cherche(new_grille, num, lg+1)
                            else:
                                print("il est dans le carré ",tmp_grille.carre(lg, cl))
                                pass
                        else:
                            print("il est dans la colonne ", str(cl), tmp_grille.colonne(cl))
                            pass
                else:
                    print("il est dans la ligne ",str(lg), tmp_grille.ligne(lg))
                    pass
            print('fin test num = ', num)
            ligne_depart = 0
        print("fin cherche grille")
        ligne_depart = 0
        num_depart = 0

    return False


'''
    On transforme le fichier grille en entrée en un tableau d'entiers
    Règle : un entier représente une case connue, et n'importe quel autre caractère (sauf espace et retour chariot) une case inconnue
'''
with open("1.txt","r") as f:
    lignes = f.readlines()

nb_lignes = 0

for ligne in lignes:

    lg = ligne.rstrip('\n')
    lg = lg.replace(' ','')
    if (len(lg) > 0):
        t = []
        for c in lg:
            try:
                t.append(int(c))
            except:
                t.append(int(0))
        if (len(t) != 9):
            print('\nMauvais format de ligne (longueur attendue : 9, lue : {})\n'.format(len(t)))
            exit()
        grille_depart.append(t)

if len(grille_depart) != 9:
    print('\nMauvais nombre de lignes (longueur attendue : 9, lue : {})\n'.format(len(grille_depart)))
    exit()
 
'''
    On lance la résolution
'''

gr = Grille(list(grille_depart))
print(est_resolu(gr))
print('-'*50)
print(gr)
print('-'*50)

sys.setrecursionlimit(99999)
print("----",sys.getrecursionlimit(),"----")

try:
    cherche(gr, 1, 0)
except Exception as e:
    print(e)
