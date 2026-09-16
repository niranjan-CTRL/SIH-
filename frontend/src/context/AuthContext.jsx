import { createContext, useContext, useState, useCallback } from 'react';
import { api } from '../api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [session, setSession] = useState(() => {
    const raw = localStorage.getItem('h2s_session');
    return raw ? JSON.parse(raw) : null;
  });

  const login = useCallback(async (workerId, pin) => {
    const data = await api.login(workerId, pin);
    localStorage.setItem('h2s_token', data.token);
    const sess = { workerId: data.worker_id, name: data.name, role: data.role };
    localStorage.setItem('h2s_session', JSON.stringify(sess));
    setSession(sess);
    return sess;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('h2s_token');
    localStorage.removeItem('h2s_session');
    localStorage.removeItem('h2s_active_shift');
    setSession(null);
  }, []);

  return (
    <AuthContext.Provider value={{ session, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
