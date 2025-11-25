import React from 'react';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import Home from './components/Home';
import Register from './components/Register';
import Login from './components/Login';
import Jobs from './components/Jobs';
import PostJob from './components/PostJob';
import Applications from './components/Applications';
import ResumeParser from './components/ResumeParser';

function App() {
  return (
    <div>
      <header>
        <h1>GigOrbit ATS</h1>
        <p style={{ marginTop: '-0.5rem' }}>Global freelancers, aligned to your projects.</p>
      </header>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/jobs">Jobs</Link>
        <Link to="/post-job">Post Job</Link>
        <Link to="/applications">Applications</Link>
        <Link to="/parse">Parse Resume</Link>
        <Link to="/register">Register</Link>
        <Link to="/login">Login</Link>
      </nav>
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/post-job" element={<PostJob />} />
          <Route path="/applications" element={<Applications />} />
          <Route path="/parse" element={<ResumeParser />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;