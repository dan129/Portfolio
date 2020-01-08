package ca.qc.cvm.dba.scoutlog.event;

/**
 * Super classe pour tous les �v�nements. Vous pouvez ajouter
 * des sous-classes pour vos �v�nements. N'oubliez pas dans ce cas
 * d'ajouter un <<Type>> (voir plus bas)
 *
 */
public abstract class CommonEvent {
	public enum Type {General, UI, GoTo, Back, AddLog, DeleteAll, Correction};
	
	private Type type;
	
	public CommonEvent(Type type) {
		this.type = type;
	}
	
	public Type getType() {
		return type;
	}
}
