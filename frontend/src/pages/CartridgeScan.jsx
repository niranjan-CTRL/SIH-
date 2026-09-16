import { useState, useRef } from 'react';
import { api } from '../api';

export default function CartridgeScan() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [step, setStep] = useState(0); // 0: upload, 1: detect, 2: lighting, 3: ai, 4: done
  const fileInputRef = useRef(null);

  function handleFileChange(e) {
    const f = e.target.files[0];
    if (!f) return;
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
    setError('');
    setStep(0);
  }

  async function handleScan() {
    if (!file) return;
    setBusy(true);
    setError('');
    setResult(null);
    
    try {
      setStep(1);
      await new Promise(r => setTimeout(r, 600)); // Simulate detection
      
      setStep(2);
      await new Promise(r => setTimeout(r, 600)); // Simulate lighting correction
      
      setStep(3);
      await new Promise(r => setTimeout(r, 600)); // Simulate AI model

      const formData = new FormData();
      formData.append('file', file);
      const res = await api.scanCartridge(formData);
      
      setStep(4);
      setResult(res);
    } catch (err) {
      setError(err.message);
      setStep(0);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="main">
      <h2>Scan Cartridge</h2>
      <p style={{ color: 'var(--text-faint)', marginBottom: 20 }}>
        Take a photo of the cartridge to estimate cumulative H₂S exposure.
        Align the reference patch in the top-left and the sensor strip in the center.
      </p>

      <div className="grid-2">
        <div className="panel">
          <input
            type="file"
            accept="image/*"
            capture="environment"
            onChange={handleFileChange}
            ref={fileInputRef}
            style={{ display: 'none' }}
          />
          
          {!preview ? (
            <div 
              className="scan-placeholder" 
              onClick={() => fileInputRef.current.click()}
              style={{
                border: '2px dashed var(--grid)',
                borderRadius: 8,
                height: 240,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                background: 'rgba(255,255,255,0.02)'
              }}
            >
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 32, marginBottom: 10 }}>📷</div>
                <div>Tap to take photo or upload</div>
              </div>
            </div>
          ) : (
            <div style={{ position: 'relative' }}>
              <img 
                src={preview} 
                alt="Cartridge preview" 
                style={{ width: '100%', borderRadius: 8, maxHeight: 300, objectFit: 'contain', background: '#000' }} 
              />
              {!busy && step === 0 && (
                <button 
                  className="btn" 
                  onClick={() => fileInputRef.current.click()}
                  style={{ position: 'absolute', top: 10, right: 10, background: 'rgba(0,0,0,0.7)' }}
                >
                  Retake
                </button>
              )}
            </div>
          )}

          {preview && step === 0 && (
            <button 
              className="btn btn-primary" 
              style={{ width: '100%', marginTop: 16 }}
              onClick={handleScan}
              disabled={busy}
            >
              Analyze Image
            </button>
          )}

          {busy && (
            <div className="scan-progress" style={{ marginTop: 20 }}>
              <div className={`scan-step ${step >= 1 ? 'active' : ''}`}>1. Detecting Cartridge Regions...</div>
              <div className={`scan-step ${step >= 2 ? 'active' : ''}`}>2. Lighting Correction...</div>
              <div className={`scan-step ${step >= 3 ? 'active' : ''}`}>3. AI Color Analysis...</div>
            </div>
          )}
          
          {error && <div className="error-banner" style={{ marginTop: 16 }}>{error}</div>}
        </div>

        {result && (
          <div className="panel">
            <h3 className="panel-title">Analysis Result</h3>
            
            {!result.ok ? (
              <div className="error-banner" style={{ marginTop: 0 }}>
                <strong>Quality Check Failed</strong><br/>
                {result.quality_warning}
              </div>
            ) : (
              <>
                <div style={{ textAlign: 'center', margin: '20px 0' }}>
                  <div style={{ fontSize: 14, color: 'var(--text-faint)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Estimated Cumulative Exposure
                  </div>
                  <div style={{ fontSize: 42, fontWeight: 'bold', margin: '10px 0', fontFamily: 'var(--font-mono)', color: result.risk_level === 'HIGH' ? 'var(--red)' : result.risk_level === 'MEDIUM' ? 'var(--amber)' : 'var(--blue)' }}>
                    {result.estimated_cumulative_exposure_ppm_hr} <span style={{ fontSize: 20, color: 'var(--text-faint)' }}>ppm·hr</span>
                  </div>
                  <div style={{ display: 'inline-block', padding: '4px 12px', borderRadius: 4, background: result.risk_level === 'HIGH' ? 'rgba(239, 68, 68, 0.2)' : result.risk_level === 'MEDIUM' ? 'rgba(245, 158, 11, 0.2)' : 'rgba(59, 130, 246, 0.2)', color: result.risk_level === 'HIGH' ? 'var(--red)' : result.risk_level === 'MEDIUM' ? 'var(--amber)' : 'var(--blue)', fontWeight: 600 }}>
                    {result.risk_level} RISK
                  </div>
                </div>
                
                <table className="report-table" style={{ fontSize: 13 }}>
                  <tbody>
                    <tr><td>Color Dist (Baseline):</td><td className="mono">{result.color_distance_from_baseline}</td></tr>
                    <tr><td>Strip RGB:</td><td className="mono">rgb({result.strip_rgb.r}, {result.strip_rgb.g}, {result.strip_rgb.b})</td></tr>
                    <tr>
                      <td>Visual:</td>
                      <td>
                        <div style={{ 
                          width: 40, height: 20, borderRadius: 4, 
                          background: `rgb(${result.strip_rgb.r}, ${result.strip_rgb.g}, ${result.strip_rgb.b})`,
                          border: '1px solid rgba(255,255,255,0.2)'
                        }} />
                      </td>
                    </tr>
                    <tr><td>Model:</td><td className="mono">{result.model_version}</td></tr>
                  </tbody>
                </table>

                {result.disclaimer && (
                  <div className="disclaimer" style={{ marginTop: 20 }}>
                    {result.disclaimer}
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
