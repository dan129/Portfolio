package ca.qc.cvm.dba.scoutlog.dao;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import org.bson.Document;
import org.neo4j.driver.Record;
import org.neo4j.driver.Session;
import org.neo4j.driver.StatementResult;
import org.neo4j.driver.internal.value.PathValue;
import org.neo4j.driver.types.Path;
import org.neo4j.driver.types.Path.Segment;

import com.mongodb.Block;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import ca.qc.cvm.dba.scoutlog.entity.LogEntry;
/* -----------------------------------------
 *					        										    
 *    Projet synthèse : A2019	          	  
 *    Fait Par : Mohamed Ilias et Dan Munteanu		        						
 *					             								
 *---------------------------------------- */
public class LogDAO {
	/**
	 * Méthode permettant d'ajouter une entrée
	 * 
	 * Note : Ne changer pas la structure de la méthode! Elle permet de faire
	 * fonctionner l'ajout d'une entrée du journal. Il faut donc que la compléter.
	 * 
	 * @param log
	 * @return
	 */
	public static boolean addLog(LogEntry log) {
		boolean success = false;
			try {
			MongoDatabase connectionMongo = MongoConnection.getConnection();
			MongoCollection<Document> collection = connectionMongo.getCollection("Journal");
			Session connectionNeo4j = Neo4jConnection.getConnection();
			Document doc = new Document();
			
			doc.append("date", log.getDate());
			doc.append("statut", log.getStatus());
			doc.append("createur", log.getName());

			if (log.getStatus() == "Anormal")
				doc.append("raison", log.getReasons());

			if (log.getStatus() == "Exploration") {
				// a rajouter dans le readme(index sur namePlanete)
				// permet de savoir si une planete a deja ete visite
				HashMap<String, Object> parameters1 = new HashMap<String, Object>();
				parameters1.put("name", log.getPlanetName());
				String queryPlaneteExistante = "MATCH (n) WHERE n.name = $name RETURN n";
				StatementResult resultPlaneteExistante = connectionNeo4j.run(queryPlaneteExistante, parameters1);

				if (resultPlaneteExistante.hasNext()) { // si la requery retourne une planete du meme nom dans la db
					System.out.println("planete deja inscrite");
					return false;
				} else {
					HashMap<String, Object> parameters = new HashMap<String, Object>();
					parameters.put("dateFK", log.getDate());
					parameters.put("name", log.getPlanetName());
					parameters.put("habitable", log.isHabitable());
					parameters.put("nameGalaxie", log.getGalaxyName());
					parameters.put("namePlaneteProximite", log.getNearPlanets());
					parameters.put("photo", log.getImage());
					
					
					String cypherRequete = "CREATE (p:Planet {dateFK:$dateFK, name: $name,habitable: $habitable,nameGalaxie:$nameGalaxie,namePlaneteProximite:$namePlaneteProximite,photo:$photo })";
					StatementResult result = connectionNeo4j.run(cypherRequete, parameters);
					//creation des relations
					HashMap<String, Object> parametersPlanetesAvoisinante= new HashMap<String, Object>(); 
					parametersPlanetesAvoisinante.put("planete",log.getPlanetName());
					for(String planetsAvoisinantes: log.getNearPlanets()) {
						parametersPlanetesAvoisinante.put("voisin",planetsAvoisinantes);
						String queryCreationRelation = "MATCH (a {name:$planete}), (b {name:$voisin}) CREATE (a)-[:VOISIN] ->(b) ";
						StatementResult resultCreationRelation = connectionNeo4j.run(queryCreationRelation,	parametersPlanetesAvoisinante);
					}
					
				}
			}
			collection.insertOne(doc);
			success = true;

		}
		// collection
		catch (Exception e) {
			e.printStackTrace();
		}

		return success;
	}
	
	
	/*
	 * Permet de retourner les 5 dernieres entrees dans la database de Mongo
	 * 
	 * 
	 */

	public static List<String> getLast5Entries() {
		MongoDatabase connectionMongo = MongoConnection.getConnection();
		MongoCollection<Document> collection = connectionMongo.getCollection("Journal");
		FindIterable<Document> iterator = collection.find().sort(new Document("date", -1)).limit(5);
		List<String> listStatus= new ArrayList<String>();
		for (Document document : iterator) {
			listStatus.add(document.getString("statut"));
		}
		return listStatus;
	}
	
