import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { TopBar, NavTabs } from './components/Layout';
import { SpaceBackground } from './components/SpaceBackground';
import Landing from './pages/Landing';
import Login from './pages/Login';
import WorkerDashboard from './pages/WorkerDashboard';
import CartridgeScan from './pages/CartridgeScan';
import ExposureHistory from './pages/ExposureHistory';
import ExposureReport from './pages/ExposureReport';
import SupervisorDashboard from './pages/SupervisorDashboard';
import { SimulationProvider } from './context/SimulationContext';

function RequireAuth({ children, role }) {
  const { session } = useAuth();
  const location = useLocation();
  if (!session) return <Navigate to="/login" state={{ from: location }} replace />;
  if (role && session.role !== role) {
    return <Navigate to={session.role === 'supervisor' ? '/supervisor' : '/dashboard'} replace />;
  }
  return children;
}

function WorkerTabs() {
  return (
    <NavTabs
      tabs={[
        { to: '/dashboard', label: 'Live dashboard' },
        { to: '/scan', label: 'Cartridge scan' },
        { to: '/history', label: 'Exposure history' },
      ]}
    />
  );
}

function AppShell({ children, showWorkerTabs }) {
  return (
    <div className="app-shell">
      <TopBar />
      {showWorkerTabs && <WorkerTabs />}
      {children}
    </div>
  );
}

function AppRoutes() {
  const { session } = useAuth();

  return (
    <Routes>
      <Route
        path="/"
        element={session ? <Navigate to={session.role === 'supervisor' ? '/supervisor' : '/dashboard'} /> : <Landing />}
      />
      <Route
        path="/login"
        element={session ? <Navigate to={session.role === 'supervisor' ? '/supervisor' : '/dashboard'} /> : <Login />}
      />
      <Route
        path="/dashboard"
        element={
          <RequireAuth role="worker">
            <AppShell showWorkerTabs><WorkerDashboard /></AppShell>
          </RequireAuth>
        }
      />
      <Route
        path="/scan"
        element={
          <RequireAuth role="worker">
            <AppShell showWorkerTabs><CartridgeScan /></AppShell>
          </RequireAuth>
        }
      />
      <Route
        path="/history"
        element={
          <RequireAuth role="worker">
            <AppShell showWorkerTabs><ExposureHistory /></AppShell>
          </RequireAuth>
        }
      />
      <Route
        path="/report/:shiftId"
        element={
          <RequireAuth role="worker">
            <AppShell showWorkerTabs><ExposureReport /></AppShell>
          </RequireAuth>
        }
      />
      <Route
        path="/supervisor"
        element={
          <RequireAuth role="supervisor">
            <AppShell><SupervisorDashboard /></AppShell>
          </RequireAuth>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <SpaceBackground />
      <AuthProvider>
        <SimulationProvider>
          <AppRoutes />
        </SimulationProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
