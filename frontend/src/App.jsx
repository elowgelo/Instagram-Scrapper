import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import StatsHeader from './components/StatsHeader';
import ScrapePanel from './components/ScrapePanel';
import KeywordFilterBar from './components/KeywordFilterBar';
import PostCard from './components/PostCard';
import PostTable from './components/PostTable';
import { Download, AlertCircle, Sparkles, Database } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export default function App() {
  const [allPosts, setAllPosts] = useState([]);
  const [filteredPosts, setFilteredPosts] = useState([]);
  const [keywords, setKeywords] = useState([]);
  const [matchMode, setMatchMode] = useState('OR');
  const [sortBy, setSortBy] = useState('newest');
  
  const [viewMode, setViewMode] = useState('grid');
  const [isLoading, setIsLoading] = useState(false);
  const [isScraping, setIsScraping] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  // Theme State (Dark / Light)
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('app_theme') || 'dark';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('app_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  const fetchPosts = async () => {
    setIsLoading(true);
    setErrorMsg('');
    try {
      const res = await fetch(`${API_BASE}/api/posts`);
      if (!res.ok) throw new Error('Gagal mengambil postingan');
      const data = await res.json();
      setAllPosts(data);
      setFilteredPosts(data);
    } catch (err) {
      console.error(err);
      setErrorMsg('Gagal terhubung ke backend server.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  const handleFilter = async () => {
    if (allPosts.length === 0) {
      setFilteredPosts([]);
      return;
    }
    
    try {
      const res = await fetch(`${API_BASE}/api/filter`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          keywords,
          match_mode: matchMode,
          posts: allPosts
        })
      });
      if (!res.ok) throw new Error('Gagal memfilter postingan');
      let result = await res.json();

      // Apply Sort Analytics
      if (sortBy === 'likes') {
        result = [...result].sort((a, b) => (b.likes_count || 0) - (a.likes_count || 0));
      } else if (sortBy === 'comments') {
        result = [...result].sort((a, b) => (b.comments_count || 0) - (a.comments_count || 0));
      }

      setFilteredPosts(result);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    handleFilter();
  }, [keywords, matchMode, sortBy, allPosts]);

  const handleScrape = async (target, maxPosts, sessionId) => {
    setIsScraping(true);
    setErrorMsg('');
    setSuccessMsg('');
    try {
      const res = await fetch(`${API_BASE}/api/scrape`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          target,
          max_posts: maxPosts,
          session_id: sessionId || null
        })
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Gagal melakukan scraping postingan Instagram.');
      }

      const newPosts = await res.json();
      
      setAllPosts(prev => {
        const existingIds = new Set(prev.map(p => p.id));
        const uniqueNew = newPosts.filter(p => !existingIds.has(p.id));
        return [...uniqueNew, ...prev];
      });

      const countLabel = newPosts.length;
      setSuccessMsg(`Berhasil meng-scrape ${countLabel} postingan real dari "${target}"!`);
      setTimeout(() => setSuccessMsg(''), 5000);
    } catch (err) {
      console.error(err);
      setErrorMsg(err.message || 'Gagal meng-scrape postingan Instagram.');
    } finally {
      setIsScraping(false);
    }
  };

  const handleClearData = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/posts`, { method: 'DELETE' });
      if (res.ok) {
        setAllPosts([]);
        setFilteredPosts([]);
        setSuccessMsg('Semua data postingan berhasil dibersihkan!');
        setTimeout(() => setSuccessMsg(''), 3000);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleExport = async (format) => {
    if (filteredPosts.length === 0) return;
    try {
      const res = await fetch(`${API_BASE}/api/export`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          posts: filteredPosts,
          format
        })
      });

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `instagram_filtered_posts.${format}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      console.error('Export error:', err);
    }
  };

  return (
    <div>
      <Navbar
        postsCount={allPosts.length}
        filteredCount={filteredPosts.length}
        isLoading={isLoading}
        onRefresh={fetchPosts}
        onClearData={handleClearData}
        theme={theme}
        onToggleTheme={toggleTheme}
      />

      <div className="app-container">
        {errorMsg && (
          <div className="glass-panel" style={{ padding: '1rem 1.25rem', borderColor: 'rgba(239, 68, 68, 0.4)', background: 'rgba(239, 68, 68, 0.15)', color: '#fca5a5', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <AlertCircle size={20} color="#ef4444" />
            <span>{errorMsg}</span>
          </div>
        )}

        {successMsg && (
          <div className="glass-panel" style={{ padding: '1rem 1.25rem', borderColor: 'rgba(16, 185, 129, 0.4)', background: 'rgba(16, 185, 129, 0.15)', color: '#6ee7b7', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <Sparkles size={20} color="#10b981" />
            <span>{successMsg}</span>
          </div>
        )}

        <StatsHeader
          totalCount={allPosts.length}
          filteredCount={filteredPosts.length}
          activeKeywords={keywords}
        />

        <ScrapePanel onScrape={handleScrape} isScraping={isScraping} scrapeError={errorMsg} />

        <KeywordFilterBar
          keywords={keywords}
          setKeywords={setKeywords}
          matchMode={matchMode}
          setMatchMode={setMatchMode}
          sortBy={sortBy}
          setSortBy={setSortBy}
        />

        <div className="glass-panel panel-card">
          <div className="toolbar-bar">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <span className="panel-title" style={{ marginBottom: 0 }}>
                Postingan Hasil Filter ({filteredPosts.length})
              </span>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
              <div className="view-toggle">
                <button
                  type="button"
                  className={`toggle-btn ${viewMode === 'grid' ? 'active' : ''}`}
                  onClick={() => setViewMode('grid')}
                >
                  Grid
                </button>
                <button
                  type="button"
                  className={`toggle-btn ${viewMode === 'table' ? 'active' : ''}`}
                  onClick={() => setViewMode('table')}
                >
                  Tabel
                </button>
              </div>

              <button
                type="button"
                className="btn-secondary"
                onClick={() => handleExport('csv')}
                disabled={filteredPosts.length === 0}
              >
                <Download size={16} /> Export CSV
              </button>
              <button
                type="button"
                className="btn-secondary"
                onClick={() => handleExport('json')}
                disabled={filteredPosts.length === 0}
              >
                <Download size={16} /> Export JSON
              </button>
            </div>
          </div>

          <div style={{ marginTop: '1.5rem' }}>
            {filteredPosts.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '3.5rem 1rem', color: 'var(--text-secondary)' }}>
                <Database size={42} style={{ marginBottom: '0.75rem', opacity: 0.5 }} />
                <p style={{ fontSize: '1.05rem', fontWeight: 600, color: 'var(--text-primary)' }}>Tidak Ada Postingan</p>
                <p style={{ fontSize: '0.88rem', marginTop: '0.25rem' }}>
                  {allPosts.length === 0
                    ? 'Belum ada postingan yang di-scrape. Gunakan panel di atas untuk melakukan scrape.'
                    : 'Tidak ada postingan yang cocok dengan kata kunci filter saat ini.'}
                </p>
              </div>
            ) : viewMode === 'grid' ? (
              <div className="feed-grid">
                {filteredPosts.map((post) => (
                  <PostCard key={post.id} post={post} activeKeywords={keywords} />
                ))}
              </div>
            ) : (
              <PostTable posts={filteredPosts} activeKeywords={keywords} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
