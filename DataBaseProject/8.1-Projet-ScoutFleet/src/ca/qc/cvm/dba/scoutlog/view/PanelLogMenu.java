package ca.qc.cvm.dba.scoutlog.view;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.JTextPane;
import javax.swing.SwingUtilities;

import ca.qc.cvm.dba.scoutlog.app.Facade;
import ca.qc.cvm.dba.scoutlog.entity.LogEntry;
import ca.qc.cvm.dba.scoutlog.event.GoToEvent;
import ca.qc.cvm.dba.scoutlog.view.util.BackgroundPanel;

public class PanelLogMenu extends CommonPanel {
	private static final long serialVersionUID = 1L;
	
	private JButton previousBtn;
	private JButton nextBtn;
	
	private JTextArea info;
	private JLabel image;
	
	private int position = 0;

	public PanelLogMenu(int width, int height) throws Exception {
		super(width, height, true, "assets/images/background-log-menu.jpg");
	}
	
	@Override
	public void jbInit() throws Exception {
		previousBtn = this.addButton("Precedent", 530, 20, 150, 40, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				position++;
				PanelLogMenu.this.resetUI();
			}
		});
		
		nextBtn = this.addButton("Suivant", 700, 20, 150, 40, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				position--;
				PanelLogMenu.this.resetUI();
			}
		});

		this.addButton("Ajouter une entree", 20, 20, 150, 40, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				Facade.getInstance().processEvent(new GoToEvent(FrameMain.Views.LogAdd));
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
	}

	@Override
	protected void digestBackEvent() {
		position = 0;
	}
	
	/**
	 * Cette m�thode est appel�e automatiquement � chaque fois qu'un panel est affich� (lorsqu'on arrive sur la page)
	 */
	@Override
	public void resetUI() {
		info.setText("Aucune entree...");
		int entriesCount = Facade.getInstance().getNumberOfEntries();
		
		if (position == 0 || entriesCount == 0) {
			nextBtn.setEnabled(false);
		}
		else {
			nextBtn.setEnabled(true);
		}
		
		if (position + 1 >= entriesCount) {
			previousBtn.setEnabled(false);
		}
		else {
			previousBtn.setEnabled(true);
		}
		
		if (entriesCount > 0) {
			image.setVisible(true);
			image.setIcon(null);
			
			LogEntry log = Facade.getInstance().getLogEntryByPosition(position);
			
			if (log != null) {
				StringBuilder data = new StringBuilder();
				
				data.append("Date : " + log.getDate() + "\n");
				data.append("------------------------------------\n");
				data.append("Nom du commandant : " + log.getName() + "\n");
				data.append("Statut : " + log.getStatus() + "\n");
				data.append("------------------------------------\n");
				
				if (log.getStatus().equals("Anormal")) {
					data.append("\n\nRaisons:\n" + log.getReasons() + "\n");
				}
				
				if (log.getStatus().equals("Exploration")) {
					data.append("Planete : " + log.getPlanetName() + "\n");
					data.append("Galaxie : " + log.getGalaxyName() + "\n");
					data.append("Habitable : " + log.isHabitable() + "\n");
					data.append("Planete(s) proche(s) : " + log.getNearPlanets() + "\n");
					image.setIcon(new ImageIcon(log.getImage()));
				}
				
				info.setText(data.toString());
			}
			else {
				info.setText("Aucune entree trouvee...");
				image.setVisible(false);
			}
			
		}
		else {
			info.setText("Aucune entree...");
			image.setVisible(false);
		}
	}

}
