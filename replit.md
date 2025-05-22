# AI Text Summarizer

## Overview

This project is an AI-powered text summarization application built with Streamlit and powered by Google's Gemini 1.5 Flash model through LangChain. The application provides a web-based interface for users to input text and receive AI-generated summaries with configurable parameters.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple three-tier architecture:

1. **Frontend Layer**: Streamlit web interface providing user interaction
2. **Business Logic Layer**: Custom TextSummarizer class handling AI model interactions
3. **External API Layer**: Google Gemini 1.5 Flash via LangChain integration

The architecture prioritizes simplicity and ease of deployment, making it suitable for rapid prototyping and demonstration purposes.

## Key Components

### Frontend (app.py)
- **Streamlit Application**: Main web interface with configuration sidebar
- **Session State Management**: Maintains summarizer instance across user interactions
- **Error Handling**: Graceful handling of API key and initialization errors
- **User Configuration**: Sidebar controls for summary style, word limits, and language

### Core Logic (summarizer.py)
- **TextSummarizer Class**: Encapsulates all AI model interactions
- **Google Gemini Integration**: Uses LangChain's ChatGoogleGenerativeAI wrapper
- **Text Preprocessing**: Cleans and prepares input text for summarization
- **Configurable Parameters**: Temperature (0.3), max tokens (1024), timeout (30s)

### Configuration Management
- **Environment Variables**: API key management through .env files
- **Default Settings**: Fallback configuration for summary style, word limits, and language
- **Streamlit Config**: Custom server settings for deployment

## Data Flow

1. **User Input**: Text entered through Streamlit interface
2. **Preprocessing**: Text cleaning and normalization in TextSummarizer
3. **API Request**: Formatted prompt sent to Google Gemini via LangChain
4. **Response Processing**: AI-generated summary returned and displayed
5. **Error Handling**: Comprehensive error messages for failed requests

The data flow is stateless except for the cached summarizer instance, ensuring reliability and simplicity.

## External Dependencies

### Core Dependencies
- **Streamlit (>=1.45.1)**: Web application framework
- **LangChain (>=0.3.25)**: AI model abstraction layer
- **LangChain Google GenAI (>=2.1.4)**: Google Gemini integration
- **Python-dotenv (>=1.1.0)**: Environment variable management

### External Services
- **Google Gemini 1.5 Flash**: Primary AI model for text summarization
- **Google AI Studio**: API key management and configuration

The application minimizes external dependencies to reduce complexity and potential points of failure.

## Deployment Strategy

### Replit Deployment
- **Autoscale Target**: Configured for automatic scaling based on demand
- **Port Configuration**: Streamlit server runs on port 5000
- **Python Environment**: Uses Python 3.11 with Nix package management

### Environment Setup
- **API Key Configuration**: Requires GOOGLE_API_KEY environment variable
- **Optional Defaults**: Configurable default values for user preferences
- **Streamlit Configuration**: Custom theme and server settings via .streamlit/config.toml

### Development Workflow
- **Parallel Execution**: Replit workflow supports concurrent task execution
- **Hot Reload**: Streamlit provides automatic reloading during development
- **Error Recovery**: Graceful handling of API failures and missing configurations

The deployment strategy emphasizes ease of setup and minimal configuration requirements, making it accessible for users with varying technical backgrounds.