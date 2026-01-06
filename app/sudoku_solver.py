"""Résolution de grille de Sudoku.

    ========================================================
      Présentation générale du programme
    ========================================================

    Principe
    --------
    On applique un algorithme de *backtracking* simple :
        1) Chercher la prochaine case vide (valeur 0).
        2) Tester les valeurs 1 à 9 et vérifier ligne, colonne et bloc 3x3.
        3) Si une valeur est valide, la placer et continuer récursivement.
        4) Si aucune ne convient, revenir en arrière (backtrack) et essayer
           une nouvelle possibilité.

    Ce module fournit :
        - un parseur tolérant pour lire une grille (fichier ou saisie) ;
        - un solveur par backtracking qui modifie la grille sur place ;
        - un formateur pour afficher proprement la grille ;
        - une interface CLI : `python -m app.sudoku_solver [chemin_du_fichier]`;
        - une recherche de toutes les solutions avec mesure du temps pour la
          première et le total.

    Format attendu
    --------------
        - 9 lignes de 9 cases ;
        - chiffres 1-9 pour les valeurs connues ;
        - "." ou "0" pour les cases vides ;
        - les espaces et séparateurs (|, -, etc.) sont ignorés, ce qui autorise
          des lignes comme "..1 23. 8.6".
"""

from __future__ import annotations

import argparse
import sys
import time
from typing import Iterable, List, Tuple


Grid = List[List[int]]


def _clean_values(lines: Iterable[str]) -> Grid:
    """
        ========================================================
          Lecture tolérante : lignes brutes -> grille 9x9
        ========================================================

        Idée générale
        -------------
        - Parcourir chaque caractère fourni.
        - Conserver uniquement les chiffres 1-9, et traduire "." ou "0" en case
          vide (valeur 0).
        - Ignorer les espaces et tout séparateur (|, -, etc.) pour rester
          permissif.
        - Vérifier que le résultat comporte bien 81 cases.
    """

    digits = []

    for line in lines:
        for char in line.strip():
            if char.isdigit() and char != "0":
                digits.append(int(char))

            elif char in {".", "0"}:
                digits.append(0)

            elif char.isspace():
                #
                # Les espaces sont ignorés (permet des grilles aérées)
                #
                continue

            else:
                #
                # Les autres séparateurs sont simplement sautés pour tolérer
                # les mises en forme « jolies » des grilles.
                #
                continue

    if len(digits) != 81:
        raise ValueError(
            f"La grille doit contenir 81 cases après nettoyage (reçu {len(digits)})."
        )

    grid: Grid = [digits[i : i + 9] for i in range(0, 81, 9)]
    return grid


def _find_empty(grid: Grid) -> Tuple[int, int] | None:
    """
        ========================================================
          Recherche d'une case vide (0) dans la grille
        ========================================================

        Retour :
            - un tuple (ligne, colonne) pour la première case vide trouvée ;
            - None si la grille est déjà complète.
    """

    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col

    return None


def _is_valid(grid: Grid, row: int, col: int, value: int) -> bool:
    """
        ========================================================
          Vérification de validité pour une case donnée
        ========================================================

        On vérifie que la valeur candidate respecte :
            - la contrainte de ligne ;
            - la contrainte de colonne ;
            - la contrainte du carré 3x3 correspondant.
    """

    #
    # Ligne et colonne
    #
    if any(grid[row][c] == value for c in range(9)):
        return False

    if any(grid[r][col] == value for r in range(9)):
        return False

    #
    # Carré 3x3
    #
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)

    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if grid[r][c] == value:
                return False

    return True


def solve(grid: Grid) -> bool:
    """
        ========================================================
          Algorithme de résolution (backtracking récursif)
        ========================================================

        Étapes :
            1) Chercher la prochaine case vide.
            2) Si aucune case vide : la grille est résolue.
            3) Essayer chaque valeur de 1 à 9 :
                - si la valeur est valide, la placer et appeler solve() ;
                - si l'appel récursif échoue, remettre 0 et tester la suivante.
    """

    empty = _find_empty(grid)

    if not empty:
        return True

    row, col = empty

    for value in range(1, 10):
        if _is_valid(grid, row, col, value):
            grid[row][col] = value

            if solve(grid):
                return True

            grid[row][col] = 0

    return False


