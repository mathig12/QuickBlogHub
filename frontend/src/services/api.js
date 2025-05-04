import axios from 'axios';

// Create an Axios instance with default configuration
const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Handle API errors
const handleApiError = (error) => {
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    console.error('API error response:', error.response.data);
    throw new Error(error.response.data.detail || 'An error occurred while processing your request.');
  } else if (error.request) {
    // The request was made but no response was received
    console.error('API error request:', error.request);
    throw new Error('No response received from server. Please check your connection.');
  } else {
    // Something happened in setting up the request that triggered an Error
    console.error('API setup error:', error.message);
    throw new Error('Error setting up request: ' + error.message);
  }
};

// Get all posts with optional status filter
export const getPosts = async (status = '') => {
  try {
    const url = status ? `/posts/?status=${status}` : '/posts/';
    const response = await api.get(url);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Get a single post by ID
export const getPost = async (id) => {
  try {
    const response = await api.get(`/posts/${id}`);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Create a new post
export const createPost = async (postData) => {
  try {
    const response = await api.post('/posts/', postData);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Update an existing post
export const updatePost = async (id, postData) => {
  try {
    const response = await api.patch(`/posts/${id}`, postData);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Submit a post for review
export const submitPostForReview = async (id) => {
  try {
    const response = await api.post(`/posts/${id}/submit/`);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Publish an approved post
export const publishPost = async (id) => {
  try {
    const response = await api.patch(`/posts/${id}/publish/`);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};