	/**
	 * Permet de retourner la liste de planétes déjé explorées
	 * 
	 * Note : Ne changer pas la structure de la méthode! Elle permet de faire
	 * fonctionner l'ajout d'une entrée du journal. Il faut donc que la compléter.
	 * 
	 * @return le nom des planétes déjé explorées
	 */
	public static List<String> getPlanetList() {
		List<String> planets = new ArrayList<String>();
		try {
			Session connectionNeo4j = Neo4jConnection.getConnection();
			String querylistePlanete = "MATCH (n) RETURN n.name as name Order by n.dateFK desc";
			StatementResult resultListePlanete = connectionNeo4j.run(querylistePlanete);

			while (resultListePlanete.hasNext()) {
				Record item = resultListePlanete.next(); // representation:  Record.toString() Record<{nb: 1}>
				planets.add(item.get("name").toString().replace("\"", "")); // neo4j retourne "" pour chaque attributs
			}

		}
		// collection
		catch (Exception e) {
			e.printStackTrace();
		}

		return planets;
	}
	/*
	 * Shortest path entre 2 nodes, et le return permet d extraire le nom des planetes 
	 */
	public static List<String> getPlanetListTrajectoire(String planeteDepart,String planeteArrivee) {
		List<String> pathPlanets = new ArrayList<String>();
		try {
			Session connectionNeo4j = Neo4jConnection.getConnection();
			HashMap<String , Object> planetsToPlanetsB= new HashMap<String, Object>();
			planetsToPlanetsB.put("planeteDepart",planeteDepart);
			planetsToPlanetsB.put("planeteArrivee",planeteArrivee);
			String queryShortestPathPlanets = "MATCH (a), (b), p = shortestPath((a)-[*]-(b)) WHERE a.name =$planeteDepart and b.name= $planeteArrivee  RETURN extract(x IN nodes(p) | x.name) as p ";
			StatementResult resultListePlanete = connectionNeo4j.run(queryShortestPathPlanets,planetsToPlanetsB);
			while(resultListePlanete.hasNext()) {
				Record item = resultListePlanete.next(); // representation Record.toString() Record<{nb: 1}>
				for (Object planetsObjects :item.get("p").asList())
					pathPlanets.add(planetsObjects.toString());	
			}
		
		}
		
		catch (Exception e) {
			e.printStackTrace();
		}
		return pathPlanets;
	}
	
	public static List<String> getPlanetesVoisines(String planete){
		
		List<String> planetesVoisines = new ArrayList<String>();
		try {
			Session connectionNeo4j = Neo4jConnection.getConnection();
			HashMap<String , Object> planeteC = new HashMap<String, Object>();
			planeteC.put("planete",planete);
			String query = "match(p)-[:VOISIN]-(x) where p.name = $planete return x.name as planete";
			StatementResult resultListePlanete = connectionNeo4j.run(query,planeteC);
			
			while (resultListePlanete.hasNext()) {
				Record item = resultListePlanete.next(); // representation Record.toString() Record<{nb: 1}>
				planetesVoisines.add(item.get("planete").toString()); // neo4j retourne ""
			}
		
		}
		
		catch (Exception e) {
			e.printStackTrace();
		}
		return planetesVoisines;
	}
	
	public static String getgalaxiePrometteuse() {
		String galaxiePrometteuse = "";
		
		try {
			Session connectionNeo4j = Neo4jConnection.getConnection();
			
			String query = "match(n) return count(n.habitable) as nb , n.nameGalaxie Order By nb Desc limit 1";
			
			//String query = "match (n {nameGalaxie:'milky way'}) where n.habitable=True  return count(*)";
			//"match (n) where n.habitable=True  return Distinct n.nameGalaxie order by(n.nameGalaxie) Desc";
					
			StatementResult resultListePlanete = connectionNeo4j.run(query);
			
			while (resultListePlanete.hasNext()) {
				Record item = resultListePlanete.next(); // representation Record.toString() Record<{nb: 1}>
				galaxiePrometteuse = (item.get("n.nameGalaxie").toString()); // neo4j retourne ""
			}
		
		}
		
		catch (Exception e) {
			e.printStackTrace();
		}
		
		return galaxiePrometteuse;
	}
	
	
	public static List<String> getGalaxieTopPlanetesExplores(){
		
		List<String> topGalaxies = new ArrayList<String>();
		//List<String> listeGalaxie = new ArrayList<String>();
		try {
			Session connectionNeo4j = Neo4jConnection.getConnection();
			String query = "match(n) return count(*) as nb , n.nameGalaxie Order By nb Desc limit 5";
			StatementResult resultListePlanete = connectionNeo4j.run(query);
			
			while (resultListePlanete.hasNext()) {
				Record item = resultListePlanete.next(); // representation Record.toString() Record<{nb: 1}>
				
				String nb = item.get("nb").toString();
				String galaxie = item.get("n.nameGalaxie").toString();
				
				topGalaxies.add(galaxie + ","+ nb +" planetes explorées  \n"); // neo4j retourne ""
			}
			
		}
		
		catch (Exception e) {
			e.printStackTrace();
		}
		return topGalaxies;
	}
	
	
	
