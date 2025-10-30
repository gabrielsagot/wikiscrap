import { useState } from 'react';
import ColorBends from './ColorBends';

export default function App() {
  const [showModal, setShowModal] = useState(false);

  const codeOptions = [
    {
      title: "Code du WebScraping",
      description: "Scraping des sites UNESCO en France",
      icon: "fa-code",
      color: "#60a5fa",
      gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      url: "./code.html"
    },
    {
      title: "Code API V1",
      description: "API Vélib Paris - Version simple",
      icon: "fa-bicycle",
      color: "#10b981",
      gradient: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
      url: "./codeAPI_1.html"
    },
    {
      title: "Code API V2",
      description: "Dashboard Vélib interactif complet",
      icon: "fa-chart-line",
      color: "#f59e0b",
      gradient: "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
      url: "./codeAPI_2.html"
    }
  ];

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
          justifyContent: 'center',
          transition: 'all 0.3s ease',
          cursor: 'pointer'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = 'rgba(255, 255, 255, 0.12)';
          e.currentTarget.style.transform = 'translateX(-50%) translateY(-2px)';
          e.currentTarget.style.boxShadow = '0 10px 30px rgba(96, 165, 250, 0.3)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'rgba(255, 255, 255, 0.08)';
          e.currentTarget.style.transform = 'translateX(-50%) translateY(0)';
          e.currentTarget.style.boxShadow = 'none';
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #60a5fa, #a78bfa)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'transform 0.3s ease'
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
                boxShadow: '0 20px 50px rgba(255, 255, 255, 0.3)',
                transition: 'all 0.3s ease',
                transform: 'translateY(0)'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-5px) scale(1.05)';
                e.currentTarget.style.boxShadow = '0 30px 60px rgba(255, 255, 255, 0.5)';
                e.currentTarget.style.background = '#f0f0f0';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0) scale(1)';
                e.currentTarget.style.boxShadow = '0 20px 50px rgba(255, 255, 255, 0.3)';
                e.currentTarget.style.background = 'white';
              }}>
              Consulter la carte
              <i className="fas fa-map-marked-alt" style={{ fontSize: '18px' }}></i>
            </button>

            <button
              onClick={() => setShowModal(true)}
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
                gap: '14px',
                transition: 'all 0.3s ease',
                transform: 'translateY(0)'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-5px) scale(1.05)';
                e.currentTarget.style.background = 'rgba(96, 165, 250, 0.25)';
                e.currentTarget.style.borderColor = 'rgba(96, 165, 250, 0.5)';
                e.currentTarget.style.boxShadow = '0 20px 40px rgba(96, 165, 250, 0.4)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0) scale(1)';
                e.currentTarget.style.background = 'rgba(96, 165, 250, 0.15)';
                e.currentTarget.style.borderColor = 'rgba(96, 165, 250, 0.3)';
                e.currentTarget.style.boxShadow = 'none';
              }}>
              <i className="fas fa-code" style={{ fontSize: '18px' }}></i>
              Consulter les codes
            </button>

            <button
              onClick={() => window.location.href = './rapport.html'}
              style={{
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
              gap: '14px',
              transition: 'all 0.3s ease',
              transform: 'translateY(0)'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-5px) scale(1.05)';
              e.currentTarget.style.background = 'rgba(0, 0, 0, 0.5)';
              e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.4)';
              e.currentTarget.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.6)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0) scale(1)';
              e.currentTarget.style.background = 'rgba(0, 0, 0, 0.3)';
              e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.2)';
              e.currentTarget.style.boxShadow = 'none';
            }}>
              <i className="fas fa-file-alt" style={{ fontSize: '18px' }}></i>
              Rapport collectif
            </button>
          </div>
        </div>
      </div>

      {/* Modal de sélection de code */}
      {showModal && (
        <div
          onClick={() => setShowModal(false)}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0, 0, 0, 0.8)',
            backdropFilter: 'blur(10px)',
            zIndex: 1000,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '20px',
            animation: 'fadeIn 0.3s ease'
          }}>
          <style>
            {`
              @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
              }
              @keyframes slideUp {
                from {
                  opacity: 0;
                  transform: translateY(30px) scale(0.95);
                }
                to {
                  opacity: 1;
                  transform: translateY(0) scale(1);
                }
              }
            `}
          </style>
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              background: 'rgba(255, 255, 255, 0.95)',
              backdropFilter: 'blur(20px)',
              borderRadius: '24px',
              padding: '40px',
              maxWidth: '900px',
              width: '100%',
              boxShadow: '0 40px 100px rgba(0, 0, 0, 0.5)',
              animation: 'slideUp 0.4s ease',
              position: 'relative'
            }}>
            {/* Bouton fermer */}
            <button
              onClick={() => setShowModal(false)}
              style={{
                position: 'absolute',
                top: '20px',
                right: '20px',
                width: '40px',
                height: '40px',
                borderRadius: '50%',
                border: 'none',
                background: 'rgba(0, 0, 0, 0.05)',
                color: '#666',
                fontSize: '20px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(0, 0, 0, 0.1)';
                e.currentTarget.style.transform = 'rotate(90deg)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'rgba(0, 0, 0, 0.05)';
                e.currentTarget.style.transform = 'rotate(0deg)';
              }}>
              <i className="fas fa-times"></i>
            </button>

            {/* Titre */}
            <h2 style={{
              fontSize: '32px',
              fontWeight: '700',
              color: '#1a1a1a',
              marginBottom: '12px',
              textAlign: 'center'
            }}>
              Choisir un code à consulter
            </h2>
            <p style={{
              fontSize: '16px',
              color: '#666',
              marginBottom: '40px',
              textAlign: 'center'
            }}>
              Sélectionnez le code source que vous souhaitez consulter
            </p>

            {/* Grille de cartes */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
              gap: '20px'
            }}>
              {codeOptions.map((option, index) => (
                <button
                  key={index}
                  onClick={() => window.location.href = option.url}
                  style={{
                    background: 'white',
                    border: '2px solid rgba(0, 0, 0, 0.08)',
                    borderRadius: '16px',
                    padding: '30px 24px',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    textAlign: 'center',
                    position: 'relative',
                    overflow: 'hidden'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-8px)';
                    e.currentTarget.style.boxShadow = `0 20px 40px ${option.color}40`;
                    e.currentTarget.style.borderColor = option.color;
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = 'none';
                    e.currentTarget.style.borderColor = 'rgba(0, 0, 0, 0.08)';
                  }}>
                  {/* Icône */}
                  <div style={{
                    width: '70px',
                    height: '70px',
                    borderRadius: '50%',
                    background: option.gradient,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    margin: '0 auto 20px',
                    boxShadow: `0 10px 30px ${option.color}40`
                  }}>
                    <i className={`fas ${option.icon}`} style={{
                      fontSize: '28px',
                      color: 'white'
                    }}></i>
                  </div>

                  {/* Titre */}
                  <h3 style={{
                    fontSize: '20px',
                    fontWeight: '700',
                    color: '#1a1a1a',
                    marginBottom: '8px'
                  }}>
                    {option.title}
                  </h3>

                  {/* Description */}
                  <p style={{
                    fontSize: '14px',
                    color: '#666',
                    lineHeight: '1.5'
                  }}>
                    {option.description}
                  </p>

                  {/* Flèche */}
                  <div style={{
                    marginTop: '16px',
                    color: option.color,
                    fontSize: '18px',
                    fontWeight: '600'
                  }}>
                    Voir le code →
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