def find_solutions(grid: Grid):
    """
        ========================================================
          Générateur : parcours de TOUTES les solutions possibles
        ========================================================

        - Parcourt récursivement la grille jusqu'à trouver une solution.
        - À chaque solution, on émet une copie indépendante pour éviter toute
          mutation ultérieure.
        - Continue la recherche afin de détecter plusieurs solutions.
    """

    empty = _find_empty(grid)

    if not empty:
        #
        # Grille complète -> on renvoie une copie profonde (ligne par ligne)
        #
        yield [row[:] for row in grid]
        return

    row, col = empty

    for value in range(1, 10):
        if _is_valid(grid, row, col, value):
            grid[row][col] = value

            yield from find_solutions(grid)

            grid[row][col] = 0


def format_grid(grid: Grid) -> str:
    """
        ========================================================
          Mise en forme « lisible » de la grille pour affichage
        ========================================================
    """

    lines = []

    for r, row in enumerate(grid):
        if r % 3 == 0 and r != 0:
            lines.append("------+-------+------")

        chunks = []

        for c, value in enumerate(row):
            if c % 3 == 0 and c != 0:
                chunks.append("|")

            chunks.append(str(value) if value else ".")

        lines.append(" ".join(chunks))

    return "\n".join(lines)


def read_from_file(path: str) -> Grid:
    """
        ========================================================
          Lecture d'une grille depuis un fichier texte
        ========================================================
    """

    with open(path, "r", encoding="utf-8") as handler:
        return _clean_values(handler.readlines())


def read_from_stdin() -> Grid:
    """
        ========================================================
          Lecture interactive depuis l'entrée standard
        ========================================================
    """

    print("Saisissez la grille (au moins 9 lignes). Laissez une ligne vide pour terminer.")

    lines = []

    while True:
        try:
            line = input(f"Ligne {len(lines) + 1}: ")
        except EOFError:
            break

        if not line.strip() and len(lines) >= 9:
            break

        lines.append(line)

    return _clean_values(lines)


def main(argv: list[str] | None = None) -> int:
    """
        ========================================================
          Point d'entrée CLI
        ========================================================

        Usage :
            python -m app.sudoku_solver [chemin_du_fichier]

        - Si le chemin est fourni, on lit la grille depuis ce fichier.
        - Sinon, on bascule en saisie interactive.
        - Les messages d'erreur sont renvoyés sur stderr pour faciliter l'usage
          en ligne de commande (redirections, etc.).
    """

    parser = argparse.ArgumentParser(description="Résout une grille de Sudoku")

    parser.add_argument(
        "path",
        nargs="?",
        help="Chemin du fichier contenant la grille. Si absent, saisie manuelle.",
    )
    args = parser.parse_args(argv)

    try:
        grid = read_from_file(args.path) if args.path else read_from_stdin()
    except Exception as exc:  # pragma: no cover - CLI UX
        print(f"Erreur de lecture de la grille: {exc}", file=sys.stderr)
        return 1

    print("\nGrille initiale:\n")
    print(format_grid(grid))

    #
    # Recherche de TOUTES les solutions, avec affichage immédiat de la première
    # puis comptage et affichage éventuel des suivantes.
    #
    start = time.perf_counter()

    solutions_count = 0
    first_solution_time = None
    extra_solutions: list[Grid] = []

    # Copie défensive pour ne pas altérer la grille affichée
    working_grid = [row[:] for row in grid]

    for solution in find_solutions(working_grid):
        solutions_count += 1

        if solutions_count == 1:
            first_solution_time = time.perf_counter() - start

            print("\nPremière solution trouvée ({} seconde(s)):\n".format(round(first_solution_time, 6)))
            print(format_grid(solution))

        else:
            # Les autres solutions seront affichées après la boucle
            extra_solutions.append(solution)

    total_time = time.perf_counter() - start

    if solutions_count == 0:
        print("Aucune solution trouvée", file=sys.stderr)
        return 2

    #
    # Affichage des solutions supplémentaires, si elles existent
    #
    for index, solution in enumerate(extra_solutions, start=2):
        print("\nSolution supplémentaire #{} :\n".format(index))
        print(format_grid(solution))

    print(
        "\nRésumé : {} solution(s) trouvée(s) en {} seconde(s).".format(
            solutions_count,
            round(total_time, 6),
        )
    )

    return 0


if __name__ == "__main__":  # pragma: no cover - exécution directe
    raise SystemExit(main())
