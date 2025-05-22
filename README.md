# AI Text Summarizer

An AI-powered text summarization tool using Google Gemini 1.5 Flash and LangChain.

## Features
- AI-powered text summarization using Google Gemini 1.5 Flash
- Multiple summary styles: Brief, Detailed, Bullet Points
- Customizable summary length (50-500 words)
- Multi-language support
- File upload support (.txt, .md)
- Download generated summaries
- Real-time progress tracking

## Setup Instructions

### 1. Install Python Requirements
```bash
pip install streamlit langchain langchain-google-genai langchain-community python-dotenv
```

### 2. Get Google API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

### 3. Set Up Environment
Create a `.env` file in the project folder:
```
GOOGLE_API_KEY=your_api_key_here
```

### 4. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Files Structure
- `app.py` - Main Streamlit application
- `summarizer.py` - AI summarization logic
- `.streamlit/config.toml` - Streamlit configuration
- `.env.example` - Environment variables template
- `README.md` - This file

## How to Use
1. Open the app in your browser
2. Choose your preferred summary style and length
3. Paste text or upload a file
4. Click "Generate Summary"
5. Download your summary if needed

## For Class Presentation
- The app runs locally on your computer
- Works offline once dependencies are installed
- Clean, professional interface perfect for demonstrations
- Real-time AI summarization with progress tracking

Enjoy your AI summarization tool!