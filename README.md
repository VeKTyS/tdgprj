# Projet SM601 - Ordonnancement

## Description
Ce projet vise à développer un programme capable de lire un tableau de contraintes, construire un graphe d'ordonnancement, et calculer différents paramètres tels que les calendriers au plus tôt et au plus tard, les marges et les chemins critiques.

## Fonctionnalités
- Lecture d'un tableau de contraintes à partir d'un fichier `.txt`
- Construction du graphe d'ordonnancement 
- Vérification des propriétés du graphe (absence de circuits et d'arcs à valeur négative)
- Calcul des rangs des sommets
- Calcul des calendriers au plus tôt et au plus tard
- Calcul des marges et des chemins critiques
- Affichage des résultats sous forme lisible (matrices, listes, etc.)

## Technologies
Le projet peut être implémenté en **C, C++, Python ou Java**. Chaque membre de l'équipe doit maîtriser le langage choisi.

## Utilisation
1. Placez un fichier `.txt` contenant le tableau de contraintes dans le dossier du projet.
2. Lancez le programme et suivez les instructions affichées.
3. Consultez les résultats affichés ou enregistrés sous forme de fichiers de traces d'exécution.

## Format du fichier de contraintes
Le fichier `.txt` doit suivre ce format :
```
1 9 
2 2 
3 3 2
4 5 1
5 2 1 4
6 2 5
7 2 4
8 4 4 5
9 5 4
10 1 2 3
11 2 1 5 6 7 8
```
Où chaque ligne correspond à une tâche avec son identifiant, sa durée et ses prédécesseurs.


## Auteurs
- VONG Lucas
- MARLIN Maceo
- WANG Leo
- REN Jonathan
- HAING AAlex

## Licence
Ce projet est réalisé dans le cadre du cours SM601 à l'EFREI Paris Panthéon-Assas Université.
