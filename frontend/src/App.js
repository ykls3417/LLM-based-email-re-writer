import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    reason: '',
    email_text: '',
    instruction: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('/api/rewrite', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>✨ Email Rewriter</h1>
          <p>Transform your emails into professional, polished messages</p>
        </header>

        <div className="content">
          <form onSubmit={handleSubmit} className="form">
            <div className="form-group">
              <label htmlFor="reason">Reason for Email</label>
              <textarea
                id="reason"
                name="reason"
                value={formData.reason}
                onChange={handleInputChange}
                placeholder="Briefly explain the purpose of your email..."
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="email_text">Draft Email</label>
              <textarea
                id="email_text"
                name="email_text"
                value={formData.email_text}
                onChange={handleInputChange}
                placeholder="Enter your draft email here..."
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="instruction">Instructions</label>
              <textarea
                id="instruction"
                name="instruction"
                value={formData.instruction}
                onChange={handleInputChange}
                placeholder="e.g., Be polite and concise, Use formal tone..."
                required
              />
            </div>

            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? 'Rewriting...' : 'Rewrite Email'}
            </button>
          </form>

          {error && (
            <div className="error">
              <h3>Error</h3>
              <p>{error}</p>
            </div>
          )}

          {result && !result.error && (
            <div className="result">
              <h3>✨ Rewritten Email</h3>
              <div className="email-preview">
                <div className="email-header">
                  <div className="email-field">
                    <strong>Subject:</strong> {result.subject || 'No subject provided'}
                  </div>
                  <div className="email-field">
                    <strong>To:</strong> {result.recipient || 'No recipient provided'}
                  </div>
                  <div className="email-field">
                    <strong>From:</strong> {result.sender || 'No sender provided'}
                  </div>
                  <div className="email-field">
                    <strong>Date:</strong> {result.date || 'No date provided'}
                  </div>
                </div>
                <div className="email-body">
                  {result.body || 'No body provided'}
                </div>
              </div>
            </div>
          )}

          {result && result.error && (
            <div className="error">
              <h3>Error in Response</h3>
              <p>{result.error}</p>
              {result.raw_content && (
                <div className="raw-content">
                  <h4>Raw Response:</h4>
                  <pre>{result.raw_content}</pre>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
