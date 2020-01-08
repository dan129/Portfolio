# README #

### Description ###

* Projet dans le cadre du cours B52 au CVM. Ce logiciel permet de trouver des synonymes ou bien des mots qui sont semblables à celui qu'on lui donne. On peut entraîner la base de donnée avec des nouveaux récits afin d'obtenir des meilleurs résultats.

### Par ###

* Dan Munteau
* Mohamed Ilias
* Maxime Denis

### Exemples de commandes à executer ###

* Entrainer la base de donnée: main.py -e -t 5 --enc utf-8 --chemin ..\textes\LesTroisMousquetairesUTF8.txt
* Rechercher un synonyme: main.py -r -t 5
* Clustering: main.py -c -t 5 -n 10 --nc 5
* Enregistrement du Clustering dans un fichier texte: main.py -c -t 5 -n 10 --nc 5 > resultats.txt
* KNN: main.py -knn -t 5 -k 5 --enc utf-8 --mots 'Belle Maison Manger'

>  -t = taille de la fenêtre utilisé lors de la recherche
> > -n = nombre de résultats qu'on veut voir
> > > --nc = nombre de clusters qu'on veut avoir
