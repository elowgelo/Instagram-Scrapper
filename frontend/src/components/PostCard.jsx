import React, { useState } from 'react';
import { Heart, MessageCircle, ExternalLink, Copy, Check } from 'lucide-react';

export default function PostCard({ post, activeKeywords = [] }) {
  const [copied, setCopied] = useState(false);

  const handleCopyCaption = () => {
    if (!post.caption) return;
    navigator.clipboard.writeText(post.caption);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const highlightCaption = (caption) => {
    if (!activeKeywords || activeKeywords.length === 0 || !caption) {
      return caption;
    }

    const escapedKws = activeKeywords
      .map(k => k.trim())
      .filter(k => k.length > 0)
      .map(k => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));

    if (escapedKws.length === 0) return caption;

    const regex = new RegExp(`(${escapedKws.join('|')})`, 'gi');
    const parts = caption.split(regex);

    return parts.map((part, idx) => {
      const isMatch = activeKeywords.some(
        kw => kw.toLowerCase() === part.toLowerCase()
      );
      if (isMatch) {
        return (
          <mark key={idx} className="highlight-kw">
            {part}
          </mark>
        );
      }
      return part;
    });
  };

  return (
    <div className="glass-panel post-card">
      <div className="post-header">
        <div className="post-user">
          {post.profile_pic_url ? (
            <img
              src={post.profile_pic_url}
              alt={post.username}
              className="user-avatar-img"
              onError={(e) => {
                e.target.style.display = 'none';
                if (e.target.nextSibling) e.target.nextSibling.style.display = 'flex';
              }}
            />
          ) : null}
          <div className="user-avatar" style={{ display: post.profile_pic_url ? 'none' : 'flex' }}>
            {post.username ? post.username[0].toUpperCase() : 'U'}
          </div>
          <span>@{post.username}</span>
        </div>

        <button
          type="button"
          onClick={handleCopyCaption}
          style={{
            background: 'transparent',
            border: 'none',
            color: copied ? '#10b981' : 'var(--text-secondary)',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '0.3rem',
            fontSize: '0.78rem',
            fontWeight: 600
          }}
          title="Salin Teks Caption"
        >
          {copied ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
          <span>{copied ? 'Tersalin' : 'Salin'}</span>
        </button>
      </div>

      <img
        src={post.media_url || 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop'}
        alt="Post media"
        className="post-media"
        onError={(e) => {
          e.target.onerror = null;
          e.target.src = 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop';
        }}
      />

      <div className="post-body">
        <p className="post-caption">{highlightCaption(post.caption)}</p>
      </div>

      <div className="post-footer">
        <div className="post-stats">
          <span className="stat-item" title="Jumlah Like">
            <Heart size={15} color="#ef4444" fill="#ef4444" />
            {post.likes_count || 0}
          </span>
          <span className="stat-item" title="Jumlah Komentar">
            <MessageCircle size={15} color="#38bdf8" />
            {post.comments_count || 0}
          </span>
        </div>

        <a
          href={post.post_url}
          target="_blank"
          rel="noopener noreferrer"
          className="link-ig"
        >
          Buka IG <ExternalLink size={13} />
        </a>
      </div>
    </div>
  );
}
