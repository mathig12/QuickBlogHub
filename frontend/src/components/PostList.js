import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getPosts } from '../services/api';

const PostList = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    fetchPosts();
  }, [statusFilter]);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const data = await getPosts(statusFilter);
      setPosts(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch posts. Please try again later.');
      console.error('Error fetching posts:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'draft': return 'status-draft';
      case 'flagged': return 'status-flagged';
      case 'approved': return 'status-approved';
      case 'published': return 'status-published';
      default: return '';
    }
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  return (
    <div className="post-list-container">
      <h2>Your Posts</h2>
      
      <div className="filter-container">
        <label htmlFor="status-filter">Filter by status:</label>
        <select 
          id="status-filter"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">All Posts</option>
          <option value="draft">Drafts</option>
          <option value="flagged">Flagged</option>
          <option value="approved">Approved</option>
          <option value="published">Published</option>
        </select>
      </div>

      {loading ? (
        <p>Loading posts...</p>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : posts.length === 0 ? (
        <p>No posts found. {statusFilter && `Try a different filter or `}<Link to="/posts/new">create a new post</Link>.</p>
      ) : (
        <div className="posts-grid">
          {posts.map((post) => (
            <div key={post.id} className="post-card">
              <h3>
                <Link to={`/posts/${post.id}`}>{post.title}</Link>
              </h3>
              <p className="post-excerpt">
                {post.content.substring(0, 120)}
                {post.content.length > 120 ? '...' : ''}
              </p>
              <div className="post-meta">
                <span className={`post-status ${getStatusClass(post.status)}`}>
                  {post.status.charAt(0).toUpperCase() + post.status.slice(1)}
                </span>
                <span className="post-date">{formatDate(post.created_at)}</span>
              </div>
              <div className="post-actions">
                <Link to={`/posts/${post.id}`} className="button view-button">View</Link>
                {post.status !== 'published' && (
                  <Link to={`/posts/${post.id}/edit`} className="button edit-button">Edit</Link>
                )}
              </div>
              {post.status === 'flagged' && post.flagged_reasons && (
                <div className="flagged-reasons">
                  <p><strong>Flagged for:</strong> {post.flagged_reasons}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="create-post-cta">
        <Link to="/posts/new" className="button primary-button">Create New Post</Link>
      </div>
    </div>
  );
};

export default PostList;
