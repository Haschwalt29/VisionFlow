# VisionFlow Setup Required

## Current Status
✅ **Backend server running** on port 5000  
✅ **Frontend server running** on port 3000  
⚠️ **OpenAI API Key needed**

## Quick Setup

Your VisionFlow application is now running, but you need to configure an OpenAI API key to enable data extraction functionality.

### Step 1: Get OpenAI API Key
1. Visit https://platform.openai.com/account/api-keys
2. Sign in to your OpenAI account
3. Create a new API key

### Step 2: Create Environment File
Create a file named `.env` in the `backend` folder with:

```
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

### Step 3: Set Environment Variable (Alternative)
Or set it directly in your terminal:

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="sk-proj-your-actual-api-key-here"
cd backend
python app.py
```

**Windows Command Prompt:**
```cmd
set OPENAI_API_KEY=sk-proj-your-actual-api-key-here
cd backend
python app.py
```

### Step 4: Restart Backend Server
After setting the API key, restart the backend server to apply the changes.

## Usage
1. Open your browser to http://localhost:3000
2. Enter any webpage URL 
3. Click "Extract Data" to see AI-powered structured data extraction

## Features Successfully Restored
- 🔧 Fixed OpenAI API integration (updated to latest version)
- 🔧 Enabled proper environment variable loading
- 🔧 Fixed backend/frontend communication
- 🔧 Graceful error handling for missing API key

The application will now work once you add your OpenAI API key!
