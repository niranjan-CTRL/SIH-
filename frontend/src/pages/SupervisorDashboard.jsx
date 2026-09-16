import { useState, useEffect, useCallback } from 'react';
import { api } from '../api';
import { Badge, AlertFeed, Readout } from '../components/Readouts';

export default function SupervisorDashboard() {
  const [workers, setWorkers] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [selected, setSelected] = useState(null);
  const [workerHistory, setWorkerHistory] = useState([]);
  const [error, setError] = useState('');

  const load = useCallback(async () => {
    try {
      const [w, a] = await Promise.all([api.supervisorWorkers(), api.supervisorAlerts()]);
      setWorkers(w);
      setAlerts(a);
    } catch (err) {
      setError(err.message);
    }
  }, []);

  useEffect(() => {
    load();
    const interval = setInterval(load, 4000);
    return () => clearInterval(interval);
  }, [load]);

  async function ack(alertId) {
    try {
      await api.acknowledgeAlert(alertId);
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function selectWorker(w) {
    setSelected(w);
    try {
      const history = await api.workerHistory(w.worker_id);
      setWorkerHistory(history);
    } catch {
      setWorkerHistory([]);
    }
  }

  const emergencyWorkers = workers.filter((w) => w.risk_level === 'EMERGENCY' || w.risk_level === 'DANGER');

  return (
    <div className="main">
      {/* SIMULATION MODE banner */}
      <div className="sim-banner">
        <span className="sim-banner-dot" />
        SIMULATION MODE — All worker data shown is from prototype simulation. Hardware not connected.
      </div>

      {error && <div className="error-banner">{error}</div>}

      {/* Emergency alert bar */}
      {emergencyWorkers.length > 0 && (
        <div className="emergency-bar">
          ⚠️ {emergencyWorkers.length} worker(s) in DANGER/EMERGENCY state — immediate attention required
        </div>
      )}

      <div className="stack">
        {/* Worker Status Board */}
        <div className="panel">
          <p className="panel-title">Worker status board</p>
          {workers.length === 0 && <div className="empty-state">No workers registered.</div>}
          {workers.length > 0 && (
            <div className="table-responsive">
              <table className="board">
                <thead>
                  <tr>
                    <th>Worker</th>
                    <th>Shift</th>
                    <th>H₂S</th>
                    <th>HR</th>
                    <th>SpO₂</th>
                    <th>Temp</th>
                    <th>Risk</th>
                    <th>Alerts</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {workers.map((w) => (
                    <tr
                      key={w.worker_id}
                      className={`worker-row ${selected?.worker_id === w.worker_id ? 'worker-row-selected' : ''}`}
                      onClick={() => selectWorker(w)}
                      style={{ cursor: 'pointer' }}
                    >
                      <td>
                        {w.name}{' '}
                        <span className="mono" style={{ color: 'var(--text-faint)' }}>
                          ({w.worker_id})
                        </span>
                      </td>
                      <td>{w.shift_status ?? 'off shift'}</td>
                      <td className="mono">{w.latest_h2s_ppm != null ? `${w.latest_h2s_ppm}` : '—'}</td>
                      <td className="mono">{w.latest_hr_bpm ?? '—'}</td>
                      <td className="mono">{w.latest_spo2_pct ?? '—'}</td>
                      <td className="mono">{w.latest_temp_c ?? '—'}</td>
                      <td><Badge level={w.risk_level} /></td>
                      <td className="mono">{w.open_alerts}</td>
                      <td>
                        <button className="btn" style={{ padding: '4px 10px', fontSize: 11 }}>
                          Details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Worker Detail Panel */}
        {selected && (
          <div className="panel worker-detail-panel">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
              <p className="panel-title" style={{ margin: 0 }}>
                Worker detail — {selected.name} ({selected.worker_id})
              </p>
              <button className="btn" onClick={() => setSelected(null)} style={{ padding: '4px 10px', fontSize: 11 }}>
                Close
              </button>
            </div>

            <div className="grid-3" style={{ marginBottom: 16 }}>
              <div>
                <Readout
                  label="Current H₂S"
                  value={selected.latest_h2s_ppm ?? '—'}
                  unit="ppm"
                  risk={selected.risk_level}
                />
              </div>
              <div>
                <Readout label="Heart rate" value={selected.latest_hr_bpm ?? '—'} unit="bpm" risk="NORMAL" />
              </div>
              <div>
                <Readout label="SpO₂" value={selected.latest_spo2_pct ?? '—'} unit="%" risk="NORMAL" />
              </div>
            </div>

            <div className="grid-3" style={{ marginBottom: 16 }}>
              <div>
                <Readout label="Temperature" value={selected.latest_temp_c ?? '—'} unit="°C" risk="NORMAL" />
              </div>
              <div>
                <Readout label="Shift status" value={selected.shift_status ?? 'Off shift'} risk={selected.shift_status === 'active' ? 'NORMAL' : 'UNKNOWN'} />
              </div>
              <div>
                <Readout label="Open alerts" value={selected.open_alerts} risk={selected.open_alerts > 0 ? 'WARNING' : 'NORMAL'} />
              </div>
            </div>

            {/* Shift History */}
            <p className="panel-title">Recent shifts</p>
            {workerHistory.length === 0 ? (
              <div className="empty-state">No shift history found.</div>
            ) : (
              <div className="table-responsive">
                <table className="board">
                  <thead>
                    <tr>
                      <th>Shift</th>
                      <th>Started</th>
                      <th>Status</th>
                      <th>Peak H₂S</th>
                      <th>Warnings</th>
                      <th>Dangers</th>
                    </tr>
                  </thead>
                  <tbody>
                    {workerHistory.slice(0, 10).map((s) => (
                      <tr key={s.id}>
                        <td>{s.shift_label}</td>
                        <td className="mono">{new Date(s.start_time).toLocaleString()}</td>
                        <td><Badge level={s.status === 'active' ? 'WARNING' : 'NORMAL'} /></td>
                        <td className="mono">{s.peak_h2s_ppm} ppm</td>
                        <td className="mono">{s.warning_count}</td>
                        <td className="mono">{s.danger_count}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* Open Alerts */}
        <div className="panel">
          <p className="panel-title">Open alerts (all workers)</p>
          <AlertFeed alerts={alerts} />
          {alerts.length > 0 && (
            <div style={{ marginTop: 12, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              {alerts.map((a) => (
                <button key={a.id} className="btn" onClick={() => ack(a.id)}>
                  Acknowledge #{a.id}
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="disclaimer">
          Supervisor dashboard shows aggregated worker status from the prototype simulation system.
          In production, this data would come from real wearable sensors connected via BLE/Wi-Fi.
          Biometric readings (HR, SpO₂) are supporting safety indicators only and do not constitute medical diagnosis.
        </div>
      </div>
    </div>
  );
}
