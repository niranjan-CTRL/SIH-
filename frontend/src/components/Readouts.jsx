export function Readout({ label, value, unit, risk = 'UNKNOWN' }) {
  return (
    <div className={`readout risk-${risk}`}>
      <div className="readout-label">{label}</div>
      <div className="readout-value">
        {value}
        {unit && <span className="readout-unit">{unit}</span>}
      </div>
    </div>
  );
}

export function Badge({ level }) {
  return <span className={`badge badge-${level}`}>{level}</span>;
}

export function AlertFeed({ alerts }) {
  if (!alerts || alerts.length === 0) {
    return <div className="empty-state">No alerts yet - all readings within configured thresholds.</div>;
  }
  return (
    <div>
      {alerts.map((a) => (
        <div className="alert-row" key={a.id}>
          <span className="alert-time">{new Date(a.timestamp).toLocaleTimeString()}</span>
          <Badge level={a.type.toUpperCase()} />
          <span className="alert-msg">{a.message}</span>
        </div>
      ))}
    </div>
  );
}
