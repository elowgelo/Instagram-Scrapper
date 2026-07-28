import React from 'react';
import { Heart, MessageCircle, ExternalLink } from 'lucide-react';

export default function PostTable({ posts, activeKeywords = [] }) {
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
    <div className="table-container">
      <table className="custom-table">
        <thead>
          <tr>
            <th>Pengguna (PP)</th>
            <th>Post Media</th>
            <th>Caption / Deskripsi</th>
            <th>Statistik</th>
            <th>Aksi</th>
          </tr>
        </thead>
        <tbody>
          {posts.map((post) => (
            <tr key={post.id}>
              <td style={{ whiteSpace: 'nowrap' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
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
                  <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>@{post.username}</span>
                </div>
              </td>
              <td style={{ width: '70px' }}>
                <img
                  src={post.media_url || 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop'}
                  alt="Thumbnail"
                  className="table-media-preview"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop';
                  }}
                />
              </td>
              <td style={{ maxWidth: '420px', lineHeight: '1.4', color: 'var(--text-secondary)' }}>
                {highlightCaption(post.caption)}
              </td>
              <td style={{ whiteSpace: 'nowrap' }}>
                <div style={{ display: 'flex', gap: '0.8rem', alignItems: 'center', fontSize: '0.85rem' }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', fontWeight: 600 }}>
                    <Heart size={14} color="#ef4444" fill="#ef4444" /> {post.likes_count || 0}
                  </span>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', fontWeight: 600 }}>
                    <MessageCircle size={14} color="#38bdf8" /> {post.comments_count || 0}
                  </span>
                </div>
              </td>
              <td>
                <a
                  href={post.post_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="link-ig"
                  style={{ whiteSpace: 'nowrap' }}
                >
                  Buka IG <ExternalLink size={13} />
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