	/**
	 * Retourne l'entrée selon sa position dans le temps. La derniére entrée est 0,
	 * l'avant derniére est 1, l'avant avant derniére est 2, etc.
	 * 
	 * Toutes les informations liées é l'entrée doivent étre affectées é l'objet
	 * retourné.
	 * 
	 * Note : Ne changer pas la structure de la méthode! Elle permet de faire
	 * fonctionner l'affichage de la liste des entrées du journal. Il faut donc que
	 * la compléter.
	 * 
	 * @param position (démarre é 0)
	 * @return
	 */
	public static LogEntry getLogEntryByPosition(int position) {

		MongoDatabase connectionMongo = MongoConnection.getConnection();
		LogEntry logEntryRecherche;
		final List<LogEntry> reports = new ArrayList<>();
		try {
			MongoCollection<Document> collection = connectionMongo.getCollection("Journal");

			FindIterable<Document> iterator = collection.find().sort(new Document("date", -1)).limit(1).skip(position);

			iterator.forEach(new Block<Document>() {
				@Override
				public void apply(final Document document) {
					Session connectionNeo4j = Neo4jConnection.getConnection();
					LogEntry entry = null;
					String statut, name, date;
					statut = document.getString("statut");
					date = document.getString("date");
					name = document.getString("createur");

					switch (statut) {
					case "Normal":
						entry = new LogEntry(date, name, statut);
						break;
					case "Anormal":
						entry = new LogEntry(date, name, statut, document.getString("raison"));
						break;
					case "Exploration":

						// Binary imageToBin = document.get("photo", org.bson.types.Binary.class);
						HashMap<String, Object> parameters1 = new HashMap<String, Object>();
						parameters1.put("dateFK", document.getString("date"));
						String queryFindPlanete = "MATCH (n) WHERE n.dateFK = $dateFK RETURN n.name as name, n.habitable as habitable, n.nameGalaxie as nameGalaxie, n.namePlaneteProximite as namePlaneteProximite,n.photo as photo";
						StatementResult resultPlaneteExistante = connectionNeo4j.run(queryFindPlanete, parameters1);
						Record item = resultPlaneteExistante.next();
						
						List<String> lstPlanetesString = new ArrayList<String>();
						for (Object planets : item.get("namePlaneteProximite").asList()) {
							lstPlanetesString.add(planets.toString().replace("\"", ""));
						}
						String planetName = item.get("name").toString().replace("\"", "");
						String galaxyName = item.get("nameGalaxie").toString().replace("\"", "");

						byte[] image = item.get("photo").asByteArray();
						boolean habitable = item.get("habitable").asBoolean();

						entry = new LogEntry(date, name, statut, "", lstPlanetesString, planetName, galaxyName, image,
								habitable);
						break;
					}

					reports.add(entry);

				}
			});
		} catch (Exception e) {
			e.printStackTrace();
		}
		return reports.get(0);
	}

	/**
	 * Doit retourner le nombre d'entrées dans le journal de bord
	 * 
	 * Note : Ne changer pas la structure de la méthode! Elle permet de faire
	 * fonctionner l'affichage de la liste des entrées du journal. Il faut donc que
	 * la compléter.
	 * 
	 * @return nombre total
	 */
	public static int getNumberOfEntries() {
		MongoDatabase connectionMongo = MongoConnection.getConnection();
		int nbEntries = 0;
		try {
			MongoCollection<Document> collection = connectionMongo.getCollection("Journal");
			nbEntries = (int) collection.count();

		} catch (Exception e) {
			e.printStackTrace();
		}
		return nbEntries;
	}

	/**
	 * Retourne le nombre de planétes habitables
	 * 
	 * @return nombre total
	 */
	public static int getNumberOfHabitablePlanets() {

		try {
			Session connectionNeo4j = Neo4jConnection.getConnection();
			String queryCountHabitable = "MATCH (n) WHERE n.habitable = true RETURN count(n) as count";
			StatementResult resultPlaneteHabitable = connectionNeo4j.run(queryCountHabitable);
			return resultPlaneteHabitable.next().get("count").asInt();
		}
		// collection
		catch (Exception e) {
			e.printStackTrace();
		}
		return 0;
	}

	/**
	 * Suppression de toute les données
	 */
	public static boolean deleteAll() {
		boolean success = false;
		try {
			MongoDatabase connectionMongo = MongoConnection.getConnection();
			MongoCollection<Document> collection = connectionMongo.getCollection("Journal");
			FindIterable<Document> findIterable = collection.find();
			for (Document document : findIterable) {
				collection.deleteMany(document);
			}
			Session connectionNeo4j = Neo4jConnection.getConnection();
			String queryDeleteAllNodes = "MATCH (n) DETACH DELETE n";
			StatementResult resultqueryDeleteAllNodes = connectionNeo4j.run(queryDeleteAllNodes);
			success = true;

		} catch (Exception e) {
			e.printStackTrace();
		}

		return success;
	}
}
