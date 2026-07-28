import React, { useState } from 'react';
import { Filter, Plus, X, Sparkles, SlidersHorizontal, Trash2, ArrowUpDown } from 'lucide-react';

const PRESETS = ["kopi", "diskon", "promo", "tech", "kuliner", "ootd", "investasi", "python"];

export default function KeywordFilterBar({
  keywords = [],
  setKeywords,
  matchMode = 'OR',
  setMatchMode,
  sortBy = 'newest',
  setSortBy
}) {
  const [inputVal, setInputVal] = useState('');

  const addKeyword = (kw) => {
    const trimmed = kw.trim();
    if (trimmed && !keywords.includes(trimmed)) {
      setKeywords([...keywords, trimmed]);
    }
  };

  const removeKeyword = (kwToRemove) => {
    setKeywords(keywords.filter(kw => kw !== kwToRemove));
  };

  const clearAllKeywords = () => {
    setKeywords([]);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && inputVal.trim()) {
      e.preventDefault();
      addKeyword(inputVal);
      setInputVal('');
    }
  };

  const handleAddClick = () => {
    if (inputVal.trim()) {
      addKeyword(inputVal);
      setInputVal('');
    }
  };

  return (
    <div className="glass-panel panel-card keyword-section">
      <div className="panel-title" style={{ justifyContent: 'space-between', marginBottom: '0.75rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <Filter size={20} color="#10b981" />
          Filter & Analisis Kata Kunci Deskripsi / Caption
        </div>

        {keywords.length > 0 && (
          <button
            type="button"
            onClick={clearAllKeywords}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#ef4444',
              cursor: 'pointer',
              fontSize: '0.85rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.3rem',
              fontWeight: 600
            }}
          >
            <Trash2 size={14} /> Reset Filter
          </button>
        )}
      </div>

      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
        <div style={{ flex: 1, minWidth: '280px', display: 'flex', gap: '0.5rem' }}>
          <input
            type="text"
            className="custom-input"
            style={{ paddingLeft: '1rem' }}
            placeholder="Ketik kata kunci / angka lalu tekan Enter (contoh: kopi, 2026, ra)..."
            value={inputVal}
            onChange={(e) => setInputVal(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button type="button" className="btn-secondary" onClick={handleAddClick}>
            <Plus size={16} /> Tambah
          </button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <SlidersHorizontal size={16} color="var(--text-secondary)" />
            <span style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>Mode:</span>
            <select
              className="select-input"
              value={matchMode}
              onChange={(e) => setMatchMode(e.target.value)}
            >
              <option value="OR">OR (Minimal 1 Kata Cocok)</option>
              <option value="AND">AND (Semua Kata Harus Ada)</option>
              <option value="EXACT">EXACT (Pencocokan Kata Utuh)</option>
              <option value="REGEX">REGEX (Ekspresi Reguler)</option>
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <ArrowUpDown size={16} color="var(--text-secondary)" />
            <span style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>Urutkan:</span>
            <select
              className="select-input"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="newest">Terbaru</option>
              <option value="likes">Paling Banyak Like</option>
              <option value="comments">Paling Banyak Komentar</option>
            </select>
          </div>
        </div>
      </div>

      {/* Preset Suggestions */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
        <Sparkles size={14} color="#f59e0b" />
        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Rekomendasi Kata Kunci:</span>
        {PRESETS.map((preset) => (
          <button
            key={preset}
            type="button"
            className="preset-btn"
            onClick={() => addKeyword(preset)}
          >
            + {preset}
          </button>
        ))}
      </div>

      {/* Active Keyword Tag Chips */}
      {keywords.length > 0 && (
        <div className="keyword-chips">
          {keywords.map((kw) => (
            <span key={kw} className="chip">
              #{kw}
              <X
                size={14}
                className="chip-remove"
                onClick={() => removeKeyword(kw)}
              />
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
