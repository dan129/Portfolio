package ca.qc.cvm.dba.scoutlog.app;

import java.beans.PropertyChangeListener;
import java.util.List;
import java.util.Observer;

import ca.qc.cvm.dba.scoutlog.dao.LogDAO;
import ca.qc.cvm.dba.scoutlog.entity.LogEntry;
import ca.qc.cvm.dba.scoutlog.event.CommonEvent;

/**
 * Cette classe est l'interm�diaire entre la logique et la vue
 * Entre les panel et le MngApplication. C'est le point d'entr�e de la vue
 * vers la logique
 */
public class Facade {
	private static Facade instance;
	
	private MngApplication app;
	
	private Facade() {
		app = new MngApplication();
	}
	
	public static Facade getInstance() {
		if (instance == null) {
			instance = new Facade();
		}
		
		return instance;
	}
	
	public void processEvent(CommonEvent event) {
		app.addEvent(event);
        new Thread(app).start();
	}
	
	public void addObserverClass( PropertyChangeListener pcl) {
		app.addPropertyChangeListener(pcl);
	}
	
	public List<String> getPlanetList() {
		return app.getPlanetList();
	}
	
	public int getNumberOfEntries() {
		return app.getNumberOfEntries();
	}
	
	public LogEntry getLogEntryByPosition(int position) {
		return app.getLogEntryByPosition(position);
	}
		
	public int getNumberOfHabitablePlanets() {
		return app.getNumberOfHabitablePlanets();
	}
	
	
	/*Nouvelle methode rajoute */
	public List<String> getPathPlanetList(String depart, String arrivee) {
		return app.getPlanetListTrajectoire(depart,arrivee);
	}
	
	public List<String> getPlanetesVoisines(String planete) {
		return app.getPlanetesVoisines(planete);
	}
	
	public String getgalaxiePrometteuse() {
		return app.getgalaxiePrometteuse();
	}
	
	public List<String> getGalaxieTopPlanetesExplores(){
		return app.getGalaxieTopPlanetesExplores();
	}
	
	
	public List<String> get5LastEntries(){
		return app.get5LastEntries();
	}
	
	public void exit() {
		app.exit();
	}
}
