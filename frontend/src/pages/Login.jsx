import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [workerId, setWorkerId] = useState('');
  const [pin, setPin] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const sess = await login(workerId.trim(), pin.trim());
      navigate(sess.role === 'supervisor' ? '/supervisor' : '/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-shell">
      <div className="login-card">
        <div className="brand" style={{ marginBottom: 22, justifyContent: 'center' }}>
          <span className="brand-mark" />
          <span className="brand-name" style={{ fontSize: 20 }}>H2S Sentinel</span>
        </div>
        <div className="panel">
          <p className="panel-title">Worker / supervisor login</p>
          {error && <div className="error-banner">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="field">
              <label>Worker ID</label>
              <input value={workerId} onChange={(e) => setWorkerId(e.target.value)} placeholder="W101" autoFocus />
            </div>
            <div className="field">
              <label>PIN</label>
              <input value={pin} onChange={(e) => setPin(e.target.value)} type="password" placeholder="••••" />
            </div>
            <button className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
              {loading ? 'Signing in…' : 'Sign in'}
            </button>
          </form>
        </div>
        <p style={{ fontSize: 12, color: 'var(--text-faint)', marginTop: 14, textAlign: 'center', lineHeight: 1.6 }}>
          Demo accounts — worker: <span className="mono">W101</span> / <span className="mono">1234</span>,{' '}
          supervisor: <span className="mono">S001</span> / <span className="mono">9999</span>
        </p>
      </div>
    </div>
  );
}
