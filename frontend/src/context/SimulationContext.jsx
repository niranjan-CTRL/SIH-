import { createContext, useContext, useState, useCallback } from 'react';

const SimulationContext = createContext(null);

const DEFAULT_STATE = {
  enabled: true,
  h2sLevel: 'normal',      // normal | warning | danger | emergency
  motionState: 'normal',    // normal | fall_suspected | inactive
  cartridgeState: 'active', // fresh | active | used | expired
  triggerSOS: false,
  customH2s: null,
};

const H2S_PRESETS = {
  normal: () => 2 + Math.random() * 6,
  warning: () => 10 + Math.random() * 8,
  danger: () => 22 + Math.random() * 20,
  emergency: () => 55 + Math.random() * 40,
};

export function SimulationProvider({ children }) {
  const [sim, setSim] = useState(DEFAULT_STATE);

  const setH2sLevel = useCallback((level) => {
    setSim((s) => ({ ...s, h2sLevel: level, customH2s: null }));
  }, []);

  const setMotionState = useCallback((state) => {
    setSim((s) => ({ ...s, motionState: state }));
  }, []);

  const setCartridgeState = useCallback((state) => {
    setSim((s) => ({ ...s, cartridgeState: state }));
  }, []);

  const fireSOS = useCallback(() => {
    setSim((s) => ({ ...s, triggerSOS: true }));
  }, []);

  const clearSOS = useCallback(() => {
    setSim((s) => ({ ...s, triggerSOS: false }));
  }, []);

  const generateReading = useCallback((tick) => {
    const h2sFn = H2S_PRESETS[sim.h2sLevel] || H2S_PRESETS.normal;
    const h2s = Math.max(0, Math.round(h2sFn() * 10) / 10);
    const elevated = h2s > 20;
    return {
      h2s_ppm: h2s,
      hr_bpm: Math.round(72 + Math.random() * 20 + (elevated ? 15 : 0)),
      spo2_pct: Math.round(97 - (elevated ? 3 : 0) + Math.random()),
      temp_c: Math.round((29 + Math.random() * 3) * 10) / 10,
      motion_state: sim.motionState,
    };
  }, [sim.h2sLevel, sim.motionState]);

  return (
    <SimulationContext.Provider
      value={{
        sim,
        setH2sLevel,
        setMotionState,
        setCartridgeState,
        fireSOS,
        clearSOS,
        generateReading,
      }}
    >
      {children}
    </SimulationContext.Provider>
  );
}

export function useSimulation() {
  const ctx = useContext(SimulationContext);
  if (!ctx) throw new Error('useSimulation must be used within SimulationProvider');
  return ctx;
}
