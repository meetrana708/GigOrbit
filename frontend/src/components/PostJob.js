import React, { useState } from 'react';

function PostJob() {
  const [form, setForm] = useState({ title: '', description: '', company: '', location: 'Remote' });
  const [message, setMessage] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);
    try {
      const res = await fetch('/api/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (res.ok) {
        setMessage({ type: 'success', text: `Job "${data.title}" posted successfully` });
        setForm({ title: '', description: '', company: '', location: 'Remote' });
      } else {
        setMessage({ type: 'error', text: data.error || 'Could not post job' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Network error' });
    }
  };

  return (
    <div>
      <h2>Post a Job</h2>
      {message && <p className={message.type === 'success' ? 'success' : 'error'}>{message.text}</p>}
      <form onSubmit={handleSubmit}>
        <label>Title</label>
        <input type="text" name="title" value={form.title} onChange={handleChange} required />
        <label>Description</label>
        <textarea name="description" value={form.description} onChange={handleChange} rows="4" />
        <label>Company</label>
        <input type="text" name="company" value={form.company} onChange={handleChange} />
        <label>Location</label>
        <input type="text" name="location" value={form.location} onChange={handleChange} />
        <button type="submit">Post Job</button>
      </form>
    </div>
  );
}

export default PostJob;