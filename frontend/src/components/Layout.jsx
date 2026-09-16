import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useSimulation } from '../context/SimulationContext';

export function TopBar() {
  const { session, logout } = useAuth();
  
  // Conditionally use simulation context if available (it might not be available in all wrappers, though here it is)
  let sim = null;
  try {
    const simCtx = useSimulation();
    sim = simCtx.sim;
  } catch (e) {
    // Ignore error if not in provider
  }

  return (
    <div className="topbar">
      <div className="brand">
        <span className="brand-mark" />
        <span className="brand-name">H2S Sentinel</span>
        <span className="brand-sub">Team Valence</span>
        {sim && sim.enabled && (
          <span style={{ marginLeft: 12, padding: '2px 6px', background: 'var(--blue)', color: '#000', fontSize: 10, fontWeight: 'bold', borderRadius: 4, letterSpacing: '0.05em' }}>
            SIM
          </span>
        )}
      </div>
      {session && (
        <div className="topbar-right">
          <span>{session.name} · <span className="mono">{session.workerId}</span></span>
          <button className="btn" onClick={logout} style={{ padding: '6px 12px' }}>Log out</button>
        </div>
      )}
    </div>
  );
}

export function NavTabs({ tabs }) {
  return (
    <div className="nav-tabs">
      {tabs.map((t) => (
        <NavLink
          key={t.to}
          to={t.to}
          className={({ isActive }) => 'nav-tab' + (isActive ? ' active' : '')}
        >
          {t.label}
        </NavLink>
      ))}
    </div>
  );
}
