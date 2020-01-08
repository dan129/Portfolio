# README #

### Description ###

* Project TP2 dans le cadre du cours B52 au CVM.

### Par ###

* Dan Munteau
* Mohamed Ilias
* Maxime Denis

### Informations pour se connecter à Oracle ###

* Nom d'utilisateur: e1720845
* Mot de passe: ruby
* Hôte: delta.decinfo.cvm
* SID: decinfo

### ** Nous sommes passés à SQLite ** ###

### Exemples de commandes à executer ###

* Entrainer la base de donnée: main.py -e -t 5 --enc utf-8 --chemin ..\textes\LesTroisMousquetairesUTF8.txt
* Rechercher un synonyme: main.py -r -t 5
* Clustering: main.py -c -t 5 -n 10 --nc 5
* Enregistrement du Clustering dans un fichier texte: main.py -c -t 5 -n 10 --nc 5 > resultats.txt
* KNN: main.py -knn -t 5 -k 5 --enc utf-8 --mots 'Belle Maison Manger'