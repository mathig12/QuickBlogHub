import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getPost, submitPostForReview, publishPost } from '../services/api';

const PostView = () => {
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    fetchPost();
  }, [id]);

  const fetchPost = async () => {
    try {
      setLoading(true);
      const data = await getPost(id);
      setPost(data);
      setError(null);
    } catch (err) {
      setError('Failed to load post. It may have been deleted or doesn\'t exist.');
      console.error('Error fetching post:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitForReview = async () => {
    try {
      setActionLoading(true);
      const updatedPost = await submitPostForReview(id);
      setPost(updatedPost);
    } catch (err) {
      setError('Failed to submit post for review. Please try again.');
      console.error('Error submitting post:', err);
    } finally {
      setActionLoading(false);
    }
  };

  const handlePublish = async () => {
    try {
      setActionLoading(true);
      const updatedPost = await publishPost(id);
      setPost(updatedPost);
    } catch (err) {
      setError('Failed to publish post. Please try again.');
      console.error('Error publishing post:', err);
    } finally {
      setActionLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  if (loading) {
    return <div className="loading">Loading post...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-message">{error}</div>
        <Link to="/" className="button secondary-button">Back to Posts</Link>
      </div>
    );
  }

  if (!post) {
    return <div className="not-found">Post not found</div>;
  }

  return (
    <div className="post-view-container">
      <div className="post-header">
        <h2>{post.title}</h2>
        <div className="post-meta">
          <span className={`post-status status-${post.status}`}>
            {post.status.charAt(0).toUpperCase() + post.status.slice(1)}
          </span>
          <span className="post-date">Created on {formatDate(post.created_at)}</span>
        </div>
      </div>

      {post.status === 'flagged' && post.flagged_reasons && (
        <div className="flagged-alert">
          <h3>This post has been flagged for the following reasons:</h3>
          <p>{post.flagged_reasons}</p>
          <p>Please edit your post to address these issues before resubmitting.</p>
        </div>
      )}

      <div className="post-content">
        {post.content.split('\n').map((paragraph, index) => (
          paragraph ? <p key={index}>{paragraph}</p> : <br key={index} />
        ))}
      </div>

      <div className="post-actions">
        <Link to="/" className="button secondary-button">Back to Posts</Link>
        
        {post.status === 'draft' && (
          <>
            <Link to={`/posts/${post.id}/edit`} className="button edit-button">Edit Draft</Link>
            <button 
              className="button primary-button" 
              onClick={handleSubmitForReview}
              disabled={actionLoading}
            >
              {actionLoading ? 'Submitting...' : 'Submit for Review'}
            </button>
          </>
        )}
        
        {post.status === 'flagged' && (
          <Link to={`/posts/${post.id}/edit`} className="button edit-button">Edit & Fix Issues</Link>
        )}
        
        {post.status === 'approved' && (
          <>
            <Link to={`/posts/${post.id}/edit`} className="button edit-button">Edit</Link>
            <button 
              className="button publish-button" 
              onClick={handlePublish}
              disabled={actionLoading}
            >
              {actionLoading ? 'Publishing...' : 'Publish Post'}
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default PostView;
