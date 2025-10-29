import ColorBends from './ColorBends';

export default function App() {
  return (
    <div className="page" style={{ background: '#000', width: '100%', height: '100vh', position: 'relative' }}>
      {/* Background - ne pas toucher */}
      <div style={{ width: '100%', height: '100%' }}>
        <ColorBends
          colors={["#ff0000", "#00ff00", "#0000ff"]}
          scale={1}
          frequency={1}
          warpStrength={1}
          transparent={false}
        />
      </div>

      {/* Interface par-dessus le fond */}
      <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, zIndex: 10 }}>
        {/* Navigation Bar */}
        <nav style={{
          position: 'absolute',
          top: '32px',
          left: '50%',
          transform: 'translateX(-50%)',
          padding: '16px 32px',
          background: 'rgba(255, 255, 255, 0.08)',
          backdropFilter: 'blur(20px)',
          borderRadius: '9999px',
          border: '1px solid rgba(255, 255, 255, 0.15)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #60a5fa, #a78bfa)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <i className="fas fa-star" style={{ color: 'white', fontSize: '16px' }}></i>
            </div>
            <span style={{ color: 'white', fontWeight: '600', fontSize: '20px', letterSpacing: '-0.01em' }}>WikiScrap UNESCO</span>
          </div>
        </nav>

        {/* Contenu central */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
          padding: '32px'
        }}>
          {/* Grand titre */}
          <h1 style={{
            textAlign: 'center',
            marginBottom: '60px',
            maxWidth: '1600px'
          }}>
            <div style={{
              fontSize: '160px',
              fontWeight: '700',
              color: 'white',
              lineHeight: '1',
              marginBottom: '20px',
              letterSpacing: '-0.03em',
              fontFamily: 'system-ui, -apple-system, sans-serif'
            }}>
              Sites UNESCO
            </div>
            <div style={{
              fontSize: '160px',
              fontWeight: '700',
              color: 'white',
              lineHeight: '1',
              letterSpacing: '-0.03em',
              fontFamily: 'system-ui, -apple-system, sans-serif'
            }}>
              de France
            </div>
          </h1>

          {/* Boutons CTA */}
          <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', justifyContent: 'center' }}>
            <button
              onClick={() => window.location.href = './carte_unesco_france.html'}
              style={{
                padding: '18px 40px',
                background: 'white',
                color: 'black',
                borderRadius: '9999px',
                fontWeight: '600',
                fontSize: '20px',
                border: 'none',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '14px',
                boxShadow: '0 20px 50px rgba(255, 255, 255, 0.3)'
              }}>
              Commencer
              <i className="fas fa-arrow-right" style={{ fontSize: '18px' }}></i>
            </button>

            <button
              onClick={() => window.location.href = './code.html'}
              style={{
                padding: '18px 40px',
                background: 'rgba(96, 165, 250, 0.15)',
                backdropFilter: 'blur(10px)',
                color: '#60a5fa',
                borderRadius: '9999px',
                fontWeight: '600',
                fontSize: '20px',
                border: '1px solid rgba(96, 165, 250, 0.3)',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '14px'
              }}>
              <i className="fas fa-code" style={{ fontSize: '18px' }}></i>
              Consulter le code
            </button>

            <button style={{
              padding: '18px 40px',
              background: 'rgba(0, 0, 0, 0.3)',
              backdropFilter: 'blur(10px)',
              color: 'white',
              borderRadius: '9999px',
              fontWeight: '600',
              fontSize: '20px',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '14px'
            }}>
              <i className="fas fa-file-alt" style={{ fontSize: '18px' }}></i>
              Rapport collectif
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}