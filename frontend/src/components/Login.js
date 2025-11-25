import React, { useState } from 'react';

function Login() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [message, setMessage] = useState(null);
  const [user, setUser] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);
    try {
      const res = await fetch('/api/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (res.ok) {
        setUser(data);
        setMessage({ type: 'success', text: `Welcome, ${data.name}!` });
        setForm({ email: '', password: '' });
      } else {
        setMessage({ type: 'error', text: data.error || 'Login failed' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Network error' });
    }
  };

  return (
    <div>
      <h2>Login</h2>
      {message && <p className={message.type === 'success' ? 'success' : 'error'}>{message.text}</p>}
      {user ? (
        <div>
          <p>You are logged in as {user.email}.</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <label>Email</label>
          <input type="email" name="email" value={form.email} onChange={handleChange} required />
          <label>Password</label>
          <input type="password" name="password" value={form.password} onChange={handleChange} required />
          <button type="submit">Login</button>
        </form>
      )}
    </div>
  );
}

export default Login;