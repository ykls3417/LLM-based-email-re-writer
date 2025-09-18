import React, { useEffect, useState } from 'react';
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
  const [copied, setCopied] = useState(false);

  // Settings sidebar state
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [settings, setSettings] = useState({
    api_key: '',
    model: '',
    base_url: ''
  });

  // Load settings from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem('email_rewriter_settings');
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setSettings(prev => ({ ...prev, ...parsed }));
      } catch (_) {}
    }
  }, []);

  const handleSettingsChange = (e) => {
    const { name, value } = e.target;
    setSettings(prev => {
      const next = { ...prev, [name]: value };
      localStorage.setItem('email_rewriter_settings', JSON.stringify(next));
      return next;
    });
  };

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
        body: JSON.stringify({
          ...formData,
          // optional settings
          api_key: settings.api_key?.trim() || undefined,
          model: settings.model?.trim() || undefined,
          base_url: settings.base_url?.trim() || undefined,
        }),
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
      <div className={`sidebar ${isSidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h2>Settings</h2>
          <button
            className="sidebar-toggle"
            onClick={() => setIsSidebarOpen(o => !o)}
            aria-label={isSidebarOpen ? 'Close settings' : 'Open settings'}
          >
            {isSidebarOpen ? '⟨' : '⟩'}
          </button>
        </div>
        {isSidebarOpen && (
          <div className="sidebar-content">
            <div className="sidebar-field">
              <label htmlFor="api_key">API Key</label>
              <input
                id="api_key"
                name="api_key"
                type="password"
                placeholder="sk-..."
                value={settings.api_key}
                onChange={handleSettingsChange}
                autoComplete="off"
              />
            </div>
            <div className="sidebar-field">
              <label htmlFor="model">Model</label>
              <input
                id="model"
                name="model"
                type="text"
                placeholder="e.g. deepseek/deepseek-chat-v3-0324:free"
                value={settings.model}
                onChange={handleSettingsChange}
                autoComplete="off"
              />
            </div>
            <div className="sidebar-field">
              <label htmlFor="base_url">Base URL</label>
              <input
                id="base_url"
                name="base_url"
                type="text"
                placeholder="https://openrouter.ai/api/v1"
                value={settings.base_url}
                onChange={handleSettingsChange}
                autoComplete="off"
              />
            </div>
            <div className="sidebar-hint">Values here override server defaults for this session.</div>
          </div>
        )}
      </div>
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
                </div>
                <div className="email-body">
                  {result.body || 'No body provided'}
                </div>
                <div className="actions">
                  <button
                    type="button"
                    className="copy-btn"
                    onClick={async () => {
                      try {
                        await navigator.clipboard.writeText(result.body || '');
                        setCopied(true);
                        setTimeout(() => setCopied(false), 1600);
                      } catch (err) {
                        setError('Failed to copy to clipboard');
                      }
                    }}
                  >
                    Copy Rewritten Email
                  </button>
                  {copied && (
                    <span className="copy-toast">Copied to Clipboard!</span>
                  )}
                </div>
                {result.caution && (
                  <div className="email-field caution-strong">
                    <strong style={{ color: '#b20000', textTransform: 'uppercase', letterSpacing: '1px' }}>
                      ⚠️ Important Caution:
                    </strong>
                    <span style={{ color: '#b20000', fontWeight: 600, marginLeft: 8 }}>
                      {result.caution}
                    </span>
                  </div>
                )}
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
