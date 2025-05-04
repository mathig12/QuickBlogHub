import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createPost } from '../services/api';

const PostCreate = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!title.trim() || !content.trim()) {
      setError('Title and content are required.');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      const newPost = await createPost({ title, content });
      navigate(`/posts/${newPost.id}/edit`);
    } catch (err) {
      setError('Failed to create post. Please try again.');
      console.error('Error creating post:', err);
    } finally {
      setLoading(false);
    }
  };

  const characterCount = content.length;
  const minLength = 50;
  const maxLength = 2000;
  const isLengthValid = characterCount >= minLength && characterCount <= maxLength;

  return (
    <div className="post-create-container">
      <h2>Create New Post</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="post-form">
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
          <button 
            type="button" 
            className="button secondary-button"
            onClick={() => navigate('/')}
          >
            Cancel
          </button>
          <button 
            type="submit" 
            className="button primary-button"
            disabled={loading}
          >
            {loading ? 'Creating...' : 'Create Draft'}
          </button>
        </div>
      </form>
      
      <div className="post-guidelines">
        <h3>Post Guidelines</h3>
        <ul>
          <li>Posts must be between 50 and 2000 characters in length.</li>
          <li>Avoid using offensive language or profanity.</li>
          <li>Don't use excessive capitalization or exclamation marks.</li>
          <li>Keep your tone respectful and constructive.</li>
          <li>After creating your draft, you can submit it for review.</li>
        </ul>
      </div>
    </div>
  );
};

export default PostCreate;
