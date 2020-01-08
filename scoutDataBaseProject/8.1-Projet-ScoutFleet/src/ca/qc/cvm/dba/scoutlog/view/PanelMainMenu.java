package ca.qc.cvm.dba.scoutlog.view;

import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JOptionPane;

import ca.qc.cvm.dba.correctionserver.lib.CorrectionDialog;
import ca.qc.cvm.dba.scoutlog.app.Facade;
import ca.qc.cvm.dba.scoutlog.event.CorrectionEvent;
import ca.qc.cvm.dba.scoutlog.event.DeleteAllEvent;
import ca.qc.cvm.dba.scoutlog.event.GoToEvent;
import ca.qc.cvm.dba.scoutlog.view.util.BackgroundPanel;

public class PanelMainMenu extends CommonPanel {
	private static final long serialVersionUID = 1L;

	public PanelMainMenu(int width, int height) throws Exception {
		super(width, height, false, "assets/images/background-main-menu.jpg");
	}
	
	@Override
	public void jbInit() throws Exception {
		this.addButton("Le journal de bord", 20, 20, 170, 40, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				
				Facade.getInstance().processEvent(new GoToEvent(FrameMain.Views.LogMenu));
			}
		});
		
		this.addButton("Repertoire et donnees", 20, 70, 170, 40, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				Facade.getInstance().processEvent(new GoToEvent(FrameMain.Views.Data));
			}
		});
		
		this.addButton("Visionnement de planetes", 20, 120, 170, 40, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				Facade.getInstance().processEvent(new GoToEvent(FrameMain.Views.PlanetsViewer));
			}
		});
		this.addButton("Trajectoire", 20, 170, 170, 40, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				Facade.getInstance().processEvent(new GoToEvent(FrameMain.Views.Trajectoire));
			}
		});
		this.addButton("Analyse", 20, 220, 170, 40, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				Facade.getInstance().processEvent(new GoToEvent(FrameMain.Views.Analyse));
			}
		});
		this.addButton("Quitter", 20, 270, 170, 40, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				int result = JOptionPane.showConfirmDialog(PanelMainMenu.this, "Voulez-vous vraiment quitter?");
				
				if (result == JOptionPane.OK_OPTION) {
					Facade.getInstance().exit();
				}
			}
		});
		
		this.addButton("Tout supprimer", 20, 520, 170, 20, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				int result = JOptionPane.showConfirmDialog(PanelMainMenu.this, "Voulez-vous vraiment supprimer toute la base de donnees?");
				
				if (result == JOptionPane.OK_OPTION) {
					Facade.getInstance().processEvent(new DeleteAllEvent());
				}
			}
		});

		this.addButton("Correction", 20, 490, 170, 20, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				String[] data = CorrectionDialog.getData(null);
				
				if (data != null) {
					Facade.getInstance().processEvent(new CorrectionEvent(data[0], data[1], data[2]));
				}
			}
		});
	}
	
	/**
	 * Cette m�thode est appel�e automatiquement � chaque fois qu'un panel est affich� (lorsqu'on arrive sur la page)
	 */
	@Override
	public void resetUI() {
	}

}
