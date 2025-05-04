import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getPost, updatePost, submitPostForReview } from '../services/api';

const PostEdit = () => {
  const [post, setPost] = useState(null);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    fetchPost();
  }, [id]);

  const fetchPost = async () => {
    try {
      setLoading(true);
      const data = await getPost(id);
      
      if (data.status === 'published') {
        // Redirect to view if post is published (can't edit published posts)
        navigate(`/posts/${id}`);
        return;
      }
      
      setPost(data);
      setTitle(data.title);
      setContent(data.content);
      setError(null);
    } catch (err) {
      setError('Failed to load post. It may have been deleted or doesn\'t exist.');
      console.error('Error fetching post:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    
    if (!title.trim() || !content.trim()) {
      setError('Title and content are required.');
      return;
    }
    
    try {
      setSaving(true);
      setError(null);
      
      await updatePost(id, { title, content });
      navigate(`/posts/${id}`);
    } catch (err) {
      setError('Failed to save post. Please try again.');
      console.error('Error updating post:', err);
    } finally {
      setSaving(false);
    }
  };

  const handleSubmitForReview = async () => {
    // First save the post, then submit for review
    try {
      setSaving(true);
      setError(null);
      
      await updatePost(id, { title, content });
      await submitPostForReview(id);
      navigate(`/posts/${id}`);
    } catch (err) {
      setError('Failed to submit post for review. Please try again.');
      console.error('Error submitting post:', err);
    } finally {
      setSaving(false);
    }
  };

  const characterCount = content.length;
  const minLength = 50;
  const maxLength = 2000;
  const isLengthValid = characterCount >= minLength && characterCount <= maxLength;

  if (loading) {
    return <div className="loading">Loading post...</div>;
  }

  if (error && !post) {
    return (
      <div className="error-container">
        <div className="error-message">{error}</div>
        <Link to="/" className="button secondary-button">Back to Posts</Link>
      </div>
    );
  }

  return (
    <div className="post-edit-container">
      <h2>Edit Post</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      {post && post.status === 'flagged' && post.flagged_reasons && (
        <div className="flagged-alert">
          <h3>This post has been flagged for the following reasons:</h3>
          <p>{post.flagged_reasons}</p>
          <p>Please address these issues before resubmitting.</p>
        </div>
      )}
      
      <form onSubmit={handleSave} className="post-form">
        <div className="form-group">
          <label htmlFor="title">Title</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            maxLength="100"
            placeholder="Enter a title for your post"
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Write your post content here..."
            rows="10"
            required
          />
          <div className={`character-count ${isLengthValid ? 'valid' : 'invalid'}`}>
            {characterCount} characters
            {characterCount < minLength && ` (${minLength - characterCount} more needed)`}
            {characterCount > maxLength && ` (${characterCount - maxLength} too many)`}
          </div>
        </div>
        
        <div className="form-actions">
          <Link 
            to={`/posts/${id}`} 
            className="button secondary-button"
          >
            Cancel
          </Link>
          <button 
            type="submit" 
            className="button primary-button"
            disabled={saving}
          >
            {saving ? 'Saving...' : 'Save Draft'}
          </button>
          {(post.status === 'draft' || post.status === 'flagged') && (
            <button 
              type="button" 
              className="button review-button"
              onClick={handleSubmitForReview}
              disabled={saving || !isLengthValid}
            >
              {saving ? 'Submitting...' : 'Save & Submit for Review'}
            </button>
          )}
        </div>
      </form>
      
      <div className="post-guidelines">
        <h3>Post Guidelines</h3>
        <ul>
          <li>Posts must be between 50 and 2000 characters in length.</li>
          <li>Avoid using offensive language or profanity.</li>
          <li>Don't use excessive capitalization or exclamation marks.</li>
          <li>Keep your tone respectful and constructive.</li>
        </ul>
      </div>
    </div>
  );
};

export default PostEdit;
