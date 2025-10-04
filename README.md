# VisionFlow

AI-powered data extraction and workflow automation platform.

![Homepage](./homepage.png)

## Features

- ✨ Extract structured data from any webpage
- 🚀 Fast processing with modern AI
- 📊 Clean dashboard interface
- 💾 SQLite data persistence
- 🔄 Real-time updates

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Google AI API key

### Installation

1. **Clone repository**
```bash
git clone <repository-url>
cd VisionFlow
```

2. **Backend setup**
```bash
cd backend
pip install -r requirements.txt
```

3. **Frontend setup**
```bash
cd frontend
npm install
```

### Configuration

1. Create `backend/.env` file:
```
GOOGLE_AI_API_KEY=your_google_ai_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

2. Get Google AI API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Running

**Start backend:**
```bash
cd backend
python app.py
```

**Start frontend:**
```bash
cd frontend
npm start
```

Visit `http://localhost:3000`

## Project Structure

```
VisionFlow/
├── backend/           # Flask API
│   ├── app.py        # Main application
│   ├── extract.py    # Data extraction logic
│   ├── database.py   # Database operations
│   └── requirements.txt
├── frontend/         # React application
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── index.css
│   └── package.json
├── scripts/          # Utility scripts
├── docs/            # Documentation
└── config/          # Configuration files
```

## API Endpoints

- `GET /` - Health check
- `POST /extract` - Extract data from URL
- `GET /data` - Retrieve extractions
- `GET /extractions/<id>` - Get specific extraction

## Development

Built with Flask and React, using Google Gemini AI for extraction.

## License

MIT License
