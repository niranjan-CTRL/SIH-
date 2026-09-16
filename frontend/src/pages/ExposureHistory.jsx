import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api';
import { Badge } from '../components/Readouts';
import { Link } from 'react-router-dom';

export default function ExposureHistory() {
  const { session } = useAuth();
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    async function load() {
      try {
        const data = await api.workerHistory(session.workerId);
        setHistory(data);
      } catch (err) {
        setError(err.message);
      }
    }
    load();
  }, [session.workerId]);

  return (
    <div className="main">
      <h2>Exposure History</h2>
      {error && <div className="error-banner">{error}</div>}
      {history.length === 0 ? (
        <div className="panel">No shift history found.</div>
      ) : (
        <div className="panel">
          <div className="table-responsive">
            <table className="board">
              <thead>
                <tr>
                  <th>Shift</th>
                  <th>Cartridge</th>
                  <th>Start</th>
                  <th>End</th>
                  <th>Peak H₂S</th>
                  <th>Warn/Danger</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {history.map((s) => (
                  <tr key={s.id}>
                    <td>{s.shift_label}</td>
                    <td className="mono">{s.cartridge_id || '—'}</td>
                    <td className="mono">{new Date(s.start_time).toLocaleString()}</td>
                    <td className="mono">{s.end_time ? new Date(s.end_time).toLocaleString() : '—'}</td>
                    <td className="mono">{s.peak_h2s_ppm} ppm</td>
                    <td className="mono">{s.warning_count} / {s.danger_count}</td>
                    <td>
                      <Badge level={s.status === 'active' ? 'WARNING' : 'NORMAL'} />
                    </td>
                    <td>
                      <Link to={`/report/${s.id}`} className="btn" style={{ padding: '4px 10px', fontSize: 11, textDecoration: 'none' }}>
                        View Report
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
