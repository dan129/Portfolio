package ca.qc.cvm.dba.scoutlog.event;

/**
 * �v�nement qui a rapport � l'interface graphique
 */
public class UIEvent extends CommonEvent {
	public enum UIType {ShowMessage, GoTo, Refresh, Back}
	
	private UIType uiType;
	private Object data;
	
	public UIEvent(UIType type, Object data) {
		super(CommonEvent.Type.UI);
		
		uiType = type;
		this.data = data;
	}
	
	public UIType getUIType() {
		return uiType;
	}
	
	public Object getData() {
		return data;
	}
}
