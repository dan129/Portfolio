package ca.qc.cvm.dba.scoutlog.view;

import java.awt.Color;
import java.awt.Dimension;
import java.util.List;

import javax.swing.BorderFactory;
import javax.swing.JLabel;

import ca.qc.cvm.dba.scoutlog.app.Facade;
import ca.qc.cvm.dba.scoutlog.view.FrameMain.Views;
import ca.qc.cvm.dba.scoutlog.view.util.BackgroundPanel;

public class PanelData extends CommonPanel {
	private static final long serialVersionUID = 1L;
	
	private JLabel nbHabitablePlanets;
	private JLabel nbVisitedPlanets;
	private JLabel nbEntriesPlanets;
	private JLabel lastFiveVisitedPlanets;
	private JLabel lastFiveEntries;
	
	public PanelData(int width, int height) throws Exception {
		super(width, height, true, "assets/images/background-data.jpg");
	}
	
	@Override
	protected void jbInit() throws Exception {
		super.addLabel("Nombre de planetes habitables : ", 20, 20, 350, 30);
		nbHabitablePlanets = super.addLabel("", 400, 20, 80, 30);
		nbHabitablePlanets.setHorizontalAlignment(JLabel.CENTER);
		nbHabitablePlanets.setBorder(BorderFactory.createLineBorder(Color.WHITE));
		
		
		super.addLabel("Nombre de planetes visites : ", 20, 50, 350, 30);
		nbVisitedPlanets = super.addLabel("", 400, 50, 80, 30);
		nbVisitedPlanets.setHorizontalAlignment(JLabel.CENTER);
		nbVisitedPlanets.setBorder(BorderFactory.createLineBorder(Color.WHITE));
		
		super.addLabel("Nombre d'entrees : ", 20, 80, 350, 30);
		nbEntriesPlanets = super.addLabel("", 400, 80, 80, 30);
		nbEntriesPlanets.setHorizontalAlignment(JLabel.CENTER);
		nbEntriesPlanets.setBorder(BorderFactory.createLineBorder(Color.WHITE));
		
		super.addLabel("5 dernieres planetes visitees : ", 20,110, 350, 30);
		lastFiveVisitedPlanets = super.addLabel("", 400,110, 280, 30);
		lastFiveVisitedPlanets.setHorizontalAlignment(JLabel.CENTER);
		lastFiveVisitedPlanets.setBorder(BorderFactory.createLineBorder(Color.WHITE));
		
		super.addLabel("5 dernieres planetes visitees : ", 20,140, 350, 30);
		lastFiveEntries = super.addLabel("", 300,140, 550, 30);
		lastFiveEntries.setHorizontalAlignment(JLabel.CENTER);
		lastFiveEntries.setBorder(BorderFactory.createLineBorder(Color.WHITE));
		
		// Utilisez super.addField et super.addButton et etc pour cr�er votre interface graphique
	}
	
	/**
	 * Cette m�thode est appel�e automatiquement � chaque fois qu'un panel est affich� (lorsqu'on arrive sur la page)
	 */
	@Override
	public void resetUI() {		
		// Aller chercher les r�sultats et afficher ici..
		nbHabitablePlanets.setText(Facade.getInstance().getNumberOfHabitablePlanets() + "");
		nbEntriesPlanets.setText(Facade.getInstance().getNumberOfEntries()+"");
		nbVisitedPlanets.setText(Facade.getInstance().getPlanetList().size()+"");
		List<String> lstPlanets=Facade.getInstance().getPlanetList();
		if (lstPlanets.size() > 5) {
			lastFiveVisitedPlanets.setText(lstPlanets.subList(lstPlanets.size()-5,lstPlanets.size())+"");
		}
		else
			lastFiveVisitedPlanets.setText(lstPlanets.subList(0,lstPlanets.size())+"");
		
		lastFiveEntries.setText(Facade.getInstance().get5LastEntries().toString()+"");
		
	}

}
