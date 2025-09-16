# ✨ Email Rewriter

A full-stack web application that uses AI to rewrite emails into professional, polished messages. Built with Flask backend and React frontend.

## 🚀 Features

- **AI-Powered Rewriting**: Uses DeepSeek AI model via OpenRouter API
- **Professional Output**: Generates properly formatted emails with subject, recipient, sender, date, and body
- **Modern UI**: Clean, bright, and responsive design
- **Easy Deployment**: Ready for local development and web deployment

## 📋 Requirements

- Python 3.11+
- Node.js 16+
- OpenRouter API key

## 🛠️ Local Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd LLM-based-email-re-writer
```

### 2. Set up environment variables
Create a `.env` file in the root directory:
```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Get your API key from [OpenRouter](https://openrouter.ai/)

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Node.js dependencies and build frontend
```bash
cd frontend
npm install
npm run build
cd ..
```

### 5. Run the application
```bash
python app.py
```

The app will be available at `http://localhost:5000`

## 🌐 Usage

1. **Reason for Email**: Briefly explain the purpose of your email
2. **Draft Email**: Enter your rough draft email text
3. **Instructions**: Specify how you want the email rewritten (e.g., "Be polite and concise")

### Example Input:
- **Reason**: "I, Marco Ho, as a student, want to have a quick meeting with the professor to discuss the project, on tmr afternoon."
- **Draft Email**: "Hi, can we meet tmrw? Thx!"
- **Instructions**: "Be polite and concise"

### Example Output:
```json
{
  "subject": "Meeting Request for Project Discussion",
  "recipient": "Professor [Name]",
  "sender": "Marco Ho",
  "date": "Tomorrow",
  "body": "Dear Professor,\n\nI hope this email finds you well. I am writing to request a brief meeting to discuss the project we are working on. Would tomorrow afternoon be convenient for you?\n\nThank you for your time.\n\nBest regards,\nMarco Ho"
}
```

## 🚀 Deployment

### Option 1: Heroku Deployment

1. Create a Heroku app:
```bash
heroku create your-app-name
```

2. Set environment variables:
```bash
heroku config:set OPENROUTER_API_KEY=your_api_key
```

3. Build and deploy:
```bash
chmod +x build.sh
./build.sh
git add .
git commit -m "Deploy email rewriter"
git push heroku main
```

### Option 2: Railway Deployment

1. Connect your GitHub repository to Railway
2. Add environment variable `OPENROUTER_API_KEY`
3. Railway will automatically detect and deploy the Flask app

### Option 3: Render Deployment

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set environment variable `OPENROUTER_API_KEY`
4. Deploy

## 📁 Project Structure

```
LLM-based-email-re-writer/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment config
├── runtime.txt           # Python version
├── build.sh              # Build script
├── .env                  # Environment variables (create this)
├── frontend/
│   ├── package.json      # Node.js dependencies
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js        # Main React component
│       ├── App.css       # Styles
│       ├── index.js      # React entry point
│       └── index.css     # Global styles
└── README.md
```

## 🔧 Development

### Running in Development Mode

1. **Backend** (Terminal 1):
```bash
python app.py
```

2. **Frontend** (Terminal 2):
```bash
cd frontend
npm start
```

The frontend will run on `http://localhost:3000` with hot reloading.

### API Endpoints

- `GET /` - Serves the React frontend
- `POST /api/rewrite` - Rewrites email based on provided data

## 🎨 Customization

The UI is designed to be bright, clean, and modern. You can customize the styling by modifying:
- `frontend/src/App.css` - Main component styles
- `frontend/src/index.css` - Global styles

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request