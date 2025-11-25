import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div>
      <h2>Welcome to GigOrbit ATS</h2>
      <p>
        GigOrbit ATS is a remote‑first applicant tracking system designed to
        connect freelancers and cloud professionals with projects around the
        world. Explore job postings, create your profile and apply for
        opportunities.
      </p>
      <p>
        Ready to get started? <Link to="/register">Register now</Link> or browse our <Link to="/jobs">open jobs</Link>.
      </p>
    </div>
  );
}

export default Home;