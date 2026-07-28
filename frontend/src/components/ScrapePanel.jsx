import React, { useState, useEffect } from 'react';
import { Search, Play, Hash, AtSign, Globe, Loader2, Key, ShieldCheck, CheckCircle2, Check, X, Terminal } from 'lucide-react';

const PIPELINE_STEPS_DEF = [
  "Menginisialisasi engine browser Chromium",
  "Memuat & membuka halaman Instagram",
  "Mengekstrak postingan, username penulis & statistik",
  "Finalisasi & sinkronisasi data ke penyimpanan"
];

export default function ScrapePanel({ onScrape, isScraping, scrapeError }) {
  const [target, setTarget] = useState('');
  const [maxPosts, setMaxPosts] = useState(25);
  const [sessionId, setSessionId] = useState(() => {
    return localStorage.getItem('ig_session_id') || '';
  });
  const [showSessionConfig, setShowSessionConfig] = useState(false);

  // Stepper Pipeline State: Each step status can be: 'pending' | 'running' | 'success' | 'error'
  const [stepStatuses, setStepStatuses] = useState(
    PIPELINE_STEPS_DEF.map(() => 'pending')
  );
  const [activeStepIdx, setActiveStepIdx] = useState(0);

  useEffect(() => {
    let interval;
    if (isScraping) {
      setStepStatuses(['running', 'pending', 'pending', 'pending']);
      setActiveStepIdx(0);

      interval = setInterval(() => {
        setActiveStepIdx((currentIdx) => {
          if (currentIdx < PIPELINE_STEPS_DEF.length - 1) {
            const nextIdx = currentIdx + 1;
            setStepStatuses((prev) => {
              const updated = [...prev];
              updated[currentIdx] = 'success';
              updated[nextIdx] = 'running';
              return updated;
            });
            return nextIdx;
          }
          return currentIdx;
        });
      }, 3000);
    } else {
      if (stepStatuses.some(s => s !== 'pending')) {
        if (scrapeError) {
          setStepStatuses((prev) => {
            const updated = [...prev];
            updated[activeStepIdx] = 'error';
            return updated;
          });
        } else {
          setStepStatuses(PIPELINE_STEPS_DEF.map(() => 'success'));
          const resetTimeout = setTimeout(() => {
            setStepStatuses(PIPELINE_STEPS_DEF.map(() => 'pending'));
          }, 3500);
          return () => clearTimeout(resetTimeout);
        }
      }
    }
    return () => clearInterval(interval);
  }, [isScraping, scrapeError]);

  const handleSessionChange = (e) => {
    const val = e.target.value;
    setSessionId(val);
    localStorage.setItem('ig_session_id', val);
  };

  const handleScrapeSubmit = (e) => {
    e.preventDefault();
    if (!target.trim()) return;
    onScrape(target.trim(), maxPosts, sessionId.trim());
  };

  const isPipelineVisible = isScraping || stepStatuses.some(s => s !== 'pending');

  return (
    <div className="glass-panel panel-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div className="panel-title" style={{ marginBottom: 0 }}>
          <Search size={20} color="#10b981" /> Scrape Instagram Otomatis
        </div>

        <button
          type="button"
          onClick={() => setShowSessionConfig(!showSessionConfig)}
          style={{
            background: sessionId ? 'rgba(16, 185, 129, 0.15)' : 'var(--input-bg)',
            border: `1px solid ${sessionId ? 'rgba(16, 185, 129, 0.4)' : 'var(--border-glass)'}`,
            color: sessionId ? '#34d399' : 'var(--text-secondary)',
            borderRadius: '20px',
            padding: '0.35rem 0.85rem',
            fontSize: '0.8rem',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem',
            fontWeight: 600
          }}
        >
          {sessionId ? <CheckCircle2 size={14} color="#10b981" /> : <Key size={14} color="#10b981" />}
          {sessionId ? 'Session Cookie Aktif' : 'Atur Session Cookie'}
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        <form onSubmit={handleScrapeSubmit} className="scrape-form">
          <div className="input-group">
            {target.startsWith('#') ? (
              <Hash size={18} className="input-icon" color="#10b981" />
            ) : target.startsWith('http') ? (
              <Globe size={18} className="input-icon" color="#10b981" />
            ) : (
              <AtSign size={18} className="input-icon" color="#10b981" />
            )}
            <input
              type="text"
              className="custom-input"
              placeholder="Masukkan @username, #hashtag, atau URL postingan..."
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              disabled={isScraping}
            />
          </div>

          <select
            className="select-input"
            value={maxPosts}
            onChange={(e) => setMaxPosts(Number(e.target.value))}
            disabled={isScraping}
          >
            <option value={10}>Batas 10 Postingan</option>
            <option value={25}>Batas 25 Postingan</option>
            <option value={50}>Batas 50 Postingan</option>
            <option value={100}>Batas 100 Postingan</option>
            <option value={0}>∞ Tidak Terbatas (Semua)</option>
          </select>

          <button
            type="submit"
            className={`btn-primary ${isScraping ? 'scraping-active' : ''}`}
            disabled={isScraping}
          >
            {isScraping ? (
              <>
                <Loader2 size={18} className="spin" color="#ffffff" /> Memproses...
              </>
            ) : (
              <>
                <Play size={18} /> Mulai Scrape
              </>
            )}
          </button>
        </form>

        {/* Multi-Step Pipeline Stepper (Harmonized Emerald Theme) */}
        {isPipelineVisible && (
          <div className="pipeline-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', borderBottom: '1px solid var(--border-glass)', paddingBottom: '0.65rem' }}>
              <Terminal size={15} color="#10b981" /> Progress Execution Pipeline
            </div>

            <div className="pipeline-list">
              {PIPELINE_STEPS_DEF.map((text, idx) => {
                const status = stepStatuses[idx];
                return (
                  <div key={idx} className="pipeline-step">
                    {status === 'running' && (
                      <div className="step-node running" title="Sedang Berproses">
                        <Loader2 size={13} className="spin" />
                      </div>
                    )}
                    {status === 'success' && (
                      <div className="step-node success" title="Selesai">
                        <Check size={13} strokeWidth={3} />
                      </div>
                    )}
                    {status === 'error' && (
                      <div className="step-node error" title="Gagal">
                        <X size={13} strokeWidth={3} />
                      </div>
                    )}
                    {status === 'pending' && (
                      <div className="step-node pending" title="Menunggu">
                        <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'currentColor', opacity: 0.5 }} />
                      </div>
                    )}

                    <span className={`step-text ${status}`}>
                      {text}{status === 'running' ? '...' : ''}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Session Cookie Drawer */}
      {showSessionConfig && (
        <div
          style={{
            marginTop: '1.25rem',
            padding: '1rem 1.25rem',
            background: 'var(--input-bg)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            borderRadius: '12px',
            fontSize: '0.85rem'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 600, color: '#10b981', marginBottom: '0.5rem' }}>
            <ShieldCheck size={16} color="#10b981" /> Instagram Cookie Header
          </div>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem', lineHeight: '1.4' }}>
            Tempelkan baris Cookie lengkap dari Chrome DevTools (F12 &rarr; Network &rarr; Request Headers &rarr; <code>cookie: ...</code>) untuk menarik data postingan secara otomatis.
          </p>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <input
              type="password"
              className="custom-input"
              style={{ paddingLeft: '1rem', flex: 1 }}
              placeholder="Tempelkan seluruh baris cookie di sini..."
              value={sessionId}
              onChange={handleSessionChange}
            />
            {sessionId && (
              <button
                type="button"
                className="btn-secondary"
                onClick={() => {
                  setSessionId('');
                  localStorage.removeItem('ig_session_id');
                }}
                style={{ color: '#ef4444' }}
              >
                Hapus Cookie
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
