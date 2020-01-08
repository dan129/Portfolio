# Project Title

Project Scout

## Getting Started

Nous avons utilisé 2 base de données différentes en raison de nos  types de données insérées. D’une part, nous avons choisi Neo4j en raison des liaisons entre nos données. Étant donnée que la relation entre deux planètes  est le facteur  primordiale  sur notre décision , nous avons opté sur ce modèle de base de données Graphe. De plus, comme l’énoncé stipule de déterminer le chemin optimal entre deux planètes , l’algorithme Dijkstra’s  intégrée en Neo4j permet de répondre a ce problème avec efficience. 

De nos jours, la plupart des données existent sous la forme de la relation entre différents objets et plus souvent, la relation entre les données a plus de valeur que les données elles-mêmes. Contrairement aux autres bases de données, les bases de données graphiques stockent les relations et les connexions en tant qu'entités de première classe.


De l’autre part , étant donnée qu’il restait comme possibilité (MongoDB, Berkeley) nous avons utilisé MongoDB en raison de son approche de type « Document oriented ». Cette distinction offre une souplesse sur l’ajout de field (attributs) facultatif. Par exemple l’attribut « raison » était nécessaire uniquement lorsque le type d’entrée du journal était  de type anormale. De ce fait , l’ajout de champs n’influençait pas les autres entrées.  Cette plus-value offerte par MongoDB permit de conclure notre choix. 

### Prerequisites for Deployment Ubuntu


```
sudo  neo4j start
Start MongoConsole
```

### Prerequisites for Indexing


```
MONGODB INDEX: Index sur la date , Index sur le statut.

scout_db.Journal.createIndex({date:-1}).

scout_db.Journal.createIndex({status:1}).



NEO4J INDEX: Index sur la date ,nameGalaxie, name.

CREATE INDEX ON:Planete(name).

CREATE INDEX ON:Planete(date).

CREATE INDEX ON:Planete(nameGalaxie).

```
### Examples of Data Structures


```
Structure Neo4j Exemple :
id: 5dfbd57ae13a431c697a4e19
date : "2001-06-05"
statut:"Exploration"
createur:"ilias"

Structure Neo4j Exemple :
<id>:1 
dateFK:2001-06-05
habitable:true
name:Saturn
nameGalaxie:Milky way
namePlaneteProximite:["Jupiter"]
photo:[object Object]


```

## Built With

* [Neo4j](https://neo4j.com) - GRAPH Database
* [MongoDB](https://www.mongodb.com/) - Document Oriented  JSON Database


## Authors

* **Mohamed Ilias** 
* **Dan Munteanu**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

*  Frederic Theriault
