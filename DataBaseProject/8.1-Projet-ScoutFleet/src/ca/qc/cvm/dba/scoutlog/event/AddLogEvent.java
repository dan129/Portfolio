package ca.qc.cvm.dba.scoutlog.event;

import ca.qc.cvm.dba.scoutlog.entity.LogEntry;

/**
 * �v�nement utilis� lorsque l'on veut sauvegarder une nouvelle
 * entr�e dans le journal
 */
public class AddLogEvent extends CommonEvent {
	private LogEntry log;
	
	public AddLogEvent(LogEntry log) {
		super(CommonEvent.Type.AddLog);
		
		this.log = log;
	}
	
	public LogEntry getLog() {
		return log;
	}
}
