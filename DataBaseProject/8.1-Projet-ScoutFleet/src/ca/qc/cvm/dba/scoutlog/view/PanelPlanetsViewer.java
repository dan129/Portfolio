package ca.qc.cvm.dba.scoutlog.view;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;

import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;

import ca.qc.cvm.dba.scoutlog.app.Facade;
import ca.qc.cvm.dba.scoutlog.entity.LogEntry;
import ca.qc.cvm.dba.scoutlog.event.BackEvent;
import ca.qc.cvm.dba.scoutlog.view.FrameMain.Views;
import ca.qc.cvm.dba.scoutlog.view.util.BackgroundPanel;

public class PanelPlanetsViewer extends CommonPanel {
	private static final long serialVersionUID = 1L;

	private JLabel galaxyName;
	private JLabel galaxyPrometteuse;
	
	private JButton previousBtn;
	private JButton nextBtn;
	
	private JTextArea info;
	private JLabel image;
	StringBuilder data = new StringBuilder();
	List<LogEntry> lst= new ArrayList<LogEntry>();
	private int position = 0;
	boolean nextActivated=false;
	public PanelPlanetsViewer(int width, int height) throws Exception {
		super(width, height, true, "assets/images/background-galaxy.jpg");
	}
	
	@Override
	protected void jbInit() throws Exception {
		previousBtn = this.addButton("Precedent", 530, 20, 150, 40, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				position--;
				nextActivated=false;
				PanelPlanetsViewer.this.resetFramesInfos();
			}
		});
		
		nextBtn = this.addButton("Suivant", 700, 20, 150, 40, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				nextActivated=true;
				position++;
				PanelPlanetsViewer.this.resetFramesInfos();
			}
		});
		info = new JTextArea();
		info.setEditable(false);
		info.setOpaque(false);
		info.setForeground(Color.WHITE);
		info.setBorder(BorderFactory.createLineBorder(Color.WHITE));
		this.addField(info, 20, 100, 400, 400);
		
		image = new JLabel();
		image.setBorder(BorderFactory.createLineBorder(Color.WHITE));
		this.addField(image, 450, 100, 250, 250);
		
	
		
		// Utilisez super.addField et super.addButton et etc pour cr�er votre interface graphique
	}
	
	/**
	 * Cette m�thode est appel�e automatiquement � chaque fois qu'un panel est affich� (lorsqu'on arrive sur la page)
	 */
	@Override
	public void resetUI() {
		String result = JOptionPane.showInputDialog(PanelPlanetsViewer.this, "Pour quelle galaxie?");
		
		lst=new ArrayList<LogEntry>();
		
		if (result != null && result.trim().length() > 0 ) {
			downloadPlanets(result);
			resetFramesInfos();
			
			 //galaxyName.setText(result);
			// Aller chercher les r�sultats et afficher ici..
		}
		else {
			Facade.getInstance().processEvent(new BackEvent());
		}
	}

	private void downloadPlanets(String result) {
		// TODO Auto-generated method stub
		int i=0;
		
		while(i<Facade.getInstance().getNumberOfEntries()) {
			if(Facade.getInstance().getLogEntryByPosition(i).getStatus().equals("Exploration") && Facade.getInstance().getLogEntryByPosition(i).getGalaxyName().equals(result) ) 
				lst.add(Facade.getInstance().getLogEntryByPosition(i));
			i++;
	}
		
	
	}

	public void resetFramesInfos() {
		info.setText("Aucune entree...");
		int entriesCount = Facade.getInstance().getNumberOfEntries(); //le nbr d'entree determine l'activation/desactivation des boutons
		
		if (position == 0 ||lst.size() == 0) {
			previousBtn.setEnabled(false);
		}
		else {
			previousBtn.setEnabled(true);
		}
		
		if (position + 1 >= lst.size()) {
			nextBtn.setEnabled(false);
		}
		else {
			nextBtn.setEnabled(true);
		}
	
		if(lst.size()>0) {
		LogEntry log = lst.get(position);
		data=new StringBuilder();
		data.append("Date : " + log.getDate() + "\n");
		data.append("------------------------------------\n");
		data.append("Nom du commandant : " + log.getName() + "\n");
		data.append("Statut : " + log.getStatus() + "\n");
		data.append("------------------------------------\n");
		data.append("Planete : " + log.getPlanetName() + "\n");
		data.append("Galaxie : " + log.getGalaxyName() + "\n");
		data.append("Habitable : " + log.isHabitable() + "\n");
		data.append("Planete(s) proche(s) : " + log.getNearPlanets() + "\n");
		image.setIcon(new ImageIcon(log.getImage()));
		info.setText(data.toString());
		}
	}
}
