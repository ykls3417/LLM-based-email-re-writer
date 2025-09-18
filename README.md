# Email Rewriter

Email Rewriter is a small full‑stack application that turns draft emails into clear, professional messages using an LLM. It includes a Flask backend and a React frontend (served as a static build by Flask).

## What it does

- Accepts three inputs: reason for the email, your draft email text, and any specific instructions.
- Calls an LLM to rewrite the email while preserving key facts, dates, and requests.
- Presents the rewritten email with Subject, To, From, Body, and an optional caution note.
- Provides a Copy Rewritten Email button to copy the body text to your clipboard with a confirmation toast.
- Includes a left settings sidebar where you can set your own API key, model, and base URL. These values override server defaults and are stored locally in your browser (localStorage) for convenience.

## Advantages

- Flexible model and provider: set your own model and base URL to use OpenAI‑compatible APIs (e.g., OpenRouter).
- No server‑side storage: the app does not persist your content or keys on the server; settings are stored only in your browser.
- Time‑aware prompt hints: gently nudges the model to interpret time references relative to the current date when such references appear.
- Robust JSON handling: retries and cleans common wrappers to improve response parsing resilience.
- Simple deployment: single Flask service can serve both the API and the static React build.

## Run locally

Prerequisites:

- Python 3.10+
- Node.js 18+ (only needed if you want to rebuild the frontend)

1) Clone and install backend dependencies

```bash
pip install -r requirements.txt
```

Optionally, set a default API key for the backend process (you can still override it in the UI):

```bash
# PowerShell (Windows)
$env:OPENROUTER_API_KEY = "sk-..."

# Bash
export OPENROUTER_API_KEY="sk-..."
```

2) (Optional) Build the frontend

If you want to modify the UI or rebuild the static assets:

```bash
cd frontend
npm install
npm run build
cd ..
```

3) Start the app

```bash
python app.py
```

Open http://localhost:5000 in your browser.

Using your own key and model without environment variables:

- Open the Settings sidebar (left side of the page).
- Enter your API key, model name, and base URL.
- Submit your email for rewriting; these values will be sent only with your requests and saved locally in your browser.

Notes:

- By default, the server uses `https://openrouter.ai/api/v1` and the model `deepseek/deepseek-chat-v3-0324:free` unless you override them via the Settings sidebar or environment variable.
- The backend serves the static React build from `frontend/build`. If you run a separate React dev server, you will need to configure a proxy to the Flask API; this repository is configured to serve the production build directly.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Contributing

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a Pull Request.