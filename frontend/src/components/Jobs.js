import React, { useState, useEffect } from 'react';

function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [applyInfo, setApplyInfo] = useState({ user_id: '', job_id: null });
  const [message, setMessage] = useState(null);

  useEffect(() => {
    fetch('/api/jobs')
      .then((res) => res.json())
      .then((data) => {
        setJobs(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const handleApply = async (jobId) => {
    if (!applyInfo.user_id) {
      setMessage({ type: 'error', text: 'Please enter your user ID to apply' });
      return;
    }
    try {
      const res = await fetch('/api/applications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: applyInfo.user_id, job_id: jobId }),
      });
      const data = await res.json();
      if (res.ok) {
        setMessage({ type: 'success', text: `Applied for job ${jobId}` });
      } else {
        setMessage({ type: 'error', text: data.error || 'Unable to apply' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Network error' });
    }
  };

  return (
    <div>
      <h2>Open Jobs</h2>
      <div>
        <label>Your user ID</label>
        <input
          type="number"
          value={applyInfo.user_id}
          onChange={(e) => setApplyInfo({ ...applyInfo, user_id: e.target.value })}
          placeholder="Enter your user ID"
        />
      </div>
      {message && <p className={message.type === 'success' ? 'success' : 'error'}>{message.text}</p>}
      {loading ? (
        <p>Loading jobs…</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {jobs.map((job) => (
            <li key={job.id} style={{ marginBottom: '1rem', borderBottom: '1px solid #ccc', paddingBottom: '1rem' }}>
              <h3>{job.title}</h3>
              <p><strong>Company:</strong> {job.company || 'N/A'}</p>
              <p><strong>Location:</strong> {job.location || 'Remote'}</p>
              <p>{job.description}</p>
              <button onClick={() => handleApply(job.id)}>Apply</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Jobs;