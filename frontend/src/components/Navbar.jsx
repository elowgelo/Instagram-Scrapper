import React from 'react';
import { Camera, Trash2, Sun, Moon } from 'lucide-react';

export default function Navbar({ postsCount, filteredCount, isLoading, onClearData, theme, onToggleTheme }) {
  return (
    <nav className="navbar">
      <div className="brand">
        <div className="brand-logo">
          <Camera size={22} />
        </div>
        <div>
          <span className="brand-title">IG Scraper & Filter</span>
          <span className="brand-badge" style={{ marginLeft: '0.6rem' }}>Live Scraping</span>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
        <button
          type="button"
          onClick={onToggleTheme}
          style={{
            background: 'var(--input-bg)',
            border: '1px solid var(--border-glass)',
            color: 'var(--text-primary)',
            borderRadius: '10px',
            width: '38px',
            height: '38px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            transition: 'var(--transition-fast)'
          }}
          title={theme === 'dark' ? 'Ganti ke Mode Terang' : 'Ganti ke Mode Gelap'}
        >
          {theme === 'dark' ? <Sun size={18} color="#10b981" /> : <Moon size={18} color="#10b981" />}
        </button>

        {postsCount > 0 && (
          <button
            type="button"
            className="btn-secondary"
            onClick={onClearData}
            style={{
              color: '#ef4444',
              borderColor: 'rgba(239, 68, 68, 0.3)',
              width: '38px',
              height: '38px',
              padding: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
            title="Hapus semua data postingan dari database"
          >
            <Trash2 size={18} />
          </button>
        )}
      </div>
    </nav>
  );
}
