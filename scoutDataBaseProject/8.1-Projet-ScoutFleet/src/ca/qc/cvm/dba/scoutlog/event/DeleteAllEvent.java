package ca.qc.cvm.dba.scoutlog.event;

/**
 * �v�nement utilis� lorsque l'on veut supprimer toute les donn�es
 */
public class DeleteAllEvent extends CommonEvent {
	
	public DeleteAllEvent() {
		super(CommonEvent.Type.DeleteAll);
	}
}
