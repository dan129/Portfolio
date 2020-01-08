package ca.qc.cvm.dba.scoutlog.view;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;
import java.util.Vector;

import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;

import ca.qc.cvm.dba.scoutlog.app.Facade;

public class PanelAnalyse extends CommonPanel {

	private static final long serialVersionUID = 1L;

	private JLabel analyseLabel;
	private JComboBox<String> choixField;

	Vector<String> choices;

	private JTextArea info;

	public PanelAnalyse(int width, int height) throws Exception {
		super(width, height, true, "assets/images/background-data.jpg");

	}

	@Override
	protected void jbInit() throws Exception {
		choices = new Vector<String>();
		for (String planets : Facade.getInstance().getPlanetList()) {
			choices.addElement(planets);
		}
		// choices.addElement("Galaxie prometteuse");
		// choices.addElement("Plan�tes explor�s");

		choixField = new JComboBox<String>(choices);
		analyseLabel = super.addLabel("Planete : ", 20, 120, 150, 30);
		super.addField(choixField, 190, 120, 250, 30);

		super.addLabel("Infos : ", 20, 220, 90, 30);
		info = new JTextArea();
		super.addField(info, 190, 220, 600, 280);
		info.setBorder(BorderFactory.createLineBorder(Color.WHITE));
		this.addButton("Infos", 20, 510, 100, 20, new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				List<String> lstPlanetes = Facade.getInstance().getPlanetList();
				StringBuilder data = new StringBuilder();

				lstPlanetes = Facade.getInstance().getGalaxieTopPlanetesExplores();

				data.append("Galaxie Prometteuse : " + Facade.getInstance().getgalaxiePrometteuse() + "\n");
				data.append("---------------------------------- \n");
				data.append("Galaxie plus grand nombre de planetes explorées \n "
						+ Facade.getInstance().getGalaxieTopPlanetesExplores() + "\n");
				data.append("---------------------------------- \n");
				data.append("Planetes voisines : "
						+ Facade.getInstance().getPlanetesVoisines((String) choixField.getSelectedItem()) + "\n");
				info.setText(data.toString());

			}
		});
		// Utilisez super.addField et super.addButton et etc pour cr�er votre interface
		// graphique
	}

	/**
	 * Cette m�thode est appel�e automatiquement � chaque fois qu'un panel est
	 * affich� (lorsqu'on arrive sur la page)
	 */
	@Override
	public void resetUI() {
		remplissage();
	}

	public void remplissage() {
		choices.clear();
		
		for (String planets : Facade.getInstance().getPlanetList()) {
			choices.addElement(planets);
		}
		info.setText("");
	}
}
