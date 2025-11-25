import React, { useState } from 'react';

function ResumeParser() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [message, setMessage] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);
    if (!file) {
      setMessage({ type: 'error', text: 'Please upload a PDF resume' });
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch('/api/parse', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        setResult(data);
      } else {
        setMessage({ type: 'error', text: data.error || 'Failed to parse resume' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Network error' });
    }
  };

  return (
    <div>
      <h2>Resume Parser</h2>
      {message && <p className={message.type === 'success' ? 'success' : 'error'}>{message.text}</p>}
      <form onSubmit={handleSubmit}>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button type="submit">Parse</button>
      </form>
      {result && (
        <div style={{ marginTop: '1rem' }}>
          <h3>Parsed Results</h3>
          <p><strong>Name:</strong> {result.name || 'N/A'}</p>
          <p><strong>Email:</strong> {result.email || 'N/A'}</p>
          <p><strong>Phone:</strong> {result.phone || 'N/A'}</p>
        </div>
      )}
    </div>
  );
}

export default ResumeParser;