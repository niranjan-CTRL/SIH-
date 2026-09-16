import { useNavigate } from 'react-router-dom';
import './Landing.css';

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="landing">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <div className="hero-mark" />
          <h1 className="hero-title">H₂S SENTINEL</h1>
          <p className="hero-subtitle">
            AI-Powered Smartwatch for H₂S Exposure Monitoring & Worker Safety
          </p>
          <p className="hero-description">
            Combining real-time electronic sensing with passive cumulative exposure monitoring to protect workers in hazardous environments.
          </p>
          <div className="hero-actions">
            <button className="btn btn-primary" onClick={() => navigate('/login')}>
              Access Dashboard
            </button>
            <button className="btn" onClick={() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })}>
              Learn More
            </button>
          </div>
        </div>
      </section>

      {/* Overview Grid */}
      <section className="section overview-grid">
        <div className="grid-item">
          <div className="grid-icon">⚡</div>
          <div className="grid-label">REAL-TIME<br />H₂S MONITORING</div>
        </div>
        <div className="grid-item">
          <div className="grid-icon">🎨</div>
          <div className="grid-label">AI COLOR<br />ANALYSIS</div>
        </div>
        <div className="grid-item">
          <div className="grid-icon">👤</div>
          <div className="grid-label">WORKER<br />SAFETY</div>
        </div>
        <div className="grid-item">
          <div className="grid-icon">📊</div>
          <div className="grid-label">DIGITAL<br />RECORDS</div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="section problem-section">
        <h2>The Problem</h2>
        <div className="problem-content">
          <div className="problem-text">
            <p>
              Workers in <strong>oil refineries, petrochemical plants, wastewater treatment facilities, chemical industries,</strong> and <strong>mining operations</strong> face constant exposure to <strong>hydrogen sulfide (H₂S)</strong>—a colorless, odorless toxic gas.
            </p>
            <p>
              Traditional electronic H₂S detectors provide <strong>instantaneous concentration readings</strong>, but they don't capture <strong>cumulative exposure over time</strong>—a critical metric for assessing worker health risks.
            </p>
            <p>
              <strong>Passive colorimetric cartridges</strong> record cumulative exposure but require <strong>manual interpretation</strong> and provide no real-time alerts.
            </p>
          </div>
          <div className="problem-stats">
            <div className="stat-card">
              <div className="stat-number">4000+</div>
              <div className="stat-label">Deaths annually from H₂S exposure*</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">10 ppm</div>
              <div className="stat-label">OSHA Ceiling Limit (15 min)</div>
            </div>
          </div>
        </div>
        <p className="disclaimer-small">*Estimated globally. Actual figures vary by region.</p>
      </section>

      {/* Solution Section */}
      <section className="section solution-section">
        <h2>Our Solution</h2>
        <p className="section-subtitle">H₂S Sentinel combines real-time electronic sensing with passive cumulative exposure monitoring on a single wearable device.</p>
        
        <div className="dual-system">
          <div className="system-flow">
            <div className="flow-title">Real-Time Monitoring</div>
            <div className="flow-step">
              <div className="step-icon">1</div>
              <div className="step-label">H₂S Sensor</div>
            </div>
            <div className="flow-arrow">↓</div>
            <div className="flow-step">
              <div className="step-icon">2</div>
              <div className="step-label">Instantaneous Reading</div>
            </div>
            <div className="flow-arrow">↓</div>
            <div className="flow-step">
              <div className="step-icon">3</div>
              <div className="step-label">Alert if Threshold Exceeded</div>
            </div>
          </div>
          
          <div className="dual-divider">+</div>
          
          <div className="system-flow">
            <div className="flow-title">Cumulative Exposure Monitoring</div>
            <div className="flow-step">
              <div className="step-icon">1</div>
              <div className="step-label">Chemical Cartridge</div>
            </div>
            <div className="flow-arrow">↓</div>
            <div className="flow-step">
              <div className="step-icon">2</div>
              <div className="step-label">Color Change Over Time</div>
            </div>
            <div className="flow-arrow">↓</div>
            <div className="flow-step">
              <div className="step-icon">3</div>
              <div className="step-label">AI Analysis = Cumulative Dose</div>
            </div>
          </div>
        </div>

        <div className="solution-result">
          <div className="result-label">Unified Worker Safety</div>
          <div className="result-arrow">↓</div>
          <div className="result-system">H₂S SENTINEL</div>
        </div>
      </section>

      {/* Features Section */}
      <section className="section features-section">
        <h2>Core Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-number">01</div>
            <div className="feature-title">Real-Time H₂S Monitoring</div>
            <p>Electronic H₂S sensor provides instantaneous ambient gas concentration with continuous monitoring.</p>
          </div>
          <div className="feature-card">
            <div className="feature-number">02</div>
            <div className="feature-title">Cumulative Exposure Monitoring</div>
            <p>Passive chemical cartridge tracks H₂S exposure over time through progressive color change.</p>
          </div>
          <div className="feature-card">
            <div className="feature-number">03</div>
            <div className="feature-title">AI Color Analysis</div>
            <p>Smartphone-based image processing and trained models estimate cumulative exposure from cartridge color.</p>
          </div>
          <div className="feature-card">
            <div className="feature-number">04</div>
            <div className="feature-title">Biometric Monitoring</div>
            <p>HR, SpO₂, and temperature monitoring as supporting safety indicators for worker health.</p>
          </div>
          <div className="feature-card">
            <div className="feature-number">05</div>
            <div className="feature-title">Motion & Fall Detection</div>
            <p>MPU6050-based motion sensing detects potential fall or inactivity events in real-time.</p>
          </div>
          <div className="feature-card">
            <div className="feature-number">06</div>
            <div className="feature-title">SOS Emergency Alert</div>
            <p>Physical SOS button enables workers to trigger emergency notifications to supervisors instantly.</p>
          </div>
          <div className="feature-card">
            <div className="feature-number">07</div>
            <div className="feature-title">Supervisor Dashboard</div>
            <p>Supervisors monitor worker status, receive alerts, track exposure history, and manage teams.</p>
          </div>
          <div className="feature-card">
            <div className="feature-number">08</div>
            <div className="feature-title">Digital Exposure Records</div>
            <p>Comprehensive digital storage of worker, shift, cartridge, and exposure data for compliance reporting.</p>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="section how-it-works">
        <h2>How It Works</h2>
        <p className="section-subtitle">An integrated system from wearable to cloud</p>
        
        <div className="system-diagram">
          <div className="diagram-item">
            <div className="diagram-icon">👤</div>
            <div className="diagram-label">Worker</div>
          </div>
          <div className="diagram-arrow">→</div>
          <div className="diagram-item">
            <div className="diagram-icon">⌚</div>
            <div className="diagram-label">H₂S Sentinel<br />Smartwatch</div>
          </div>
          <div className="diagram-arrow">→</div>
          <div className="diagram-item">
            <div className="diagram-icon">🔌</div>
            <div className="diagram-label">Sensors<br />(H₂S, HR, SpO₂, Temp, Motion)</div>
          </div>
          <div className="diagram-arrow">→</div>
          <div className="diagram-item">
            <div className="diagram-icon">📱</div>
            <div className="diagram-label">Mobile App</div>
          </div>
          <div className="diagram-arrow">→</div>
          <div className="diagram-item">
            <div className="diagram-icon">🤖</div>
            <div className="diagram-label">AI Color<br />Analysis</div>
          </div>
          <div className="diagram-arrow">→</div>
          <div className="diagram-item">
            <div className="diagram-icon">☁️</div>
            <div className="diagram-label">Cloud<br />Database</div>
          </div>
          <div className="diagram-arrow">→</div>
          <div className="diagram-item">
            <div className="diagram-icon">📊</div>
            <div className="diagram-label">Supervisor<br />Dashboard</div>
          </div>
        </div>
      </section>

      {/* AI Color Analysis Section */}
      <section className="section ai-section">
        <h2>AI Color Analysis Pipeline</h2>
        <div className="ai-pipeline">
          <div className="pipeline-step">
            <div className="step-box">Cartridge<br />Image</div>
          </div>
          <div className="pipeline-arrow">→</div>
          <div className="pipeline-step">
            <div className="step-box">Cartridge &<br />Reference Detection</div>
          </div>
          <div className="pipeline-arrow">→</div>
          <div className="pipeline-step">
            <div className="step-box">Lighting<br />Correction</div>
          </div>
          <div className="pipeline-arrow">→</div>
          <div className="pipeline-step">
            <div className="step-box">Feature<br />Extraction<br />(RGB/HSV/CIELAB)</div>
          </div>
          <div className="pipeline-arrow">→</div>
          <div className="pipeline-step">
            <div className="step-box">AI Model<br />Inference</div>
          </div>
          <div className="pipeline-arrow">→</div>
          <div className="pipeline-step">
            <div className="step-box">Estimated<br />Cumulative<br />Exposure</div>
          </div>
        </div>
        <p className="ai-note">The AI model is trained on calibrated cartridge data and laboratory measurements to estimate cumulative H₂S exposure.</p>
      </section>

      {/* Technology Stack*/}
      <section className="section tech-section">
        <h2>Technology Stack</h2>
        <div className="tech-grid">
          <div className="tech-category">
            <h3>Hardware & Sensors</h3>
            <ul>
              <li>ESP32 Microcontroller</li>
              <li>Electronic H₂S Sensor</li>
              <li>Passive H₂S Cartridge</li>
              <li>MAX30102 BioSensor</li>
              <li>Temperature Sensor</li>
              <li>MPU6050 IMU</li>
              <li>OLED Display</li>
              <li>Vibration Motor & Buzzer</li>
              <li>SOS Button</li>
            </ul>
          </div>
          <div className="tech-category">
            <h3>Backend & Cloud</h3>
            <ul>
              <li>Python FastAPI</li>
              <li>SQLite/PostgreSQL</li>
              <li>RESTful APIs</li>
              <li>JWT Authentication</li>
              <li>Deployment Ready</li>
            </ul>
          </div>
          <div className="tech-category">
            <h3>Mobile & Frontend</h3>
            <ul>
              <li>React</li>
              <li>React Router</li>
              <li>Responsive Design</li>
              <li>Real-time Updates</li>
              <li>Professional UI</li>
            </ul>
          </div>
          <div className="tech-category">
            <h3>AI & Image Processing</h3>
            <ul>
              <li>OpenCV</li>
              <li>NumPy</li>
              <li>scikit-learn</li>
              <li>Calibrated Models</li>
              <li>Color Analysis</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Safety Disclaimer */}
      <section className="section safety-section">
        <h2>Safety & Compliance</h2>
        <div className="safety-content">
          <div className="safety-card">
            <h3>Important Disclaimer</h3>
            <p>
              <strong>H₂S Sentinel is a supplementary occupational-safety prototype</strong> and is NOT:
            </p>
            <ul>
              <li>A replacement for certified industrial H₂S detection systems</li>
              <li>A replacement for fixed-site gas monitoring infrastructure</li>
              <li>A replacement for proper personal protective equipment (PPE)</li>
              <li>A replacement for emergency response procedures</li>
            </ul>
            <p>
              Biometric readings (HR, SpO₂) are <strong>supporting safety indicators only</strong> and do not constitute medical diagnosis.
            </p>
            <p>
              Use H₂S Sentinel as part of a comprehensive occupational health and safety program in compliance with OSHA, local regulations, and workplace protocols.
            </p>
          </div>
        </div>
      </section>

      {/* Architecture Section */}
      <section className="section architecture-section">
        <h2>System Architecture</h2>
        <div className="architecture-diagram">
          <div className="arch-box">
            <strong>H₂S SENTINEL</strong>
          </div>
          <div className="arch-level">
            <div className="arch-item">Hardware</div>
            <div className="arch-item">Mobile App</div>
          </div>
          <div className="arch-arrows-down">↓</div>
          <div className="arch-level">
            <div className="arch-item">Image Processing</div>
            <div className="arch-item">Sensors</div>
          </div>
          <div className="arch-arrows-down">↓</div>
          <div className="arch-box">
            <strong>Cloud / Database</strong>
          </div>
          <div className="arch-arrows-down">↓</div>
          <div className="arch-box">
            <strong>Supervisor Dashboard</strong>
          </div>
        </div>
      </section>

      {/* Footer CTA */}
      <section className="section footer-cta">
        <h2>Ready to Enhance Worker Safety?</h2>
        <p>Access the H₂S Sentinel dashboard and start monitoring worker exposure in real-time.</p>
        <button className="btn btn-primary" onClick={() => navigate('/login')}>
          Go to Dashboard
        </button>
      </section>

      <footer className="landing-footer">
        <p>H₂S Sentinel • AI-Powered Worker Safety • Team Valence · SIH26118</p>
      </footer>
    </div>
  );
}
