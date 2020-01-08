package ca.qc.cvm.dba.scoutlog.event;

/**
 * �v�nement permettant de retourner � un panel parent 
 * (C'est pour le bouton retour)
 */
public class BackEvent extends CommonEvent {
	
	public BackEvent() {
		super(CommonEvent.Type.Back);
	}
}
