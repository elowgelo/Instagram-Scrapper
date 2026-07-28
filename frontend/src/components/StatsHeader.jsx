import React from 'react';
import { Database, Filter, Percent, Tag } from 'lucide-react';

export default function StatsHeader({ totalCount, filteredCount, activeKeywords }) {
  const matchPercentage = totalCount > 0 ? Math.round((filteredCount / totalCount) * 100) : 0;

  return (
    <div className="stats-grid">
      <div className="glass-panel stat-card">
        <div className="stat-info">
          <div className="stat-label">Total Postingan Di-Scrape</div>
          <div className="stat-value">{totalCount}</div>
        </div>
        <div className="stat-icon" style={{ background: 'rgba(16, 185, 129, 0.12)', color: '#10b981' }}>
          <Database size={24} />
        </div>
      </div>

      <div className="glass-panel stat-card">
        <div className="stat-info">
          <div className="stat-label">Lolos Keyword Filter</div>
          <div className="stat-value" style={{ color: '#10b981' }}>{filteredCount}</div>
        </div>
        <div className="stat-icon" style={{ background: 'rgba(16, 185, 129, 0.2)', color: '#34d399' }}>
          <Filter size={24} />
        </div>
      </div>

      <div className="glass-panel stat-card">
        <div className="stat-info">
          <div className="stat-label">Rasio Match (%)</div>
          <div className="stat-value" style={{ color: '#34d399' }}>{matchPercentage}%</div>
        </div>
        <div className="stat-icon" style={{ background: 'rgba(16, 185, 129, 0.12)', color: '#10b981' }}>
          <Percent size={24} />
        </div>
      </div>

      <div className="glass-panel stat-card">
        <div className="stat-info">
          <div className="stat-label">Kata Kunci Aktif</div>
          <div className="stat-value" style={{ fontSize: '1.25rem' }}>
            {activeKeywords.length > 0 ? `${activeKeywords.length} Tag` : 'Semua Post'}
          </div>
        </div>
        <div className="stat-icon" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#10b981' }}>
          <Tag size={24} />
        </div>
      </div>
    </div>
  );
}
