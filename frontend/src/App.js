import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import PostList from './components/PostList';
import PostCreate from './components/PostCreate';
import PostView from './components/PostView';
import PostEdit from './components/PostEdit';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <header className="app-header">
          <h1>Content Publishing Platform</h1>
          <nav>
            <ul className="nav-links">
              <li>
                <Link to="/">Home</Link>
              </li>
              <li>
                <Link to="/posts/new">Create Post</Link>
              </li>
            </ul>
          </nav>
        </header>

        <main className="app-main">
          <Routes>
            <Route path="/" element={<PostList />} />
            <Route path="/posts/new" element={<PostCreate />} />
            <Route path="/posts/:id" element={<PostView />} />
            <Route path="/posts/:id/edit" element={<PostEdit />} />
          </Routes>
        </main>

        <footer className="app-footer">
          <p>&copy; 2023 Content Publishing Platform</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
