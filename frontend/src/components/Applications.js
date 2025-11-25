import React, { useState } from 'react';

function Applications() {
  const [userId, setUserId] = useState('');
  const [applications, setApplications] = useState([]);
  const [message, setMessage] = useState(null);

  const fetchApplications = async () => {
    if (!userId) {
      setMessage({ type: 'error', text: 'Please enter your user ID' });
      return;
    }
    try {
      const res = await fetch(`/api/applications?user_id=${userId}`);
      const data = await res.json();
      if (res.ok) {
        setApplications(data);
        setMessage(null);
      } else {
        setMessage({ type: 'error', text: data.error || 'Could not fetch applications' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Network error' });
    }
  };

  return (
    <div>
      <h2>Your Applications</h2>
      <div>
        <label>Your user ID</label>
        <input type="number" value={userId} onChange={(e) => setUserId(e.target.value)} placeholder="Enter your user ID" />
        <button onClick={fetchApplications}>Fetch Applications</button>
      </div>
      {message && <p className={message.type === 'success' ? 'success' : 'error'}>{message.text}</p>}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {applications.map((app) => (
          <li key={app.id} style={{ marginBottom: '1rem', borderBottom: '1px solid #ccc', paddingBottom: '1rem' }}>
            <p><strong>Application ID:</strong> {app.id}</p>
            <p><strong>Job ID:</strong> {app.job_id}</p>
            <p><strong>Status:</strong> {app.status}</p>
            <p><strong>Date:</strong> {new Date(app.created_at).toLocaleString()}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Applications;